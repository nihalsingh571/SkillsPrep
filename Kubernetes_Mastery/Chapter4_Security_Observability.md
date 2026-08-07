# Chapter 4: Security, Observability, and Production Operations

Welcome to the ultimate guide on Kubernetes Security, Observability, and Production Operations. This chapter is designed to transition you from a competent Kubernetes user to a production-ready Site Reliability Engineer (SRE) and Kubernetes Administrator. We will dive deep into the internal mechanics of Kubernetes security, explore modern observability stacks, and provide battle-tested playbooks for debugging production incidents. This material is also highly optimized for FAANG-level system design and infrastructure interviews.

---

## PART A: KUBERNETES SECURITY

Security in Kubernetes is multidimensional. It encompasses securing the cluster infrastructure, securing the workloads running on it, and securing the supply chain of container images. We approach Kubernetes security in layers, often referred to as the "4C's of Cloud Native Security": Cloud, Cluster, Container, and Code.

### 1. Authentication Deep Dive

Authentication (AuthN) answers the question: *Who are you?* The Kubernetes API server does not have a built-in "user" database. Instead, it relies on external identity providers or cryptographic proofs.

#### Internal Working
When a request hits the API server, it passes through a chain of authenticators. The first one to successfully authenticate the request stops the evaluation and attaches the user's identity to the request context.

```text
+-----------+        +--------------------------+        +----------------+
|           |        | Kube-API Server          |        |                |
|  Client   | -----> | 1. X.509 Client Certs    | -----> | Authorization  |
| (kubectl/ |        | 2. Bearer Tokens         |        |    (RBAC)      |
|  pod)     |        | 3. Authenticating Proxy  |        |                |
+-----------+        | 4. OIDC / Webhook        |        +----------------+
                     +--------------------------+
```

#### Authentication Methods

1. **X.509 Client Certificates**: Often used for cluster components (kubelet, kube-proxy, controller-manager) and initial admin access. The API server trusts certs signed by its CA (`--client-ca-file`). The `Common Name` (CN) becomes the username, and the `Organization` (O) becomes the group.
2. **Bearer Tokens**: Used for ServiceAccounts.
3. **OIDC (OpenID Connect)**: The standard for enterprise environments. Integrates with Google Workspace, Okta, Azure AD. The API server verifies the signature of a JWT issued by the OIDC provider.
4. **Webhook Token Authentication**: Delegates token verification to an external service.

#### How `kubeconfig` Works
Your `~/.kube/config` file is a YAML file tying together three concepts:
- **Clusters**: API server URL and CA certificate data.
- **Users**: Credentials (client cert/key, auth provider configs like OIDC, or tokens).
- **Contexts**: A mapping of (Cluster + User + Namespace).

#### ServiceAccount Token Validation
When a Pod makes a request to the API server, it uses a ServiceAccount token mounted at `/var/run/secrets/kubernetes.io/serviceaccount/token`.
Historically, these were long-lived Secrets. Modern Kubernetes (1.21+) uses **Bound Service Account Tokens**. These are short-lived, projected volumes.

**JWT Structure**:
- **Header**: Contains the signing algorithm and key ID (`kid`).
- **Payload**: Contains the `sub` (subject - the ServiceAccount name), `aud` (audience - typically the API server), and `exp` (expiration time). The audience validation is crucial to prevent token reuse across different systems.
- **Signature**: Verified by the API server using its Service Account signing key.

#### Production Best Practices
- **Never share kubeconfig files.** Use an OIDC provider mapped to your corporate identity.
- **Implement short-lived credentials.** Rely on automated certificate rotation.
- **Disable anonymous authentication** (`--anonymous-auth=false` on the API server).

#### Interview Q&A
**Q: How does kubectl authenticate to the API server when using OIDC?**
**A**: When using OIDC, `kubectl` initiates an OAuth2 flow with the identity provider (IdP) to obtain an ID token (JWT) and a refresh token. These are stored in the `kubeconfig`. When making a request, `kubectl` sends the ID token in the `Authorization: Bearer <token>` header. The API server, configured with the IdP's OIDC discovery URL, fetches the public keys and verifies the JWT's signature and claims. If the ID token is expired, `kubectl` uses the refresh token to get a new one before making the request.

---

### 2. RBAC Complete Guide

Role-Based Access Control (RBAC) answers: *What can you do?* It controls access to the Kubernetes API.

#### The 4 Core Objects
1. **Role**: Defines permissions (rules) within a specific namespace.
2. **ClusterRole**: Defines cluster-wide permissions or permissions for cluster-scoped resources (like Nodes).
3. **RoleBinding**: Grants a Role to a user, group, or ServiceAccount within a namespace.
4. **ClusterRoleBinding**: Grants a ClusterRole cluster-wide.

#### API Verbs and Resources
- **Verbs**: `get`, `list`, `watch` (Read operations); `create`, `update`, `patch`, `delete`, `deletecollection` (Write operations).
- **Resources**: Standard objects (`pods`, `deployments`, `secrets`, etc.).
- **SubResources**: Actions on resources, like `pods/log`, `pods/exec`, `pods/portforward`.

#### Production Examples

**1. Developer (Read-only plus logs/exec in specific namespace)**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev-team-alpha
  name: developer-role
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "deployments", "statefulsets", "jobs", "cronjobs", "services", "configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods/log", "pods/exec", "pods/portforward"]
  verbs: ["get", "create"] # 'create' is needed for exec and portforward
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-team-alpha-binding
  namespace: dev-team-alpha
subjects:
- kind: Group
  name: "oidc:dev-team-alpha" # Group from OIDC provider
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```
*Line-by-line explanation:* We define a `Role` restricted to the `dev-team-alpha` namespace. It allows reading standard workload resources. Crucially, it allows `get` on `pods/log` and `create` on `pods/exec` and `pods/portforward`. The `RoleBinding` ties this role to an OIDC group.

**2. CI/CD Bot (Deployments and Secrets)**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: cicd-deployer
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list", "create", "update", "patch"]
```

#### Troubleshooting and Commands
Check permissions using `auth can-i`:
```bash
# As current user
kubectl auth can-i create deployments -n default

# Impersonating a ServiceAccount (useful for testing CI roles)
kubectl auth can-i get secrets --as=system:serviceaccount:default:cicd-bot
```

#### ClusterRole Aggregation
You can build a `ClusterRole` by combining rules from other `ClusterRoles` using labels.
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-aggregate
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: [] # Rules are dynamically populated
```

#### Interview Q&A
**Q: Design RBAC for a company with 5 teams, each with their own namespace.**
**A**: I would use an OIDC integration for authentication. Each developer belongs to a specific group in the IdP (e.g., `team-a`, `team-b`). I would create a standard `ClusterRole`, say `namespace-developer`, granting typical permissions (`get/list/watch` on most resources, `create/update` on deployments/configmaps, `pods/log`, `pods/exec`). However, I would NOT bind this cluster-wide. Instead, in each team's namespace, I would create a `RoleBinding` that binds the `namespace-developer` `ClusterRole` to that specific team's OIDC group. This leverages the reusability of ClusterRoles while restricting the scope to specific namespaces via RoleBindings. I would strictly avoid giving `*` permissions or access to `secrets` unless absolutely necessary, utilizing a secrets management tool instead.

---

### 3. Service Accounts Deep Dive

ServiceAccounts provide an identity for processes running in a Pod.

#### The Default ServiceAccount Risk
Every namespace has a `default` ServiceAccount. By default, Kubernetes auto-mounts the token for this account into every Pod. If this account is granted elevated privileges (e.g., via a lazy ClusterRoleBinding), every Pod in the namespace gains those privileges.
**Best Practice**: Always set `automountServiceAccountToken: false` on the `default` ServiceAccount.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: default
automountServiceAccountToken: false
```

#### IRSA (IAM Roles for Service Accounts) on AWS EKS
IRSA is the AWS-native way to provide granular AWS permissions to specific Pods without hardcoding AWS credentials or assigning an IAM role to the underlying Node.

**How it works**:
1. EKS hosts an OIDC provider URL.
2. You create an AWS IAM Role with a Trust Policy that allows federated authentication from the EKS OIDC provider, conditionally checking that the `sub` claim matches the specific namespace and ServiceAccount name.
3. You annotate the Kubernetes ServiceAccount with the ARN of the IAM Role.
4. EKS injects AWS SDK configuration environment variables and a projected volume containing an OIDC token (a Web Identity Token) into the Pod.
5. The AWS SDK inside the Pod uses this token to call `sts:AssumeRoleWithWebIdentity` and get short-lived AWS credentials.

**Complete Setup YAML**:
```yaml
# 1. The ServiceAccount annotated with the IAM Role
apiVersion: v1
kind: ServiceAccount
metadata:
  name: s3-reader-sa
  namespace: data-processing
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/S3ReaderRole
```

**IAM Trust Policy (JSON)**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53E5107693BA735"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53E5107693BA735:sub": "system:serviceaccount:data-processing:s3-reader-sa",
          "oidc.eks.us-east-1.amazonaws.com/id/EXAMPLED539D4633E53E5107693BA735:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```
*Explanation:* This policy only allows assuming the role if the token comes from the specific EKS cluster's OIDC provider AND the token was issued to the `s3-reader-sa` ServiceAccount in the `data-processing` namespace.

---

### 4. Secrets Management

Native Kubernetes Secrets are merely base64 encoded. Anyone with read access to etcd or the API server can read them. This is insufficient for production.

#### Encryption at Rest
You must configure `EncryptionConfiguration` on the API server to encrypt secrets before storing them in etcd. Use strong providers like `aescbc` or a KMS provider (AWS KMS, GCP Cloud KMS).

#### The Secret Delivery Problem
How do you get a database password into a cluster without committing it to Git?

**1. Sealed Secrets (Bitnami)**
- You generate an asymmetric key pair inside the cluster.
- You encrypt your secret locally using `kubeseal` and the public key, creating a `SealedSecret` custom resource.
- You commit the `SealedSecret` to Git (Safe!).
- A controller inside the cluster uses the private key to decrypt it into a standard native Secret.

**2. External Secrets Operator (ESO)**
- Integrates with external secret management systems (AWS Parameter Store, Secrets Manager, Azure Key Vault, HashiCorp Vault).
- You define a `SecretStore` (connection details) and an `ExternalSecret` (what to fetch).
- ESO fetches the value and creates a native Kubernetes Secret.

**ESO Example (AWS Systems Manager Parameter Store)**:
```yaml
# Connect to AWS using IRSA
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-parameter-store
spec:
  provider:
    aws:
      service: ParameterStore
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-sa
            namespace: external-secrets
---
# Fetch the secret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: my-app
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-parameter-store
    kind: ClusterSecretStore
  target:
    name: app-db-secret # Creates this K8s Secret
    creationPolicy: Owner
  data:
  - secretKey: DB_PASSWORD
    remoteRef:
      key: /production/myapp/db-password
```
*Explanation:* The `ExternalSecret` instructs the operator to look up `/production/myapp/db-password` in AWS SSM and place the value into a new Kubernetes Secret named `app-db-secret` under the key `DB_PASSWORD`. It refreshes every hour.

**3. HashiCorp Vault Agent Injector**
- Instead of creating native Kubernetes Secrets, Vault uses an Admission Webhook to inject a sidecar container into your Pod.
- The sidecar authenticates to Vault (using the Pod's ServiceAccount token), fetches the secrets, and writes them to a shared memory volume (`/vault/secrets`).
- The application reads the secrets from the file system.
- **Advantage**: The secret never exists as a Kubernetes Secret object.

| Tool | Pros | Cons | Best For |
| :--- | :--- | :--- | :--- |
| **K8s Secrets** | Built-in, simple | Unencrypted (by default), no GitOps | Minikube, trivial data |
| **Sealed Secrets** | GitOps friendly, no external infra | Key rotation can be painful, secrets end up as native k8s objects | Startups heavily invested in GitOps |
| **ESO** | Connects to existing cloud KMS, creates native secrets | External dependency | Enterprises already using AWS/GCP/Azure secret managers |
| **Vault Injector**| Highest security, secrets not in API | High complexity, requires running Vault | High-security/compliance environments |

---

### 5. Pod Security

Securing the Pod is the last line of defense. A compromised container should not mean a compromised node.

#### Security Context
The `securityContext` can be defined at the Pod level (applies to all containers/volumes) and the Container level.

#### Complete Hardened Pod YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      automountServiceAccountToken: false
      # Pod-level security context
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 20000 # Owns mounted volumes
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: main-app
        image: my-app:v1.2.3
        # Container-level security context
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
      volumes:
      - name: tmp-volume
        emptyDir: {}
```
*Line-by-line explanation:*
- `automountServiceAccountToken: false`: Prevents unnecessary API access.
- `runAsNonRoot: true`: Forces the kubelet to validate the image does not run as root (UID 0).
- `runAsUser: 10001`: Explicitly sets the user ID.
- `seccompProfile: RuntimeDefault`: Applies the default seccomp profile, blocking dangerous system calls (like `ptrace`).
- `allowPrivilegeEscalation: false`: Prevents the process from gaining more privileges than its parent (disables `setuid` binaries).
- `readOnlyRootFilesystem: true`: Prevents attackers from modifying binaries or writing scripts to the filesystem. We provide an `emptyDir` volume mounted at `/tmp` for legitimate temporary writes.
- `capabilities: drop: [ALL]`: Drops all Linux capabilities (like `CHOWN`, `NET_RAW`, etc.). If the app needs to bind to a port < 1024, you would add `NET_BIND_SERVICE`.

#### Pod Security Admission (PSA)
PSA replaces the deprecated PodSecurityPolicies (PSP). It enforces standards at the namespace level using labels.
Levels: `Privileged` (unrestricted), `Baseline` (prevents known privilege escalations), `Restricted` (enforces strict best practices like the YAML above).

```bash
# Enforce restricted mode on a namespace
kubectl label namespace secure-ns pod-security.kubernetes.io/enforce=restricted
# Audit baseline mode (logs violations but allows creation)
kubectl label namespace secure-ns pod-security.kubernetes.io/audit=baseline
```

#### Interview Q&A
**Q: What is the minimum security configuration for a production pod?**
**A**: A production pod should never run as root (`runAsNonRoot: true`, `runAsUser: <non-zero>`). It should have `allowPrivilegeEscalation` set to `false`. The root filesystem should be read-only (`readOnlyRootFilesystem: true`) to prevent tampering, utilizing memory-backed `emptyDir` volumes for temporary data. It should drop all Linux capabilities, adding back only what is strictly necessary. Finally, it should not mount the default ServiceAccount token unless required, and should apply the `RuntimeDefault` seccomp profile.

---

### 6. OPA Gatekeeper

Open Policy Agent (OPA) Gatekeeper is an Admission Controller Webhook. Before an object is persisted to etcd, Gatekeeper evaluates it against custom policies written in the Rego language.

#### Architecture
1. **ConstraintTemplate**: Defines the Rego logic and the schema for parameters. (The "Code").
2. **Constraint**: Instantiates the template and applies it to specific resources (e.g., "Deployments in namespace X"). (The "Configuration").

#### Example: Require specific labels
**1. The ConstraintTemplate**
```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        openAPIV3Schema:
          type: object
          properties:
            labels:
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels

        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
```
*Explanation:* The Rego code extracts the provided labels from the incoming request (`input.review.object.metadata.labels`). It gets the required labels from the constraint parameters. It performs a set difference (`missing := required - provided`). If `missing` is not empty, it triggers a `violation`.

**2. The Constraint**
```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: must-have-owner
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment", "StatefulSet"]
  parameters:
    labels: ["owner", "cost-center"]
```
*Explanation:* This applies the logic to all Deployments and StatefulSets, requiring the labels "owner" and "cost-center". Any creation request missing these will be rejected.

#### Audit Mode
You can set `enforcementAction: dryrun` on a Constraint to evaluate existing resources and report violations in the Constraint's status field without blocking new deployments.

#### Interview Q&A
**Q: How is OPA Gatekeeper different from NetworkPolicy?**
**A**: They operate at entirely different layers. NetworkPolicy is implemented by the CNI plugin (like Calico or Cilium) and controls network traffic (L3/L4/L7) between pods (e.g., "Pod A cannot talk to Pod B on port 80"). OPA Gatekeeper is an Admission Controller working at the API server level. It controls what Kubernetes *resources* can be created or modified (e.g., "You cannot create a Pod unless it has a resource limit"). NetworkPolicy secures data in motion; Gatekeeper secures the configuration of the cluster itself.

---

### 7. Supply Chain Security

Securing the cluster is irrelevant if you are deploying compromised images.

#### Trivy (Vulnerability Scanning)
Trivy scans container images for known CVEs. It should be run in CI/CD pipelines to block builds with high/critical severity issues.
```bash
# Fail CI pipeline if critical vulnerabilities exist
trivy image --severity CRITICAL --exit-code 1 my-company/app:latest
```

#### Cosign & Sigstore (Signing Images)
How does the cluster know the image hasn't been tampered with between the CI build and deployment? You sign it.
Sigstore enables "keyless" signing using OIDC identities, generating ephemeral certificates recorded in a public transparency log (Rekor).

```bash
# In CI: Sign the image using an OIDC identity
cosign sign --keyless my-company/app:latest
```
To enforce this, deploy an admission controller (like Kyverno or Sigstore Policy Controller) to reject images without a valid signature verifying they were built by your CI system.

#### Falco (Runtime Security)
Trivy protects the build; Falco protects the runtime. Falco uses eBPF (Extended Berkeley Packet Filter) to trace kernel system calls securely with low overhead.

```text
+-------------------+      +----------------+      +---------------+
| Container Process | ---> | Syscall (open) | ---> | Linux Kernel  |
+-------------------+      +----------------+      +-------+-------+
                                                           |
                                                           v
                                                  +--------+--------+
                                                  | Falco eBPF hook |
                                                  +--------+--------+
                                                           |
                                                  +--------v--------+
                                                  | Falco Rules     |
                                                  | (alert engine)  |
                                                  +-----------------+
```

Falco detects anomalous behavior based on rules. E.g., a process trying to read `/etc/shadow`, a shell spawning inside a container, or a process attempting network communication on an unexpected port.

**Example Falco Rule**: Alert when someone opens a shell via `kubectl exec`.
```yaml
- rule: Terminal shell in container
  desc: A shell was spawned by a program in a container
  condition: >
    spawned_process and container
    and shell_procs and proc.tty != 0
    and container_entrypoint
  output: "A shell was spawned in a container (user=%user.name container_id=%container.id command=%proc.cmdline)"
  priority: WARNING
```

---

### 8. Network Security

By default, Kubernetes networking is flat: any pod can talk to any pod.

#### Default Deny NetworkPolicy
The first step in securing a namespace is to implement a default deny policy, forcing developers to explicitly allow necessary traffic.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {} # Selects ALL pods in the namespace
  policyTypes:
  - Ingress
  - Egress
  # Empty ingress and egress sections mean DENY ALL
```
*Note*: You will need to explicitly allow DNS egress (port 53 UDP/TCP to `kube-system`) to allow name resolution to function.

#### mTLS with Service Mesh (Istio/Linkerd)
NetworkPolicies operate at L3/L4 (IPs and Ports). A Service Mesh like Istio provides L7 security and mutual TLS (mTLS).
- Every pod gets an Envoy proxy sidecar.
- The control plane issues X.509 certificates to every proxy.
- All service-to-service communication goes proxy-to-proxy.
- The traffic is encrypted (confidentiality) and mutually authenticated (Identity). You know for a fact that "Service A" is calling "Service B", regardless of IPs.

---

## PART B: OBSERVABILITY

Observability is not just metrics; it's the ability to infer the internal state of a system based on its external outputs: Metrics, Logs, and Traces (The Three Pillars).

### 9. Prometheus on Kubernetes

Prometheus is the de facto standard for Kubernetes metrics. It uses a pull-based model, scraping `/metrics` endpoints.

#### The kube-prometheus-stack
Never deploy Prometheus manually. Use the `kube-prometheus-stack` Helm chart. It deploys:
- **Prometheus Operator**: Manages Prometheus configurations via CRDs.
- **Prometheus**: The time-series database.
- **Alertmanager**: Handles routing and silencing alerts.
- **Grafana**: For visualization.
- **kube-state-metrics**: Exposes metrics about Kubernetes objects (e.g., "How many pods are pending?").
- **node-exporter**: Runs on every node to expose hardware and OS metrics.

#### ServiceMonitor and PodMonitor
Instead of complex Prometheus configuration files, the Operator uses CRDs.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backend-monitor
  labels:
    release: prometheus # Label must match Prometheus selector
spec:
  selector:
    matchLabels:
      app: backend-api
  endpoints:
  - port: web
    path: /metrics
    interval: 15s
```
*Explanation:* The Prometheus Operator watches for `ServiceMonitor` objects. When it sees this, it configures Prometheus to find the Kubernetes Service with `app: backend-api`, look up its endpoints (pods), and scrape the `web` port at `/metrics` every 15 seconds.

#### Crucial PromQL Metrics for Production
- **CPU Throttling**: Are limits too low?
  `rate(container_cpu_cfs_throttled_seconds_total[5m])`
- **Memory Saturation**: How close to OOMKill?
  `container_memory_working_set_bytes / container_spec_memory_limit_bytes`
- **CrashLoopBackOffs**:
  `kube_pod_container_status_restarts_total > 5`
- **API Server Latency**: (99th percentile)
  `histogram_quantile(0.99, rate(apiserver_request_duration_seconds_bucket[5m]))`

#### Alerting Rules
Define alerts as code using `PrometheusRule`.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: app-alerts
spec:
  groups:
  - name: application.rules
    rules:
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m])) > 0.05
      for: 2m
      labels:
        severity: critical
        team: backend
      annotations:
        summary: "High HTTP 5xx error rate (>5%)"
        description: "Service is experiencing high failure rate. Check logs."
```
*Explanation:* Calculates the ratio of 5xx errors to total requests over a 5-minute window. If it exceeds 5% for 2 consecutive minutes, an alert is fired and routed via Alertmanager based on the `team: backend` label.

---

### 10. Grafana Dashboards

Grafana visualizes Prometheus data. Manage dashboards as code via ConfigMaps.

#### Essential Production Dashboards
1. **Cluster Overview**: Node CPU/Memory allocation vs. actual usage.
2. **Namespace Resource Quota**: Are teams hitting their limits?
3. **Application RED Metrics**: Rate (requests/sec), Errors (5xx rate), Duration (P50/P90/P99 latency).
4. **Kubelet & API Server Health**: Core infrastructure components.

**The USE Method (For Infrastructure)**:
- **Utilization**: % of resource used.
- **Saturation**: Queuing/Throttling (e.g., CPU run queue length).
- **Errors**: e.g., disk I/O errors.

**The RED Method (For Services)**:
- **Rate**: Number of requests per second.
- **Errors**: Number of failed requests per second.
- **Duration**: Time taken to process a request (latency histograms).

---

### 11. Logging with Loki

Loki is a log aggregation system heavily inspired by Prometheus. Unlike Elasticsearch, Loki does *not* index the content of the logs. It only indexes labels (like namespace, pod name). This makes it vastly cheaper and faster for Kubernetes workloads.

#### Architecture
- **Promtail**: A DaemonSet running on every node. It mounts `/var/log/containers` (where kubelet writes pod logs), extracts labels using Kubernetes API metadata, and ships logs to Loki.
- **Loki**: Stores the log chunks and indices.
- **Grafana**: Queries Loki using LogQL.

```text
Node 1: [Pod A logs] -> Promtail \
Node 2: [Pod B logs] -> Promtail --> Loki Storage <-- Grafana UI
Node 3: [Pod C logs] -> Promtail /
```

#### LogQL (Log Query Language)
Filter logs similar to PromQL:
```logql
# Find all ERROR logs in the backend deployment
{app="backend-api", namespace="production"} |= "ERROR"

# Find logs containing "payment failed" but NOT containing "timeout"
{app="payment-service"} |= "payment failed" != "timeout"

# Metric query: Rate of errors per second
rate({app="backend-api"} |= "ERROR" [5m])
```

#### Correlation
Because Loki uses the exact same labeling system as Prometheus (e.g., `namespace="prod", pod="app-123"`), Grafana allows you to seamlessly switch from a spike in a Prometheus metric dashboard directly to the exact Loki logs for that specific pod during that specific time window.

---

### 12. Distributed Tracing

In microservices, a single user request might traverse 10 different pods. If it's slow, logs and metrics won't tell you *where* the bottleneck is. Tracing maps the entire journey.

#### OpenTelemetry (OTel) and Tempo
- **OpenTelemetry**: The standard for instrumenting code (SDKs for Go, Java, Python). It generates spans (a single operation) and traces (a collection of spans).
- **Context Propagation**: OTel injects headers (like `traceparent`) into HTTP requests to pass the Trace ID between services.
- **OTel Collector**: A daemon/sidecar that receives spans from apps, batches them, and exports them.
- **Grafana Tempo**: A highly scalable backend that stores traces, accessible via Grafana.

By logging the `trace_id` in your application logs (which Promtail sends to Loki), you can correlate an error log directly to the distributed trace to see exactly what API calls failed downstream.

---

## PART C: PRODUCTION DEBUGGING

This section covers the definitive workflows for resolving the most critical Kubernetes production incidents.

### 13. CrashLoopBackOff — Complete Debugging

**What it means**: The container starts, fails (exits with non-zero code or is killed by a probe), and Kubernetes restarts it. It happens repeatedly, and Kubernetes increases the backoff delay (10s, 20s, 40s... up to 5 minutes) between restarts.

**Root Causes**:
1. Application panic/exception on startup.
2. Missing configuration (ConfigMap/Secret).
3. Liveness probe failing too quickly.
4. OOMKilled (Out of Memory).

#### Systematic Debugging Workflow
1. **Identify the failing container** (Pods can have multiple):
   ```bash
   kubectl get pods -n prod
   kubectl describe pod <pod-name> -n prod
   ```
2. **Look at the `Events` section at the bottom of the describe output.**
   Look for `Liveness probe failed` or `Back-off restarting failed container`.
3. **Look at the `Last State` section in the container spec.**
   Look at the `Exit Code`.
   - `Exit Code 1`: General application error. Look at logs.
   - `Exit Code 137`: OOMKilled (See section 14) or SIGKILL.
   - `Exit Code 143`: SIGTERM (graceful shutdown taking too long).
4. **Check the logs.** Crucially, check the logs of the *previous* crashed instance.
   ```bash
   kubectl logs <pod-name> -n prod               # Current instance
   kubectl logs <pod-name> -n prod --previous -c <container> # The one that crashed
   ```
5. **Check probes.** If the app takes 30 seconds to start, but `initialDelaySeconds` on the liveness probe is 5 seconds, Kubernetes will kill it before it finishes starting.

---

### 14. OOMKilled — Complete Debugging

**What it means**: The container exceeded its configured `resources.limits.memory`. The Linux Out-Of-Memory (OOM) killer sent a SIGKILL (137) to the process.

**Debugging**:
1. `kubectl describe pod` will show `Reason: OOMKilled` and `Exit Code: 137`.
2. **Java specific**: Java 8/11 often don't respect cgroup limits properly without flags. Setting `-Xmx` (Heap size) to the exact pod limit will cause OOMs because the JVM needs non-heap memory (threads, metaspace, native buffers). General rule: `-Xmx` should be 70-80% of the pod memory limit.
3. **Node OOM**: Sometimes the *Node* runs out of memory, not the pod limit. Run `kubectl describe node` and look at the `Conditions`. If `MemoryPressure` is True, the kubelet will evict pods (starting with BestEffort QOS pods) to save the node.

**Solutions**:
- Increase the memory `limit`.
- Profile the application for memory leaks.
- Implement Vertical Pod Autoscaler (VPA) to automatically suggest or apply correct limits based on historical usage.

---

### 15. ImagePullBackOff / ErrImagePull

**What it means**: The kubelet cannot pull the container image from the registry.

**Root Causes**:
1. Typo in image name or tag.
2. The image does not exist.
3. Missing or incorrect `imagePullSecrets` for private registries.
4. Rate limiting (e.g., Docker Hub's limit on anonymous pulls).

**Debugging**:
1. `kubectl describe pod <pod-name>` -> check the `Events` at the bottom.
2. The event message will tell you exactly what failed:
   - `rpc error: code = NotFound`: Image doesn't exist.
   - `pull access denied`: Missing credentials.
   - `toomanyrequests`: Rate limited.

**Fixing Private Registry Access**:
```bash
# 1. Create the secret
kubectl create secret docker-registry acr-secret \
  --docker-server=myregistry.azurecr.io \
  --docker-username=my-user \
  --docker-password=my-pass \
  -n prod

# 2. Reference it in the Pod spec
# ...
spec:
  imagePullSecrets:
  - name: acr-secret
  containers:
  # ...
```

---

### 16. Pending Pods

**What it means**: The Pod object has been created in the API server, but the Scheduler cannot find a suitable Node to run it on.

**Root Causes**:
1. **Insufficient Resources**: No node has enough unallocated CPU or Memory to satisfy the Pod's `resources.requests`.
2. **Taints and Tolerations**: Nodes have taints (e.g., `gpu=true:NoSchedule`), and the pod lacks the corresponding toleration.
3. **Affinity Rules**: Unsatisfiable `nodeSelector`, `nodeAffinity`, or `podAntiAffinity` rules (e.g., asking to spread pods across 3 zones, but only 2 zones exist).
4. **Storage**: Pod requests a PersistentVolumeClaim (PVC) that is pending provisioning, or the provisioned volume is in a zone where no compute nodes are available.

**Debugging**:
1. Run `kubectl describe pod <pod-name>`.
2. The scheduler writes clear events explaining exactly why each node was rejected.
   Example Event: `0/5 nodes are available: 2 Insufficient memory, 3 node(s) had taint {dedicated: database}, that the pod didn't tolerate.`
3. To check cluster capacity: `kubectl get nodes` and `kubectl describe node <node-name>` (look at the `Allocated resources` section, not just total capacity).

---

### 17. Node NotReady

**What it means**: The `kubelet` daemon on the worker node has stopped reporting its health status to the API server, or has reported an unhealthy condition. After a grace period (default 40s), the API server marks the node as `NotReady`.

**Impact**: After another grace period (default 5 minutes), the control plane will add a `NoExecute` taint to the node, evicting all running pods and scheduling them elsewhere.

**Root Causes**:
1. Kubelet process crashed.
2. Network partition (API server cannot reach node).
3. Severe resource exhaustion (CPU starvation preventing kubelet from running).
4. Container runtime (containerd/CRI-O) is deadlocked.

**Debugging**:
1. `kubectl get nodes`
2. `kubectl describe node <node-name>` -> Check the `Conditions` section (Ready, DiskPressure, MemoryPressure, PIDPressure, NetworkUnavailable).
3. If it's a hard down, you must SSH into the node or use cloud provider serial consoles.
4. On the node:
   ```bash
   # Check kubelet status
   systemctl status kubelet
   # Follow logs for errors
   journalctl -u kubelet -f
   # Check container runtime
   systemctl status containerd
   ```

---

### 18. Pod Stuck Terminating

**What it means**: You delete a pod, but it hangs in the `Terminating` state forever.

**Root Causes**:
1. **Finalizers**: A controller (like a storage CSI driver) added a finalizer to the pod metadata to perform cleanup. If that controller crashes or fails to clean up, the finalizer is never removed, and the API server refuses to delete the object.
2. **Unreachable Node**: If the node running the pod is dead/NotReady, the API server waits for the kubelet to confirm the pod is killed. Since the kubelet is dead, it never confirms.

**Debugging & Fixes**:
1. Check for finalizers: `kubectl get pod <pod-name> -o yaml | grep finalizers -A 2`
2. **Graceful wait**: Is the application ignoring SIGTERM signals and waiting out the full `terminationGracePeriodSeconds` (default 30s)?
3. **Emergency Force Delete** (Use with extreme caution, especially for StatefulSets, as it can lead to split-brain data corruption):
   ```bash
   kubectl delete pod <pod-name> --grace-period=0 --force
   ```
4. **Remove Finalizer manually** (Patching):
   ```bash
   kubectl patch pod <pod-name> -p '{"metadata":{"finalizers":null}}'
   ```

---

### 19. Production Incident Debugging Workflow

When PagerDuty goes off at 3 AM, follow this systematic playbook. Do not guess; follow the data.

**The SRE Playbook:**

1. **Assess Blast Radius**: Is it one pod, one node, one namespace, or the whole cluster?
   ```bash
   # Quick cluster health check
   kubectl get componentstatuses (deprecated but useful in older clusters)
   kubectl get nodes
   ```
2. **Find the Noise**: What is currently breaking?
   ```bash
   # Show all pods NOT running properly across all namespaces
   kubectl get pods -A | grep -v -E 'Running|Completed'
   ```
3. **Check the Event Stream**: The cluster's audit log of what just happened.
   ```bash
   # Get the most recent 50 events cluster-wide
   kubectl get events -A --sort-by=.metadata.creationTimestamp | tail -50
   ```
4. **Correlate with Observability Stack**:
   - Go to Grafana. Check the Cluster Overview dashboard. Are nodes maxed out on CPU/Memory?
   - Check the Application RED dashboard. Did traffic spike? Did errors spike?
   - Find the exact time the errors started.
5. **Dive into Logs**:
   - Go to Loki. Query logs for the failing namespace/app during the exact minute the errors started. Look for stack traces.
6. **Check Scaling and Limits**:
   ```bash
   # Are HPA's maxed out?
   kubectl get hpa -A
   # Are nodes heavily utilized?
   kubectl top nodes
   # Are specific pods hogging resources?
   kubectl top pods -n <namespace>
   ```
7. **Control Plane Check**: If `kubectl` is slow or timing out, the API server or etcd might be under stress.
   ```bash
   kubectl get pods -n kube-system
   ```

---

## END OF CHAPTER

### Security Checklist for Production
- [ ] API server endpoint is private or IP-restricted.
- [ ] Anonymous authentication disabled on API server.
- [ ] `automountServiceAccountToken: false` applied to default service accounts.
- [ ] All pods run as non-root (`runAsNonRoot: true`).
- [ ] Root filesystem is read-only (`readOnlyRootFilesystem: true`).
- [ ] Privilege escalation disabled (`allowPrivilegeEscalation: false`).
- [ ] OPA Gatekeeper or Kyverno enforcing Pod Security Standards (Restricted).
- [ ] NetworkPolicies implemented (Default Deny Ingress/Egress).
- [ ] Secrets managed via External Secrets Operator or Vault (never bare K8s Secrets).
- [ ] Images scanned in CI via Trivy and signed via Cosign.

### Observability Cheat Sheet
- **Metrics (Prometheus)**: Best for aggregation, alerting, and identifying *when* something broke. Use PromQL.
- **Logs (Loki)**: Best for debugging high-cardinality data and identifying *why* something broke. Use LogQL.
- **Traces (Tempo/OTel)**: Best for microservice architecture to identify *where* something broke in a complex call chain.

### Interview Q&A (Bonus)

**Q1: How would you debug an application that is intermittently slow but not crashing?**
A: I would rely heavily on the observability stack. I'd start with Grafana to look at the RED metrics (Rate, Errors, Duration) for that specific service. If the P99 latency is high, I'd check CPU/Memory utilization to see if the pod is being CPU throttled (`container_cpu_cfs_throttled_seconds_total`). If resources are fine, I'd use distributed tracing (Tempo) to see the waterfall graph of a slow request. This would show if the delay is internal computation, a slow database query, or a slow downstream API call. I'd also check Loki logs for garbage collection pauses if it's a Java/Go app.

**Q2: A developer says their pod is Pending. Walk me through your debugging steps.**
A: First, I run `kubectl describe pod <name>` and check the Events. The scheduler event will state why it couldn't place the pod. Common reasons are insufficient CPU/Memory on nodes, which I'd verify with `kubectl top nodes` and `kubectl describe node`. Another reason could be unsatisified NodeAffinity or PodAntiAffinity rules, or the pod lacking a Toleration for a tainted node. Finally, if the pod uses a PersistentVolumeClaim, the scheduler will leave the pod pending until the volume is provisioned and bound; I'd check `kubectl get pvc`.

**Q3: Explain the difference between Liveness, Readiness, and Startup probes.**
A: A **Liveness** probe checks if the container is deadlocked or crashed; if it fails, the kubelet restarts the container. A **Readiness** probe checks if the container is ready to accept HTTP traffic; if it fails, the pod's IP is removed from the Service endpoints, stopping traffic, but the container is *not* restarted. A **Startup** probe runs first and pauses the other two probes until it succeeds; it's used for legacy applications that take a very long (and unpredictable) time to initialize, preventing aggressive liveness probes from killing the app before it even finishes booting.

**Q4: How do you prevent a compromised pod from accessing the cloud provider's metadata service (e.g., AWS IMDSv1 on 169.254.169.254)?**
A: Historically, you would use a NetworkPolicy to block egress to `169.254.169.254`. The modern best practice is to enforce IMDSv2 at the node/EC2 level (which requires a PUT request with a specific header and limits hop count), and strictly use IAM Roles for Service Accounts (IRSA). With IRSA, pods are given temporary credentials via OIDC token injection and do not need to hit the node's metadata endpoint at all to assume AWS roles.

### Mini Lab: Simulate a Production Incident
1. Deploy `kube-prometheus-stack` via Helm.
2. Create a Deployment of Nginx, but set the `image` to `nginx:does-not-exist`.
3. Run `kubectl get pods`. Notice the `ErrImagePull` or `ImagePullBackOff`.
4. Run `kubectl describe pod <pod-name>`. Read the explicit event stating the manifest is unknown.
5. Fix the image to `nginx:latest`.
6. Add a liveness probe pointing to `/healthz` (which doesn't exist by default in Nginx).
7. Watch the pod enter `CrashLoopBackOff`.
8. Open Grafana, look at the Kubernetes / Compute Resources / Namespace (Pods) dashboard to see the restart metric climb.
9. Fix the probe to point to `/` or remove it. The incident is resolved.
