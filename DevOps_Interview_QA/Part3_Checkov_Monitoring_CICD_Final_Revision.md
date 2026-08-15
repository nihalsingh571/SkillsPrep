# DevOps Interview QA - Part 3: Checkov, Monitoring, CI/CD & Final Revision

=== SECTION 8: CHECKOV / PRODUCTION / MONITORING (Q80–Q92) ===

---
**Q80. What is Checkov? Why did you use Checkov for Terraform, Kubernetes, and Docker?**

**Short Interview Answer:** Checkov is a static code analysis tool specifically designed for Infrastructure as Code (IaC). I used Checkov to shift security left, automatically scanning our Terraform, Kubernetes manifests, and Dockerfiles for security misconfigurations and compliance violations during the CI pipeline, preventing insecure infrastructure from reaching production.

**Detailed Explanation:**
Checkov, maintained by Prisma Cloud (Palo Alto Networks), parses IaC files and evaluates them against hundreds of built-in policies (like CIS benchmarks). 
- **For Terraform:** It checks if S3 buckets are encrypted, if security groups allow 0.0.0.0/0, or if RDS has backups enabled.
- **For Kubernetes:** It checks if containers are running as root, if CPU/memory limits are set, or if read-only root filesystems are enforced.
- **For Docker:** It checks for exposed sensitive ports, running as root, or missing HEALTHCHECK instructions.

**Why & How:** 
- **Why:** Finding security flaws in production is costly and risky. Checking IaC code before deployment saves time and prevents breaches.
- **How:** Checkov builds a graph of your infrastructure configurations and evaluates it using Python-based policies. It integrates seamlessly into GitHub Actions, Jenkins, or GitLab CI, failing the build if high-severity issues are found.

**Real-World Example:** 
In my previous project, developers occasionally created S3 buckets without encryption in Terraform. By integrating Checkov in our GitHub Actions PR workflow, any PR introducing an unencrypted bucket was automatically blocked, and the developer received a comment on how to fix it before the code was even merged.

**Example/Commands:**
```bash
# Install checkov
pip install checkov

# Scan a Terraform directory
checkov -d ./terraform-dir

# Scan a Kubernetes manifest
checkov -f deployment.yaml

# Scan a Dockerfile
checkov -f Dockerfile

# Output as JSON for CI/CD reporting
checkov -d . -o json
```

**Troubleshooting:**
- **Problem:** Checkov fails a build due to a known but acceptable risk (e.g., a public S3 bucket meant for website hosting).
- **Possible Causes:** Checkov strictly enforces best practices, but context matters.
- **Checks:** Review the Checkov output identifying the specific policy ID (e.g., CKV_AWS_20).
- **Fix:** Add an inline skip comment in the Terraform code: `# checkov:skip=CKV_AWS_20: This bucket hosts public web assets`
- **Verification:** Re-run the scan to ensure it passes with the skip acknowledged.

**Difficult Terms:** 
- **Static Code Analysis:** Examining source code before it is run (or deployed) to find vulnerabilities.
- **Shift-left security:** Moving security checks to the earliest possible phase of the software development lifecycle.

**Interview Answer:** 
"I implemented Checkov because we needed a unified tool to secure our IaC across multiple domains—Terraform, Kubernetes, and Docker. By running Checkov in our CI/CD pipelines, we caught misconfigurations like unencrypted databases, containers running as root, and exposed Docker ports before they ever reached AWS. It helped us shift security left, enforce CIS benchmarks, and educate developers on secure coding practices without slowing down delivery."

---
**Q81. What are the common Checkov errors you encounter while scanning Terraform, Kubernetes, and Docker configurations?**

**Short Interview Answer:** Common errors include unencrypted storage or overly permissive security groups in Terraform, missing resource limits or running as root in Kubernetes, and using the `latest` tag or lacking a `USER` instruction in Dockerfiles.

**Detailed Explanation:**
When scanning IaC, Checkov flags violations based on predefined policies.
- **Terraform Errors:**
  - `CKV_AWS_20`: S3 bucket does not have public access block.
  - `CKV_AWS_79`: RDS instance does not have backup enabled.
  - `CKV_AWS_24`: Security group allows ingress from 0.0.0.0/0 on SSH (port 22).
- **Kubernetes Errors:**
  - `CKV_K8S_11`: CPU and memory limits are not set.
  - `CKV_K8S_21`: Container is running with root privileges.
  - `CKV_K8S_38`: ServiceAccount token is automatically mounted.
- **Docker Errors:**
  - `CKV_DOCKER_2`: HEALTHCHECK instruction is missing.
  - `CKV_DOCKER_3`: Container runs as root (missing `USER` command).
  - `CKV_DOCKER_7`: Base image uses `latest` tag instead of a specific version.

**Why & How:** 
These checks exist to align infrastructure with the Principle of Least Privilege, enforce high availability (backups), and prevent resource exhaustion (K8s limits). Checkov evaluates the Abstract Syntax Tree (AST) of the files to detect missing or incorrectly configured attributes.

**Real-World Example:** 
A junior developer deployed a Redis pod without memory limits. The pod consumed all node memory, causing an OutOfMemory (OOM) killer to terminate critical system pods. After that incident, we enabled Checkov to strictly enforce `CKV_K8S_11` (resource limits), and the pipeline would fail if limits were missing.

**Example/Commands:**
```yaml
# Kubernetes example failing CKV_K8S_11
apiVersion: v1
kind: Pod
metadata:
  name: bad-pod
spec:
  containers:
  - name: myapp
    image: myapp:1.0
    # Missing resources block causes Checkov failure!

# Fixing it to pass Checkov
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

**Troubleshooting:**
- **Problem:** Frequent pipeline failures due to overly strict Dockerfile checks (e.g., missing HEALTHCHECK).
- **Possible Causes:** The Checkov policy is universally applied, but some base images don't support standard health checks easily.
- **Checks:** Review pipeline logs to identify the failing check ID.
- **Fix:** If the check is deemed unnecessary globally, configure a `.checkov.yaml` config file to skip specific policies globally, or use inline skips in the Dockerfile.
- **Verification:** Run `checkov -f Dockerfile --config-file .checkov.yaml`.

**Difficult Terms:** 
- **OOM Killer:** A Linux kernel process that terminates processes when the system is critically low on memory.
- **AST (Abstract Syntax Tree):** A tree representation of the structure of source code, used by Checkov to understand configurations.

**Interview Answer:** 
"In Terraform, the most frequent flags I see are unencrypted S3 buckets, missing KMS keys for RDS, or open SSH ports. For Kubernetes, it's almost always developers forgetting to define CPU/Memory limits, or not dropping root privileges. In Docker, it's missing HEALTHCHECKs or using the 'latest' tag. I usually handle these by setting up automated pipeline blocks for critical issues, while providing clear remediation steps in the PR comments so developers know exactly how to fix them."

---
**Q82. After receiving a Checkov scan report, what steps do you follow before deployment?**

**Short Interview Answer:** I review the report to categorize issues by severity. Critical and high vulnerabilities must be fixed immediately. For false positives or acceptable risks, I apply documented suppressions. Medium/low issues are added to the technical debt backlog, and only then is the deployment approved.

**Detailed Explanation:**
The CI/CD pipeline stops and outputs a Checkov report if thresholds are breached. The procedure is:
1. **Analyze:** Parse the JSON/CLI output to understand the failing policies.
2. **Prioritize:** Focus on `CRITICAL` and `HIGH` severity. 
3. **Remediate:** Work with developers to fix actual vulnerabilities (e.g., removing a public IP from a database).
4. **Suppress:** If a policy flag is a known, accepted risk (e.g., an S3 bucket meant for public website hosting), add an inline suppression (`# checkov:skip`) with a justification.
5. **Backlog:** Log `LOW` severity issues (like missing tags) into Jira for future sprints.
6. **Re-run:** Trigger the pipeline again. Deployment proceeds only when the pipeline is green.

**Why & How:** 
You cannot blindly block every deployment for minor issues, nor can you ignore critical ones. A structured triage process ensures security without paralyzing developer velocity.

**Real-World Example:** 
During a major release, Checkov flagged 50+ missing tags (Low severity) and one open security group (High severity). We fixed the security group immediately, suppressed two checks that were false positives due to a complex Terraform module, and created a Jira ticket for the missing tags, allowing the release to proceed on time securely.

**Example/Commands:**
```bash
# Run Checkov and only fail the build for HIGH or CRITICAL issues
checkov -d . --hard-fail-on HIGH,CRITICAL

# Output Checkov results in JUnit XML format for Jenkins to parse
checkov -d . -o junitxml > checkov-report.xml
```

**Troubleshooting:**
- **Problem:** Pipeline is stuck because a developer doesn't understand the Checkov error.
- **Possible Causes:** Cryptic policy IDs like `CKV_AWS_123`.
- **Checks:** Look up the Checkov documentation link provided in the CI output.
- **Fix:** Each Checkov failure outputs a URL explaining the issue and providing exact code snippets to fix it. Share this with the developer.
- **Verification:** Developer updates code, pushes, pipeline goes green.

**Difficult Terms:** 
- **False Positive:** A test result that incorrectly indicates a vulnerability is present.
- **Technical Debt:** The implied cost of future reworking required when choosing an easy/fast solution now instead of a better approach.

**Interview Answer:** 
"When a Checkov report fails a build, I first look at the severity. Anything Critical or High, like a public database or missing encryption, is a hard blocker and I work with the devs to fix it immediately using Checkov's remediation guides. If it's a false positive or an accepted risk, I add a targeted inline skip comment with a justification for audit purposes. Low severity issues like missing resource tags get ticketed into our backlog. Once the criticals are cleared and skips are documented, I re-trigger the pipeline to proceed with the deployment."

---
**Q83. Explain one production issue you handled and how you resolved it.**

**Short Interview Answer:** I handled an issue where our EKS cluster ran out of IP addresses because of rapid pod scaling, causing new deployments to fail. I resolved it temporarily by clearing unused pods, and permanently by attaching secondary IPv4 CIDR blocks to the VPC and configuring the AWS VPC CNI to use custom networking.

**Detailed Explanation:**
In an AWS EKS environment using the default VPC CNI, every Pod gets a secondary IP address from the VPC subnets.
1. **The Incident:** During a Black Friday traffic spike, our autoscaler spun up hundreds of new Pods.
2. **The Symptom:** New Pods stayed in `ContainerCreating` or `Pending` state. Deployment pipelines failed.
3. **The Investigation:** `kubectl describe pod <name>` showed the error `Failed to create pod sandbox: rpc error: ... networkPlugin cni failed to set up pod: add cmd: failed to assign an IP address to container`. 
4. **The Resolution:** 
   - *Immediate:* Deleted dormant internal testing deployments to free up IPs.
   - *Permanent:* Added a secondary CIDR block (e.g., `100.64.0.0/16` CGNAT range) to the VPC. Configured `ENIConfig` custom resources in EKS so the CNI plugin would allocate Pod IPs from this new massive subnet, while nodes remained on the primary subnet.

**Why & How:** 
AWS VPC CNI natively routes Pod IPs within the VPC, which is great for performance but drains VPC IP pools quickly. Custom networking separates the node subnets from pod subnets, solving IP exhaustion.

**Real-World Example:** 
This actually happened at my last e-commerce company. We had a /24 subnet (256 IPs) for private subnets. Between EC2 nodes, load balancers, and pods, we hit the limit in 20 minutes of high traffic. Moving pods to a /16 secondary CIDR completely eliminated the bottleneck.

**Example/Commands:**
```bash
# Check why pod is pending
kubectl get pods
kubectl describe pod pending-pod-name
# Look for "Failed to assign an IP address" in Events

# Check available IPs in AWS CLI
aws ec2 describe-subnets --subnet-ids subnet-12345 --query 'Subnets[*].AvailableIpAddressCount'
```

**Troubleshooting:**
- **Problem:** Pods stuck in `Pending`.
- **Possible Causes:** Node resources full (CPU/Mem), IP exhaustion, missing Persistent Volumes.
- **Checks:** `kubectl describe pod`, check Node IP capacity.
- **Fix:** Implement EKS custom networking with ENIConfigs.
- **Verification:** Scale a dummy deployment to 500 pods and ensure they all receive IPs from the new CGNAT range.

**Difficult Terms:** 
- **CNI (Container Network Interface):** The plugin in Kubernetes responsible for assigning IP addresses to Pods (e.g., AWS VPC CNI, Calico, Flannel).
- **CGNAT (Carrier-Grade NAT):** A specific IP range (100.64.0.0/10) often used for secondary Pod networks because it doesn't conflict with standard RFC1918 private IPs.

**Interview Answer:** 
"One major production issue I resolved was VPC IP exhaustion in our EKS cluster. During a traffic spike, our CI/CD pipelines started failing because new Pods were stuck in the Pending state. `kubectl describe` revealed the AWS VPC CNI couldn't assign IP addresses because our private subnets were full. To mitigate it quickly, I scaled down non-critical staging workloads. For the permanent fix, I architected a solution using EKS Custom Networking. I attached a secondary CGNAT /16 CIDR block to the VPC, deployed ENIConfigs, and configured the CNI to draw Pod IPs from this massive new pool. We never faced IP exhaustion again."

---
**Q84. You mentioned rollback. How do you prepare a rollback strategy before deployment?**

**Short Interview Answer:** A rollback strategy involves ensuring backward compatibility of databases, keeping previous immutable container images available, using deployment strategies like Blue/Green or Canary, and maintaining IaC state backups. I ensure a single click or command can instantly revert the environment to the last known good state.

**Detailed Explanation:**
Preparation is key to a successful rollback:
1. **Immutable Artifacts:** Every build gets a unique tag (e.g., Git commit SHA). Never use `latest`. This ensures you can deploy `myapp:v1.2` immediately if `myapp:v1.3` fails.
2. **Database Migrations:** Code must be forward and backward compatible with the database. We use the "expand and contract" pattern (add new columns, don't delete old ones until the next release) so the old code can still run if rolled back.
3. **Deployment Strategy:** Using Helm for Kubernetes allows instant rollbacks using `helm rollback`. Blue/Green deployments keep the old infrastructure running; rolling back is just an ALB routing change.
4. **IaC State:** In Terraform, we rely on versioned S3 state files. If a TF apply breaks infrastructure, we can revert the code and re-apply, or restore state if absolutely necessary.

**Why & How:** 
Things break in production despite testing. If a rollback takes 30 minutes to rebuild code, you lose customers. Pre-baking artifacts and maintaining parallel states (Blue/Green) reduces MTTR (Mean Time To Recovery) to seconds.

**Real-World Example:** 
We deployed a new checkout microservice. Within 5 minutes of Hypercare, Datadog showed a 40% spike in 500 errors. Because we used Helm and immutable tags, I simply ran `helm rollback checkout-service 1`, and traffic returned to normal in 10 seconds. We then debugged the bad image offline.

**Example/Commands:**
```bash
# Helm Rollback Example
# 1. Check history
helm history my-app -n production
# Output:
# REVISION  UPDATED                   STATUS      CHART       APP VERSION
# 1         Mon Oct 2 10:00:00 2023   superseded  app-1.0.0   v1.0
# 2         Mon Oct 2 11:00:00 2023   deployed    app-1.1.0   v1.1

# 2. Rollback to revision 1
helm rollback my-app 1 -n production

# Kubernetes native rollout undo
kubectl rollout undo deployment/my-app -n production
```

**Troubleshooting:**
- **Problem:** Application rolled back successfully, but now it's crashing because the database schema was altered by the bad deployment.
- **Possible Causes:** Destructive database migrations (e.g., dropping a column) were run simultaneously with the code deployment.
- **Checks:** Check app logs for "Column not found" SQL exceptions.
- **Fix:** Restore database from the pre-deployment snapshot, or run the reverse database migration script.
- **Verification:** Verify application starts connecting to the DB correctly.

**Difficult Terms:** 
- **Immutable Artifact:** A deployment package (like a Docker image) that is built once and never changed; updates require a new artifact with a new version tag.
- **Expand and Contract Pattern:** A DB migration strategy where you first add a new column (Expand), update code to use it, and in a future release, drop the old column (Contract).

**Interview Answer:** 
"I prepare for rollbacks at three layers. First, at the artifact layer, I enforce immutable Docker tags so we can always revert to the exact previous image. Second, at the deployment layer, I use Helm and Kubernetes Deployments, which allow a one-command `helm rollback` or `kubectl rollout undo` to restore the previous ReplicaSet instantly. Third, at the database layer, I enforce backward-compatible migrations—developers are not allowed to drop or rename columns during a standard release, only add them. If an issue is caught by our Datadog alerts during deployment, the CI/CD pipeline triggers an automatic rollback via a webhook, achieving an MTTR of under a minute."

---
**Q85. What is the Hypercare period after deployment? How long do you monitor an application?**

**Short Interview Answer:** Hypercare is a critical, intensive monitoring phase immediately following a production deployment. The DevOps and Dev teams actively watch live dashboards, logs, and user metrics to catch anomalies early. It typically lasts from a few hours to 48 hours depending on the release complexity.

**Detailed Explanation:**
- **What it is:** Instead of deploying and walking away, the team sits in a "war room" (or a dedicated Slack/Teams call). We stare at Datadog/Prometheus dashboards looking for CPU spikes, 5xx error rates, latency increases, and database deadlocks.
- **Duration:** For minor microservice updates, Hypercare might last 1-2 hours. For major platform migrations or core architecture changes, it can last 1 to 2 weeks.
- **The Process:** 
  1. Deployment completes.
  2. Run synthetic tests (smoke tests) against production.
  3. Monitor APM (Application Performance Monitoring) for latency and error rates.
  4. Monitor infrastructure (Node/Pod CPU/Memory).
  5. Check customer support channels for user-reported issues.
  6. Sign-off and return to standard on-call monitoring.

**Why & How:** 
Many bugs only manifest under real user traffic and production data volume. Hypercare ensures that if a critical failure occurs, the team is already assembled and can trigger a rollback in seconds, rather than waking up to a P1 incident 4 hours later.

**Real-World Example:** 
We migrated our payment gateway provider. The deployment succeeded, and synthetic tests passed. However, during the 4-hour Hypercare window, we noticed on our Grafana dashboard that payments originating from legacy mobile app versions were failing with 400 errors. Because we were actively monitoring, we caught it in 15 minutes, deployed a hotfix, and saved thousands in lost revenue.

**Example/Commands:**
```bash
# During hypercare, aggressively tailing logs of a new deployment
kubectl logs -f deployment/payment-service -n prod --tail=100 | grep "ERROR"

# Watching pod restarts in real-time
watch -n 2 kubectl get pods -n prod
```

**Troubleshooting:**
- **Problem:** Error rates spike immediately during Hypercare.
- **Possible Causes:** Code bug, missing environment variable, database connection limits reached.
- **Checks:** Check APM traces, pod logs, and infrastructure metrics.
- **Fix:** If the cause isn't immediately obvious and fixable within 5 minutes, execute the rollback plan.
- **Verification:** Ensure metrics return to pre-deployment baseline after rollback.

**Difficult Terms:** 
- **Synthetic Tests:** Automated scripts simulating user behavior (e.g., logging in, adding to cart) to verify system functionality continuously.
- **APM (Application Performance Monitoring):** Tools (like Datadog, New Relic, AppDynamics) that track software performance at the code level (e.g., slow database queries, slow functions).

**Interview Answer:** 
"Hypercare is the 'high-alert' period immediately following a production release. Instead of waiting for alerts to trigger, our engineering and DevOps teams actively monitor dashboards—Grafana, Kibana, or Datadog—watching application latency, error rates, and resource utilization. For standard deployments, I usually enforce a 1 to 2-hour Hypercare window. During this time, if error rates breach our SLA thresholds, we don't try to debug in production; we immediately execute our rollback strategy to restore service, and then investigate the logs offline. It's about minimizing customer impact."

---
**Q86. Production Scenario: Users report that the application is running slowly. How would you troubleshoot the issue end-to-end?**

**Short Interview Answer:** I use a top-down approach. I start at the edge (CDN/WAF latency), move to the Load Balancer (Target response times), check APM for application code bottlenecks, investigate Kubernetes node/pod resources (CPU throttling), and finally check the Database for slow queries, deadlocks, or high connection counts.

**Detailed Explanation:**
Troubleshooting "slowness" is complex because the bottleneck could be anywhere.
1. **Edge/Network:** Check Cloudflare/Route53/CloudFront. Is there a DDoS attack? Is latency high before it even reaches AWS?
2. **Load Balancer (ALB):** Check AWS CloudWatch for `TargetResponseTime` and `HTTPCode_Target_5XX_Count`. If TargetResponseTime is high, the backend is slow.
3. **Infrastructure (Kubernetes/EC2):** Use Grafana/Prometheus. Are Nodes or Pods hitting 100% CPU? Are Pods being CPU throttled by Kubernetes limits? Is there high Disk I/O wait?
4. **Application (APM):** Look at Datadog/New Relic APM traces. Is a specific API endpoint taking 5 seconds? Is it waiting on an external 3rd party API?
5. **Database:** Look at RDS Performance Insights. Are there slow queries? Is the CPU at 100% due to missing indexes? Are we hitting maximum connection limits?

**Why & How:** 
A top-down isolation method prevents guessing. You look at metrics at each layer to definitively rule it in or out, narrowing down the root cause systematically.

**Real-World Example:** 
Users reported our inventory app was slow. I checked the ALB; target response time spiked from 50ms to 4000ms. I checked K8s pods; CPU was fine. I looked at Datadog APM and saw the delay was entirely inside database calls. I opened RDS Performance Insights and found a missing table index was causing full table scans due to a new feature release. We added the index, and latency dropped back to 50ms.

**Example/Commands:**
```bash
# Check if pods are getting restarted or CPU throttled
kubectl top pods -n production
kubectl describe node <node-name>

# Check Linux OS level stats if on EC2
top          # Check CPU/Load Average
iostat -xz 1 # Check Disk I/O bottlenecks
free -m      # Check memory/swap
```

**Troubleshooting:**
- **Problem:** Application is slow, but CPU/Memory on servers are completely normal.
- **Possible Causes:** Application is blocked waiting for an external dependency (like a payment gateway), or database lock contention.
- **Checks:** APM distributed traces, RDS locking metrics.
- **Fix:** Implement timeouts/circuit breakers for 3rd party APIs, or optimize DB transactions.
- **Verification:** Ensure 99th percentile (p99) latency returns to normal levels.

**Difficult Terms:** 
- **Target Response Time:** The time elapsed from when a load balancer sends a request to a backend target until it receives the response.
- **CPU Throttling:** When a container tries to use more CPU than its allowed limit, the kernel pauses it, causing severe application latency without crashing the pod.

**Interview Answer:** 
"When dealing with latency, I follow a systematic top-down isolation strategy. First, I check the ALB metrics in CloudWatch—specifically `TargetResponseTime`—to confirm if the delay is network-level or backend-level. Next, I check our infrastructure in Grafana: are our EKS pods experiencing CPU throttling, or are the EC2 nodes out of memory? If infrastructure is healthy, I dive into Datadog APM to trace the slow requests. 90% of the time, slowness is at the data layer, so I'll check RDS Performance Insights for slow SQL queries, locked tables, or exhausted connection pools. Once I isolate the layer, I can scale resources, rollback bad code, or apply DB indexes to resolve it."

---
**Q87. Which AWS Application Load Balancer (ALB) metrics do you monitor regularly?**

**Short Interview Answer:** I monitor `TargetResponseTime` for latency, `HTTPCode_Target_5XX_Count` for backend application errors, `HTTPCode_ELB_5XX_Count` for load balancer exhaustion, `RequestCount` for traffic spikes, and `UnHealthyHostCount` to ensure backend targets are passing health checks.

**Detailed Explanation:**
ALB metrics are the most critical indicator of application health because they sit between the users and your servers.
- **TargetResponseTime:** Measures application latency. If this spikes, your app or DB is slow.
- **HTTPCode_Target_5XX_Count:** The number of 500-level errors generated by your application backend. Indicates bad deployments or crashing code.
- **HTTPCode_ELB_5XX_Count:** Errors generated by the ALB itself (e.g., 502 Bad Gateway, 504 Gateway Timeout). Usually means the backend targets are down or not responding in time.
- **RequestCount:** Total requests. Monitored for sudden spikes (DDoS or viral traffic) or sudden drops (DNS/network failure upstream).
- **HealthyHostCount / UnHealthyHostCount:** Shows how many EC2 instances or Pods are passing the ALB health checks. If Healthy drops to 0, total outage.
- **TargetConnectionErrorCount:** Failures in establishing connections to targets.

**Why & How:** 
The ALB sees all HTTP traffic. Monitoring these metrics via CloudWatch Alarms allows you to trigger automated responses, such as Auto Scaling groups adding more servers when `RequestCount` or `TargetResponseTime` increases.

**Real-World Example:** 
I set up a CloudWatch Alarm that triggers a PagerDuty alert if `HTTPCode_Target_5XX_Count` exceeds 5% of total requests over a 5-minute period. One night, a database migration locked a critical table. The application started throwing 500 errors. The ALB metric caught it, alerted me, and I was able to kill the locked query before customers noticed a widespread outage.

**Example/Commands:**
```json
// Example Terraform snippet creating an alarm for ALB 5xx errors
resource "aws_cloudwatch_metric_alarm" "alb_5xx_errors" {
  alarm_name          = "alb-high-5xx-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "HTTPCode_Target_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = "60"
  statistic           = "Sum"
  threshold           = "100"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions = {
    LoadBalancer = aws_lb.main.arn_suffix
  }
}
```

**Troubleshooting:**
- **Problem:** Spikes in `HTTPCode_ELB_502_Count` (502 Bad Gateway).
- **Possible Causes:** The backend closed the connection prematurely, or the ALB idle timeout is longer than the backend server's keep-alive timeout.
- **Checks:** Compare ALB idle timeout settings with backend web server (Nginx/Tomcat) keep-alive settings.
- **Fix:** Increase the backend web server's keep-alive timeout to be greater than the ALB's idle timeout.
- **Verification:** Monitor the metric; 502s should drop to zero.

**Difficult Terms:** 
- **502 Bad Gateway:** The load balancer acting as a gateway received an invalid response from the backend server.
- **504 Gateway Timeout:** The load balancer did not get a response from the backend server within the configured timeout period.

**Interview Answer:** 
"To ensure high availability, I monitor five golden ALB metrics in CloudWatch. First, `TargetResponseTime` to track application latency. Second, `HTTPCode_Target_5XX_Count` to catch application-level crashes or bugs. Third, `HTTPCode_ELB_5XX_Count`—specifically 502s and 504s—to detect network timeouts or targets closing connections prematurely. Fourth, `UnHealthyHostCount` to ensure our target groups have enough active compute capacity. Finally, `RequestCount` to identify sudden traffic surges or drops. I tie these metrics to CloudWatch Alarms and PagerDuty to guarantee a fast response to production incidents."

---
**Q88. Apart from DevOps, what other technologies or domains have you worked on or learned?**

**Short Interview Answer:** Alongside core DevOps, I have strong experience in Cloud Security (IAM, WAF, Checkov), basic Backend Development (Python/Go for scripting APIs), FinOps (AWS Cost Optimization), and Database Administration (managing RDS, writing SQL queries for debugging).

**Detailed Explanation:**
A modern Senior DevOps engineer is often a "Platform Engineer," touching many domains:
- **Cloud Security:** Managing AWS IAM Least Privilege, configuring Web Application Firewalls (WAF), setting up KMS encryption, and integrating security scanners (Checkov, SonarQube, Trivy).
- **Development/Scripting:** Writing Python Lambda functions for automation (e.g., auto-stopping EC2 instances at night), using Go for Kubernetes operators, or writing Bash for complex CI/CD tasks.
- **FinOps (Financial Operations):** Analyzing AWS Cost Explorer, purchasing Compute Savings Plans/Reserved Instances, implementing lifecycle policies for S3, and rightsizing EC2/Kubernetes nodes using Karpenter to save money.
- **Database Administration (DBA):** While not a full DBA, knowing how to take RDS snapshots, setup Read Replicas, configure Parameter Groups, and run SQL queries to find locked tables is crucial for troubleshooting.

**Why & How:** 
DevOps sits at the intersection of all teams. Understanding security prevents breaches. Understanding code helps you talk to developers. Understanding FinOps keeps the company profitable. 

**Real-World Example:** 
I utilized my FinOps skills when I noticed our AWS bill spiking. I wrote a Python Boto3 script that ran weekly to find and delete unattached EBS volumes and outdated snapshots. I also moved our non-production EKS node groups to EC2 Spot Instances, reducing our AWS compute bill by 40%.

**Example/Commands:**
```python
# Python Boto3 script to find unattached EBS volumes (Dev/Scripting domain)
import boto3

ec2 = boto3.client('ec2')
volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

for vol in volumes['Volumes']:
    print(f"Unattached volume found: {vol['VolumeId']}, Size: {vol['Size']}GB")
    # ec2.delete_volume(VolumeId=vol['VolumeId']) # Uncomment to delete
```

**Troubleshooting:**
- **Problem:** AWS bill is significantly higher than last month.
- **Possible Causes:** Orphaned resources (EBS, EIPs), oversized instances, huge CloudWatch log ingestion.
- **Checks:** AWS Cost Explorer grouped by Service and Usage Type.
- **Fix:** Implement tagging strategies, right-size instances, delete unused resources.
- **Verification:** Monitor daily spend in Cost Explorer to confirm it drops.

**Difficult Terms:** 
- **FinOps:** The practice of bringing financial accountability to the variable spend model of cloud computing.
- **Spot Instances:** Unused AWS EC2 capacity available at up to a 90% discount, but AWS can reclaim them with a 2-minute warning.

**Interview Answer:** 
"To be an effective DevOps engineer, I've had to expand into adjacent domains. I have a strong focus on DevSecOps—implementing WAFs, enforcing strict IAM policies, and integrating Checkov for IaC scanning. I also have solid FinOps experience; in my last role, I optimized our AWS infrastructure using Spot Instances and S3 lifecycle rules, cutting costs by 30%. Additionally, I write Python and Bash extensively for writing custom automation scripts and Lambda functions, which helps me bridge the gap between operations and software development."

---
**Q89. How do you monitor context switches in Linux? Which commands do you use?**

**Short Interview Answer:** I use commands like `vmstat`, `pidstat`, and `sar` to monitor context switches. High context switching indicates the CPU is spending too much time swapping processes instead of executing them, often caused by having too many threads or poorly optimized applications.

**Detailed Explanation:**
A context switch occurs when the CPU scheduler stops executing one process (or thread), saves its state, and loads the state of another process to execute it.
- **Commands:**
  - `vmstat 1` : Shows system-wide context switches under the `cs` column. (1 means update every 1 second).
  - `pidstat -w 1`: Shows context switches per specific process. It breaks them down into:
    - *cswch/s* (Voluntary): Process yields CPU because it's waiting for I/O (disk/network).
    - *nvcswch/s* (Non-voluntary): Process is forced to yield CPU because its time slice expired (CPU starvation).
  - `sar -w 1`: Collects, reports, and saves system activity information, including context switches.

**Why & How:** 
Context switches are normal in multitasking, but excessive switching (millions per second) wastes CPU cycles on operating system overhead rather than application work. This causes high CPU usage but low actual throughput.

**Real-World Example:** 
We had a Java application running on an EC2 instance that was at 90% CPU, but handling very few requests. I ran `vmstat 1` and saw the `cs` (context switches) column was over 500,000 per second. I then ran `pidstat -wt 1` and found the Java process had spawned 10,000 threads. The CPU was thrashing trying to manage them. We tuned the Tomcat thread pool down to 200, and CPU usage dropped to 20%.

**Example/Commands:**
```bash
# System-wide context switches
$ vmstat 1
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 2  0      0 123456  78901 234567    0    0    12    34  500 8000 15  5 80  0  0
# Look at the 'cs' column (8000 context switches per second here)

# Context switches per process
$ pidstat -w 1
10:00:00 AM   UID       PID   cswch/s nvcswch/s  Command
10:00:01 AM  1000      1234   1500.00    500.00  java
```

**Troubleshooting:**
- **Problem:** High CPU usage, but application throughput is very low.
- **Possible Causes:** High context switching due to thread explosion, interrupt storms (bad hardware/drivers).
- **Checks:** `vmstat 1` (look at `cs`), `top` (look at `sy` - system CPU time).
- **Fix:** Tune application thread pools, use asynchronous I/O (like Node.js or Java NIO) instead of thread-per-request models.
- **Verification:** Observe `cs` drop in `vmstat` and application throughput increase.

**Difficult Terms:** 
- **Voluntary Context Switch:** Process asks to wait (e.g., waiting for database response).
- **Non-Voluntary Context Switch:** OS forces the process off the CPU because its turn is over.
- **Thrashing:** When a system spends more time managing resources (like swapping memory or threads) than performing actual productive work.

**Interview Answer:** 
"To monitor context switches in Linux, I primarily use `vmstat 1` to get a system-wide view looking at the 'cs' column. If I see an abnormally high number—like hundreds of thousands per second—I know the CPU is thrashing. To isolate the exact culprit, I use `pidstat -w`. This is incredibly useful because it distinguishes between voluntary context switches, where an app is waiting on I/O, and non-voluntary context switches, where the CPU is starved. I typically see this issue when Java or Node applications are misconfigured and spawn thousands of threads, and the fix is usually tuning the application's thread pool or worker count."

---
=== SECTION 9: CI/CD / JENKINS / KUBERNETES / AUTOMATION (Q90–Q100) ===

**Q90. Explain the CI/CD pipeline using Jenkins and GitHub. (Start from developer push to production deployment — every stage with tools.)**

**Short Interview Answer:** The pipeline starts with a GitHub push triggering a Jenkins webhook. Jenkins checks out the code, runs unit tests and SonarQube, builds a Docker image, scans it with Trivy, pushes it to AWS ECR, and finally updates the Kubernetes manifests. ArgoCD detects the manifest change and syncs the new image to the EKS production cluster.

**Detailed Explanation:**
A modern CI/CD flow has distinct stages:
1. **Source (GitHub):** Developer pushes code to a feature branch and creates a PR.
2. **Trigger:** GitHub Webhook sends a payload to Jenkins.
3. **Continuous Integration (Jenkins):**
   - *Checkout:* Jenkins clones the repo.
   - *Test:* Runs Maven/npm tests (JUnit/Jest).
   - *Static Analysis (SAST):* SonarQube scans code for bugs/smells. Checkov scans IaC.
   - *Build:* `docker build` creates the container image.
   - *Security Scan:* Trivy scans the local Docker image for CVE vulnerabilities.
4. **Artifact Storage:** If scans pass, Jenkins tags the image (using Git SHA) and pushes it to an artifact registry like AWS ECR, DockerHub, or Nexus.
5. **Continuous Deployment (GitOps/ArgoCD):**
   - Jenkins updates the deployment YAML file in a separate "manifests" Git repository with the new image tag.
   - ArgoCD (running inside Kubernetes) constantly polls this Git repo.
   - ArgoCD detects the change and automatically applies (`kubectl apply`) the new state to the cluster, performing a rolling update.

**Why & How:** 
Separating CI (building/testing) from CD (deploying) using GitOps ensures that the cluster state always matches Git. If the cluster crashes, ArgoCD can rebuild it instantly from Git. It also removes the need to give Jenkins direct Admin access to the Kubernetes cluster.

**Real-World Example:** 
At my last job, we automated this entirely. A developer merges a PR. Jenkins builds and pushes `myapp:vabc123` to ECR, and commits `image: myapp:vabc123` to our config repo. Within 3 minutes, ArgoCD syncs the changes to our AWS EKS staging cluster. Once QA approves, a similar pipeline promotes it to production. 

**Example/Commands:**
```groovy
// Jenkinsfile snippet
pipeline {
    agent any
    environment {
        ECR_REPO = "12345.dkr.ecr.us-east-1.amazonaws.com/myapp"
        GIT_SHA = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    stages {
        stage('Test & Sonar') {
            steps { sh 'mvn clean test sonar:sonar' }
        }
        stage('Docker Build & Trivy Scan') {
            steps {
                sh "docker build -t ${ECR_REPO}:${GIT_SHA} ."
                sh "trivy image --exit-code 1 --severity CRITICAL ${ECR_REPO}:${GIT_SHA}"
            }
        }
        stage('Push to ECR') {
            steps {
                sh "aws ecr get-login-password | docker login --username AWS --password-stdin ${ECR_REPO}"
                sh "docker push ${ECR_REPO}:${GIT_SHA}"
            }
        }
        stage('Update Manifests Repo') {
            steps {
                // Bash script to clone manifest repo, sed new image tag, commit and push
                sh "./update-gitops-repo.sh ${GIT_SHA}"
            }
        }
    }
}
```

**Troubleshooting:**
- **Problem:** Jenkins pipeline successfully finishes, but the new code isn't in Kubernetes.
- **Possible Causes:** ArgoCD sync is paused, ArgoCD webhook failed, or the image tag update in Git failed.
- **Checks:** Check Jenkins logs for the Git push step. Check ArgoCD dashboard for Sync status.
- **Fix:** If ArgoCD is out of sync, click "Sync" manually or fix the syntax error in the updated YAML manifest.
- **Verification:** `kubectl describe deployment myapp` to verify the new image tag is running.

**Difficult Terms:** 
- **GitOps:** A methodology where a Git repository is the single source of truth for infrastructure and application configurations.
- **CVE (Common Vulnerabilities and Exposures):** A database of publicly disclosed information security issues (used by Trivy).

**Interview Answer:** 
"My ideal CI/CD pipeline uses Jenkins for CI and ArgoCD for CD. When a developer merges to the main branch, a GitHub webhook triggers Jenkins. Jenkins checks out the code, runs unit tests, and executes SonarQube for code quality. Next, it builds a Docker image and scans it with Trivy. If no critical vulnerabilities are found, Jenkins pushes the immutable image to AWS ECR. For the CD portion, instead of Jenkins running kubectl directly, Jenkins simply commits the new image tag to a separate GitOps repository. ArgoCD, running inside our EKS cluster, detects this Git commit and automatically syncs the new deployment to the cluster. This GitOps approach is highly secure and provides a perfect audit trail."

---
**Q91. If you have to set up a CI/CD pipeline from scratch, how would you do it? What tools would you use and why?**

**Short Interview Answer:** I would use GitHub Actions for CI, AWS ECR for the image registry, and ArgoCD for Continuous Deployment to Kubernetes. I choose GitHub Actions over Jenkins because it requires zero server maintenance, and ArgoCD because it enforces GitOps, providing better security and easy rollbacks.

**Detailed Explanation:**
If starting from scratch today, I avoid self-hosted heavy tools unless legally required.
1. **Source Control:** GitHub or GitLab. (Industry standard, great developer experience).
2. **CI Tool:** GitHub Actions. 
   - *Why:* No Jenkins master server to maintain, patch, or upgrade. Native integration with code. Ephemeral, scalable runners.
3. **Quality & Security:** 
   - *SAST:* SonarCloud (SaaS version of SonarQube).
   - *IaC Scan:* Checkov or Checkov GitHub Action.
   - *Container Scan:* Trivy Action.
4. **Artifact Repository:** AWS ECR or GitHub Container Registry (GHCR). 
   - *Why:* Highly available, integrated IAM permissions if deploying to AWS.
5. **CD Tool:** ArgoCD.
   - *Why:* Pull-based deployment. The cluster pulls config from Git, meaning you don't have to expose your Kubernetes API server to the internet or CI tools. 
6. **Infrastructure:** Terraform via GitHub Actions to provision the underlying EKS clusters and VPCs.

**Why & How:** 
The goal of a modern setup is "NoOps" for the tooling itself. You want to spend time building pipelines, not managing Jenkins VMs, handling plugin dependency hell, or upgrading Java versions.

**Real-World Example:** 
I was hired at a startup using manual bash scripts for deployment. Within a month, I migrated them to GitHub Actions. I created reusable workflows for Node.js builds, added Trivy scanning, and set up ArgoCD in their EKS cluster. Deployment time went from 45 minutes of manual work to 4 minutes fully automated, and developers loved the native GitHub UI.

**Example/Commands:**
```yaml
# Sample GitHub Actions CI setup from scratch
name: CI to ECR
on:
  push:
    branches: [ main ]
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Tests
        run: npm test
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::123:role/github-role
          aws-region: us-east-1
      - name: Build and Push Docker image
        run: |
          docker build -t my-repo/app:${{ github.sha }} .
          docker push my-repo/app:${{ github.sha }}
```

**Troubleshooting:**
- **Problem:** GitHub Actions runs out of free minutes, or fails to connect to private AWS resources.
- **Possible Causes:** Using public GitHub runners for heavy workloads or private VPC deployments.
- **Checks:** Check billing or network timeout errors in logs.
- **Fix:** Deploy Self-Hosted GitHub Runners inside the AWS VPC (e.g., using Actions Runner Controller on EKS).
- **Verification:** Run the pipeline; the job should show `runs-on: self-hosted` and succeed.

**Difficult Terms:** 
- **OIDC (OpenID Connect):** A protocol used by GitHub Actions to securely authenticate with AWS (assume an IAM role) without needing to store long-lived static AWS access keys as secrets.
- **Ephemeral Runners:** CI runners that are created fresh for a single job and destroyed immediately after, ensuring a clean state and high security.

**Interview Answer:** 
"If I were building a pipeline from scratch today, I would move away from Jenkins and use GitHub Actions for CI and ArgoCD for CD. I prefer GitHub Actions because it's a managed service—there are no master nodes to maintain, no plugin conflicts to debug, and it uses OIDC to authenticate with AWS without storing static secrets. For deployment, I would definitely implement GitOps with ArgoCD. By having ArgoCD pull configurations from a Git repository into Kubernetes, we eliminate the need to grant our CI server direct access to the cluster's API, vastly improving our security posture while making rollbacks as simple as a Git revert."

---
**Q92. Given the following Kubernetes Pod information:
`pods = [{"name": "api-7d8f", "status": "Running", "restarts": 0}, {"name": "api-3a2b", "status": "Running", "restarts": 5}, {"name": "worker-9c1e", "status": "CrashLoopBackOff", "restarts": 12}, {"name": "redis-4f5a", "status": "Running", "restarts": 1}]`
Identify the problematic Pod(s) and explain how you would investigate the issue.**

**Short Interview Answer:** The problematic Pod is `worker-9c1e` (in CrashLoopBackOff with 12 restarts) and potentially `api-3a2b` (Running but with 5 restarts). I would investigate the worker pod by running `kubectl describe pod` to check events and exit codes, and `kubectl logs --previous` to see why the container crashed before it restarted.

**Detailed Explanation:**
- **Identifying the Issues:**
  1. `worker-9c1e` is the most critical. `CrashLoopBackOff` means the container starts, crashes immediately, and Kubernetes is backing off (waiting longer) before trying to restart it again. 
  2. `api-3a2b` is currently Running, but 5 restarts indicate it occasionally crashes (perhaps hitting memory limits/OOMKilled) or fails liveness probes.
- **Investigation Steps for `worker-9c1e`:**
  1. **Describe:** `kubectl describe pod worker-9c1e`. Scroll to the bottom to look at "Events" (e.g., Back-off restarting failed container, or scheduling issues) and look at the "State" section for the `Exit Code` (e.g., Code 137 means OOMKilled, Code 1 means application error).
  2. **Logs:** `kubectl logs worker-9c1e`. Since it's crashing, current logs might be empty.
  3. **Previous Logs:** `kubectl logs worker-9c1e --previous`. This is crucial. It shows the logs of the container *just before* it crashed, which usually contains the Python/Java stack trace or the fatal error message.

**Why & How:** 
Kubernetes tries to keep applications highly available by restarting failed containers. However, if the application has a fatal configuration error (e.g., missing database credentials), it will fail endlessly. `CrashLoopBackOff` is a protection mechanism to prevent the kubelet from burning CPU by restarting a broken app millions of times a second.

**Real-World Example:** 
I saw a worker pod in `CrashLoopBackOff`. `kubectl describe` showed `Exit Code 1`. I ran `kubectl logs worker-9c1e --previous` and saw `KeyError: 'AWS_ACCESS_KEY'`. The developer had added a new environment variable requirement in the code, but forgot to add it to the Kubernetes Deployment YAML. We added the env var, and the pod started successfully.

**Example/Commands:**
```bash
# 1. Identify exit codes and reasons
kubectl describe pod worker-9c1e

# 2. View logs of the crashed instance
kubectl logs worker-9c1e --previous

# 3. If investigating api-3a2b (which has 5 restarts but is running)
# Check if it was OOMKilled recently
kubectl describe pod api-3a2b | grep -A 5 "Last State:"
```

**Troubleshooting:**
- **Problem:** `kubectl logs --previous` shows nothing.
- **Possible Causes:** The container process never even started (e.g., bad entrypoint command, missing file).
- **Checks:** Check `kubectl describe pod` for `CreateContainerConfigError` or `RunContainerError`.
- **Fix:** Fix the Dockerfile ENTRYPOINT or correct the configmap mount path in the YAML.
- **Verification:** Delete the pod to force a recreation; it should stay in `Running` state.

**Difficult Terms:** 
- **CrashLoopBackOff:** A state indicating a pod is repeatedly failing to start and Kubernetes is applying an exponential delay before trying again.
- **Exit Code 137:** Process was terminated by the SIGKILL signal, almost always due to OOMKilled (Out of Memory).

**Interview Answer:** 
"Looking at the list, `worker-9c1e` is completely down in a CrashLoopBackOff state, and `api-3a2b` is unstable with 5 restarts. I would immediately focus on the worker pod. First, I would run `kubectl describe pod worker-9c1e` to check the pod Events and specifically look at the Exit Code of the last termination. If it's 137, it's a memory issue. If it's an application error, I would run `kubectl logs worker-9c1e --previous`. The `--previous` flag is the secret weapon here because it retrieves the logs from the container instance right before it died, which almost always contains the fatal stack trace or missing configuration error. For `api-3a2b`, I'd check if it's failing its liveness probes occasionally under heavy load."

---
**Q93. I have a script/program that I want to run every 2 hours. How would you schedule and automate it? (Cover cron on Linux, systemd timer, Kubernetes CronJob, and GitHub Actions schedule — give examples of each.)**

**Short Interview Answer:** I can schedule it at the OS level using Linux `cron` or `systemd timers` for standalone VMs. In a containerized environment, I use a Kubernetes `CronJob` to ensure high availability. For CI/CD and automation tasks outside of production infrastructure, I use a `GitHub Actions schedule`.

**Detailed Explanation:**
- **1. Linux Cron:** The traditional Unix task scheduler. Simple but hard to monitor centrally. Good for simple VM backups.
- **2. Systemd Timer:** The modern Linux alternative to cron. It integrates with systemctl, provides better logging (journalctl), and can trigger dependencies. 
- **3. Kubernetes CronJob:** The cloud-native way. K8s spins up a Pod on a schedule, runs the script, and destroys the Pod. Highly available (if a node dies, K8s schedules it elsewhere).
- **4. GitHub Actions:** Great for operational tasks (e.g., scanning repos, building nightly images) without needing to maintain any infrastructure.

**Why & How:** 
The choice depends on the environment. Hardcoding a crontab on a random EC2 instance is an anti-pattern in modern cloud (pet vs. cattle). Using Kubernetes CronJobs or GitHub Actions brings scheduling into Infrastructure as Code, making it version-controlled and observable.

**Real-World Example:** 
We had a script to clear stale database sessions. Originally, it was a cron job on an EC2 instance. When that EC2 instance was accidentally terminated, the job stopped running, causing database bloat. I containerized the Python script and deployed it as a Kubernetes CronJob. Now, it's version-controlled in Git, and Kubernetes ensures it runs every 2 hours regardless of underlying node failures.

**Example/Commands:**
```bash
# 1. Linux Cron (Run every 2 hours)
# Edit with: crontab -e
0 */2 * * * /path/to/script.sh >> /var/log/script.log 2>&1
```
```ini
# 2. Systemd Timer
# /etc/systemd/system/myscript.timer
[Unit]
Description=Run script every 2 hours
[Timer]
OnCalendar=*-*-* 00/2:00:00
[Install]
WantedBy=timers.target
# Enable with: systemctl enable --now myscript.timer
```
```yaml
# 3. Kubernetes CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-script-job
spec:
  schedule: "0 */2 * * *" # Every 2 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: script
            image: my-python-script:1.0
          restartPolicy: OnFailure
```
```yaml
# 4. GitHub Actions Schedule
name: Run Script
on:
  schedule:
    - cron: '0 */2 * * *'
jobs:
  run-it:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running automation script"
```

**Troubleshooting:**
- **Problem:** Kubernetes CronJob spawns multiple concurrent pods and crashes the database.
- **Possible Causes:** The script takes 3 hours to run, but the schedule triggers every 2 hours, causing overlap.
- **Checks:** `kubectl get jobs`, check duration.
- **Fix:** Set `concurrencyPolicy: Forbid` in the CronJob spec so it won't start a new job if the old one is still running.
- **Verification:** Wait for the next schedule tick; no new pod should spawn if the old one is active.

**Difficult Terms:** 
- **Concurrency Policy:** Rules defining what happens if a new scheduled job is triggered before the previous one finishes (Allow, Forbid, Replace).
- **cron expression:** A string of 5 (or 6) fields separated by spaces that represents a set of times (Minute Hour Day Month DayOfWeek). `0 */2 * * *` means minute 0, every 2nd hour, every day.

**Interview Answer:** 
"Depending on where the architecture lives, I have four approaches. For legacy standalone Linux VMs, I can use a standard `crontab` entry or a `systemd timer`. A systemd timer is preferred there because it writes standard logs to journalctl. However, in a modern cloud environment, I avoid local cron. If the workload is containerized, I deploy a Kubernetes `CronJob`. This is highly resilient; if a node fails, K8s just runs the job on another node, and I can set a `concurrencyPolicy` to prevent overlapping runs. Finally, if it's an infrastructure or CI/CD maintenance script—like cleaning up old ECR images—I use a GitHub Actions scheduled workflow, which entirely removes the need to manage scheduling infrastructure."

---
**Q94. How would you troubleshoot a Kubernetes Pod that is in CrashLoopBackOff? (Give complete step-by-step approach with every command.)**

**Short Interview Answer:** I use a 4-step approach. 1. `kubectl get pods` to identify the pod. 2. `kubectl describe pod` to check events, state, and exit codes (like 137 for OOM). 3. `kubectl logs <pod> --previous` to see the application error right before the crash. 4. If logs are empty, `kubectl get events --sort-by='.metadata.creationTimestamp'` to check for cluster-level issues like missing secrets.

**Detailed Explanation:**
CrashLoopBackOff means the pod starts, crashes, and K8s is waiting to restart it. 
- **Step 1: Status Check.** `kubectl get pods -n <namespace>`
- **Step 2: Describe.** `kubectl describe pod <pod-name> -n <namespace>`
  - Look at `State: Waiting` (Reason: CrashLoopBackOff).
  - Look at `Last State: Terminated` -> `Reason: Error` -> `Exit Code: X`.
  - Exit Code `1`: Application code error (syntax, missing file).
  - Exit Code `137`: OOMKilled (Out of memory).
  - Exit Code `255`: Node failed.
  - Look at `Events` at the bottom for errors like `FailedMount` or `Back-off restarting failed container`.
- **Step 3: Logs.** `kubectl logs <pod-name> -n <namespace> --previous`
  - Because it's crashing, current logs might be empty. `--previous` shows the logs of the dead container. Look for Python/Java stack traces or DB connection timeouts.
- **Step 4: Debug Container (Optional).** If the image lacks tools, run a temporary debug pod or shell into a crashing one (if it stays up for a few seconds). `kubectl exec -it <pod-name> -- /bin/sh` (Hard to do if it crashes instantly).

**Why & How:** 
A container crashes because the main process (PID 1) exits. Kubernetes detects PID 1 exiting and restarts the container. You must find out *why* PID 1 decided to exit.

**Real-World Example:** 
A new frontend pod went into CrashLoopBackOff. `kubectl describe` showed Exit Code 1. `kubectl logs --previous` showed `nginx: [emerg] host not found in upstream "backend-service" in /etc/nginx/nginx.conf`. The root cause was that the backend service had a typo in its Kubernetes Service YAML, so Nginx couldn't resolve the DNS and crashed on startup.

**Example/Commands:**
```bash
# Get pod details
kubectl get pods -n prod

# Describe to find exit code and events
kubectl describe pod frontend-5bb8c7d -n prod

# Get logs of the previous crashed instance
kubectl logs frontend-5bb8c7d -n prod --previous

# Check cluster events in chronological order for broader issues
kubectl get events --sort-by='.metadata.creationTimestamp' -n prod
```

**Troubleshooting:**
- **Problem:** Pod is in CrashLoopBackOff, but logs are completely empty, and describe shows `CreateContainerConfigError`.
- **Possible Causes:** The pod is trying to mount a ConfigMap or Secret that doesn't exist. The container never actually started, so there are no logs.
- **Checks:** Look at the Events in `kubectl describe pod`.
- **Fix:** Create the missing Secret or ConfigMap, or fix the typo in the pod YAML volume mount.
- **Verification:** The pod should automatically transition to `ContainerCreating` and then `Running`.

**Difficult Terms:** 
- **PID 1:** The first process started in a Linux container. If this process stops, the container stops.
- **Exponential Backoff:** The delay Kubernetes adds between restarts (10s, 20s, 40s, up to 5 minutes) to prevent overloading the system.

**Interview Answer:** 
"To troubleshoot a CrashLoopBackOff, I follow a strict diagnostic path. First, I run `kubectl describe pod`. I check the 'Events' at the bottom to see if it's failing to mount a volume or pull a secret. Then I check the 'Last State' for the Exit Code. If it's 137, I know we need to increase memory limits because it was OOMKilled. If the Exit Code is 1, it's an application error. To find that error, my next step is running `kubectl logs <pod-name> --previous`. This pulls the stdout from the container just before it died. 95% of the time, that log contains the exact exception, like a database connection failure or a missing environment variable, allowing me to apply the fix immediately."

---
**Q95. Why do we use monitoring tools like Prometheus and Zabbix? What is the difference between them?**

**Short Interview Answer:** We use monitoring tools to gain visibility into system health, track performance metrics (CPU, latency), and trigger alerts before outages affect users. Prometheus is a modern, cloud-native tool designed for dynamic environments like Kubernetes using a pull model. Zabbix is a traditional, robust tool often used for static VMs and network devices using a push/agent model.

**Detailed Explanation:**
- **Why we need them:** Without monitoring, you are flying blind. You only know a server is down when a customer complains. Monitoring allows proactive alerting, capacity planning (tracking disk usage over months), and debugging (correlating CPU spikes with deployments).
- **Prometheus:** 
  - **Architecture:** Pull-based. It scrapes metrics from HTTP endpoints (e.g., `/metrics`) exposed by applications or exporters.
  - **Data Model:** Multi-dimensional time-series database. Metrics have key-value labels (e.g., `http_requests{status="500", app="frontend"}`).
  - **Ecosystem:** Heavily integrated with Kubernetes and Grafana. Very dynamic (auto-discovers pods as they spin up/down).
- **Zabbix:** 
  - **Architecture:** Push-based (usually via Zabbix Agent installed on servers).
  - **Data Model:** Relational database (MySQL/PostgreSQL) backing it. Hierarchical templates.
  - **Ecosystem:** Excellent for legacy IT, static VMs, network switches (SNMP), and environments with strict firewall rules where pull-based scraping is hard.

**Why & How:** 
Prometheus thrives in ephemeral environments. If a Kubernetes pod lives for 5 minutes, Prometheus discovers it via the K8s API, scrapes it, and remembers the data. Zabbix struggles with thousands of constantly changing IPs, but excels at deep OS-level monitoring of permanent database servers.

**Real-World Example:** 
In a hybrid cloud migration, I used both. We kept Zabbix on-premise to monitor our physical Cisco switches, VMware hosts, and legacy Oracle databases because Zabbix has great out-of-the-box templates for physical hardware. For our new AWS EKS environment, I deployed Prometheus and Grafana, because Prometheus natively understands Kubernetes auto-scaling and exposes custom application metrics seamlessly.

**Example/Commands:**
```yaml
# Prometheus configuration snippet (prometheus.yml) showing Pull model
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

**Troubleshooting:**
- **Problem:** Prometheus is missing metrics for a newly deployed application.
- **Possible Causes:** The application doesn't expose a `/metrics` endpoint, or the Kubernetes Service lacks the correct annotations.
- **Checks:** Try to `curl http://pod-ip:port/metrics`. Check pod annotations.
- **Fix:** Add `prometheus.io/scrape: "true"` to the pod annotations in the deployment YAML.
- **Verification:** Check the "Targets" page in the Prometheus UI to see if the pod is now listed and "UP".

**Difficult Terms:** 
- **Time-Series Database (TSDB):** A database optimized for storing data points associated with time stamps (e.g., CPU usage every 5 seconds).
- **Pull Model (Prometheus):** The monitoring server reaches out to the target to grab data.
- **Push Model (Zabbix/Datadog):** The target runs an agent that sends data to the monitoring server.

**Interview Answer:** 
"Monitoring tools are essential for proactive incident management and capacity planning. The choice between Prometheus and Zabbix usually comes down to architecture. I use Prometheus in modern, cloud-native environments like Kubernetes. It uses a pull model, a powerful query language (PromQL), and dynamic service discovery, which is perfect for pods that are constantly created and destroyed. On the other hand, I use Zabbix for more traditional infrastructure. It uses an agent-based push model and is fantastic for monitoring static VMs, legacy databases, and network appliances via SNMP. In many large enterprises, you'll actually see both used side-by-side for their respective strengths."

---
**Q96. Why would you choose Terraform instead of AWS CloudFormation? Give a detailed comparison.**

**Short Interview Answer:** I choose Terraform because it is cloud-agnostic, allowing me to manage AWS, Datadog, and GitHub from one tool using a unified language (HCL). Terraform also has the `plan` command to preview changes safely before applying them, whereas CloudFormation is strictly AWS-only and uses verbose JSON/YAML.

**Detailed Explanation:**
- **Provider Support (The biggest difference):** 
  - *CloudFormation:* Native to AWS. It manages AWS resources perfectly but cannot easily manage resources outside AWS.
  - *Terraform:* Multi-cloud. It uses a provider plugin system. In one Terraform state, I can create an AWS EKS cluster, configure a Kubernetes namespace inside it, set up a Datadog monitor for it, and create a GitHub repo for the code.
- **Language:**
  - *CloudFormation:* JSON or YAML. Can become extremely long and hard to read. (Though AWS CDK improves this).
  - *Terraform:* HashiCorp Configuration Language (HCL). It is highly readable, supports complex logic (loops, conditionals), and modularity.
- **State Management:**
  - *CloudFormation:* Managed by AWS automatically. You don't have to worry about storing state files.
  - *Terraform:* Uses a `.tfstate` file. You must manage this file securely (usually in an S3 bucket with DynamoDB locking) to coordinate team deployments.
- **Execution Strategy:**
  - *CloudFormation:* You submit a template, and AWS figures it out. Difficult to see exactly what will change without Change Sets (which can be clunky).
  - *Terraform:* `terraform plan` clearly shows exactly what will be created, updated, or destroyed (in a git diff style) before you run `terraform apply`.

**Why & How:** 
Modern DevOps environments use a mix of SaaS tools (AWS, PagerDuty, Cloudflare). Using Terraform allows a team to learn one tool (HCL) and codify their entire tech stack, not just their cloud provider.

**Real-World Example:** 
We needed to deploy a new microservice. Using Terraform, I wrote a single module that: 1. Created the AWS ECS cluster. 2. Created the Cloudflare DNS records pointing to the ALB. 3. Created PagerDuty services for on-call alerting. Doing this in CloudFormation would have required writing custom Python Lambda functions (Custom Resources) to talk to the Cloudflare and PagerDuty APIs.

**Example/Commands:**
```hcl
# Terraform multi-provider example in one file
provider "aws" { region = "us-east-1" }
provider "github" { token = var.github_token }

# Create AWS S3 Bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "company-assets-bucket"
}

# Create GitHub Repo
resource "github_repository" "my_repo" {
  name        = "new-microservice"
  description = "Managed by Terraform"
}
```

**Troubleshooting:**
- **Problem:** Two developers run Terraform at the same time, corrupting the infrastructure.
- **Possible Causes:** Local state file usage or missing state locking.
- **Checks:** Check if `backend "s3"` is configured with a DynamoDB table.
- **Fix:** Implement remote state with state locking using an S3 bucket and DynamoDB table.
- **Verification:** Run `terraform apply` on two machines simultaneously; the second one should error out with "Error acquiring the state lock."

**Difficult Terms:** 
- **Cloud-Agnostic:** Software that is compatible across multiple cloud providers (AWS, Azure, GCP).
- **State File (.tfstate):** A JSON file Terraform uses to map the code you wrote to the real-world resources it created.

**Interview Answer:** 
"While CloudFormation is great for strict, AWS-only environments because of its deep native integration, I almost always choose Terraform. The primary reason is its multi-provider ecosystem. With Terraform, I can use HCL to provision an AWS EKS cluster, create Datadog monitoring dashboards, and configure Cloudflare DNS all in a single pipeline. CloudFormation is strictly AWS-centric. Secondly, the developer experience is much better; `terraform plan` gives a crystal-clear, diff-style preview of exactly what will change before any destructive actions happen, which is critical for production safety."

---

## FINAL REVISION SHEET — DEVOPS INTERVIEW

### SECTION A: TOP 20 MOST IMPORTANT CONCEPTS
1. **Infrastructure as Code (IaC):** Managing infrastructure using code (Terraform, Ansible) to ensure consistency, version control, and automation.
2. **Immutable Infrastructure:** Servers/containers are never modified after deployment. If an update is needed, a new image is built and deployed.
3. **CI/CD (Continuous Integration / Continuous Deployment):** Automating the building, testing, and deployment of code to production frequently and reliably.
4. **GitOps:** Using a Git repository as the single source of truth for declarative infrastructure and applications (e.g., ArgoCD).
5. **Containerization (Docker):** Packaging an application and its dependencies into a single image to ensure it runs identically in any environment.
6. **Orchestration (Kubernetes):** Automating the deployment, scaling, and management of containerized applications across a cluster of nodes.
7. **Blue/Green Deployment:** Running two identical production environments. Traffic is switched from Blue (old) to Green (new) instantly, allowing fast rollbacks.
8. **Canary Deployment:** Rolling out a new version to a small subset of users (e.g., 5%) to monitor for errors before a full rollout.
9. **Microservices Architecture:** Breaking a monolithic app into small, independent services communicating via APIs, allowing independent scaling.
10. **High Availability (HA):** Designing systems to operate continuously without failure, usually via Multi-AZ deployments, Load Balancers, and Auto Scaling.
11. **Disaster Recovery (DR):** The process and policies for restoring systems after a catastrophic failure. Key metrics are RTO (Recovery Time Objective) and RPO (Recovery Point Objective).
12. **Principle of Least Privilege (IAM):** Granting users or services only the minimum permissions necessary to perform their exact job.
13. **Shift-Left Security:** Integrating security checks (Checkov, Trivy, SonarQube) early in the CI/CD pipeline rather than waiting until production.
14. **Service Mesh (Istio):** An infrastructure layer that manages service-to-service communication, providing mutual TLS, routing, and observability.
15. **Stateful vs. Stateless:** Stateless apps don't save local data (easy to scale). Stateful apps (databases) require persistent storage (harder to scale).
16. **Observability:** Understanding system internal states from external outputs (Metrics, Logs, Traces). Datadog, Prometheus, ELK.
17. **Autoscaling (HPA / Cluster Autoscaler):** Automatically adjusting the number of pods (HPA) or EC2 nodes (CA) based on CPU/Memory or custom metrics.
18. **VPC (Virtual Private Cloud):** A logically isolated network in AWS. Core concepts: Subnets, Route Tables, Internet Gateways, NAT Gateways.
19. **Load Balancing (ALB/NLB):** Distributing incoming network traffic across multiple servers to ensure no single server becomes overwhelmed.
20. **Serverless (Lambda/Fargate):** Running code or containers without provisioning or managing the underlying servers. You only pay for execution time.

---

### SECTION B: MUST-KNOW COMMANDS

**Kubernetes (`kubectl`)**
1. `kubectl get pods -n <ns>` - List all pods in a namespace.
2. `kubectl describe pod <pod>` - Show detailed pod configuration and events.
3. `kubectl logs <pod>` - Print stdout logs of a container.
4. `kubectl logs <pod> --previous` - Print logs of the previously crashed container instance.
5. `kubectl exec -it <pod> -- /bin/sh` - Open an interactive shell inside a running pod.
6. `kubectl apply -f deployment.yaml` - Create or update resources from a file.
7. `kubectl delete pod <pod>` - Delete a pod (K8s will recreate it if managed by a Deployment).
8. `kubectl get nodes -o wide` - List nodes with detailed IP info.
9. `kubectl top pods` - Show CPU and Memory usage of pods (requires metrics-server).
10. `kubectl get svc` - List services to find ClusterIPs or LoadBalancer endpoints.
11. `kubectl port-forward svc/<svc> 8080:80` - Forward local port 8080 to service port 80 for debugging.
12. `kubectl rollout restart deploy/<name>` - Force a rolling restart of all pods in a deployment.
13. `kubectl rollout undo deploy/<name>` - Revert a deployment to the previous version.
14. `kubectl scale deploy/<name> --replicas=5` - Manually scale a deployment up or down.
15. `kubectl get events --sort-by='.metadata.creationTimestamp'` - View cluster-wide events chronologically.
16. `kubectl auth can-i create pods` - Check RBAC permissions for your current user.
17. `kubectl config use-context <cluster>` - Switch between different K8s clusters.
18. `kubectl label nodes <node> key=value` - Add a label to a node (useful for nodeSelector).
19. `kubectl get ingress` - View Ingress routing rules and external IPs.
20. `kubectl drain <node> --ignore-daemonsets` - Safely evict all pods from a node before maintenance.

**Docker**
1. `docker build -t app:v1 .` - Build an image from a Dockerfile.
2. `docker run -d -p 8080:80 app:v1` - Run a container in the background, mapping ports.
3. `docker ps` - List running containers.
4. `docker ps -a` - List all containers (including stopped/exited).
5. `docker logs -f <container>` - Tail logs of a running container.
6. `docker exec -it <container> /bin/bash` - Shell into a container.
7. `docker images` - List local Docker images.
8. `docker rmi <image>` - Delete a local image.
9. `docker system prune -a` - Delete all unused containers, networks, and images (clean disk space).
10. `docker push <repo/app:tag>` - Push an image to a remote registry.

**Terraform**
1. `terraform init` - Initialize working directory, download provider plugins.
2. `terraform plan` - Generate and show an execution plan (dry run).
3. `terraform apply` - Build or change infrastructure according to the plan.
4. `terraform destroy` - Destroy all Terraform-managed infrastructure.
5. `terraform validate` - Check syntax and validity of configuration files.
6. `terraform fmt` - Reformat configuration files to a standard style.
7. `terraform state list` - List all resources in the state file.
8. `terraform state show <resource>` - Show detailed state attributes of a specific resource.
9. `terraform import <resource> <id>` - Import existing infrastructure into Terraform state.
10. `terraform workspace select <env>` - Switch between isolated workspaces (e.g., dev, prod).

**Linux System Commands**
1. `top` / `htop` - Monitor real-time CPU and Memory usage per process.
2. `df -h` - Show disk space usage in human-readable format.
3. `du -sh *` - Show size of files and directories in current folder.
4. `free -m` - Show available RAM and Swap memory in MB.
5. `netstat -tulpn` / `ss -tulpn` - List open network ports and the processes listening on them.
6. `ps aux | grep <process>` - Find a specific running process and its PID.
7. `kill -9 <PID>` - Force kill an unresponsive process.
8. `tail -f /var/log/syslog` - Continuously read the end of a log file.
9. `chmod 755 script.sh` - Change file permissions (executable).
10. `curl -I https://google.com` - Fetch HTTP headers to test connectivity and DNS.

**AWS CLI**
1. `aws configure` - Set up AWS credentials and default region.
2. `aws s3 ls` - List all S3 buckets.
3. `aws s3 cp file.txt s3://bucket/` - Copy a local file to S3.
4. `aws ec2 describe-instances` - List details of EC2 instances.
5. `aws ecr get-login-password | docker login ...` - Authenticate Docker to AWS ECR.
6. `aws eks update-kubeconfig --name <cluster>` - Generate Kubeconfig to connect to EKS.
7. `aws sts get-caller-identity` - Verify which IAM user/role you are currently using.
8. `aws iam list-users` - List all IAM users in the account.
9. `aws rds describe-db-instances` - Get status of RDS databases.
10. `aws cloudformation describe-stacks` - Check status of CloudFormation deployments.

**Git (CI/CD context)**
1. `git rebase main` - Reapply local commits on top of another base tip (keeps history clean).
2. `git cherry-pick <commit>` - Apply the changes introduced by an existing commit.
3. `git commit --amend` - Modify the most recent commit.
4. `git tag -a v1.0 -m "Release"` - Create an immutable tag for a CD release trigger.
5. `git reset --hard HEAD~1` - Permanently discard the last commit and local changes.

---

### SECTION C: COMMON TROUBLESHOOTING SCENARIOS

**1. Pod in CrashLoopBackOff**
- **Summary:** Container starts, hits a fatal error, exits, and K8s backs off before restarting.
- **Checks:** `kubectl describe pod`, `kubectl logs <pod> --previous`, check Exit Code.
- **Fix:** Fix application code bug (Exit Code 1), increase memory limits (Exit Code 137), or fix missing env vars.

**2. Pod in Pending state**
- **Summary:** Pod is created but K8s cannot find a suitable Node to run it on.
- **Checks:** `kubectl describe pod` -> look at Events (e.g., Insufficient CPU/Memory, unmatching NodeSelectors).
- **Fix:** Scale up the cluster, reduce pod resource requests, or fix NodeAffinity/Taints.

**3. ImagePullBackOff**
- **Summary:** Kubelet cannot pull the Docker image from the registry.
- **Checks:** Verify image tag spelling, check if image exists in registry, check ImagePullSecrets.
- **Fix:** Correct the typo in the YAML tag, or provide K8s with valid ECR/DockerHub credentials via a Secret.

**4. Service not accessible**
- **Summary:** Users cannot reach the application via the LoadBalancer or ClusterIP.
- **Checks:** `kubectl get endpoints <svc>` (are IPs listed?), check pod labels vs service selectors, check target port.
- **Fix:** Correct the Service `selector` to match the Pod `labels`, ensure app is listening on `0.0.0.0`, not `127.0.0.1`.

**5. 503 errors intermittently**
- **Summary:** Application occasionally drops requests with 503 Service Unavailable.
- **Checks:** Check ALB TargetResponse metrics, check K8s readiness probes, check pod CPU throttling.
- **Fix:** Tune readiness probe timings (don't send traffic before app is ready), fix memory leaks causing slow response.

**6. High CPU/memory on nodes**
- **Summary:** Underlying EC2 instances are at 100% capacity.
- **Checks:** `top` on node, `kubectl top nodes`, check for missing resource requests/limits on pods.
- **Fix:** Enforce `requests` and `limits` on all pods so K8s schedules them efficiently, implement Cluster Autoscaler.

**7. Terraform apply failing midway**
- **Summary:** Terraform provisions half the resources, then errors (e.g., API timeout), leaving partial state.
- **Checks:** Read the error message, run `terraform state list` to see what succeeded.
- **Fix:** Fix the code error, re-run `terraform apply` (it is idempotent and will pick up where it left off).

**8. CI/CD pipeline failing**
- **Summary:** GitHub Actions or Jenkins build turns red.
- **Checks:** Look at the specific step that failed in the logs. Did tests fail? Did Checkov flag a security issue?
- **Fix:** Developer fixes failing unit test, or adds suppression for a false positive Checkov flag.

**9. AWS cost spike**
- **Summary:** The monthly bill suddenly increases by 30%.
- **Checks:** Open AWS Cost Explorer, group by Service and Tag, identify the culprit (e.g., NAT Gateway data processing).
- **Fix:** Implement VPC endpoints (S3/DynamoDB) to avoid NAT costs, delete unattached EBS volumes.

**10. Kubernetes cluster IP exhaustion**
- **Summary:** New pods fail to create with "Failed to assign IP".
- **Checks:** Check VPC subnet available IPs in AWS console, check AWS VPC CNI configuration.
- **Fix:** Add a secondary IPv4 CIDR block to the VPC and configure EKS custom networking (ENIConfigs).

---

### SECTION D: TOP 20 QUESTIONS TO PRACTICE
1. **Explain the architecture of Kubernetes.** (Control plane components: API server, etcd, scheduler, controller. Worker node: kubelet, kube-proxy, container runtime).
2. **How does a packet flow from a user browser to a Kubernetes pod?** (Route53 -> ALB -> NodePort -> Kube-proxy/iptables -> Pod).
3. **What is the difference between a Deployment and a StatefulSet?** (Deployments are for stateless, identical pods. StatefulSets provide stable network IDs and persistent storage for databases).
4. **Explain your CI/CD pipeline end-to-end.** (GitHub -> Jenkins webhook -> Build/Test -> SonarQube -> Docker Build -> Trivy -> Push to ECR -> ArgoCD deploy).
5. **How do you manage secrets in Kubernetes?** (Never in plain YAML. Use AWS Secrets Manager + External Secrets Operator, or HashiCorp Vault).
6. **What is Terraform State and why is it important?** (It maps configuration to real-world resources. Must be stored remotely (S3) with locking (DynamoDB) for teams).
7. **How do you handle a production rollback?** (Immutable image tags, backward-compatible databases, `helm rollback` or Blue/Green traffic switch).
8. **What is a VPC and how do public/private subnets work?** (Public has a route to Internet Gateway. Private has a route to a NAT Gateway. Resources in private are secure).
9. **Explain Docker caching and how to optimize a Dockerfile.** (Put rarely changed instructions like `COPY package.json` and `RUN npm install` at the top, and `COPY . .` at the bottom).
10. **Difference between CPU Requests and Limits in K8s?** (Request is guaranteed minimum for scheduling. Limit is the hard maximum; exceeding it causes throttling).
11. **How do you troubleshoot a slow application?** (Top-down: Check ALB metrics -> Node CPU -> Pod Logs -> APM for slow queries -> Database locks).
12. **What is GitOps?** (Using Git as the single source of truth for infrastructure. Changes are made via PRs, and operators like ArgoCD pull changes to the cluster).
13. **How do you secure an AWS environment?** (IAM Least Privilege, private subnets, Security Groups, WAF, KMS encryption, CloudTrail logging).
14. **What are Readiness and Liveness probes?** (Liveness: Restart the pod if it's dead/deadlocked. Readiness: Remove pod from the Service load balancer if it's busy/not ready).
15. **Difference between ALB and NLB?** (ALB is Layer 7, HTTP/HTTPS, supports path routing. NLB is Layer 4, TCP/UDP, ultra-fast, static IPs).
16. **How does Checkov work in a pipeline?** (Static analysis tool that parses IaC like Terraform/K8s and fails the CI build if security misconfigurations are found).
17. **What happens when you type `terraform apply`?** (Reads code, compares with state file, fetches current AWS status, generates diff, executes API calls to match code).
18. **Explain Blue/Green vs Canary deployments.** (B/G: 100% traffic cutover to a full new environment. Canary: 5% traffic sent to new version, slowly increased).
19. **How do you monitor a Kubernetes cluster?** (Prometheus scrapes metrics, Grafana visualizes them, Alertmanager sends Slack/PagerDuty alerts based on thresholds).
20. **Describe a time you solved a difficult technical issue.** (Use the STAR method: Situation, Task, Action, Result. Focus on the troubleshooting steps).

---

### SECTION E: COMPARISON TABLES QUICK REFERENCE

**GitHub-hosted vs Self-hosted runners**
| Feature | GitHub-hosted | Self-hosted (e.g., EC2/EKS) |
| :--- | :--- | :--- |
| **Maintenance** | Zero maintenance | You must patch, update, and secure |
| **Cost** | Pay per minute | Pay for underlying AWS compute |
| **Security** | Runs in public cloud | Runs securely inside your private VPC |
| **Speed** | Standard speeds, clean state | Can cache heavily locally, much faster |

**EKS vs ECS**
| Feature | Amazon EKS (Kubernetes) | Amazon ECS |
| :--- | :--- | :--- |
| **Complexity** | High (steep learning curve) | Low (easier for AWS-only teams) |
| **Portability** | High (Cloud agnostic K8s API) | Low (Vendor locked to AWS) |
| **Ecosystem** | Massive (Helm, Istio, Prometheus) | Limited to AWS native tools |
| **Best for** | Large, complex microservices | Simple containerized workloads |

**ALB vs NLB**
| Feature | ALB (Application LB) | NLB (Network LB) |
| :--- | :--- | :--- |
| **OSI Layer** | Layer 7 (HTTP/HTTPS) | Layer 4 (TCP/UDP) |
| **Routing** | Path-based (/api), Host-based | Port-based |
| **Performance** | High | Ultra-high (millions of req/sec) |
| **IP Address** | Dynamic IPs | Static/Elastic IPs |

**Blue-Green vs Canary Deployment**
| Feature | Blue-Green | Canary |
| :--- | :--- | :--- |
| **Infrastructure cost**| Double (run 2 full environments) | Minimal (just a few extra pods) |
| **Traffic Cutover** | Instant (100% switch) | Gradual (1%, 10%, 50%, 100%) |
| **Risk profile** | Higher (if bug hits, it hits 100% users)| Lower (bug only impacts 5% of users) |
| **Rollback speed** | Instant (flip router back) | Slow (must scale back down) |

**Terraform vs CloudFormation**
| Feature | Terraform | CloudFormation |
| :--- | :--- | :--- |
| **Cloud Support** | Multi-cloud (AWS, GCP, Azure, SaaS) | AWS only |
| **Language** | HCL (HashiCorp Config Language) | JSON / YAML |
| **Dry Run feature** | Excellent (`terraform plan`) | Change Sets (Clunky) |
| **State File** | Managed by user (S3/DynamoDB) | Managed entirely by AWS |

**Prometheus vs Zabbix**
| Feature | Prometheus | Zabbix |
| :--- | :--- | :--- |
| **Data Collection** | Pull model (scrapes /metrics) | Push model (Agent based) |
| **Best For** | Kubernetes, ephemeral containers | Static VMs, Network switches, legacy |
| **Database** | Time-Series (TSDB) | Relational (MySQL/Postgres) |
| **Alerting** | Alertmanager | Built-in triggers and actions |

**ClusterIP vs NodePort vs LoadBalancer**
| Service Type | Reachability | Use Case |
| :--- | :--- | :--- |
| **ClusterIP** | Internal to cluster only | Microservices talking to each other, Databases |
| **NodePort** | Opens port (30000-32767) on all Nodes| Debugging, or using an external load balancer |
| **LoadBalancer** | Creates AWS ALB/NLB externally | Exposing frontend web apps to the internet |

**Launch Template vs Launch Configuration**
| Feature | Launch Template | Launch Configuration |
| :--- | :--- | :--- |
| **Versioning** | Yes (can have multiple versions) | No (must create new and replace) |
| **Spot/On-Demand Mix**| Supported in Auto Scaling Groups | Not supported |
| **Status** | AWS Recommended standard | Deprecated by AWS |

**SLO vs SLA vs SLI**
| Term | Definition | Example |
| :--- | :--- | :--- |
| **SLI (Indicator)** | The actual measurement | 99.95% uptime measured this month |
| **SLO (Objective)** | The internal team goal | We aim for 99.9% uptime |
| **SLA (Agreement)** | The legal contract with customers | If uptime drops below 99.9%, we refund money |

**Git Webhook vs Poll SCM**
| Feature | Webhook | Poll SCM |
| :--- | :--- | :--- |
| **Mechanism** | GitHub pushes an event to Jenkins | Jenkins asks GitHub "any changes?" |
| **Speed** | Instant trigger | Delayed (e.g., checks every 5 mins) |
| **Efficiency** | High (only fires when needed) | Low (wastes API calls checking unchanged repos)|

---

### SECTION F: ARCHITECTURE PATTERNS TO REMEMBER

**1. Multi-region HA on Kubernetes:**
Traffic hits Route53 (DNS routing based on latency/health). Traffic goes to AWS us-east-1 ALB or eu-west-1 ALB. Behind ALBs are independent EKS clusters. Databases (RDS/DynamoDB) use Cross-Region Replication. If us-east-1 goes down, Route53 instantly routes 100% traffic to eu-west-1.

**2. GitOps for 20+ teams:**
Use a central ArgoCD cluster. Instead of a single repo, use the "App of Apps" pattern. One master repo contains pointers to 20 team-specific repos. Teams only have access to their specific repo. They merge YAMLs, ArgoCD syncs them. Strict RBAC ensures Team A cannot deploy to Team B's namespace.

**3. Secrets management for microservices:**
Do not use K8s native secrets (they are base64, not encrypted). Store secrets in AWS Secrets Manager. Deploy `External Secrets Operator` in EKS. The operator fetches the AWS secret using IAM roles for Service Accounts (IRSA) and dynamically injects it into the pod. Developers never touch the actual passwords.

**4. SLO-based alerting:**
Instead of alerting on "CPU is high", alert on Error Budgets. "We guarantee 99.9% success rate (allow 43 minutes of downtime/month). If our error rate over the last hour is consuming the budget 5x faster than allowed, page the on-call engineer." This prevents alert fatigue.

**5. Self-healing platform:**
Combine K8s Liveness Probes (restarts dead apps), Horizontal Pod Autoscaler (scales pods on high CPU), and Karpenter/Cluster Autoscaler (adds EC2 nodes when pods are pending). The system automatically fixes app crashes and resource exhaustion without human intervention.

**6. Disaster Recovery (RTO/RPO):**
Pilot Light approach. Run a minimal version of core infrastructure in a secondary region. Continuously replicate the database (RPO: 5 mins). In a disaster, trigger a Terraform pipeline to scale up the compute nodes (RTO: 15 mins) and flip DNS. 

**7. Zero-downtime deployment:**
Achieved using Kubernetes Deployments with a Rolling Update strategy (`maxUnavailable: 0`, `maxSurge: 25%`). Combined with strict Readiness Probes so K8s only sends traffic to new pods after they are fully booted and connected to the DB.

**8. CI/CD with Terraform + EKS + Helm:**
GitHub Actions runs `terraform apply` to build VPC and EKS. GitHub Actions then builds app Docker images. Finally, GitHub Actions runs `helm upgrade --install` to deploy the app to EKS, injecting dynamic environment variables during the deploy.

---

### SECTION G: GITHUB ACTIONS CHEAT SHEET

**Trigger events (push, PR, schedule, manual)**
```yaml
on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *' # 2 AM daily
  workflow_dispatch: # Manual trigger button in UI
```

**Secrets usage syntax**
```yaml
steps:
  - name: Login to DB
    env:
      DB_PASS: ${{ secrets.PROD_DB_PASSWORD }}
    run: echo "Using secret securely"
```

**Matrix strategy example**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14.x, 16.x, 18.x]
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
```

**Reusable workflow syntax**
```yaml
# In caller workflow:
jobs:
  call-reusable:
    uses: my-org/my-repo/.github/workflows/reusable.yaml@main
    with:
      env_name: "staging"
    secrets: inherit
```

**Caching example**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

**Environment with approval example**
```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: 
      name: production
      url: https://myapp.com
    # GitHub UI will pause here and require a manager's click to proceed
```

**Docker build + ECR push snippet**
```yaml
- name: Login to ECR
  uses: aws-actions/amazon-ecr-login@v1
- name: Build and Push
  run: |
    docker build -t $REGISTRY/$REPOSITORY:$IMAGE_TAG .
    docker push $REGISTRY/$REPOSITORY:$IMAGE_TAG
```

**EKS deploy snippet**
```yaml
- name: Update Kubeconfig
  run: aws eks update-kubeconfig --name my-cluster --region us-east-1
- name: Deploy to K8s
  run: kubectl apply -f k8s/deployment.yaml
```

---

### SECTION H: HELM CHEAT SHEET

**Helm Basics**
- `helm install my-release my-repo/my-chart` - Install a chart.
- `helm upgrade my-release my-repo/my-chart` - Upgrade an existing release.
- `helm uninstall my-release` - Delete a release completely.

**Visibility & History**
- `helm list -n <namespace>` - List all installed Helm releases in a namespace.
- `helm status my-release` - Show the status, deployed resources, and notes.
- `helm history my-release` - Show revision history (essential for rollbacks).

**Development & Debugging**
- `helm template my-chart/` - Render chart templates locally to see the generated YAML without installing.
- `helm lint my-chart/` - Examine a chart for syntax errors and best practices.

**Values Override**
- `helm install my-app ./my-chart -f custom-values.yaml` - Override default values with a custom file.
- `helm install my-app ./my-chart --set replicaCount=5 --set image.tag=v2.0` - Override specific values via CLI.

**Repositories**
- `helm repo add bitnami https://charts.bitnami.com/bitnami` - Add a public chart repo.
- `helm repo update` - Fetch the latest list of charts from repos.
- `helm search repo nginx` - Search for charts in your added repos.

**Rollback Procedure Step-by-Step**
```bash
# 1. Developer reports an issue with the latest deployment
# 2. Check history to find the previous good revision
helm history frontend-app -n production
# Output shows Revision 4 is FAILED, Revision 3 is SUPERSEDED (last good one)

# 3. Execute rollback to revision 3
helm rollback frontend-app 3 -n production

# 4. Verify the rollback
helm status frontend-app -n production
kubectl get pods -n production
```

---
*End of DevOps Interview QA Part 3 and Final Revision Sheet.*
