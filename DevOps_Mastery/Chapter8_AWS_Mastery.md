# Chapter 8: AWS Mastery (Production & FAANG-Level)

Welcome to AWS Mastery. We aren't going to talk about what a server is, or how to click around the AWS console. If you're here, you already know the basics. You know EC2 is a VM and S3 is object storage. 

Instead, we are going to look at AWS the way a Senior DevOps Engineer or a Cloud Architect at a top-tier tech company sees it. We are going to learn *why* things are designed the way they are. As Richard Feynman would say, if you can't explain it simply, you don't understand it well enough. We will break down complex, production-grade architectures into fundamental truths. 

For every topic, we'll dive into the internal workflows, draw it out with ASCII diagrams, look at real-world production use cases, and give you the CLI commands and Terraform snippets you actually need. We'll also cover common mistakes, troubleshooting, and what you'll be asked in a FAANG interview.

Let's get started.

---

## SECTION 1: IAM Deep Dive

IAM (Identity and Access Management) is the absolute core of AWS security. It's not just about users and groups; it's a massive, globally distributed authorization engine. Every single API call you make to AWS passes through this engine.

### 1. Internal Workflow + Request Flow

When you make an AWS API call (e.g., `aws s3 ls`), the following evaluation logic happens in microseconds:

1. **Authentication**: Are you who you say you are? (Checked via SigV4 cryptographic signature using your access keys).
2. **Authorization**: Are you allowed to do this? This is where the IAM evaluation logic kicks in.

**The IAM Evaluation Logic:**
By default, everything is an implicit DENY.
AWS checks policies in this order to determine the final Allow/Deny:
1. **Explicit Deny**: If *any* policy explicitly denies the action, the request is instantly rejected. Explicit Deny always wins.
2. **Organizations SCPs (Service Control Policies)**: Are you part of an AWS Organization, and does an SCP allow this? (If an SCP doesn't allow it, implicit deny).
3. **Resource-based Policies**: Does the resource (like an S3 bucket policy) allow you?
4. **Permissions Boundaries**: Does a boundary policy limit your identity's permissions?
5. **Session Policies**: Were session policies passed when assuming the role?
6. **Identity-based Policies**: Does your user/group/role policy allow this?

If at any point there's an Explicit Deny, it's over. Otherwise, if there is at least one Allow and no Explicit Denys, the request succeeds.

### 2. ASCII Architecture Diagram: AssumeRole Flow

```text
  [Your App/User]                          [AWS STS]                         [Target Resource]
         |                                     |                                     |
         | 1. aws sts assume-role              |                                     |
         |------------------------------------>|                                     |
         |                                     |                                     |
         | 2. Validates Trust Policy           |                                     |
         |    (Who can assume this?)           |                                     |
         |                                     |                                     |
         | 3. Returns Temp Credentials         |                                     |
         |<------------------------------------|                                     |
         |    - AccessKeyId                    |                                     |
         |    - SecretAccessKey                |                                     |
         |    - SessionToken                   |                                     |
         |                                     |                                     |
         | 4. API Call using Temp Creds        |                                     |
         |-------------------------------------------------------------------------->|
         |                                     |                                     | 5. Validates IAM
         |                                     |                                     |    Permission Policy
         | 6. Returns Data                     |                                     |
         |<--------------------------------------------------------------------------|
```

### 3. Production Use Case: IRSA on EKS

In modern Kubernetes on AWS (EKS), you don't give EC2 instances a giant IAM role, and you never put AWS access keys in Kubernetes Secrets. Why? Because if a pod gets compromised, the attacker has access to everything the node can do.

Instead, we use **IRSA (IAM Roles for Service Accounts)**. 
- EKS hosts an OIDC (OpenID Connect) discovery endpoint.
- You create an IAM Role and set its *Trust Policy* to trust this OIDC provider.
- You annotate a Kubernetes ServiceAccount with the IAM Role ARN.
- The pod uses this ServiceAccount, and AWS injects temporary STS credentials directly into the pod via environment variables.

### 4. CLI Commands

Test permissions without actually making the API call (great for debugging):
```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/MyRole \
  --action-names s3:PutObject \
  --resource-arns arn:aws:s3:::my-production-bucket/*
```

Assume a role manually from the CLI:
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/CrossAccountDBAdmin \
  --role-session-name AdminSession
```

### 5. Terraform Example Snippet

Here is a complete IAM policy and role for an EC2 instance that needs read-only access to S3. Notice the separation of the *Trust Policy* (assume_role_policy) and the *Permission Policy*.

```hcl
data "aws_iam_policy_document" "ec2_trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "app_role" {
  name               = "production-app-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
}

data "aws_iam_policy_document" "s3_read" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:ListBucket"]
    resources = [
      "arn:aws:s3:::my-app-data-bucket",
      "arn:aws:s3:::my-app-data-bucket/*"
    ]
  }
}

resource "aws_iam_role_policy" "s3_read_policy" {
  name   = "S3ReadOnly"
  role   = aws_iam_role.app_role.id
  policy = data.aws_iam_policy_document.s3_read.json
}

# Attach to EC2 via Instance Profile
resource "aws_iam_instance_profile" "app_profile" {
  name = "production-app-profile"
  role = aws_iam_role.app_role.name
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Using `Action: *` and `Resource: *`. Never do this. Always practice least privilege.
- **Mistake**: Using long-lived access keys for applications.
- **Best Practice**: Use AWS Organizations SCPs to put guardrails in place (e.g., "Deny all regions except us-east-1", "Deny disabling CloudTrail"). Even the root user of a member account cannot override an SCP.
- **Best Practice**: Use Permissions Boundaries for delegated administration. Allow developers to create IAM roles, but attach a boundary so they can't escalate privileges.

### 7. Troubleshooting
- **Symptom**: "Access Denied" when accessing an S3 bucket, but your IAM user policy allows it.
- **Why?**: Check the S3 Bucket Policy. Is there an Explicit Deny? Or, check if an SCP is blocking the action. Check if a Permissions Boundary is attached to your user restricting the action.

### 8. Interview Q&A
**Q: Walk me through the IAM policy evaluation order.**
**A:** "By default, everything is an implicit deny. AWS evaluates all applicable policies. If there is a single Explicit Deny anywhere—in an SCP, a resource policy, a permissions boundary, or an identity policy—the request is denied. If there is no explicit deny, AWS looks for an explicit Allow. If an Allow exists in the identity policy (and is not restricted by an SCP or boundary), or in a resource policy, the request is allowed."

**Q: What is the difference between a Trust Policy and a Permissions Policy on an IAM Role?**
**A:** "A Trust Policy defines *who* or *what* can assume the role (e.g., an EC2 service, an OIDC provider, or another AWS account). A Permissions Policy defines *what actions* the entity can perform once it has successfully assumed the role."

---

## SECTION 2: VPC Deep Dive

A VPC (Virtual Private Cloud) is your logically isolated slice of the AWS network. If you screw up your VPC design, everything built on top of it will be fragile, insecure, or hard to scale.

### 1. Internal Workflow + Request Flow

Let's look at how routing actually works when an EC2 instance in a private subnet tries to download a package from the internet.

1. Instance generates outbound packet (Dest: 8.8.8.8).
2. Packet hits the Subnet's **Route Table**.
3. Route table has a rule: `0.0.0.0/0 -> nat-gw-id`.
4. Packet is routed to the NAT Gateway (which lives in a public subnet).
5. NAT Gateway replaces the internal source IP with its own Elastic IP (Source NAT).
6. Packet hits the Public Subnet's Route Table.
7. Route table has a rule: `0.0.0.0/0 -> igw-id`.
8. Packet goes to the Internet Gateway (IGW) and out to the internet.
9. Return traffic flows back through the IGW -> NAT GW (state is tracked) -> Instance.

**Most Specific Route Wins**: If a route table has `10.0.1.0/24 -> local` and `0.0.0.0/0 -> igw`, traffic for `10.0.1.5` goes local because `/24` is more specific than `/0`.

### 2. ASCII Architecture Diagram: Production VPC

```text
VPC CIDR: 10.0.0.0/16
+-----------------------------------------------------------------------+
|  Internet Gateway (IGW)                                               |
|    |                                                                  |
|  +---------------------------+       +---------------------------+    |
|  | AZ-A                      |       | AZ-B                      |    |
|  |                           |       |                           |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  |  | Public Subnet A     |  |       |  | Public Subnet B     |  |    |
|  |  | 10.0.1.0/24         |  |       |  | 10.0.2.0/24         |  |    |
|  |  | [ NAT Gateway A ]   |  |       |  | [ NAT Gateway B ]   |  |    |
|  |  | [ ALB Node ]        |  |       |  | [ ALB Node ]        |  |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  |            |              |       |            |              |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  |  | Private Subnet A    |  |       |  | Private Subnet B    |  |    |
|  |  | 10.0.11.0/24        |  |       |  | 10.0.12.0/24        |  |    |
|  |  | [ EKS Worker Node ] |  |       |  | [ EKS Worker Node ] |  |    |
|  |  | Routes to NAT GW A  |  |       |  | Routes to NAT GW B  |  |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  |            |              |       |            |              |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  |  | Isolated Subnet A   |  |       |  | Isolated Subnet B   |  |    |
|  |  | 10.0.21.0/24        |  |       |  | 10.0.22.0/24        |  |    |
|  |  | [ RDS Primary ]     |  |       |  | [ RDS Standby ]     |  |    |
|  |  | NO INTERNET ROUTE   |  |       |  | NO INTERNET ROUTE   |  |    |
|  |  +---------------------+  |       |  +---------------------+  |    |
|  +---------------------------+       +---------------------------+    |
+-----------------------------------------------------------------------+
```

### 3. Production Use Case: VPC Endpoints & Transit Gateway

**VPC Endpoints (PrivateLink)**: You have an app in an Isolated Subnet that needs to read from S3. Because there is no NAT Gateway route, it can't reach public AWS APIs. You deploy a **Gateway VPC Endpoint** for S3. AWS injects a prefix list into your route table pointing to the endpoint. Traffic to S3 never leaves the AWS backbone. (Note: Gateway endpoints are for S3/DynamoDB and are free. Interface endpoints use ENIs and cost money).

**Transit Gateway (TGW)**: You have 50 VPCs. Peering them creates a messy full-mesh network (N*(N-1)/2 connections). Instead, you use a Transit Gateway as a hub router. All VPCs connect to the TGW. You control routing centrally.

### 4. CLI Commands

Find out which Security Group is allowing port 22:
```bash
aws ec2 describe-security-group-rules \
  --filters Name="group-id",Values="sg-0123456789abcdef0"
```

Check if a VPC has overlapping CIDRs before peering:
```bash
aws ec2 describe-vpcs --vpc-ids vpc-a1b2c3d4 vpc-e5f6g7h8
```

### 5. Terraform Example Snippet

Using the official AWS VPC module is the industry standard.

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "production-vpc"
  cidr = "10.0.0.0/16"

  azs              = ["us-east-1a", "us-east-1b", "us-east-1c"]
  public_subnets   = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets  = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = false # PROD: Deploy one per AZ for HA
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  # Security best practice: DB subnets cannot reach the internet
  create_database_subnet_route_table = true
  create_database_nat_gateway_route  = false
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Putting a NAT Gateway in a private subnet. NAT Gateways MUST go in a public subnet, otherwise they have no route to the IGW!
- **Mistake**: Hardcoding IPs in Security Groups instead of referencing other Security Groups.
- **Best Practice**: Always use 3 tiers of subnets (Public, Private, Isolated/Database). 
- **Best Practice**: Use Security Groups for logical firewalling (App tier can talk to DB tier) and NACLs for broad network boundaries (Block an entire malicious CIDR block at the subnet level).

### 7. Troubleshooting
- **Symptom**: Instance in private subnet can't reach the internet.
- **Checklist**:
  1. Does the private subnet route table point `0.0.0.0/0` to a NAT GW?
  2. Is the NAT GW deployed in a *public* subnet?
  3. Does the public subnet route table point `0.0.0.0/0` to an IGW?
  4. Do Security Groups allow outbound HTTP/HTTPS?
  5. Do NACLs allow outbound AND inbound ephemeral ports (1024-65535)? NACLs are stateless!

### 8. Interview Q&A
**Q: What is the difference between a Security Group and a Network ACL (NACL)?**
**A:** "Security Groups operate at the instance level (ENI), are stateful (if request is allowed out, response is automatically allowed in), and only support ALLOW rules. NACLs operate at the subnet level, are stateless (you must explicitly allow return traffic on ephemeral ports), and support both ALLOW and DENY rules, evaluated in numerical order."

**Q: Can you ping a NAT Gateway?**
**A:** "No. NAT Gateways do not support ICMP traffic. To test connectivity, you must use TCP/UDP tools like `curl` or `telnet` against an external endpoint."

---

## SECTION 3: EC2 and Auto Scaling

Compute on AWS. We don't manually provision instances in production. We use Auto Scaling Groups (ASG) backed by Launch Templates.

### 1. Internal Workflow + Request Flow

How Target Tracking Auto Scaling works (closed-loop control system):
1. You set a target: "Keep average CPU at 60%".
2. ASG queries CloudWatch every 1 minute.
3. If CPU is 80%, ASG calculates how many instances are needed to bring it back to 60%.
4. ASG provisions new instances using the Launch Template.
5. New instances boot. If attached to an ALB, they begin health checks.
6. Once healthy, traffic routes to them.
7. ASG enters a **Cooldown Period** (or Warm-up time) to prevent over-provisioning while the new instances absorb load.

### 2. ASCII Architecture Diagram: ASG with Mixed Instances

```text
+-------------------------------------------------------------+
|  Auto Scaling Group (Desired: 10, Min: 2, Max: 20)          |
|                                                             |
|  Base Capacity (On-Demand): 2 instances (Always running)    |
|  +--------+ +--------+                                      |
|  | On-Dem | | On-Dem |                                      |
|  +--------+ +--------+                                      |
|                                                             |
|  Above Base Capacity (Spot 100%): 8 instances               |
|  +--------+ +--------+ +--------+ +--------+                |
|  | Spot   | | Spot   | | Spot   | | Spot   |                |
|  +--------+ +--------+ +--------+ +--------+                |
|  +--------+ +--------+ +--------+ +--------+                |
|  | Spot   | | Spot   | | Spot   | | Spot   |                |
|  +--------+ +--------+ +--------+ +--------+                |
|                                                             |
|  Diversified across AZs and Instance Types (c5.large,       |
|  m5.large, r5.large) to minimize Spot interruption risk.    |
+-------------------------------------------------------------+
```

### 3. Production Use Case: Instance Refresh and Lifecycle Hooks

**Instance Refresh**: You update your Launch Template with a new hardened AMI. You don't want to manually kill instances. You trigger an Instance Refresh. The ASG rolls out the new instances in batches, waits for them to become healthy behind the ALB, and then terminates the old ones.

**Lifecycle Hooks**: When an instance scales in (terminates), you want to cleanly drain connections or save logs. You add a `terminating:wait` hook. The instance goes into `Terminating:Wait` state. Your script runs, sends logs to S3, and then calls `aws autoscaling complete-lifecycle-action` to let the ASG finally kill it.

### 4. CLI Commands

Trigger an Instance Refresh:
```bash
aws autoscaling start-instance-refresh \
  --auto-scaling-group-name prod-web-asg \
  --preferences '{"MinHealthyPercentage": 90, "InstanceWarmup": 300}'
```

Check spot instance interruption notices (run inside the EC2 instance via metadata service):
```bash
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/spot/instance-action
```

### 5. Terraform Example Snippet

```hcl
resource "aws_launch_template" "app" {
  name_prefix   = "app-lt-"
  image_id      = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"

  iam_instance_profile {
    name = aws_iam_instance_profile.app_profile.name
  }
  
  user_data = filebase64("${path.module}/userdata.sh")
}

resource "aws_autoscaling_group" "app" {
  name                = "app-asg"
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.app.arn]
  
  min_size         = 2
  max_size         = 10
  desired_capacity = 2

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 2
      on_demand_percentage_above_base_capacity = 0 # 100% Spot above base
      spot_allocation_strategy                 = "capacity-optimized"
    }
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.app.id
        version            = "$Latest"
      }
      override { instance_type = "t3.micro" }
      override { instance_type = "t3.small" }
    }
  }
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Using Launch Configurations. They are deprecated. Always use Launch Templates.
- **Mistake**: Relying on a single Spot instance type. Always provide multiple overrides in a mixed instances policy so if AWS runs out of `c5.large`, it can use `m5.large`.
- **Best Practice**: Use `capacity-optimized` spot allocation strategy. AWS will launch instances from the deepest capacity pools, reducing interruption rates.
- **Best Practice**: Treat servers like cattle, not pets. If an instance is unhealthy, let the ASG kill it. Don't SSH in to fix it.

### 7. Troubleshooting
- **Symptom**: ASG keeps launching and terminating instances immediately.
- **Why?**: The EC2 instance passes EC2 health checks, but fails ALB health checks (e.g., the web server isn't starting due to a bad user-data script). The ALB reports it as unhealthy, the ASG terminates it, and tries again. Fix your user-data script.

### 8. Interview Q&A
**Q: How do you gracefully shut down an instance in an ASG so active connections aren't dropped?**
**A:** "Two things. First, enable Connection Draining (Deregistration Delay) on the ALB Target Group. This stops new requests from going to the instance while waiting for active requests to finish. Second, use an ASG Lifecycle Hook (`terminating:wait`) if you need to run custom scripts before the instance is actually terminated."

---

## SECTION 4: Load Balancing

Load balancing distributes traffic. But choosing the right one (ALB vs NLB) defines your architecture.

### 1. Internal Workflow + Request Flow

**ALB (Application Load Balancer - Layer 7)**
1. Client connects to ALB IP.
2. ALB terminates the SSL/TLS connection (TLS Offloading).
3. ALB inspects the HTTP headers (Host, Path, User-Agent).
4. ALB evaluates Listener Rules (e.g., if path is `/api/*`, route to Target Group B).
5. ALB establishes a *new* TCP connection to the backend instance. (The backend sees the ALB's IP, not the client's. Client IP is in the `X-Forwarded-For` header).

**NLB (Network Load Balancer - Layer 4)**
1. Client connects to NLB IP (NLBs provide static IPs per AZ).
2. NLB passes the TCP/UDP traffic directly to the backend instance.
3. The connection is *not* terminated at the NLB.
4. The backend instance sees the *actual Client Source IP* (Source IP preservation).
5. Ultra-low latency. Millions of requests per second.

### 2. ASCII Architecture Diagram: Host/Path Routing with ALB

```text
                      [ Client ]
                          | (HTTPS /api/v1/users)
                          v
                +-------------------+
                |       ALB         |
                |  Listener: 443    |
                +-------------------+
                          |
             +------------+-------------+
             |                          |
    Rule 1: Path=/api/*        Rule 2: Default (catch-all)
             |                          |
             v                          v
    [ Target Group 1 ]         [ Target Group 2 ]
    (Microservice APIs)        (Frontend Web Servers)
      +----+  +----+             +----+  +----+
      |EC2 |  |EC2 |             |EC2 |  |EC2 |
      +----+  +----+             +----+  +----+
```

### 3. Production Use Case: WAF Integration & Weighted Target Groups

**Blue/Green Deployments with Weighted Target Groups**:
You want to deploy v2 of your app with zero downtime. You create a second Target Group with the new code. On the ALB Listener Rule, you set a forward action to split traffic: 90% to TG-v1, 10% to TG-v2. You monitor metrics. If healthy, shift to 100%.

**ALB + WAF**:
You attach AWS WAF directly to the ALB. You configure rate limiting (block IPs making >1000 requests/5min) and managed rules for SQL Injection and Cross-Site Scripting (XSS). Malicious requests are blocked at the load balancer and never hit your EC2 instances.

### 4. CLI Commands

Find out which targets are failing health checks:
```bash
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-tg/1234
```

### 5. Terraform Example Snippet

```hcl
resource "aws_lb" "app" {
  name               = "production-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = module.vpc.public_subnets
}

resource "aws_lb_target_group" "app_tg" {
  name     = "app-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    timeout             = 5
    interval            = 10
    matcher             = "200"
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.app.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.domain.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Using a Classic Load Balancer (CLB). Just don't.
- **Mistake**: Backend security groups allowing `0.0.0.0/0` on port 80. Backend instances should ONLY accept traffic from the ALB's Security Group.
- **Best Practice**: Enable ALB Access Logs to S3. When an incident happens, you use Athena to query these logs to find out which IPs hit which paths.
- **Best Practice**: Use Deregistration Delay (Connection Draining). Default is 300s. Adjust this based on how long your longest requests take.

### 7. Troubleshooting
- **Symptom**: ALB returns 502 Bad Gateway.
- **Why?**: The ALB couldn't parse the response from the backend, or the backend closed the connection unexpectedly.
- **Symptom**: ALB returns 504 Gateway Timeout.
- **Why?**: The backend instance took too long to respond (exceeded the ALB idle timeout, default 60s). Check if database queries are hanging.

### 8. Interview Q&A
**Q: What is the difference between an ALB and an NLB?**
**A:** "ALB operates at Layer 7, routes based on HTTP headers/paths, terminates SSL, and changes the source IP (passes it in X-Forwarded-For). NLB operates at Layer 4, routes TCP/UDP, is meant for ultra-high throughput and low latency, provides static IPs per AZ, and preserves the client source IP to the backend."

---

## SECTION 5: S3 Deep Dive

S3 is not a file system. It's an object store. It has a flat structure (folders are just prefixes in the object key).

### 1. Internal Workflow + Request Flow

**S3 Consistency Model (Strong Consistency)**:
Since Dec 2020, S3 provides strong read-after-write consistency for all PUTs and DELETEs.
1. Thread A writes `data.json` to S3.
2. S3 replicates it internally across multiple storage nodes in the AZs.
3. Once the 200 OK is returned to Thread A, Thread B can read `data.json` and is guaranteed to get the latest version.

### 2. ASCII Architecture Diagram: S3 Transfer Acceleration & CloudFront

```text
[ User in Tokyo ]                        [ AWS Global Network ]
       |                                           |
       v                                           v
[ Tokyo Edge Location ] ======(fast fiber)======> [ us-east-1 S3 Bucket ]
(S3 Transfer Accel.)                               |
                                                   |-- PUT Object
                                                   |-- Trigger S3 Event
                                                   v
                                             [ SQS Queue ] -> [ Lambda Worker ]
```

### 3. Production Use Case: Multipart Upload & Presigned URLs

**Presigned URLs**: You have a private S3 bucket. A user authenticates to your web app and wants to download their invoice PDF. You DO NOT download the PDF to your web server and stream it to the user. Instead, your backend generates an S3 Presigned URL (using the backend's IAM credentials, valid for e.g., 5 minutes) and gives the URL to the frontend. The user's browser downloads directly from S3.

**Multipart Upload**: If a user uploads a 10GB video, you use Multipart Upload. The file is split into chunks. Each chunk is uploaded in parallel. If one fails, only that chunk is retried. S3 reassembles them at the end. Required for >5GB, recommended >100MB.

### 4. CLI Commands

Sync local directory to S3 (only uploads changed files):
```bash
aws s3 sync ./dist s3://my-frontend-bucket/ --delete
```

Generate a presigned URL valid for 1 hour:
```bash
aws s3 presign s3://my-private-bucket/invoice.pdf --expires-in 3600
```

### 5. Terraform Example Snippet

Setting up a bucket strictly for VPC Endpoint access only.

```hcl
resource "aws_s3_bucket" "data" {
  bucket = "company-secure-data-prod"
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket                  = aws_s3_bucket.data.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_iam_policy_document" "vpc_only" {
  statement {
    effect = "Deny"
    principals { type = "*" }
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.data.arn,
      "${aws_s3_bucket.data.arn}/*"
    ]
    condition {
      test     = "StringNotEquals"
      variable = "aws:SourceVpce"
      values   = ["vpce-12345678"] # Your VPC Endpoint ID
    }
  }
}

resource "aws_s3_bucket_policy" "vpc_only" {
  bucket = aws_s3_bucket.data.id
  policy = data.aws_iam_policy_document.vpc_only.json
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Using ACLs. S3 ACLs are legacy. Always enable "Block Public Access" and use IAM/Bucket Policies.
- **Mistake**: Deleting millions of objects using the CLI (`aws s3 rm --recursive`). It's too slow and you pay per API call.
- **Best Practice**: Use S3 Lifecycle Rules to delete millions of objects, or transition them to Glacier.
- **Best Practice**: Always enable Bucket Versioning in production to protect against accidental overwrites/deletes.

### 7. Troubleshooting
- **Symptom**: S3 bucket policy prevents even you (the admin) from accessing the bucket.
- **Why?**: You wrote a `Deny *` policy without conditions, locking yourself out. Only the AWS Account Root User can delete the bucket policy to restore access.

### 8. Interview Q&A
**Q: How do you enforce that objects are encrypted when uploaded to S3?**
**A:** "S3 now applies AES-256 (SSE-S3) encryption by default to all objects. However, if you mandate KMS encryption, you can write a Bucket Policy with a `Deny` effect for `s3:PutObject` if the `s3:x-amz-server-side-encryption` header is not equal to `aws:kms`."

---

## SECTION 6: RDS and Aurora

Relational databases. RDS is managed open-source (Postgres, MySQL). Aurora is AWS's proprietary cloud-native database engine.

### 1. Internal Workflow + Request Flow

**RDS Multi-AZ vs Read Replicas**:
- **Multi-AZ (High Availability)**: Synchronous replication at the block storage level to a standby instance in another AZ. You only get one endpoint. If the primary dies, DNS automatically fails over to the standby (takes 60-120 seconds). You cannot read from the standby.
- **Read Replicas (Scalability)**: Asynchronous replication at the database engine level. Replicas have their own endpoints. Used to offload read-heavy queries. They can be promoted to standalone DBs.

**Aurora Architecture**:
Compute is separated from storage. The storage layer is a distributed, purpose-built log-structured filesystem spanning 3 AZs. Data is replicated 6 ways (2 copies per AZ). Compute nodes just send redo logs to the storage layer. This makes Aurora much faster and more resilient than standard RDS.

### 2. ASCII Architecture Diagram: Aurora with RDS Proxy

```text
[ Lambda Functions ] --- (Many concurrent connections) ---> [ RDS Proxy ]
                                                                 |
                                                          (Connection Pool)
                                                                 |
    +------------------------------------------------------------+
    |                                                            |
    v                                                            v
[ Aurora Writer (Primary) ]                                [ Aurora Reader ]
         |                                                       |
         |-------------------------------------------------------|
         |         Aurora Distributed Storage Volume             |
         |         (6 copies across 3 AZs, auto-scales)          |
         +-------------------------------------------------------+
```

### 3. Production Use Case: RDS Proxy for Serverless

Lambda functions scale horizontally. If you get a traffic spike and 1000 Lambdas spin up, they will open 1000 connections to your RDS database, exhausting the DB's connection limit (`max_connections`) and crashing it. 

You deploy **RDS Proxy**. The Lambdas connect to the Proxy. The Proxy holds a pool of e.g., 50 warm connections to the DB and multiplexes the Lambda requests over them. Database saved.

### 4. CLI Commands

Force a failover in Multi-AZ (great for testing Game Days):
```bash
aws rds reboot-db-instance \
  --db-instance-identifier prod-db \
  --force-failover
```

### 5. Terraform Example Snippet

```hcl
resource "aws_db_instance" "postgres" {
  identifier           = "prod-postgres"
  engine               = "postgres"
  engine_version       = "15.3"
  instance_class       = "db.r6g.large"
  allocated_storage    = 100
  storage_type         = "gp3"
  
  db_name              = "appdb"
  username             = "admin"
  password             = jsondecode(data.aws_secretsmanager_secret_version.db.secret_string)["password"]
  
  multi_az             = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name = aws_db_subnet_group.default.name
  
  storage_encrypted    = true
  backup_retention_period = 7
  
  deletion_protection  = true
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Making RDS publicly accessible. Never do this. Put it in private/isolated subnets and use a VPN or Session Manager to connect.
- **Mistake**: Storing DB credentials in plaintext in environment variables.
- **Best Practice**: Use AWS Secrets Manager to store DB credentials and enable automatic rotation (Secrets Manager deploys a Lambda to change the password every 30 days).
- **Best Practice**: Use IAM Database Authentication instead of passwords where possible.

### 7. Troubleshooting
- **Symptom**: High DB CPU, queries are timing out.
- **Why?**: Open **Performance Insights**. Look at the DB Load chart grouped by Wait Events. If you see high `CPU` and high `IO:XactSync`, your queries are likely lacking indexes. Performance Insights will show you exactly which SQL statement is causing the load.

### 8. Interview Q&A
**Q: How does Aurora handle a compute node failure?**
**A:** "Because compute is decoupled from storage, if the primary writer fails, Aurora promotes one of the read replicas to become the new writer. Since the storage is shared, there is no data copying required. Failover typically takes under 30 seconds."

---

## SECTION 7: EKS Deep Dive

Elastic Kubernetes Service. Running K8s on AWS the right way.

### 1. Internal Workflow + Request Flow

**VPC CNI (Container Network Interface)**:
In standard Kubernetes (like Flannel), pods get virtual IPs that the underlying network doesn't understand. 
In EKS with the AWS VPC CNI, pods get *real IP addresses from your VPC subnets*.
1. Worker node has an ENI (Elastic Network Interface).
2. The ENI has a primary IP, and can have multiple Secondary IPs.
3. The CNI daemon assigns these Secondary IPs to the pods.
4. Because pods have real VPC IPs, you can route to them natively, and apply AWS Security Groups directly to pods!

### 2. ASCII Architecture Diagram: AWS Load Balancer Controller

```text
[ Internet ]
      |
[ ALB (Provisioned automatically) ]
      | (Routes traffic directly to Pod IP via VPC CNI)
      +-------------------+-------------------+
      |                   |                   |
[ Pod 1 (IP: 10.0.1.5) ]  [ Pod 2 (IP: 10.0.1.6) ]  (In EKS Worker Nodes)
```

### 3. Production Use Case: Karpenter

Forget Cluster Autoscaler. **Karpenter** is the modern way to scale EKS nodes.
1. A pod is scheduled but there's no space on current nodes. It goes into `Pending`.
2. Karpenter intercepts this. It calculates exactly what CPU/Memory the pod needs.
3. Karpenter calls EC2 Fleet API directly (bypassing ASGs entirely) and provisions a node of the exact right size (e.g., a Spot instance) just-in-time.
4. The node boots in seconds, the pod runs.

### 4. CLI Commands

Update your local kubeconfig to talk to EKS:
```bash
aws eks update-kubeconfig --region us-east-1 --name prod-cluster
```

### 5. Terraform Example Snippet

Using the official EKS module.

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3"

  cluster_name    = "prod-cluster"
  cluster_version = "1.28"

  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 5
      instance_types = ["m5.large"]
    }
  }

  manage_aws_auth_configmap = true
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Running out of IP addresses in your subnets because every EKS pod takes a real VPC IP. 
- **Best Practice**: Dedicate large CIDR blocks (e.g., `/19`) for EKS subnets if using VPC CNI.
- **Best Practice**: Upgrade the control plane first, verify addons, then upgrade node groups.

### 7. Troubleshooting
- **Symptom**: Pods are stuck in `ContainerCreating`.
- **Why?**: Describe the pod. You'll likely see `FailedCreatePodSandBox: failed to allocate IP`. The VPC CNI ran out of IP addresses in the subnet, or the node hit its max ENI limit.

### 8. Interview Q&A
**Q: How does IAM integrate with EKS?**
**A:** "Through IRSA (IAM Roles for Service Accounts). The EKS cluster acts as an OIDC identity provider. We create an IAM role trusting that OIDC provider, attach the role ARN to a Kubernetes ServiceAccount, and assign that to a pod. The pod receives temporary STS credentials seamlessly."

---

## SECTION 8: Lambda and Serverless

Serverless means no servers to manage, event-driven, and you pay per millisecond.

### 1. Internal Workflow + Request Flow

**The Cold Start Problem**:
1. Event triggers Lambda.
2. AWS allocates a Firecracker micro-VM.
3. Downloads your code.
4. Starts the runtime (e.g., Node.js, Java JVM).
5. Runs the initialization code (outside the handler). <-- **COLD START**
6. Runs the handler function.
7. The environment stays "warm" for a while. Subsequent requests skip steps 2-5.

**Lambda in a VPC**:
Previously, putting Lambda in a VPC caused massive cold starts because AWS had to create an ENI for every instance. Now, AWS uses **Hyperplane ENIs**. ENIs are created at function creation time and shared across executions. Cold starts are gone.

### 2. ASCII Architecture Diagram: Serverless Event-Driven

```text
[ API Gateway ] -> [ Lambda (Sync) ] -> [ DynamoDB ]
                               |
                               | (DynamoDB Streams)
                               v
                        [ EventBridge ] -> Rule: On New Order
                               |
                   +-----------+-----------+
                   |                       |
           [ SQS Queue ]           [ Lambda (Async) ]
           (For shipping app)      (Sends Email via SES)
```

### 3. Production Use Case: Provisioned Concurrency & Dead Letter Queues

**Provisioned Concurrency**: You have a Java Spring Boot Lambda. Cold starts take 5 seconds. Unacceptable for user-facing APIs. You enable Provisioned Concurrency. AWS keeps e.g., 50 instances warm at all times.

**Asynchronous Invocations and DLQs**: If an S3 event triggers a Lambda asynchronously and the Lambda fails (e.g., downstream API is down), Lambda retries twice. If it still fails, the event is dropped. You MUST configure a **Dead Letter Queue (DLQ)** (SQS or SNS) or **Lambda Destinations** to capture these failed events for replay.

### 4. CLI Commands

Invoke Lambda synchronously to test:
```bash
aws lambda invoke --function-name MyFunction --payload '{"key":"value"}' response.json
```

### 5. Terraform Example Snippet

```hcl
resource "aws_lambda_function" "api" {
  filename         = "function.zip"
  function_name    = "app-api"
  role             = aws_iam_role.lambda_exec.arn
  handler          = "index.handler"
  runtime          = "nodejs18.x"
  
  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.app.name
    }
  }
}

resource "aws_apigatewayv2_api" "http" {
  name          = "app-http-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.http.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.api.invoke_arn
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Putting database connection logic *inside* the handler. It reconnects every invocation! Put it *outside* the handler so it's reused during warm starts.
- **Best Practice**: Use HTTP APIs instead of REST APIs in API Gateway if you don't need advanced features (WAF, rate limiting per key). HTTP APIs are 70% cheaper and 50% faster.

### 7. Troubleshooting
- **Symptom**: Lambda is timing out exactly at 3 seconds.
- **Why?**: 3 seconds is the default timeout. If your API call takes 4 seconds, it fails. Increase the timeout.
- **Symptom**: Lambda async trigger processing same message multiple times.
- **Why?**: Idempotency. Network issues can cause at-least-once delivery. Ensure your Lambda code is idempotent (can run twice safely).

### 8. Interview Q&A
**Q: When should a Lambda function be placed inside a VPC?**
**A:** "Only when it absolutely needs to access private resources within that VPC, such as an RDS database, an ElastiCache cluster, or internal APIs. Otherwise, leave it outside the VPC, as it still has access to the internet and AWS public APIs."

---

## SECTION 9: Security Services

AWS security is defense in depth. Logging, monitoring, and proactive threat detection.

### 1. Internal Workflow + Request Flow

**GuardDuty workflow**:
1. GuardDuty ingests CloudTrail logs, VPC Flow Logs, and DNS logs in the background (no agents needed).
2. Uses machine learning and threat intelligence feeds.
3. Detects anomalies: "An EC2 instance is communicating with a known Bitcoin mining IP."
4. Generates a Finding.
5. Finding goes to EventBridge.
6. EventBridge triggers a Lambda to isolate the instance by changing its Security Group.

### 2. ASCII Architecture Diagram: Security Monitoring

```text
[ EC2 / VPC ]      [ API Calls ]
     |                  |
 (VPC Flow Logs)   (CloudTrail Logs)
     |                  |
     +---------+--------+
               |
               v
        [ GuardDuty ] ---> (Generates Finding)
               |
               v
        [ EventBridge ] ---> [ SNS ] -> Alert Security Team
               |
               v
           [ Lambda ] -> (Auto-Remediation: Block IP in WAF/NACL)
```

### 3. Production Use Case: AWS Config for Compliance

You want to ensure no developer ever creates a public S3 bucket.
You enable **AWS Config** and turn on the managed rule `s3-bucket-public-read-prohibited`.
If a developer creates a public bucket, Config flags it as Noncompliant. You configure automatic remediation: Config triggers a Systems Manager (SSM) document that immediately modifies the bucket to block public access.

### 4. CLI Commands

Query CloudTrail for a specific event (e.g., who deleted my DB?):
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteDBInstance
```

### 5. Terraform Example Snippet

```hcl
resource "aws_guardduty_detector" "primary" {
  enable = true
}

resource "aws_cloudtrail" "main" {
  name                          = "org-trail"
  s3_bucket_name                = aws_s3_bucket.trail.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true
}
```

### 6. Common Mistakes + Best Practices
- **Mistake**: Not enabling CloudTrail globally. Always enable multi-region CloudTrail, even if you only use one region (global events like IAM are logged in us-east-1).
- **Best Practice**: Use AWS Security Hub to aggregate findings from GuardDuty, Inspector, and Macie into a single pane of glass.

### 7. Troubleshooting
- **Symptom**: GuardDuty reports "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration".
- **Why?**: Someone stole the temporary STS credentials from an EC2 instance metadata service and is trying to use them from an IP address outside of AWS. This is a critical security breach (SSRF vulnerability).

### 8. Interview Q&A
**Q: What is the difference between Secrets Manager and Systems Manager (SSM) Parameter Store?**
**A:** "Both store secrets and use KMS encryption. Secrets Manager is more expensive but supports automatic secret rotation (e.g., changing DB passwords automatically) and cross-account access easily. SSM Parameter Store is free for standard parameters and is great for basic configuration data and simple secrets."

---

## SECTION 10: Monitoring and Observability

You can't fix what you can't see.

### 1. Internal Workflow + Request Flow

**CloudWatch Logs Insights**:
Logs are ingested into Log Groups. Instead of downloading gigabytes of logs to grep, you use Insights. It uses a purpose-built query language to scan terabytes of logs in seconds across multiple log groups.

### 2. Production Use Case: Composite Alarms

You have a microservice. Sometimes CPU spikes briefly, which is fine. Sometimes DB latency spikes briefly, which is fine. But if CPU > 80% AND DB Latency > 100ms simultaneously, the system is failing.
Instead of pager fatigue from individual alarms, you create a **Composite Alarm** that only triggers if both child alarms are in ALARM state.

### 3. CLI Commands

Publish a custom metric:
```bash
aws cloudwatch put-metric-data \
  --namespace "MyApp" \
  --metric-name "ActiveUsers" \
  --value 150
```

### 4. Terraform Example Snippet

```hcl
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "ec2-cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

### 5. Common Mistakes + Best Practices
- **Mistake**: Logging sensitive PII or passwords to CloudWatch.
- **Best Practice**: Set Log Group retention policies! By default they are "Never Expire", which will cost you a fortune over time. Set it to 14 or 30 days.

---

## SECTION 11: Cost Optimization

FinOps is a core DevOps skill.

### 1. Production Use Case: Savings Plans vs Spot

- **Spot Instances**: Use for stateless, fault-tolerant workloads (batch processing, CI/CD runners, EKS worker nodes). 70-90% discount.
- **Compute Savings Plans**: You commit to spending $X/hour for 1 or 3 years. Applies to EC2, Fargate, and Lambda automatically. Massive discount without tying you to a specific instance family.

### 2. Common Mistakes + Best Practices
- **Mistake**: The hidden NAT Gateway cost. NAT GW charges per GB processed. If internal instances are sending massive data to S3 over NAT GW, you get a huge bill. Use a Gateway VPC Endpoint for S3 to keep traffic internal and free.
- **Best Practice**: Use S3 Intelligent Tiering if you don't know the access patterns. It automatically moves untouched objects to cheaper storage tiers.

---

## SECTION 12: Disaster Recovery Patterns

### 1. DR Strategies (From Cheapest/Slowest to Most Expensive/Fastest)

1. **Backup & Restore**: Data backed up to S3. If disaster strikes, provision infrastructure via Terraform, restore DB from snapshot. (RTO: Hours, RPO: Hours)
2. **Pilot Light**: Core DB is continuously replicated to DR region. App servers are OFF. In disaster, turn ON app servers. (RTO: Tens of minutes).
3. **Warm Standby**: Scaled down version of full environment running in DR region. (RTO: Minutes).
4. **Multi-Site Active-Active**: Both regions take production traffic globally via Route53 latency routing. (RTO: Zero, RPO: Zero).

---

## SECTION 13: Production AWS Architecture

Let's put it all together.

### 1. ASCII Diagram: Complete 3-Tier Architecture

```text
               [ AWS Shield / WAF ]
                        |
            [ Route 53 (DNS / Routing) ]
                        |
    +-------------------+-------------------+
    |                                       |
[ CloudFront ]                           [ ALB ]
 (Static Assets)                            |
    |                                       |
[ S3 Bucket ]                  +------------+------------+
                          AZ-A |                         | AZ-B
                      [ EKS Worker Node ]       [ EKS Worker Node ]
                      (App Microservices)       (App Microservices)
                               |                         |
                      +--------+-------------------------+
                      |
           [ RDS Proxy (Connection Pool) ]
                      |
           +----------+----------+
           |                     |
  [ RDS Aurora Primary ]   [ RDS Aurora Reader ]
  (AZ-A / Writer)          (AZ-B / Reader)
```

### 2. Architecture Challenge: Design for 1M+ Users
**Solution**:
1. Global edge caching with CloudFront and S3 for frontend.
2. Route53 routing to regional ALBs.
3. Compute layer: EKS with Karpenter auto-scaling spot instances.
4. Database: Aurora Serverless v2 or Aurora Global Database.
5. Caching: ElastiCache for Redis in front of RDS.
6. Async processing: SQS queues + Lambda for decoupled backend tasks.
7. Security: WAF, Private subnets, VPC Endpoints, Secrets Manager.

---

## END OF CHAPTER

### Top 50 AWS Interview Takeaways (Quick Fire)
1. SG vs NACL: Stateful instance vs Stateless subnet.
2. IAM Role vs User: Roles are assumed temporarily, Users have long-lived credentials.
3. ALB vs NLB: L7 (HTTP/HTTPS) vs L4 (TCP/UDP).
4. Spot vs On-Demand: 90% discount, can be interrupted with 2-min warning.
5. RDS vs Aurora: Standard DB vs cloud-native distributed storage engine.
6. S3 Classes: Standard, IA, Glacier.
7. CloudTrail vs Config: API calls (who did what) vs resource state (what changed).
8. VPC Endpoints: Keep traffic on AWS backbone, no internet needed.
9. Launch Template vs Config: Template supports versioning, always use it.
10. SQS DLQ: Catch failed async messages.

### Hands-on Lab Suggestions
1. Terraform a 3-tier VPC architecture.
2. Deploy an ALB routing to an ASG of Apache servers.
3. Setup an EKS cluster with Karpenter and deploy a test pod.
4. Trigger a Lambda function via an S3 put event.
5. Create an IAM policy that allows access to only a specific folder in S3.

Mastering AWS is about understanding the boundaries between services, networking fundamentals, and security primitives. Go build.
