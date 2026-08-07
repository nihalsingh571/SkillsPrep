# Chapter 5: Production Architecture

Welcome to the pinnacle of Kubernetes mastery: Production Architecture. In this chapter, we bridge the gap between "it works on my machine" and "it handles Black Friday traffic at Netflix." We will focus heavily on AWS EKS (Elastic Kubernetes Service), as it is the industry standard for enterprise Kubernetes, but the design patterns apply universally. 

This chapter is designed for those who already know Kubernetes primitives but need to design, deploy, and maintain FAANG-level architectures. We will cover real-world production decisions, advanced scaling with Karpenter, GitOps with ArgoCD, zero-downtime deployment strategies, and bulletproof incident response.

---

## SECTION 1: Production EKS Architecture

### 1.1 EKS Complete Architecture

AWS EKS splits responsibility between AWS and you. AWS manages the control plane (API server, etcd, scheduler, controller manager), ensuring it is highly available across multiple Availability Zones (AZs) and automatically backed up. You are responsible for the data plane (worker nodes) and the workloads running on them.

**Control Plane Dynamics:**
- The EKS control plane runs in an AWS-managed VPC, not your VPC.
- AWS exposes an endpoint (public, private, or both) for you to communicate with the API server.
- Communication between your worker nodes and the control plane happens via Elastic Network Interfaces (ENIs) that EKS provisions in your VPC subnets.

**Worker Nodes Options:**
1. **Managed Node Groups:** AWS manages the lifecycle of your EC2 instances (upgrades, scaling). Best for standard stateless and stateful workloads.
2. **Self-Managed Nodes:** You manage the Auto Scaling Groups. Rare today unless you need custom AMIs or OS-level modifications not supported by managed nodes.
3. **Fargate:** Serverless compute for containers. No nodes to manage, but limited to stateless workloads, no DaemonSets, and higher cost at scale. Best for sporadic jobs.

**Complete HA EKS Cluster Architecture:**

```text
+-------------------------------------------------------------------------+
|                              AWS Cloud                                  |
|                                                                         |
|  +-------------------------------------------------------------------+  |
|  |                          AWS Managed VPC                          |  |
|  |  +----------------+    +----------------+    +----------------+   |  |
|  |  |  API Server    |    |   Scheduler    |    |   Controller   |   |  |
|  |  |  (Multi-AZ)    |    |                |    |                |   |  |
|  |  +-------+--------+    +-------+--------+    +-------+--------+   |  |
|  |          |                     |                     |            |  |
|  |          +---------------------+---------------------+            |  |
|  |                                |                                  |  |
|  |                         +------+------+                           |  |
|  |                         |   etcd      |                           |  |
|  |                         | (Quorum)    |                           |  |
|  |                         +-------------+                           |  |
|  +--------------------------------|----------------------------------+  |
|                                   | (Cross-VPC ENI)                     |
|                                   v                                     |
|  +-------------------------------------------------------------------+  |
|  |                          Customer VPC                             |  |
|  |                                                                   |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  |  | Public Subnet AZ1 |  | Public Subnet AZ2 |  | Public AZ3     | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  | |  NAT Gateway  | |  | |  NAT Gateway  | |  |                | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  | | ALB (Ingress) | |  | | ALB (Ingress) | |  |                | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  |                                                                   |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  |  | Private Sub AZ1   |  | Private Sub AZ2   |  | Private AZ3    | |  |
|  |  | +---------------+ |  | +---------------+ |  | +------------+ | |  |
|  |  | | Worker Node 1 | |  | | Worker Node 2 | |  | | Node 3     | | |  |
|  |  | | (On-Demand)   | |  | | (Spot Fleet)  | |  | | (Fargate)  | | |  |
|  |  | +---------------+ |  | +---------------+ |  | +------------+ | |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  |                                                                   |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  |  | Data Subnet AZ1   |  | Data Subnet AZ2   |  | Data AZ3       | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  | | Amazon RDS    | |  | | RDS Standby   | |  |                | |  |
|  |  | +---------------+ |  | +---------------+ |  |                | |  |
|  |  +-------------------+  +-------------------+  +----------------+ |  |
|  +-------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

**Production Best Practices:**
- Place worker nodes strictly in **Private Subnets**. They should only route internet-bound traffic through NAT Gateways in the Public Subnets.
- The API Server endpoint should ideally be Private. If Public, restrict access using a strict CIDR block (your VPN/office IPs).
- Use **VPC Endpoints** (PrivateLink) for AWS services like S3, ECR, and DynamoDB. This keeps traffic on the AWS backbone, significantly reducing NAT Gateway data processing costs.
- Separate subnets for Data layer (RDS, ElastiCache) with strict Security Groups allowing ingress only from the EKS Node Security Group.

**EKS Add-ons:**
EKS requires specific add-ons to function efficiently:
- **VPC CNI:** Provides pod networking.
- **CoreDNS:** Cluster DNS service.
- **kube-proxy:** Manages network rules on nodes for Services.
- **EBS CSI Driver:** Required for dynamic provisioning of Persistent Volumes using EBS.

**Interview Q&A:**
*Q: How does EKS control plane communicate with worker nodes in a private subnet?*
A: When you create an EKS cluster, AWS provisions Cross-Account ENIs in your VPC subnets. The control plane uses these ENIs to establish a secure tunnel (historically SSH, now primarily managed grpc/konnectivity) to communicate with the kubelet and pods on the worker nodes.

### 1.2 EKS Networking (aws-vpc-cni)

Unlike Calico or Flannel which use overlay networks (VXLAN/IPIP), the AWS VPC CNI assigns a real VPC IP address to every single pod.

**Internal Working:**
The CNI plugin runs as a DaemonSet (`aws-node`). It manages ENIs attached to the EC2 instance and maintains a pool of secondary IP addresses. When a pod is scheduled, the CNI assigns one of these secondary IPs to the pod.

**Benefits:**
- Pods are first-class citizens on the VPC. You can ping a pod directly from an EC2 instance or over a VPN.
- High performance (no encapsulation/decapsulation overhead).
- **Security Groups for Pods (SGP):** You can assign an AWS Security Group directly to a pod using an ENI Trunking mechanism.

**Drawbacks:**
- **IP Exhaustion:** Because every pod gets a real VPC IP, a small subnet will quickly run out of IPs.

**Prefix Delegation:**
To solve IP density limits (e.g., a t3.medium can normally only run ~17 pods), enable Prefix Delegation. Instead of requesting single secondary IPs, the CNI requests `/28` prefixes (16 IPs at a time). This drastically increases the number of pods per node.

**SNAT Behavior:**
By default, when a pod communicates outside the VPC (e.g., the internet), the `aws-node` DaemonSet performs Source NAT (SNAT), translating the pod's IP to the Node's primary IP. This is required because the internet router doesn't know about secondary IPs.

**Interview Q&A:**
*Q: We are migrating to EKS and our VPC has limited IP space (/24 subnets). We plan to run hundreds of micro-pods. What is the architecture risk and how do you solve it?*
A: The risk is IP exhaustion. Because aws-vpc-cni assigns real VPC IPs, a /24 only has 251 usable IPs, limiting the cluster size. Solutions:
1. Enable Custom Networking: Configure the CNI to use a secondary CIDR block (like 100.64.0.0/10) specifically for pods.
2. Use IPv6 for the cluster (EKS supports IPv6).
3. If not tied to VPC IPs, replace aws-vpc-cni with an overlay CNI like Cilium or Calico.

### 1.3 Karpenter on EKS

Karpenter is the modern replacement for Cluster Autoscaler. While Cluster Autoscaler relies on EC2 Auto Scaling Groups (ASGs) and is tied to specific instance types, Karpenter provisions compute resources directly from the EC2 Fleet API.

**Why Karpenter over Cluster Autoscaler?**
- **Group-less:** No ASGs. Karpenter looks at pending pods and provisions the *exact right instance* to fit them.
- **Speed:** Provisions nodes in seconds (bypasses ASG lifecycle).
- **Cost Savings:** Consolidation feature actively moves pods to cheaper/smaller instances or packs them tighter to shut down empty nodes.

**Production Karpenter Configuration (YAML):**

```yaml
# NodePool defines the constraints on what compute can be provisioned.
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  # 1. Template for the nodes
  template:
    spec:
      requirements:
        # Require spot instances to save money
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        # Allow multiple instance families (gives EC2 fleet flexibility)
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["c5", "m5", "r5", "t3"]
        # Architecture constraint
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
      # Reference to the cloud provider specific configuration
      nodeClassRef:
        apiVersion: karpenter.k8s.aws/v1beta1
        kind: EC2NodeClass
        name: default
  
  # 2. Disruption (Consolidation) Rules
  disruption:
    # When underutilized, Karpenter will drain nodes and move workloads
    # to smaller nodes or pack them onto other running nodes.
    consolidationPolicy: WhenUnderutilized
    expireAfter: 720h # 30 days: Force nodes to recycle for OS patching

---
# EC2NodeClass defines AWS-specific infrastructure details
apiVersion: karpenter.k8s.aws/v1beta1
kind: EC2NodeClass
metadata:
  name: default
spec:
  # 3. AMI Family
  amiFamily: AL2 # Amazon Linux 2
  
  # 4. Subnet discovery tags (where to place nodes)
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-eks-cluster
        environment: private
        
  # 5. Security Group discovery tags
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: my-eks-cluster
        
  # 6. IAM Role for the instances
  role: "KarpenterNodeRole-my-eks-cluster"
```

**Line-by-Line Explanation:**
- `NodePool`: The generic Karpenter resource.
- `requirements`: This is where Karpenter shines. Instead of defining one instance type, you define *rules*. Karpenter will look at the AWS price list and choose the cheapest instance that satisfies these requirements and fits the pending pods.
- `consolidationPolicy: WhenUnderutilized`: The magic bullet for cost savings. Karpenter continuously evaluates if the cluster can run on cheaper compute and will actively terminate nodes to save money.
- `EC2NodeClass`: AWS-specific implementation details.
- `subnetSelectorTerms`: Uses AWS tags to find which subnets to place nodes in. Highly dynamic.

**Interview Q&A:**
*Q: A pending pod requires a GPU. How does Karpenter handle this compared to Cluster Autoscaler?*
A: With Cluster Autoscaler, you must pre-create a GPU-specific ASG (even if scaled to 0). With Karpenter, as long as your NodePool allows GPU instance families (e.g., p3, g4), Karpenter detects the pod's resource request, finds the cheapest GPU instance via the EC2 API, and spins it up instantly without any ASG configuration.

### 1.4 Load Balancing on EKS

In AWS, Kubernetes Services of type `LoadBalancer` and `Ingress` resources are fulfilled by the **AWS Load Balancer Controller**.

**ALB vs NLB:**
| Feature | Application Load Balancer (ALB) | Network Load Balancer (NLB) |
|---------|--------------------------------|-----------------------------|
| **OSI Layer** | Layer 7 (HTTP/HTTPS) | Layer 4 (TCP/UDP) |
| **K8s Resource** | `Ingress` | `Service` (type: LoadBalancer) |
| **Routing** | Path-based, Host-based, Headers | Port-based |
| **Source IP** | Preserved in `X-Forwarded-For` header | Preserved natively at IP packet level |
| **Use Case** | Web apps, APIs, gRPC, WAF integration | Databases, massive throughput, custom protocols |

**Complete Production Ingress YAML (ALB):**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: production-api-ingress
  namespace: api-prod
  annotations:
    # 1. Use the AWS ALB Controller
    kubernetes.io/ingress.class: alb
    
    # 2. Facing: internal or internet-facing
    alb.ingress.kubernetes.io/scheme: internet-facing
    
    # 3. Target type: IP or Instance. 
    # 'ip' routes traffic directly to the pod IP (requires aws-vpc-cni). Highly efficient.
    alb.ingress.kubernetes.io/target-type: ip
    
    # 4. HTTPS/TLS Setup
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS": 443}]'
    # Auto-redirect HTTP to HTTPS
    alb.ingress.kubernetes.io/actions.ssl-redirect: '{"Type": "redirect", "RedirectConfig": { "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"}}'
    # Attach ACM Certificate (ARN)
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:123456789:certificate/xxxx-xxxx
    
    # 5. Security and WAF
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:us-east-1:123456789:regional/webacl/prod-waf/xxxx-xxxx
    
    # 6. Health Checks
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
spec:
  rules:
    # Host-based routing
    - host: api.production.com
      http:
        paths:
          # Path-based routing
          - path: /v1/users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port:
                  number: 8080
          - path: /v1/payments
            pathType: Prefix
            backend:
              service:
                name: payment-service
                port:
                  number: 8080
```

**Line-by-Line Explanation:**
- `alb.ingress.kubernetes.io/target-type: ip`: Crucial for performance. Instead of hitting NodePort and bouncing around kube-proxy rules, the ALB routes packets *directly* to the pod's IP address.
- `alb.ingress.kubernetes.io/certificate-arn`: Offloads TLS termination at the ALB. The traffic from ALB to pod is unencrypted (unless end-to-end encryption is explicitly configured).
- `alb.ingress.kubernetes.io/wafv2-acl-arn`: Attaches AWS WAF (Web Application Firewall) to protect against SQLi, XSS, and botnets before traffic even reaches the cluster.

---

## SECTION 2: Deployment Strategies

Deploying v2 of an application without downtime is the core promise of Kubernetes. 

### 2.1 Rolling Update (Default)

Kubernetes Deployments default to a RollingUpdate strategy. It replaces old pods with new pods incrementally.

**Key Parameters:**
- `maxSurge`: How many extra pods can be created above the desired replica count during the update. (e.g., 25% or 1).
- `maxUnavailable`: How many pods can be unavailable during the update. (e.g., 25% or 0).

**Complete Deployment YAML:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # Can scale up to 5 pods during rollout
      maxUnavailable: 25%  # At least 3 pods must be running
  selector:
    matchLabels:
      app: payment
  template:
    metadata:
      labels:
        app: payment
    spec:
      containers:
      - name: app
        image: myrepo/payment:v2.0.0
        # 1. Probes are the gatekeepers of Rolling Updates
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        # 2. Graceful Shutdown
        lifecycle:
          preStop:
            exec:
              # Sleep gives Ingress/kube-proxy time to remove pod from endpoints
              command: ["/bin/sh", "-c", "sleep 15"]
```

**Production Best Practice:** The `readinessProbe` is critical. Kubernetes will *not* kill an old pod until the new pod passes its readiness probe. Without it, K8s assumes the new pod is ready instantly, kills all old pods, and causes a massive outage while the new app boots up. The `preStop` sleep is a famous production hack to prevent dropped connections during pod termination.

### 2.2 Blue-Green Deployment

Rolling updates are slow to rollback if things go wrong (you have to roll backward, spinning down new pods and spinning up old ones). Blue-Green creates two entirely separate environments.

**How it works:**
1. **Blue (v1.0)** is live, serving 100% of traffic.
2. **Green (v2.0)** is deployed alongside Blue.
3. Testing runs internally against Green.
4. If tests pass, traffic is instantly switched at the Load Balancer / Service level to Green.
5. If Green crashes, switch traffic back to Blue instantly.

**Complete Blue-Green implementation via Service Selector:**

```yaml
# 1. The Blue Deployment (Currently Live)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: v1.0 # Unique version label
  template:
    metadata:
      labels:
        app: my-app
        version: v1.0
    spec:
      containers:
      - name: app
        image: my-app:v1.0

---
# 2. The Green Deployment (New Version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: v2.0 # Unique version label
  template:
    metadata:
      labels:
        app: my-app
        version: v2.0
    spec:
      containers:
      - name: app
        image: my-app:v2.0

---
# 3. The Active Service
apiVersion: v1
kind: Service
metadata:
  name: app-service-active
spec:
  selector:
    app: my-app
    # THE SWITCH: Change this from v1.0 to v2.0 to instantly route traffic
    version: v2.0 
  ports:
  - port: 80
    targetPort: 8080
```

**Pros/Cons:**
- **Pro:** Instant rollback. Zero downtime deployment.
- **Con:** Requires double the infrastructure capacity (2x pods) during the deployment window. State/DB schema migrations must be strictly backward compatible.

### 2.3 Canary Deployment & Argo Rollouts

Canary deployments shift a small percentage of traffic (e.g., 5%) to the new version. You monitor metrics (error rates, latency). If stable, you increase to 20%, 50%, then 100%.

While you can do this natively with NGINX Ingress annotations (`nginx.ingress.kubernetes.io/canary-weight: "10"`), managing this manually is a nightmare. Enter **Argo Rollouts**.

Argo Rollouts introduces a Custom Resource Definition (CRD) called `Rollout` that acts as a drop-in replacement for the native `Deployment` object.

**Complete Argo Rollouts Canary YAML:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: checkout-service
spec:
  replicas: 10
  # Drop-in replacement for Deployment selector
  selector:
    matchLabels:
      app: checkout
  template:
    metadata:
      labels:
        app: checkout
    spec:
      containers:
      - name: checkout
        image: myrepo/checkout:v3.0.0
        
  # The Magic: Canary Strategy Definition
  strategy:
    canary:
      # Use ALB for traffic shaping
      trafficRouting:
        alb:
          ingress: production-api-ingress
          servicePort: 80
          rootService: checkout-stable
      
      # The steps for the progressive rollout
      steps:
      # Step 1: Send 10% of traffic to the new version (canary)
      - setWeight: 10
      
      # Step 2: Pause. Wait for human approval OR automated analysis
      - pause: {duration: 10m} # Optional: wait 10 mins
      
      # Step 3: Run an automated analysis against Datadog/Prometheus
      - analysis:
          templates:
          - templateName: success-rate-check
          args:
          - name: service-name
            value: checkout
            
      # Step 4: If analysis passes, increase to 50%
      - setWeight: 50
      - pause: {duration: 10m}
      
      # Step 5: If we reach the end, promote to 100%
```

**AnalysisTemplate (The automated rollback engine):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-check
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    # If the success rate drops below 95%, fail the analysis (triggers rollback)
    successCondition: result[0] >= 0.95
    provider:
      prometheus:
        address: http://prometheus-server.monitoring.svc.cluster.local:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.*"}[5m])) / 
          sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

**Interview Q&A:**
*Q: Walk me through a canary deployment using Argo Rollouts with automated rollback.*
A: When a new image tag is detected, Argo Rollouts spins up a canary replica. It configures the Ingress/Service mesh to route (e.g., 10%) traffic to the canary. It then executes an AnalysisTemplate, querying Prometheus for the HTTP 5xx error rate of the canary pods. If the error rate breaches the threshold (e.g., >5%), Argo Rollouts instantly aborts the deployment, shifts 100% traffic back to the stable pods, and scales down the canary. Zero human intervention required.

---

## SECTION 3: GitOps in Production

GitOps is the principle that Git is the single source of truth for your infrastructure and applications. You do not run `kubectl apply`. You push to Git, and a software agent inside the cluster syncs the state.

### 3.1 ArgoCD Production Setup

ArgoCD continuously monitors a Git repository and compares it to the live state of the Kubernetes cluster. If they drift, ArgoCD syncs the cluster to match Git.

**Complete ArgoCD Application YAML:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: order-service-prod
  namespace: argocd
  # Deletion finalizer prevents accidental deletion of the app via UI
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  # 1. Source: Where does the code live?
  source:
    repoURL: 'https://github.com/my-company/k8s-manifests.git'
    path: 'apps/order-service/overlays/prod'
    targetRevision: HEAD
    
  # 2. Destination: Where is it being deployed?
  destination:
    server: 'https://kubernetes.default.svc' # Deploy to local cluster
    namespace: prod-namespace
    
  # 3. Sync Policy: How does it deploy?
  syncPolicy:
    # Automated sync when git changes
    automated:
      prune: true     # Delete resources that were removed from Git
      selfHeal: true  # Fix manual `kubectl edit` changes (revert drift)
    
    # Sync options for production stability
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true # Don't delete old resources until new ones are healthy
      
  # 4. Ignore drift for things controlled by K8s (like HPA changing replicas)
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

**App of Apps Pattern:**
In an environment with 100 microservices, you don't manually apply 100 ArgoCD Application manifests. Instead, you create a "Root Application" that points to a folder in Git. That folder contains the Application manifests for all 100 microservices. ArgoCD deploys the Root Application, which spawns the 100 child Applications.

### 3.2 Complete CI/CD Pipeline Architecture

```text
+-------------------+      +-------------------+      +-------------------+
|    Developer      |      |   GitHub Actions  |      |   ArgoCD (EKS)    |
|                   |      |                   |      |                   |
| 1. Code Commit    | ---> | 2. Run Tests      |      |                   |
| 2. Open PR        |      | 3. Build Docker   |      |                   |
| 3. Merge to Main  |      | 4. Security Scan  |      |                   |
+-------------------+      | 5. Push to ECR    |      |                   |
                           | 6. Update Helm    |      |                   |
                           |    values in Git  | ---> | 7. Detects Git    |
                           +-------------------+      |    Change         |
                                                      | 8. Apply to K8s   |
                                                      +--------+----------+
                                                               |
                                                               v
                                                      +--------+----------+
                                                      |   Argo Rollouts   |
                                                      |                   |
                                                      | 9. 10% Canary     |
                                                      | 10. Metric Check  |
                                                      | 11. 100% Promote  |
                                                      +-------------------+
```

**The CI Pipeline (GitHub Actions updating GitOps Repo):**

The trickiest part of GitOps is bridging CI (Code build) to CD (GitOps deployment). The CI pipeline must modify the GitOps repository.

```yaml
# .github/workflows/ci.yml
name: Build and Release
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker Image
      run: docker build -t my-company/app:${{ github.sha }} .
      
    - name: Push to ECR
      run: docker push my-company/app:${{ github.sha }}
      
    # The Bridge to CD: Update the GitOps manifest repo
    - name: Update GitOps Repository
      uses: fjogeleit/yaml-update-action@main
      with:
        repository: my-company/gitops-infra
        masterBranchName: main
        valueFile: 'apps/my-app/values.yaml'
        propertyPath: 'image.tag'
        value: ${{ github.sha }}
        commitChange: true
        branch: main
        message: 'Update my-app image tag to ${{ github.sha }}'
        githubToken: ${{ secrets.GITOPS_REPO_PAT }}
```

---

## SECTION 4: Production Operations

### 4.1 Backup and Disaster Recovery (Velero)

A Kubernetes cluster is mostly stateless, except for etcd and Persistent Volumes. However, rebuilding hundreds of manifests during an outage is slow. **Velero** is the standard for K8s backups.

**Velero Architecture:**
- **BSL (BackupStorageLocation):** S3 bucket where manifest JSON files are stored.
- **VSL (VolumeSnapshotLocation):** Cloud-specific snapshotting mechanism (AWS EBS Snapshots).

**Complete Velero Backup YAML (Schedule):**

```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: prod-daily-backup
  namespace: velero
spec:
  # Cron expression: Every day at 2 AM
  schedule: "0 2 * * *"
  template:
    # 1. What to include
    includedNamespaces:
    - '*' # Backup everything
    excludedNamespaces:
    - kube-system # Ignore system namespaces, rebuild them dynamically
    
    # 2. Snapshot EBS volumes
    snapshotVolumes: true
    
    # 3. Retention policy (Keep backups for 14 days)
    ttl: 336h0m0s
```

**DR Strategy:** If cluster A dies, spin up empty cluster B, install Velero, point it at the same S3 bucket, and run `velero restore create --from-backup my-backup`. The workloads and PVs spin up exactly as they were.

### 4.2 Kubernetes Upgrade Strategy

Upgrading Kubernetes in production requires extreme care. The control plane and worker nodes must be orchestrated perfectly.

**EKS Upgrade Path:**
1. Upgrade Control Plane via AWS Console/Terraform (AWS handles etcd/API upgrade).
2. Upgrade Add-ons (CoreDNS, kube-proxy, VPC CNI) to match new version.
3. Upgrade Worker Nodes.

**Blue-Green Node Upgrade (Safest Method):**
Do not use rolling updates on node groups in critical production. Instead:
1. Create a brand new Managed Node Group (MNG) using the new K8s version AMI.
2. Wait for new nodes to become `Ready`.
3. Taint and Cordon the old MNG nodes (`kubectl cordon <node>`).
4. Drain the old nodes (`kubectl drain <node> --ignore-daemonsets --delete-emptydir-data`). Pods are evicted and rescheduled gracefully onto the new MNG.
5. Delete the old MNG.

### 4.3 Production Multi-Region Architecture

For high availability, run multiple EKS clusters across regions (e.g., us-east-1 and eu-west-1).

**Active-Active Architecture:**
- AWS Route53 uses Latency-Based Routing to direct users to the closest healthy cluster.
- **State is the hard part:** Databases must replicate across regions (e.g., Aurora Global Database, DynamoDB Global Tables).
- Application pods must be entirely stateless.
- **ArgoCD:** A single ArgoCD control plane in a management cluster connects to both region clusters and deploys identical manifests to both.

### 4.4 Cost Optimization

K8s is notorious for ballooning cloud bills. 
1. **Vertical Pod Autoscaler (VPA):** Run VPA in `Recommendation` mode. It monitors actual CPU/Memory usage and tells you how over-provisioned your pod requests are. Lower the requests to save money.
2. **Karpenter Consolidation:** (Discussed in 1.3).
3. **Spot Instances:** Run all stateless workloads (web frontends, background workers) on EC2 Spot. Use a Node Termination Handler (built into Karpenter) to gracefully drain pods when AWS recalls the Spot instance with a 2-minute warning.
4. **Kubecost:** Deploy Kubecost to get granular billing per namespace/deployment. You can see exactly which microservice costs $10,000/month.

---

## SECTION 5: Real Production Architectures

### 5.1 Netflix-Style Kubernetes Architecture (Global Scale)

Netflix operates at a scale where K8s limits break. They run "Titus" natively but the equivalent K8s architecture looks like this:

```text
         +-------------------+
         |  Global Route53   | (Geo-Routing)
         +---------+---------+
                   |
     +-------------+-------------+
     |                           |
+----v-----+                +----v-----+
| us-east-1|                | eu-west-1|
|  ALB     |                |  ALB     |
|          |                |          |
|  API GW  | (Zuul/Envoy)   |  API GW  |
|          |                |          |
| +------+ |                | +------+ |
| | Pods | | <------------> | | Pods | | (Cross-region mesh via Cilium)
| +------+ |                | +------+ |
+----------+                +----------+
     |                           |
+----v---------------------------v----+
|        Aurora Global Database       |
+-------------------------------------+
```
**Key Components:**
- **API Gateway:** Envoy handles rate limiting, auth, and routing before hitting pods.
- **Service Mesh:** Linkerd or Istio for mTLS between microservices, retries, and circuit breaking.
- **Chaos Engineering:** Chaos Mesh deployed continuously to kill random pods in production during business hours to ensure system resilience.

### 5.2 E-Commerce (Swiggy/Flipkart) Architecture

Focus: Extreme scaling during Flash Sales (e.g., Black Friday).

- **Event-Driven Architecture:** Synchronous HTTP calls break under load. When a user clicks "Buy", the pod drops an event into Kafka and returns 200 OK immediately.
- **Autoscaling Chain:**
  1. KEDA (Kubernetes Event-driven Autoscaling) monitors Kafka queue length.
  2. Queue grows -> KEDA scales the HPA (Horizontal Pod Autoscaler) to 500 pods.
  3. Pods go to Pending -> Karpenter detects Pending pods -> Spins up 50 EC2 nodes in 45 seconds.
  4. Sale ends -> Queue empties -> HPA scales down to 10 pods -> Karpenter consolidates and terminates 49 EC2 nodes.

---

## SECTION 6: Production Incident Response

### Common Incidents and Playbooks

**1. All pods OOMKilling across cluster**
- **Symptom:** App crashes, `kubectl get pods` shows `OOMKilled`.
- **Cause:** Memory leaks, or limits are set too low for traffic spikes.
- **Playbook:**
  1. Temporarily increase memory `limits` via `kubectl edit deployment` (ArgoCD will auto-heal it back, so pause ArgoCD sync first).
  2. Check Datadog/Prometheus for memory usage graphs.
  3. Capture a heap dump from the JVM/Node application to find the leak.

**2. Node group exhausted, pods Pending**
- **Symptom:** Pods stuck in `Pending`. `kubectl describe pod` shows "0/10 nodes are available: insufficient cpu."
- **Cause:** ASG max size reached, or AWS AZ is out of capacity for that instance type.
- **Playbook:**
  1. If ASG: Increase ASG max size in Terraform.
  2. If AWS capacity error: Add new instance types to Karpenter NodePool or ASG mixed-instances policy (e.g., if c5.large is out, add c5a.large or m5.large).

**3. Certificate expiry taking down API server**
- **Prevention:** Run `cert-manager` to automatically rotate Let's Encrypt TLS certificates 30 days before expiry. Monitor cert expiry via Prometheus alerts.

---

## END OF CHAPTER

### Production Readiness Checklist
1. [ ] Control plane HA (Multi-AZ).
2. [ ] Worker nodes in private subnets.
3. [ ] Karpenter configured with Spot and Consolidation.
4. [ ] Metrics Server and Prometheus installed.
5. [ ] Logs forwarding to Datadog/Splunk/CloudWatch via FluentBit.
6. [ ] Readiness and Liveness probes on ALL deployments.
7. [ ] Resource requests/limits defined on ALL containers.
8. [ ] PodDisruptionBudgets (PDB) configured for critical apps.
9. [ ] GitOps (ArgoCD) manages all cluster state.
10. [ ] Automated backups via Velero.
*(Complete list of 50 items available in supplementary materials)*

### Architecture Decision Tree
- Need stateful storage? -> Avoid if possible. If required -> StatefulSet + EBS CSI.
- Need to save money? -> Karpenter + Spot Instances.
- Need zero downtime deployments? -> Argo Rollouts Canary.
- Need cross-region failover? -> Route53 + Global Database.

### Interview Q&A

**Q: In a production cluster, your worker node dies unexpectedly. Walk me through exactly what happens to the pods running on it.**
A: 
1. The Kubelet on the dead node stops sending heartbeats to the API Server.
2. After `node-monitor-grace-period` (default 40s), the Node Controller marks the node as `NotReady`.
3. After `pod-eviction-timeout` (default 5m), the controller evicts the pods.
4. The ReplicaSet notices the actual state (pods dead) doesn't match desired state.
5. Scheduler places new pods on healthy nodes.
6. Karpenter detects pending pods (if cluster is full) and spins up new nodes.

**Q: Explain the difference between Resource Requests and Limits.**
A: Requests are for the **Scheduler**. A pod requesting 1 CPU will only be scheduled on a node with 1 available CPU. Limits are for the **CRI/Linux cgroups**. If a pod uses more memory than its limit, it is OOMKilled. If it uses more CPU, it is throttled (slows down), but not killed.

**Q: Why do we need PodDisruptionBudgets (PDB)?**
A: PDBs protect against voluntary disruptions (like node drains during upgrades). If an app has 3 replicas and a PDB requiring `minAvailable: 2`, Kubernetes will refuse to drain a node if it causes the app to drop to 1 replica. It safely ensures HA during cluster maintenance.

### Mini Project
Design a complete EKS production architecture:
1. Write a Terraform script to deploy EKS with managed node groups.
2. Install Karpenter via Helm.
3. Deploy an NGINX app with Argo Rollouts.
4. Execute a canary deployment and observe the traffic shift.
