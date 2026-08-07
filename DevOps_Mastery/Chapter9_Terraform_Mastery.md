# Chapter 9: Terraform Mastery – Production-Grade Infrastructure as Code

Welcome to Chapter 9. You already know the basics of Terraform—what it is, how to write a simple `main.tf`, and how to `terraform apply` it. 

Now, we are going to dive deep. We are going to look under the hood. As Richard Feynman would say, "I couldn't reduce it to the freshman level. That means we really don't understand it." We are going to understand *why* Terraform does what it does. We'll explore its internal architecture, how to manage state like a professional, advanced HCL expressions, module design patterns, CI/CD integration, and policy enforcement.

By the end of this chapter, you won't just be writing Terraform; you'll be architecting production-grade, bulletproof infrastructure.

---

## SECTION 1: Terraform Architecture Internals

### The "Why" and "How"
To master Terraform, you must understand how it operates under the hood. Terraform isn't magic; it's a Go binary that parses text files, builds a graph, and talks to APIs. 

Terraform uses a **Core + Provider Plugin Architecture**.
- **Terraform Core:** The main engine. It reads configuration, reads state, builds the dependency graph, and creates the plan. It doesn't know how to create an EC2 instance.
- **Provider Plugins:** Separate binaries (e.g., `terraform-provider-aws`) that know how to talk to specific APIs (AWS, Azure, GitHub). 

When you run `terraform apply`, here is what happens internally:
1. **Parse:** Core parses your HCL files and builds a Dependency Graph.
2. **Read State:** It reads the current state (local or remote) to know what already exists.
3. **Plan (Call Providers):** Core asks the Provider, "I want state X. Current state is Y. What API calls do you need to make?"
4. **Execute:** Core walks the dependency graph. If resource A depends on B, B is created first. Core tells the Provider to execute the changes.
5. **Update State:** The new state is saved.

### ASCII Diagram: Terraform Execution Flow

```text
+-----------------------+       (1) Parse        +-----------------------+
|  .tf Configuration    | ---------------------> |                       |
+-----------------------+                        |                       |
                                                 |   Terraform Core      |
+-----------------------+       (2) Read         |   (Dependency Graph)  |
|  terraform.tfstate    | ---------------------> |                       |
+-----------------------+                        |                       |
                                                 +-----------+-----------+
                                                             |
                                         (3) gRPC Protocol   | (Plan/Apply)
                                                             v
                                                 +-----------------------+
                                                 |                       |
                                                 |  Provider Plugin      |
                                                 |  (e.g., AWS, GCP)     |
                                                 |                       |
                                                 +-----------+-----------+
                                                             |
                                         (4) HTTP/REST API   |
                                                             v
                                                 +-----------------------+
                                                 |                       |
                                                 |  Cloud Provider API   |
                                                 |                       |
                                                 +-----------------------+
```

### Provider Protocol and Installation
The communication between Terraform Core and the Provider Plugin happens via **gRPC** (a high-performance remote procedure call framework). 
When you run `terraform init`, Terraform reaches out to `registry.terraform.io`, downloads the provider binary, and generates a `.terraform.lock.hcl` file.

**Best Practice:** Always commit the `.terraform.lock.hcl` file. It ensures that everyone on your team (and your CI/CD pipeline) uses the exact same cryptographic hash of the provider, preventing "it works on my machine" issues.

### Interview Q&A
**Q:** How does Terraform determine the order in which to create resources?
**A:** Terraform parses the configuration and builds a Directed Acyclic Graph (DAG). Resources are nodes, and dependencies (implicit via interpolation, or explicit via `depends_on`) are edges. Terraform performs a topological sort on this graph to determine the execution order. Independent branches of the graph are executed in parallel.

---

## SECTION 2: State Management Deep Dive

### The Heart of Terraform
Terraform's state file (`terraform.tfstate`) is its memory. It is a JSON file that maps your HCL configuration to real-world infrastructure. 

**Why is it critical?**
1. **Mapping:** It maps a resource address in your code (e.g., `aws_instance.web`) to a physical ID in the cloud (e.g., `i-1234567890abcdef0`).
2. **Metadata:** It stores dependencies, resource dependencies, and provider versions.
3. **Performance:** It caches resource attributes so Terraform doesn't have to query the entire cloud API every time.

### Remote State: S3 Backend with DynamoDB Locking
In production, you **never** store state locally. If two engineers run `terraform apply` simultaneously on a local state, or if the CI/CD pipeline runs concurrently, you get **state corruption**.

The industry standard on AWS is the **S3 Backend with DynamoDB Locking**.
- **S3:** Stores the state file. Enables versioning (for rollback if state is corrupted) and encryption at rest.
- **DynamoDB:** Provides state locking. Before Terraform modifies the state, it writes a lock item to DynamoDB. If another process tries to run, it sees the lock and fails safely.

### Complete S3+DynamoDB Backend Configuration

```hcl
# backend.tf
terraform {
  backend "s3" {
    # The name of the S3 bucket to store the state file
    bucket         = "my-company-terraform-state-prod"
    
    # The path within the bucket where the state will be saved
    key            = "core-infrastructure/terraform.tfstate"
    
    # The AWS region where the bucket exists
    region         = "us-east-1"
    
    # Encrypt the state file at rest using AES-256 or KMS
    encrypt        = true
    
    # The DynamoDB table used for state locking
    dynamodb_table = "terraform-state-locks"
    
    # An IAM role to assume (optional, but good for cross-account setups)
    # role_arn     = "arn:aws:iam::123456789012:role/TerraformBackendRole"
  }
}
```

*Line-by-line breakdown:*
- `backend "s3"`: Tells Terraform to use the AWS S3 provider for state.
- `bucket`: Must be globally unique. Should have versioning enabled.
- `key`: The "filepath" inside the bucket. Crucial for organizing multiple state files.
- `encrypt`: Always set to true. State files can contain sensitive data.
- `dynamodb_table`: The table must have a primary key named `LockID` (String).

### State Commands: State Surgery
Sometimes things go wrong. A resource is deleted manually in the console, or you want to refactor your code without destroying the infrastructure.

- `terraform state list`: Lists all resources in the state.
- `terraform state show aws_instance.web`: Shows the full JSON attributes of a specific resource.
- `terraform state rm aws_instance.web`: Removes the resource from Terraform's memory. *It does not destroy the actual EC2 instance.* Useful if you want to stop managing a resource.
- `terraform state mv aws_instance.old_name aws_instance.new_name`: Renames a resource in the state. Crucial when refactoring HCL code.

### Sensitive Values in State
**WARNING:** If you pass a database password into Terraform, even if you mark the variable as `sensitive = true`, **it is stored in plaintext inside the `terraform.tfstate` JSON file.** 
*Why?* Because Terraform needs the actual value to compare it against the real-world infrastructure.
*Solution:* Restrict access to the S3 bucket using IAM policies. Only the CI/CD role should be able to read the state file.

### Interview Q&A
**Q:** What happens if two engineers run `terraform apply` at the same time using a remote backend with locking?
**A:** The first engineer's process acquires the lock in DynamoDB. The second engineer's process will check DynamoDB, see the lock exists, and exit immediately with an "Error: Error acquiring the state lock" message, preventing concurrent modification and state corruption.

---

## SECTION 3: Variables, Outputs, Locals

### Variable Types
Terraform is strongly typed. 
- Primitive: `string`, `number`, `bool`
- Complex: `list(type)`, `set(type)`, `map(type)`, `object({attr=type})`, `tuple([type])`

### Variable Validation Blocks
Stop bad data before the plan even runs.

```hcl
variable "instance_type" {
  description = "The EC2 instance type"
  type        = string
  default     = "t3.micro"

  validation {
    # The condition must evaluate to true, or the plan fails
    condition     = can(regex("^t[234]\\.", var.instance_type))
    # The error message shown to the user
    error_message = "The instance type must be a t2, t3, or t4 family instance."
  }
}
```

### Variable Precedence
How does Terraform decide which value to use? (Highest precedence wins):
1. Command line flag: `-var 'foo=bar'`
2. Environment variables: `TF_VAR_foo=bar`
3. Automatically loaded files: `terraform.tfvars` or `*.auto.tfvars`
4. Default values in the variable declaration

### Locals: DRY (Don't Repeat Yourself)
Variables are inputs from the user. **Locals** are computed values internal to your module. If you find yourself writing the same expression twice, put it in a local.

```hcl
locals {
  # Merge common tags with resource-specific tags
  common_tags = {
    Environment = var.environment
    Project     = "ProjectApollo"
    ManagedBy   = "Terraform"
  }
  
  # Format a standard naming convention
  name_prefix = "${var.project}-${var.environment}"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  # Using the local
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}
```

### Outputs
Outputs expose data from a module. They are also printed to the console after an apply.

```hcl
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
  # Redacts the value in console output, but STILL PLAINTEXT IN STATE!
  sensitive   = false 
}
```

### Interview Q&A
**Q:** What is the difference between locals and variables?
**A:** Variables are inputs provided by the user (or caller of a module) to customize the deployment. Locals are private, internal variables used within a module to store computed values or reduce repetition. Users cannot override locals from the outside.

---

## SECTION 4: Meta-Arguments

Meta-arguments change the behavior of resources. 

### `count` vs `for_each`
Both allow you to create multiple instances of a resource. 
**Rule of Thumb:** Use `count` for identical resources where order doesn't matter (like identical null_resources). **Use `for_each` for almost everything else in production.**

*Why?* If you use `count = 3` to create 3 subnets, Terraform identifies them as `aws_subnet.main[0]`, `[1]`, `[2]`. If you remove the subnet at index 1, Terraform will shift index 2 to index 1, and destroy/recreate it!

`for_each` uses a map or set of strings. The identifier becomes the key (e.g., `aws_subnet.main["us-east-1a"]`). Removing one does not affect the others.

```hcl
variable "subnets" {
  type = map(string)
  default = {
    "app-a" = "10.0.1.0/24"
    "app-b" = "10.0.2.0/24"
  }
}

resource "aws_subnet" "app" {
  # Iterate over the map. each.key is the name, each.value is the CIDR.
  for_each = var.subnets
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  
  tags = {
    Name = "subnet-${each.key}"
  }
}
```

### `depends_on`
Terraform builds its dependency graph automatically based on references (e.g., passing `aws_vpc.main.id` to a subnet). You only use `depends_on` when there is a **hidden dependency** that Terraform cannot see.

```hcl
resource "aws_iam_role_policy_attachment" "ecs_node_role" {
  role       = aws_iam_role.ecs_node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_autoscaling_group" "ecs_nodes" {
  # The ASG instances will fail to join the cluster if the IAM policy isn't attached yet.
  # Terraform doesn't know this, so we force the ordering.
  depends_on = [aws_iam_role_policy_attachment.ecs_node_role]
  
  # ... configuration ...
}
```

### The `lifecycle` Block
Controls how Terraform creates, updates, and destroys resources.

```hcl
resource "aws_instance" "critical_db" {
  ami           = "ami-123456"
  instance_type = "t3.large"

  lifecycle {
    # If the AMI changes, Terraform normally destroys the old instance, then creates the new one.
    # This reverses it: create new first, update load balancers, then destroy old. Zero downtime!
    create_before_destroy = true
    
    # If someone tries to destroy this, Terraform will throw an error and stop.
    prevent_destroy       = true
    
    # If an external script adds tags, Terraform will ignore the drift and won't try to remove them.
    ignore_changes        = [tags["LastScanned"]]
  }
}
```

---

## SECTION 5: Dynamic Blocks and Expressions

### Dynamic Blocks
Sometimes a resource has nested blocks (like `ingress` rules in a Security Group) that you want to generate dynamically based on a variable. You cannot use `for_each` directly on a block, you must use a `dynamic` block.

```hcl
variable "ingress_rules" {
  type = list(object({
    port        = number
    description = string
    cidr_blocks = list(string)
  }))
  default = [
    { port = 80, description = "HTTP", cidr_blocks = ["0.0.0.0/0"] },
    { port = 443, description = "HTTPS", cidr_blocks = ["0.0.0.0/0"] }
  ]
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Allow inbound traffic"

  # The word 'ingress' defines what type of block we are generating
  dynamic "ingress" {
    for_each = var.ingress_rules
    
    # 'ingress' becomes an iterator object
    content {
      description = ingress.value.description
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

### Expressions and Functions
- **For Expressions:** `[for s in var.subnets : s.id]` transforms a list.
- **Ternary:** `var.is_prod ? "t3.large" : "t3.micro"`
- **Splat:** `aws_subnet.app[*].id` gets a list of IDs (only works with `count`, not `for_each`).

### VPC Subnet Calculation (`cidrsubnet`)
Never hardcode subnet CIDRs. Let Terraform calculate them.

```hcl
variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count = 3
  
  # cidrsubnet(prefix, newbits, netnum)
  # 10.0.0.0/16 + 8 bits = /24. 
  # count.index (0,1,2) determines the network number.
  # Results: 10.0.0.0/24, 10.0.1.0/24, 10.0.2.0/24
  cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)
}
```

---

## SECTION 6: Modules Design Patterns

### What Makes a Good Module?
A module is just a folder with Terraform files. 
1. **Single Responsibility:** A VPC module should not create an EKS cluster.
2. **Encapsulation:** Inputs (`variables.tf`) and Outputs (`outputs.tf`) form the API. 
3. **No Hardcoding:** If it's specific to an environment, it should be a variable.

### Production Module Composition
In production, you don't build one massive monolithic root module. You compose them.

```hcl
# ROOT MODULE (environments/prod/main.tf)

# 1. Foundation Module
module "vpc" {
  source             = "git::https://github.com/company/terraform-aws-vpc.git?ref=v2.1.0"
  cidr_block         = "10.1.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b"]
}

# 2. Compute Module (Consumes Output of VPC)
module "eks" {
  source     = "../../modules/eks"
  # Passing the outputs from the VPC module as inputs to the EKS module
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids
  
  cluster_name    = "prod-cluster"
  node_size       = "m5.large"
}
```
*Notice the `?ref=v2.1.0`*. **Always pin module versions** from Git or Registries to prevent breaking changes when upstream code is modified.

### Interview Q&A
**Q:** How do you design Terraform modules for a large team?
**A:** I treat modules like software libraries. I separate them into two tiers: "Child Modules" (reusable, generic building blocks like a standardized VPC or RDS instance, stored in separate repos with version tags) and "Root Modules" (environment-specific configurations that call the child modules). I enforce version pinning, write automated tests using Terratest, and generate documentation automatically using terraform-docs.

---

## SECTION 7: Workspaces and Environment Separation

### Terraform Workspaces
Workspaces allow you to maintain multiple state files for a single directory of Terraform configuration.
`terraform workspace new dev` creates a new state. `terraform plan` will use the `dev` state.

**When to use:** Identical infrastructure that just needs different scaling (e.g., identical dev and test environments). 

**When to AVOID (Production Warning):** Do not use workspaces to separate Staging and Production. Why?
1. Production and Staging often diverge architecturally (Prod has Multi-AZ RDS, Staging has Single-AZ).
2. A single mistake (running `apply` in the wrong workspace) can destroy production.
3. IAM permissions are harder to isolate.

### The Recommended Approach: Directory Separation
Keep your environments in separate folders. This ensures blast radius isolation.

```text
environments/
├── dev/
│   ├── backend.tf (points to dev-state bucket)
│   ├── main.tf    (calls modules with dev variables)
│   └── terraform.tfvars
├── staging/
│   ├── backend.tf
│   └── main.tf
└── prod/
    ├── backend.tf
    └── main.tf
modules/
├── vpc/
└── rds/
```
If you want to keep this DRY, look into **Terragrunt**, a wrapper that generates the `backend.tf` and manages module dependencies automatically.

---

## SECTION 8: Import and Drift Detection

### Dealing with the Real World
Sometimes infrastructure is created manually via the AWS Console. How do you bring it into Terraform?

**Old Way:** `terraform import aws_instance.web i-1234567890`. This updates the state, but you still have to manually write the HCL code to match it.

**New Way (Terraform 1.5+): The `import` block.**

```hcl
# Tell Terraform to import the EC2 instance
import {
  to = aws_instance.web
  id = "i-1234567890"
}
```
Run `terraform plan -generate-config-out=generated.tf`. Terraform will inspect the real-world instance and *write the HCL code for you* into `generated.tf`. 

### Drift Detection
Drift is when reality doesn't match your state/code.
Run `terraform plan`. Terraform refreshes the state against the cloud API. If someone manually opened port 22 in a security group, `plan` will show that Terraform wants to close it to match the code.
- To fix drift: Either revert the manual change via `terraform apply`, or update your HCL code to reflect the new reality.

---

## SECTION 9: Terraform in CI/CD

Running Terraform from your laptop is a recipe for disaster. In production, Terraform runs in CI/CD.

### The Pipeline Architecture
1. **Pull Request (PR):** Developer opens a PR.
2. **CI Check:**
   - `terraform fmt -check` (fails if code isn't formatted)
   - `terraform validate` (syntax check)
   - Security scanning (Checkov/tfsec)
   - `terraform plan` (generates the plan)
3. **Review:** The CI system posts the plan output as a comment on the PR. Reviewers approve.
4. **Merge to Main:** 
5. **Deployment:** `terraform apply -auto-approve` runs automatically.

### OIDC Authentication (No Long-Lived Secrets)
Never store AWS Access Keys in GitHub Secrets. Use OIDC (OpenID Connect). GitHub Actions assumes an IAM Role in AWS dynamically using a cryptographic token.

### Complete GitHub Actions Workflow

```yaml
name: Terraform Production Pipeline

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

# Required for AWS OIDC authentication
permissions:
  id-token: write
  contents: read

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsTerraformRole
          aws-region: us-east-1

      - name: Terraform Init
        run: terraform init

      - name: Terraform Format
        run: terraform fmt -check

      - name: Terraform Validate
        run: terraform validate

      - name: Checkov Security Scan
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform

      - name: Terraform Plan
        id: plan
        if: github.event_name == 'pull_request'
        run: terraform plan -no-color -out=tfplan
        
      # (In a real pipeline, you would use a script to post this plan to the PR)

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve
```

---

## SECTION 10: Policy as Code

In large organizations, you cannot review every PR manually. You need guardrails.

### OPA (Open Policy Agent) & Conftest
You can write policies in **Rego** to evaluate Terraform plans before they are applied.

1. Convert plan to JSON: `terraform show -json tfplan > plan.json`
2. Run Conftest: `conftest verify -p policies/ plan.json`

**Example Rego Policy: Deny Public S3 Buckets**
```rego
package main

# Deny if any aws_s3_bucket has acl set to public-read
deny[msg] {
  resource := input.resource_changes[_]
  resource.type == "aws_s3_bucket"
  resource.change.after.acl == "public-read"
  msg := sprintf("S3 Bucket %v cannot be public-read", [resource.name])
}
```

### Static Analysis: Checkov
Checkov parses your `.tf` files and checks them against hundreds of known security misconfigurations (e.g., RDS without encryption, Security Groups with 0.0.0.0/0). Integrating `checkov -d .` into your CI pipeline is a mandatory day-one best practice.

---

## SECTION 11: Terraform Debugging and Troubleshooting

When Terraform breaks, it breaks hard. Here is how you debug.

### Tracing with TF_LOG
If a provider is throwing a vague error, turn on tracing.
```bash
export TF_LOG=TRACE
export TF_LOG_PATH=terraform-debug.log
terraform apply
```
This dumps the raw HTTP/REST API calls being made by the provider. You will see exactly what AWS API returned a 400 Bad Request.

### Common Errors & Runbook
- **"Error: Cycle"**: You have a circular dependency (A depends on B, B depends on A). Restructure your code or remove unnecessary `depends_on`.
- **"Error acquiring the state lock"**: The CI pipeline crashed midway and left the DynamoDB lock intact. 
  - *Fix:* Verify no pipelines are running. Go to DynamoDB console and manually delete the lock item, or run `terraform force-unlock <LOCK_ID>`.
- **"Error: Resource already exists"**: Someone created it manually. 
  - *Fix:* Use the `import` block to bring it into state, or manually delete it in the console and rerun.
- **"Provider produced inconsistent result after apply"**: The Provider code has a bug (it expected an attribute to be "X" after creation, but the cloud API returned "Y"). 
  - *Fix:* Check GitHub issues for the provider, upgrade provider version.

---

## SECTION 12: Production Terraform Best Practices

If you remember nothing else from this chapter, remember these rules:

1. **State Isolation:** Never use the same state file for Prod and Dev.
2. **Remote Backend Always:** S3 + DynamoDB locking is non-negotiable.
3. **Pin Versions:** Pin Terraform Core (`required_version = "~> 1.5.0"`) and Provider versions (`version = "~> 5.0"`). The `~>` allows patch updates but prevents breaking minor/major updates.
4. **Use Data Sources:** Don't hardcode VPC IDs. Use `data "aws_vpc"` to look them up dynamically.
5. **Tag Everything:** Use a `locals` block with `merge()` to enforce a strict tagging standard across all resources.
6. **No Secrets in HCL:** Never put passwords in code. Use `aws_secretsmanager_secret_version` data sources to fetch them at runtime, or pass them in via secure CI variables.
7. **Pre-Commit Hooks:** Run `terraform fmt`, `tflint`, and `checkov` automatically every time a developer commits code.

---

## END OF CHAPTER

### One-Page Revision Sheet
- **Architecture:** Core (Graph/Plan) + Provider Plugin (API execution) via gRPC.
- **State:** JSON memory mapping config to reality. Needs locking (DynamoDB) and remote storage (S3).
- **Meta-arguments:** `for_each` (maps, safe), `count` (lists, risky), `depends_on` (hidden dependencies), `lifecycle` (creation rules).
- **Modules:** Encapsulated, versioned, DRY building blocks.
- **Drift:** When reality deviates from state. Fix via `import` or apply.
- **CI/CD:** Plan on PR, Apply on Merge. Use OIDC, never static keys.

### Top Terraform Interview Takeaways
1. Explain the execution flow (`init` -> `plan` -> `apply`).
2. Why is state locking necessary and how is it implemented in AWS?
3. What is the difference between `count` and `for_each`?
4. How do you handle sensitive data in Terraform?
5. How do you refactor resources without destroying them? (`state mv`)

### Common Production Mistakes Table
| Mistake | Consequence | Solution |
|---|---|---|
| Local state | State corruption, out of sync teams | S3 + DynamoDB Backend |
| Unpinned providers | Broken pipelines on Monday morning | `version = "~> x.y"` |
| Monolithic root module | 30 minute `plan` times, huge blast radius | Decompose into smaller states |
| Using `count` for subnets | Removing index 1 destroys index 2 | Use `for_each` with maps |
| Hardcoded IDs | Not reusable across environments | Use variables and Data Sources |

### Hands-on Exercises (Labs)
1. **Lab 1: Remote Backend Setup.** Create an S3 bucket and DynamoDB table. Migrate a local state to the remote backend.
2. **Lab 2: State Surgery.** Deploy an EC2 instance. Use `state mv` to rename it in HCL without destroying it.
3. **Lab 3: Dynamic Security Groups.** Write a module that uses a `dynamic "ingress"` block to open ports based on a variable list.
4. **Lab 4: Drift Recovery.** Deploy an S3 bucket via Terraform. Add a tag manually in the AWS Console. Run a plan to see drift, and configure `lifecycle { ignore_changes = [tags] }` to ignore it.
5. **Lab 5: CI/CD Pipeline.** Set up a GitHub Action that runs `terraform validate`, `fmt`, and `checkov` on a Pull Request.

### Architecture Challenge
**Scenario:** You are the Lead DevOps Engineer for a company with 10 engineering teams. They all need AWS infrastructure.
**Challenge:** Design the repository structure, module strategy, and CI/CD workflow to allow them to self-serve infrastructure safely.
*Hint: Think about Private Module Registries, Terragrunt/Workspaces for state separation, OPA policies for guardrails, and OIDC for secure deployments.*
