# Chapter 2: GitOps and ArgoCD - The Modern Delivery Paradigm

Welcome to Chapter 2. If you've ever felt the pain of deploying to production and watching it break, only to realize nobody knows *what* actually changed, you are in the right place. 

Imagine you are a chef in a massive restaurant kitchen. In the old days, waiters (developers) would run into the kitchen, shouting orders and sometimes tossing ingredients straight into the pots (manual `kubectl apply` commands). The kitchen became chaos. No one knew the exact recipe being cooked. 

GitOps is like hiring a strict Kitchen Manager. The waiters must write their orders on a ticket (Git commit). The Kitchen Manager (ArgoCD) constantly looks at the ticket and ensures the soup in the pot *exactly* matches the ticket. If someone sneaks in and adds salt to the pot, the Kitchen Manager instantly detects it, scoops it out, and makes it match the ticket again.

Let's master GitOps and ArgoCD, the industry standard used by Netflix, Uber, and Google.

---

## SECTION 1: GitOps Philosophy

### 1.1 What is GitOps?
GitOps is a paradigm where Git is the single source of truth for your infrastructure and applications. If it's not in Git, it doesn't exist. Instead of having deployment scripts that *push* code into Kubernetes, we have agents inside Kubernetes that *pull* from Git.

### 1.2 Push-based vs Pull-based CD
In traditional CI/CD (like Jenkins), your pipeline builds the image, and then runs `kubectl apply` to push it to the cluster. This is **Push-based**.

**Push-Based CD Architecture:**
```text
[Developer] -> (Git Commit) -> [Jenkins/GitLab CI] --(kubectl apply)--> [Kubernetes Cluster]
                                      |
                               (Requires Cluster Credentials & Firewall Hole)
```

**Pull-Based CD (GitOps) Architecture:**
```text
[Developer] -> (Git Commit) -> [Git Repo]
                                   ^
                                   | (Pulls changes, no firewall hole needed)
                                   |
[Kubernetes Cluster] <-------- [ArgoCD Controller]
```

### 1.3 Why Pull-based is superior
1. **Security**: Your CI server doesn't need admin access to your production cluster. ArgoCD lives *inside* the cluster and reaches out to Git. No firewall holes needed.
2. **Audit Trail**: Every change, who made it, and why, is permanently recorded in Git commit history.
3. **Drift Detection**: If an operator manually edits a deployment using `kubectl edit`, ArgoCD immediately detects the configuration drift and reverts it.

### 1.4 The 4 GitOps Principles
1. **Declarative**: A system managed by GitOps must have its desired state expressed declaratively (like Kubernetes YAML).
2. **Versioned and Immutable**: The desired state is stored in a way that enforces immutability and versioning (Git).
3. **Pulled Automatically**: Software agents automatically pull the declared state declarations.
4. **Continuously Reconciled**: Software agents continuously observe actual system state and apply the desired state.

### 1.5 Interview Q&A
**Q: "What is GitOps and how is it different from regular CI/CD?"**
A: "Regular CI/CD typically uses a push-based model where the CI server runs deployment commands against the cluster, requiring cluster credentials outside the cluster. GitOps uses a pull-based model where an operator (like ArgoCD) runs *inside* the cluster, constantly monitoring a Git repository (the single source of truth) and synchronizing the cluster state to match Git. This eliminates configuration drift, enhances security, and provides a clear audit trail."

---

## SECTION 2: ArgoCD Architecture

### 2.1 ArgoCD Components
To understand ArgoCD, you must understand its internal organs. 

- **argocd-server**: The API server and Web UI. This is what you interact with via the `argocd` CLI or browser.
- **argocd-repo-server**: This component is responsible for cloning your Git repositories and rendering the manifests (running `helm template` or `kustomize build`). It maintains a local cache of Git repositories.
- **argocd-application-controller**: The heart of ArgoCD. This is the reconciliation loop. It constantly compares the live state in Kubernetes with the desired state in Git (rendered by repo-server).
- **argocd-dex-server**: An integrated identity provider that allows you to connect ArgoCD to GitHub, Okta, Google, etc., using OIDC/SAML.
- **argocd-redis**: Used for caching data, drastically improving UI responsiveness and reducing the load on the Kubernetes API server and Git providers.

### 2.2 ASCII Architecture Diagram

```text
       [Web UI / CLI]               [Git Repository] (GitHub/GitLab)
             |                               ^
             v                               | (git fetch)
    +-----------------+             +-------------------+
    |                 |             |                   |
    | argocd-server   |             | argocd-repo-server| <--- [argocd-redis] (Cache)
    |                 |             |                   |
    +--------+--------+             +--------+----------+
             |                               ^
             |       (gRPC)                  | (Rendered Manifests)
             v                               |
    +----------------------------------------+----------+
    |                                                   |
    |           argocd-application-controller           |
    |                 (Reconciliation Loop)             |
    +------------------------+--------------------------+
                             |
                             v
                 [Kubernetes API Server]
```

### 2.3 The Reconciliation Loop
By default, the `argocd-application-controller` polls Git every 3 minutes. If it detects a change, it updates the application state to "OutOfSync". If Auto-Sync is enabled, it applies the changes.

**Pro-tip**: You can configure Git Webhooks (GitHub/GitLab) to ping the `argocd-server`. When a webhook is received, ArgoCD triggers an immediate reconciliation, bypassing the 3-minute wait.

### 2.4 How ArgoCD renders YAML
ArgoCD doesn't just read plain YAML. The `argocd-repo-server` has built-in support for Helm, Kustomize, and Jsonnet. If it sees a `Chart.yaml`, it knows to run the equivalent of `helm template` and pass the resulting raw YAML to the controller.

---

## SECTION 3: ArgoCD Application Manifest

In Kubernetes, everything is a Custom Resource Definition (CRD). ArgoCD introduces the `Application` CRD to define a GitOps deployment.

### 3.1 Complete Application YAML Example

Let's dissect a production-grade Application manifest line-by-line:

```yaml
apiVersion: argoproj.io/v1alpha1     # The API version for ArgoCD CRDs
kind: Application                    # The Custom Resource type
metadata:
  name: payment-service              # Name of the ArgoCD Application
  namespace: argocd                  # ArgoCD apps MUST live in the ArgoCD namespace!
  finalizers:
    - resources-finalizer.argocd.argoproj.io # Deletes K8s resources when this App is deleted
spec:
  project: default                   # Logical grouping of apps (AppProject)
  
  source:                            # WHERE to pull the code from
    repoURL: https://github.com/myorg/microservices.git # Git repo URL
    targetRevision: HEAD             # Branch, tag, or commit hash
    path: k8s/payment                # Directory inside the git repo
    helm:                            # Optional: Helm specific overrides
      valueFiles:
        - values-prod.yaml
  
  destination:                       # WHERE to deploy the code to
    server: https://kubernetes.default.svc # The target cluster (this means local cluster)
    namespace: payments-prod         # The target namespace for the deployed resources
  
  syncPolicy:                        # HOW to synchronize
    automated:                       # Enable automatic sync
      prune: true                    # If file deleted in Git, delete resource in K8s
      selfHeal: true                 # Revert manual kubectl edits
    syncOptions:
      - CreateNamespace=true         # Auto-create the target namespace if it doesn't exist
      - ServerSideApply=true         # Use K8s server-side apply (fixes large CRD issues)
      - ApplyOutOfSyncOnly=true      # Only apply resources that actually changed
  
  revisionHistoryLimit: 10           # Keep the last 10 ReplicaSets/Deployments for fast rollback
```

### 3.2 Deep Dive into Sync Policies
- **selfHeal**: If a developer SSHes into a bastion host and runs `kubectl scale deployment payment-service --replicas=100`, ArgoCD detects this drift. If `selfHeal` is true, ArgoCD instantly scales it back down to what Git says.
- **prune**: If a developer deletes `ingress.yaml` from the Git repository, ArgoCD will delete the Ingress resource in Kubernetes. Without `prune: true`, the Ingress would become an "orphaned" resource.

### 3.3 Interview Q&A
**Q: "I deleted an Application in ArgoCD, but the pods are still running in my cluster. Why?"**
A: "By default, deleting an ArgoCD Application only deletes the ArgoCD tracking object, not the actual deployed resources. To ensure deployed resources are deleted when the Application object is deleted, you must add the `resources-finalizer.argocd.argoproj.io` finalizer to the Application metadata."

---

## SECTION 4: Sync Strategies

### 4.1 Manual vs Automated Sync
- **Manual Sync**: ArgoCD detects changes in Git and marks the app as "OutOfSync", but takes no action. A human must click "Sync" in the UI. Good for production if you lack confidence.
- **Automated Sync**: ArgoCD immediately applies changes when Git changes.

### 4.2 Sync Phases and Waves
When deploying a complex application, order matters. You can't deploy a backend API before the database is ready. ArgoCD solves this with Sync Waves and Hooks.

Add this annotation to your Kubernetes manifests (e.g., in a ConfigMap or Deployment):
`argocd.argoproj.io/sync-wave: "1"`

ArgoCD sorts resources by their wave number (lowest to highest) and waits for resources in Wave 1 to become healthy before deploying Wave 2.

### 4.3 Sync Hooks (PreSync, Sync, PostSync)
Hooks allow you to run jobs during the sync process.

**Production Use Case**: Running a Database Migration before deploying the new API version.

```yaml
# db-migration-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync            # Run this BEFORE syncing the main app
    argocd.argoproj.io/hook-delete-policy: HookSucceeded # Delete job when done
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myorg/db-migrate:v2.0
      restartPolicy: Never
```
ArgoCD will run this Job. Only if the Job succeeds, it proceeds to deploy the actual Application.

### 4.4 Sync Windows
Imagine deploying to production on a Friday at 5 PM. Bad idea. 
ArgoCD allows configuring Sync Windows in AppProjects, e.g., "Allow syncs only Mon-Thu from 9 AM to 4 PM". Outside these hours, syncs are blocked.

---

## SECTION 5: Health Checks

### 5.1 App Health Statuses
An application in ArgoCD has two main indicators:
1. **Sync Status**: Is the cluster state exactly matching Git? (Synced, OutOfSync)
2. **Health Status**: Is the application actually running and functioning?

Health Statuses:
- **Healthy**: Pods are running, services are routing, ingresses are active.
- **Progressing**: Pods are currently spinning up or pulling images.
- **Degraded**: Pods are crashing (CrashLoopBackOff), or readiness probes are failing.
- **Missing**: Resources exist in Git but not in the cluster.
- **Suspended**: A Rollout or Job is paused.
- **Unknown**: ArgoCD doesn't know how to evaluate the health of a custom CRD.

### 5.2 OutOfSync vs Degraded
**Interview Question**: "Can an application be Synced but Degraded?"
**Answer**: "Yes. Synced means ArgoCD successfully applied the YAML from Git to the Kubernetes API. The configuration matches perfectly. However, Degraded means the Kubernetes controllers cannot run the application. For example, if you specified a Docker image that doesn't exist, the state is Synced (YAML applied), but the pods will fail with `ImagePullBackOff`, making the app Degraded."

---

## SECTION 6: App of Apps Pattern

### 6.1 The Problem
If you have 50 microservices, creating 50 ArgoCD Application CRDs manually via the CLI or UI is an anti-pattern. How do you GitOps your GitOps?

### 6.2 The Solution
The "App of Apps" pattern. You create a single "Root" Application. This Root Application points to a Git repository directory containing the YAML files for all your other Applications.

When you deploy the Root Application, ArgoCD reads it, deploys 50 child Applications, and then recursively syncs all 50 microservices.

### 6.3 Example Structure
```text
git-repo/
├── root-app.yaml (The bootstrap app)
└── apps/
    ├── payment-app.yaml (Creates Payment Application)
    ├── frontend-app.yaml (Creates Frontend Application)
    └── redis-app.yaml (Creates Redis Application)
```

**Production Use Case**: A common pattern is having one Root App per environment. `root-app-prod.yaml` deploys the production cluster, `root-app-staging.yaml` deploys the staging cluster.

---

## SECTION 7: ApplicationSets

### 7.1 What is an ApplicationSet?
While App of Apps is great, what if you have 100 identical clusters (e.g., edge computing for retail stores) and need to deploy the same app to all 100? Creating 100 Application YAMLs manually is tedious. 

The `ApplicationSet` controller dynamically generates ArgoCD Applications based on "Generators".

### 7.2 Generators

#### A. List Generator
Generates apps based on a hardcoded list.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook
spec:
  generators:
  - list:
      elements:
      - cluster: dev-cluster
        url: https://dev-cluster.local
      - cluster: prod-cluster
        url: https://prod-cluster.local
  template:
    metadata:
      name: 'guestbook-{{cluster}}' # Resolves to guestbook-dev-cluster
    spec:
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps.git
        targetRevision: HEAD
        path: guestbook
      destination:
        server: '{{url}}'
        namespace: guestbook
```

#### B. Cluster Generator
Automatically generates an app for every cluster registered in ArgoCD. As soon as you add a new cluster, the app is deployed!

#### C. Git Generator
Generates apps based on folders in a Git repository. 
If you have `apps/frontend`, `apps/backend`, `apps/db`, the Git generator will dynamically create 3 Applications.

### 7.3 Use Case
ApplicationSets are heavily used in multi-tenant SaaS environments or multi-region deployments (e.g., deploying the same ingress controller configuration to us-east-1, eu-west-1, and ap-south-1).

---

## SECTION 8: Projects (AppProject)

### 8.1 What is an AppProject?
By default, ArgoCD uses the `default` project. Projects allow you to isolate teams. If the "Frontend Team" and "Backend Team" share an ArgoCD instance, you don't want the frontend team deleting backend databases.

### 8.2 AppProject YAML Example
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: frontend-team
  namespace: argocd
spec:
  description: Project for frontend developers
  
  # Allow deploying ONLY to the dev and prod clusters, in specific namespaces
  destinations:
  - namespace: frontend-dev
    server: https://dev.cluster.local
  - namespace: frontend-prod
    server: https://prod.cluster.local
    
  # Allow pulling code ONLY from this specific git repo
  sourceRepos:
  - "https://github.com/myorg/frontend.git"
  
  # DENY creating cluster-scoped resources like Namespaces or ClusterRoles
  clusterResourceWhitelist: []
  
  # DENY creating specific sensitive resources within namespaces
  namespaceResourceBlacklist:
  - group: '*'
    kind: NetworkPolicy
```
This is a zero-trust model implemented at the CD level.

---

## SECTION 9: Multi-Environment Architecture

How do you manage Dev, Staging, and Prod without duplicating a million YAML files?

### 9.1 Git Repository Strategies
- **Monorepo**: App code and infrastructure YAML live in one repo. Great for small teams, messy for large ones (CI loops get complex).
- **Polyrepo**: One repo for application source code (Java/Go), one repo purely for GitOps Kubernetes manifests. **(Industry Best Practice)**

### 9.2 Kustomize Folder Structure
Use Kustomize to avoid repetition:
```text
gitops-repo/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml (Changes replicas to 1, tags image with -dev)
    │   └── configmap-dev.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml (Changes replicas to 10, requests 4 CPU)
        └── hpa.yaml
```

### 9.3 Promotion Workflow
To promote an image from Dev to Prod:
1. CI builds Image `v2.0` and pushes to ECR.
2. Developer opens a Pull Request modifying `overlays/prod/kustomization.yaml` to change the image tag to `v2.0`.
3. Tech Lead reviews and merges the PR.
4. ArgoCD detects the change in the `prod` folder and deploys it.

---

## SECTION 10: Image Updater

### 10.1 The Problem
Updating Git manifests manually for every single CI build is tedious. Developers hate creating PRs just to bump an image tag.

### 10.2 The Solution: argocd-image-updater
It constantly polls your Docker container registry (e.g., AWS ECR, DockerHub). When a new image is pushed, Image Updater automatically commits the new image tag back to your Git repository, which triggers ArgoCD to sync.

### 10.3 Annotation-Based Configuration
Add these annotations to your ArgoCD Application:
```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: myapp=myregistry/myapp
    argocd-image-updater.argoproj.io/myapp.update-strategy: semver
    argocd-image-updater.argoproj.io/write-back-method: git # Commits to Git!
```
- **semver**: Only update if the new image is a higher semantic version (e.g., `v1.2.0` -> `v1.3.0`).
- **latest**: Pull the most recently built image.

---

## SECTION 11: Progressive Delivery (Argo Rollouts)

Standard Kubernetes Deployments use a "Rolling Update". It replaces pods one by one. But if the new code crashes on startup, a subset of users will experience errors until you manually rollback.

**Argo Rollouts** provides advanced deployment strategies: Blue/Green and Canary.

### 11.1 Canary Deployment
Slowly route traffic to the new version and observe metrics before proceeding.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: payment-api
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20       # Route 20% of traffic to the new version
      - pause: {duration: 10m} # Wait 10 minutes to observe error rates
      - setWeight: 50       # Route 50% traffic
      - pause: {}           # Wait indefinitely for human approval via UI/CLI
      - setWeight: 100      # Full promotion
  template: # standard pod template here
```

### 11.2 Blue-Green
Spins up the entirely new version alongside the old version. No traffic is routed to the new version until it passes smoke tests.

### 11.3 Integration with ArgoCD
ArgoCD natively understands the `Rollout` CRD. The ArgoCD UI displays the glowing blue/green pods and allows you to click "Promote" or "Abort" directly from the GitOps dashboard.

---

## SECTION 12: Multi-Cluster GitOps

Large companies don't run one giant Kubernetes cluster; they run dozens.

### 12.1 Hub-and-Spoke Model
You install ArgoCD on one "Hub" management cluster. You then register "Spoke" clusters to it.

Registering a cluster:
```bash
# Login to argocd
argocd login argocd.myorg.com

# List local kubernetes contexts
kubectl config get-contexts

# Add an external cluster to ArgoCD
argocd cluster add prod-cluster-us-east-1
```
Behind the scenes, ArgoCD creates a ServiceAccount in the target cluster, generates a bearer token, and stores it as a Kubernetes Secret in the ArgoCD namespace on the Hub cluster.

---

## SECTION 13: SSO and RBAC

### 13.1 OIDC Integration
No one should use local `admin` passwords in production.
In `argocd-cm` ConfigMap:
```yaml
data:
  oidc.config: |
    name: GitHub
    issuer: https://github.com
    clientID: xxxxx
    clientSecret: $oidc.github.clientSecret
```

### 13.2 RBAC Policy
Map SSO groups (e.g., GitHub Teams) to ArgoCD Roles in `argocd-rbac-cm`:
```yaml
data:
  policy.csv: |
    # Grant read-only access to all projects to the engineering group
    p, role:readonly, applications, get, */*, allow
    g, org:engineering, role:readonly
    
    # Grant admin access to frontend developers for frontend project
    p, role:frontend-admin, applications, *, frontend-team/*, allow
    g, org:frontend-team, role:frontend-admin
```

---

## SECTION 14: Notifications

GitOps means you don't watch logs manually. The `argocd-notifications` controller alerts you.

### 14.1 Slack Notification Example
Define a trigger in `argocd-notifications-cm`:
```yaml
data:
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase in ['Error', 'Failed']
      send: [slack]
```
Add an annotation to your Application:
```yaml
metadata:
  annotations:
    notifications.argoproj.io/subscribe.on-sync-failed.slack: backend-alerts
```
When a sync fails (e.g., invalid YAML), a message is sent to the `#backend-alerts` Slack channel.

---

## SECTION 15: Secrets in GitOps

### 15.1 The Core Problem
You **cannot** commit raw Kubernetes Secrets to Git. Anyone with Git access can read your database passwords.

### 15.2 Solutions
1. **Sealed Secrets (Bitnami)**: You encrypt the secret locally using `kubeseal` and a public key. You commit the *encrypted* SealedSecret CRD to Git. A controller inside the cluster decrypts it using a private key.
2. **External Secrets Operator**: You store secrets in AWS Secrets Manager or HashiCorp Vault. You commit an `ExternalSecret` CRD to Git (which just contains references, no passwords). The operator fetches the real password from Vault and injects it into a Kubernetes Secret. **(Enterprise Favorite)**

### 15.3 Sealed Secret Workflow
```bash
# 1. Create a raw secret locally (DO NOT COMMIT)
kubectl create secret generic db-pass --from-literal=password=supersecret -o yaml --dry-run=client > secret.yaml

# 2. Encrypt it
kubeseal < secret.yaml > sealed-secret.yaml

# 3. Commit sealed-secret.yaml to Git
git add sealed-secret.yaml && git commit -m "Add db credentials"
```

---

## SECTION 16: Troubleshooting ArgoCD

### 16.1 Common Issues & Fixes
- **App stuck in Progressing**: Usually a Deployment that cannot reach its desired replicas. Check for `CrashLoopBackOff` or `ImagePullBackOff`. Run `kubectl describe pod`.
- **Sync failed: resource already exists**: You manually created a resource using `kubectl apply` without ArgoCD, and now ArgoCD is trying to deploy the same resource. ArgoCD refuses to overwrite unmanaged resources. Fix: Add annotation `argocd.argoproj.io/compare-options: IgnoreExtraneous`.
- **ComparisonError**: Usually means your Helm chart or Kustomize is broken. The `argocd-repo-server` failed to render it. Check the repo-server logs.

### 16.2 CLI Troubleshooting Commands
```bash
# Force a hard refresh and sync
argocd app sync my-app --force

# View logs of the repo server to debug Helm rendering errors
kubectl logs -n argocd -l app.kubernetes.io/name=argocd-repo-server -f

# Get detailed app status
argocd app get my-app
```

---

## END OF CHAPTER

### Complete Production Architecture Diagram
```text
+-------------------+       +-------------------+       +-------------------+
|  Dev Repository   |       | GitOps Repository |       | AWS ECR (Registry)|
| (Java, Go, Node)  |       | (Kustomize, YAML) |       | (Docker Images)   |
+--------+----------+       +---------+---------+       +---------+---------+
         |                            ^                           |
    (CI Pipeline)             (Image Updater commits)             |
         |                            |                           |
         v                            v                           |
+-------------------+       +-------------------+                 |
|   Build Docker    | ----> | argocd-image      | <---------------+
|   Run Tests       |       | updater           |
+-------------------+       +-------------------+
                                      |
                            +---------v---------+
                            |     ArgoCD        |
                            |   Controller      |
                            +---------+---------+
                                      |
                      +---------------+---------------+
                      |                               |
             +--------v--------+             +--------v--------+
             | Dev Cluster     |             | Prod Cluster    |
             | (Auto-Sync)     |             | (Manual Sync)   |
             +-----------------+             +-----------------+
```

### Mini Project Checklist
1. Install ArgoCD via Helm.
2. Create a GitHub repo with Kustomize overlays for dev and prod.
3. Use ApplicationSet Git Generator to deploy both environments automatically.
4. Implement Argo Rollouts to deploy the prod environment via a Canary strategy.
5. Secure your database passwords using External Secrets Operator.

Happy GitOps-ing!
