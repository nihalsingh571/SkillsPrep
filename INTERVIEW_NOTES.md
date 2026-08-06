# INTERVIEW_NOTES: Chaos-Engineered Self-Healing GitOps Platform on Minikube

## Section 0: PROJECT PITCH

### 30-Second Pitch (Recruiter Screen)
"I built a self-healing GitOps platform on Minikube to demonstrate modern cloud-native resilience. It’s a 3-tier application (NGINX, FastAPI, Postgres) managed entirely through a custom Helm chart and deployed automatically via ArgoCD. I implemented comprehensive observability with the kube-prometheus-stack and introduced Chaos Mesh to run automated chaos experiments, like killing pods, to measure and optimize Mean Time To Recovery (MTTR). It showcases my hands-on skills with Kubernetes, Helm, GitOps, and chaos engineering principles."

### 2-Minute Pitch (Phone Interview)
"For my capstone project, I wanted to move beyond just deploying apps and focus on resilience and automated operations. I engineered a complete local GitOps environment using Minikube. The core is a 3-tier Python/React/Postgres stack, but the real value is in the infrastructure. I wrote a custom Helm chart from scratch—12 templates with a single `values.yaml` as the source of truth. 

I integrated ArgoCD to enforce the desired state directly from GitHub, configuring it for automated sync, self-healing, and pruning. This means any manual kubectl changes are automatically reverted by ArgoCD, enforcing true GitOps.

To prove the system is actually resilient, I implemented Chaos Mesh and wrote experiments like `pod-kill`. I monitor these experiments using a Prometheus and Grafana stack. For instance, when I inject a pod-kill failure, I can measure my MTTR down to the second—currently around 30 to 60 seconds. Through tuning Kubernetes primitives like Horizontal Pod Autoscalers, Pod Disruption Budgets, and fine-tuning readiness and liveness probes, I ensured zero-downtime rolling updates and highly resilient workloads. This project mimics real-world SRE and platform engineering workflows on a local cluster."

### 5-Minute Demo Walkthrough Order
1. **The GitOps Workflow (ArgoCD):** Open ArgoCD UI. Show the application status as 'Synced' and 'Healthy'. Demonstrate self-healing by deleting a Deployment manually via `kubectl delete deploy backend` and watching ArgoCD recreate it instantly.
2. **The Infrastructure as Code (Helm):** Show the GitHub repo, specifically the `values.yaml` and a couple of templates (like deployment or HPA) to explain the dry and declarative nature of the setup.
3. **Observability (Grafana):** Open the Grafana dashboard. Show the CPU utilization, memory, and pod status panels. Explain how Prometheus scrapes the metrics via annotations.
4. **Chaos Injection (Chaos Mesh):** Open the Chaos Mesh dashboard or apply the `pod-kill.yaml` manifest. Watch the pods terminate.
5. **Resilience & MTTR Validation:** Switch back to Grafana and `kubectl get pods -w`. Show how the ReplicaSet spawns a new pod, how the Readiness probe gates traffic until the app is ready, and how the MTTR is tracked on the dashboard.

### One-liner for Resume/LinkedIn
"Architected a self-healing GitOps platform on Minikube using ArgoCD, Helm, and Chaos Mesh to automate deployments and validate system resilience through chaos engineering, achieving a 30s MTTR."

---

## Section 1: CORE SKILL AREAS CHECKLIST

| Skill Area | Depth | What the Repo Demonstrates | What's Missing |
| :--- | :--- | :--- | :--- |
| **Kubernetes Fundamentals** | Hands-on | Deployments, StatefulSets, Services, ConfigMaps, HPA, PDBs, Probes, Resource limits/requests. | Ingress controllers, NetworkPolicies, DaemonSets. |
| **Helm Templating** | Hands-on | 12 custom templates, flow control (`if`/`range`), `values.yaml` as single source of truth. | Subcharts, Helm hooks, complex library charts. |
| **GitOps/ArgoCD** | Hands-on | Automated sync, self-heal, prune, finalizers, pullPolicy overrides for local dev. | ApplicationSets, multi-cluster management, SSO integration. |
| **Observability** | Hands-on | `kube-prometheus-stack`, custom metrics via annotations, Grafana dashboards, PromQL. | Distributed tracing (Tempo/Jaeger), Centralized logging (Loki/Elasticsearch). |
| **Chaos Engineering** | Hands-on | Chaos Mesh integration, defining blast radius, `pod-kill` experiment, measuring MTTR. | Network-delay, CPU-stress, automated CI chaos testing. |
| **Resilience Patterns** | Hands-on | Graceful termination, rolling updates, readiness gating, redundancy via HPA. | Circuit breakers (Service Mesh), rate limiting, multi-region failover. |
| **Container/Docker** | Surface | Running standard images (nginx, postgres, python). | Multi-stage Dockerfile optimization, distroless images, image scanning. |
| **Linux/Networking** | Surface | ClusterIP, internal DNS resolution, basic port forwarding. | Calico/Cilium CNI deep dives, BGP, kernel tuning. |
| **Application Design** | Surface | Basic 3-tier architecture separating state (DB) from stateless apps. | Microservices event-driven architecture, message queues (Kafka/RabbitMQ). |
| **Git Workflow** | Hands-on | Git as the source of truth for all declarative state. | Advanced branching strategies (GitFlow), pre-commit hooks. |
| **Logging/Tracing** | Not done | Basic `kubectl logs`. | Fluentd/Promtail log shipping, OpenTelemetry instrumentation. |
| **Security/RBAC** | Surface | Basic secret handling (even if flawed), non-root containers concept. | Sealed Secrets/External Secrets, Network Policies, OPA Gatekeeper. |
| **CI/CD Pipeline** | Not done | CD is handled by ArgoCD. | GitHub Actions CI (build, test, lint, push image). |

---

## Section 2: DEEP CONCEPT NOTES

### 2.1 Kubernetes Fundamentals

#### Liveness vs Readiness vs Startup Probes
- **Explanation:** 
  - *Liveness:* Checks if the container is running and healthy. If it fails, the kubelet restarts the container.
  - *Readiness:* Checks if the container is ready to accept traffic. If it fails, the pod's IP is removed from the Service endpoints.
  - *Startup:* Used for legacy apps that take a long time to start. Disables liveness/readiness checks until it succeeds. (Not used in this repo).
- **Repo Values:**
  - *Backend Liveness:* `GET /health`, initialDelay=20s, period=15s, failureThreshold=3
  - *Backend Readiness:* `GET /ready` (tests DB connection), initialDelay=15s, period=10s
  - *Frontend Liveness:* `GET /healthz`, initialDelay=10s, period=15s
  - *Postgres Liveness:* `exec pg_isready -U appuser -d appdb`, initialDelay=30s, period=20s
- **Interviewer Question:** "What happens if your readiness probe starts failing but liveness is passing?"
- **Great Answer:** "The pod remains running, but Kubernetes removes it from the Service load balancer. Traffic stops routing to that specific pod until the readiness probe passes again. This is perfect for transient issues like a temporary database timeout, as restarting the pod (which liveness would do) wouldn't fix the database issue and would just cause unnecessary churn."

#### Resource Requests vs Limits
- **Explanation:** 
  - *Requests:* What the pod is guaranteed. Used by the scheduler to find a node with enough capacity.
  - *Limits:* The hard cap. If a pod exceeds CPU limits, it is throttled. If it exceeds memory limits, it gets OOMKilled.
- **Repo Values:**
  - *Backend:* req cpu=100m mem=128Mi | limit cpu=500m mem=256Mi
  - *Frontend:* req cpu=50m mem=64Mi | limit cpu=200m mem=128Mi
  - *Postgres:* req cpu=100m mem=128Mi | limit cpu=500m mem=512Mi
  - *QoS Class:* Burstable (since requests < limits and > 0).
- **Interviewer Question:** "Why shouldn't you set CPU limits in production for latency-sensitive apps?"
- **Great Answer:** "Setting CPU limits can lead to CPU throttling due to CFS (Completely Fair Scheduler) quota bugs or bursty traffic, even if the node has available CPU. This causes artificial latency. Often, it's better to rely on Requests for scheduling and let pods use available node CPU, relying on HPA to scale out instead."

#### Scheduler Placement Algorithm
- **Explanation:** The `kube-scheduler` filters nodes that can't run the pod (e.g., inadequate requested resources, node selectors) and scores the remaining nodes to pick the best one.
- **Interviewer Question:** "Does the scheduler look at actual CPU usage or requested CPU?"
- **Great Answer:** "It looks purely at the *requested* CPU of all pods currently assigned to the node, plus the new pod's request. It does not look at real-time actual CPU utilization. This is why setting accurate requests is vital for cluster bin-packing."

#### HorizontalPodAutoscaler (HPA) Internals
- **Explanation:** HPA scales the number of pods in a deployment based on observed metrics (like CPU). 
  - Formula: `desiredReplicas = ceil[currentReplicas * ( currentMetricValue / desiredMetricValue )]`
- **Repo Values:**
  - `minReplicas=2`, `maxReplicas=5`, `targetCPUUtilizationPercentage=60`
  - *ScaleUp:* stabilizationWindow=30s, value=2 pods per 30s
  - *ScaleDown:* stabilizationWindow=180s, value=1 pod per 60s
- **Interviewer Question:** "Why is your scale-down stabilization window longer than scale-up?"
- **Great Answer:** "To prevent 'thrashing' or flapping. If traffic spikes, we want to scale up quickly (30s window). But if traffic dips momentarily, we don't want to immediately kill pods, only to recreate them a minute later. A 180s window ensures the traffic decrease is sustained before we scale down, maintaining stability."

#### PodDisruptionBudget (PDB)
- **Explanation:** Protects applications from *voluntary* disruptions (like node drains, deployments) by ensuring a minimum number of pods remain running. It cannot prevent *involuntary* disruptions (hardware failure, OOMKills, Chaos Mesh eviction).
- **Repo Values:** `minAvailable=1`, selector `app=backend`
- **Interviewer Question:** "If I have 2 replicas and a PDB requiring minAvailable=2, what happens when I drain a node?"
- **Great Answer:** "The drain will block indefinitely. The eviction API respects the PDB, and since killing one pod would drop the available count to 1 (violating the minAvailable=2 rule), it will refuse to evict the pod."

#### RollingUpdate Strategy
- **Explanation:** Ensures zero-downtime deployments by gradually replacing old pods with new ones.
- **Repo Values:** `maxSurge=1`, `maxUnavailable=0`
- **Interviewer Question:** "Walk me through what happens with your settings during a new deployment."
- **Great Answer:** "With maxSurge=1 and maxUnavailable=0 on a 2-replica deployment: K8s creates 1 new pod (total 3). It waits for the new pod's readiness probe to pass. Once ready, it kills 1 old pod (total 2). Then it creates the next new pod (total 3), waits for readiness, and kills the final old pod. Capacity never drops below 100% (2 pods) during the rollout."

#### StatefulSet vs Deployment
- **Explanation:** Deployments are for stateless apps (pods are interchangeable). StatefulSets provide strict guarantees about ordering, uniqueness, and stable network identities, crucial for databases.
- **Repo Values:** Postgres uses a StatefulSet with a hostPath PV. NodeSelector: `kubernetes.io/hostname=minikube`
- **Interviewer Question:** "Why did you use a hostPath on a specific node for Postgres instead of standard dynamic provisioning?"
- **Great Answer:** "Because I am running on a local Minikube cluster without a robust external storage provider. By pinning the pod to a specific node via NodeSelector and using hostPath, I guarantee that if the Postgres pod restarts, it lands on the same node and finds its data. In production (EKS/GKE), I would absolutely use standard StorageClasses (like gp3) and PersistentVolumeClaims, removing the node affinity requirement."

#### TopologySpreadConstraints
- **Explanation:** Controls how pods are distributed across your cluster (e.g., across zones, nodes) for high availability.
- **Repo Values:** `maxSkew=1`, `topologyKey=kubernetes.io/hostname`, `whenUnsatisfiable=ScheduleAnyway`
- **Interviewer Question:** "Why did you use `ScheduleAnyway` instead of `DoNotSchedule`?"
- **Great Answer:** "It's a trade-off. `DoNotSchedule` guarantees perfect anti-affinity, but if I only have 2 nodes and I scale to 3 replicas, the 3rd replica stays pending forever. `ScheduleAnyway` is a soft constraint: it tries its best to spread them across nodes, but prioritizes getting the pod running even if it has to place 2 pods on the same node."

#### TerminationGracePeriodSeconds
- **Explanation:** The time Kubernetes waits between sending a SIGTERM to a container and forcefully killing it with a SIGKILL. Allows the app to finish processing active requests and cleanly close DB connections.
- **Repo Values:** Backend=30s, Frontend=15s, Postgres=60s
- **Interviewer Question:** "Why does Postgres have a longer grace period?"
- **Great Answer:** "Databases need more time to flush dirty pages from memory to disk and cleanly shut down write-ahead logs. Force-killing a database risks data corruption. Frontend apps can die quickly as they just serve static files or proxy requests."

---

### 2.2 Helm Templating

#### Why Helm over Raw Manifests/Kustomize?
Helm provides true templating and packaging. Unlike Kustomize (which is overlay-based patch management), Helm allows for complex logic (`if/else`, loops) and dynamic value injection. It acts as a package manager, versioning the whole configuration as a single deployable artifact.

#### Chart Structure
1. `deployment-backend.yaml`
2. `deployment-frontend.yaml`
3. `statefulset-postgres.yaml`
4. `service-backend.yaml`
5. `service-frontend.yaml`
6. `service-postgres.yaml`
7. `hpa-backend.yaml`
8. `hpa-frontend.yaml`
9. `pdb-backend.yaml`
10. `configmap-app.yaml`
11. `secret-db.yaml`
12. `serviceaccount.yaml`

#### Template Syntax Examples
- `.Values`: `{{ .Values.backend.replicaCount }}` grabs data from values.yaml.
- `quote`: `{{ .Values.env | quote }}` ensures the value is interpreted as a string, avoiding YAML parsing errors for values like "true" or "yes".
- `if`: `{{- if .Values.metrics.enabled }}` conditionally renders blocks. The `-` strips whitespace.

#### Secret Handling (stringData vs data)
- In Helm, creating a Secret with `data` requires you to base64 encode the values via `{{ .Values.dbPassword | b64enc }}`. Using `stringData` allows you to pass plain text, and Kubernetes API handles the base64 encoding automatically.

#### chart version vs appVersion
- `version` in `Chart.yaml`: The version of the Helm chart itself (e.g., infrastructure changes).
- `appVersion`: The version of the underlying application code being deployed.

#### How ArgoCD Renders Helm
ArgoCD doesn't run `helm install`. It runs `helm template` to generate the raw YAML manifests, compares those to what is in the cluster, and applies the differences natively via `kubectl apply`.

---

### 2.3 GitOps / ArgoCD

#### Declarative vs Imperative
Imperative: "Run this command to create a pod" (`kubectl run`).
Declarative GitOps: "Make the cluster look exactly like this Git repository." ArgoCD continuously monitors the repo and reconciles state.

#### Automated, Prune, SelfHeal
- **Automated Sync:** ArgoCD automatically applies changes when Git updates.
- **Prune:** If a file is deleted from Git, ArgoCD deletes the resource from the cluster.
- **SelfHeal:** If someone manually modifies a resource via `kubectl edit`, ArgoCD immediately overrides it back to the Git state.
- **Edge Case:** SelfHeal only applies to resources defined in Git. If someone creates a *brand new* rogue resource via kubectl, ArgoCD ignores it unless configured to track the whole namespace.

#### Finalizers
- **Repo Value:** `resources-finalizer.argocd.argoproj.io`
- **Effect:** If you delete the Application object in ArgoCD, this finalizer ensures that ArgoCD first deletes all the child resources (pods, services, configmaps) before the Application itself is deleted. Without it, the Application is deleted, but the resources are orphaned and left running.

#### pullPolicy=Never and Local Development
Because Minikube is a local cluster, we often build Docker images directly into Minikube's Docker daemon. Setting `imagePullPolicy: Never` forces Kubernetes to use the locally built image instead of trying (and failing) to pull from Docker Hub. 

#### OutOfSync vs Degraded
- **OutOfSync:** The cluster state doesn't match Git (e.g., someone changed Git, but sync hasn't run yet).
- **Degraded:** The resources are synced, but unhealthy in K8s (e.g., a Deployment is CrashLoopBackOff).

#### The Three-Way Merge Diff
ArgoCD compares:
1. The desired state in Git.
2. The live state in Kubernetes.
3. The last applied configuration annotation.
This prevents it from overriding fields injected dynamically by controllers (like node IPs or admission webhook mutations).

---

### 2.4 Observability

#### The Three Pillars
1. **Metrics:** Implemented via Prometheus.
2. **Logs:** Missing (would need Loki/Promtail).
3. **Traces:** Missing (would need Tempo/Jaeger).

#### Prometheus Scrape Annotations
- **How it works:** We add annotations to the Service or Pod:
  `prometheus.io/scrape: "true"`
  `prometheus.io/port: "8000"`
  `prometheus.io/path: "/metrics"`
- The Prometheus operator discovers these annotations via the Kubernetes API and dynamically adds the pod IPs to its scrape targets, hitting `http://<pod-ip>:8000/metrics` every 15 seconds.

#### prometheus_fastapi_instrumentator
This Python library exposes standard RED metrics (Rate, Errors, Duration).
- Rate: Total requests.
- Errors: Total 4xx/5xx responses.
- Duration: Histogram of response times.

#### kube-state-metrics vs node-exporter
- `kube-state-metrics`: Talks to K8s API. Exposes metrics about objects (number of pods pending, HPA status, deployment replicas).
- `node-exporter`: Runs on the Linux node. Exposes hardware/OS metrics (CPU load, memory RAM, disk I/O, network bandwidth).

#### Histogram vs Gauge
- **Gauge:** A value that goes up and down (Current Memory Usage, Active Connections).
- **Histogram:** Buckets of observations (Latency). Used because average latency lies; we need to calculate the 95th percentile (P95) to see the tail latency experienced by users.

#### Retention: 2h
- **Impact:** We can only see data from the last 2 hours. This is fine for a local Minikube lab. In production, we need at least 1-2 weeks to calculate weekly SLOs (Service Level Objectives) and see week-over-week trends.

#### Essential PromQL Queries
1. **CPU Utilization:** `rate(container_cpu_usage_seconds_total{namespace="default"}[5m])`
2. **Error Rate:** `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
3. **HPA Replicas:** `kube_hpa_status_current_replicas`
4. **Pod Restarts:** `changes(kube_pod_container_status_restarts_total[1h])`
5. **Readiness:** `kube_pod_status_ready{condition="true"}`
6. **Memory Usage:** `container_memory_working_set_bytes`

#### Grafana Debugging Workflow
1. Look at RED metrics (Are errors spiking? Is latency high?).
2. Check Infrastructure Dashboards (Are nodes out of CPU? Are pods OOMKilling?).
3. Check K8s Events (Are pods CrashLooping or Pending?).

---

### 2.5 Chaos Engineering

#### Philosophy
Testing is verifying what you *know* (assertions). Chaos engineering is exploring what you *don't know* (injecting failures to reveal emergent systemic weaknesses).

#### Chaos Mesh vs Kubectl Delete
`kubectl delete pod` is graceful (sends SIGTERM, waits). Chaos Mesh often uses the Eviction API or direct container killing, which accurately mimics sudden node deaths and tests how the system handles ungraceful termination and PDB adherence.

#### Experiment 1: pod-kill.yaml
- **Hypothesis:** If a backend pod dies randomly, the system will maintain availability, and K8s will spin up a replacement within 60 seconds.
- **Blast Radius:** Limited to `app=backend` pods in the `default` namespace. 1 pod killed every 2 minutes.
- **Result:** Success. Traffic routes to the remaining replica. K8s schedules a new pod, which passes readiness in ~15-20s.

#### Proposed Experiment 2: Network-Delay
- **Hypothesis:** Adding 500ms latency between frontend and backend will trigger HPA scale-up due to thread starvation and increased CPU/memory usage, but the app won't crash.
- **Tests:** Timeout configurations, circuit breaker efficacy.

#### Proposed Experiment 3: CPU-Stress
- **Hypothesis:** Burning CPU on a backend pod will trigger the HPA to scale out before the app becomes completely unresponsive.
- **Tests:** HPA stabilization windows and scale-up speed.

#### Blast Radius Controls in this setup
1. Namespace scoping.
2. Label selectors (`app=backend`).
3. `mode: one` (only affects one pod at a time, not all).
4. Cron scheduling (predictable windows).
5. Pause/Delete annotations via GitOps to stop it.

#### MTTR Measurement Methodology
- **Start Clock:** Timestamp when Chaos Mesh injects the fault (pod goes down).
- **End Clock:** Timestamp when the new pod's readiness probe returns 200 OK and it enters the Service endpoints.

---

### 2.6 Resilience Patterns and MTTR

#### MTTR Breakdown
Total MTTR for pod-kill: ~45 seconds.
1. Detection (kubelet notices container exit): ~1-2s.
2. Scheduling (ReplicaSet creates new Pod, Scheduler assigns node): ~3-5s.
3. Image Pulling (Minikube cache, so nearly instant): ~1s.
4. App Startup (Python Uvicorn boots): ~2s.
5. Readiness Probe (initialDelaySeconds=15s, runs, passes): ~15s.
*Bottleneck:* The 15s initialDelay on readiness. We could optimize this by reducing it to 5s, bringing MTTR down to ~25s.

#### MTTD (Mean Time To Detection)
Currently, MTTD is poor because we rely on looking at Grafana. Fixing this requires configuring Alertmanager with rules (e.g., `alert: HighErrorRate`) sending webhooks to Slack/PagerDuty.

#### Blameless Postmortem Format
1. **Incident Summary:** What happened, when, severity.
2. **Timeline:** Exactly what happened down to the minute.
3. **Root Cause:** The underlying technical reason (The "5 Whys").
4. **Impact:** User-facing effects.
5. **Action Items:** Preventive measures.

#### Sample Incident Timeline (Fabricated for Pod-Kill)
- 10:00:00 - Chaos Mesh executes `pod-kill` on `backend-abc`.
- 10:00:02 - Active connections to `backend-abc` drop (502 Bad Gateway).
- 10:00:05 - ReplicaSet notices desired=2, current=1. Creates `backend-xyz`.
- 10:00:10 - `backend-xyz` container is running.
- 10:00:25 - Readiness probe passes. Traffic resumes full capacity.
- *Action Item:* Implement retries on the Frontend NGINX proxy to mask the 502 errors during the 2-second drop window.

#### Error Budget
If our SLO is 99.9% uptime, we have ~43 minutes of allowed downtime per month. That 43 minutes is the "Error Budget". We use it to run chaos experiments or push risky deployments. If we exhaust it, we freeze features and focus on reliability.

---

## Section 3: WEAK-SPOT FLAGS

When interviewing, be preemptively honest about shortcuts taken for the local lab environment.

### 1. DB Password in values.yaml (`Ch4ng3Me!GitOps`)
- **Interviewer:** "I see you committed a database password in plaintext to Git. Is this how you'd do it in production?"
- **Say:** "Absolutely not. This is a known shortcut for this local lab to keep the setup self-contained. In production, I would use External Secrets Operator to sync credentials from AWS Secrets Manager or HashiCorp Vault, or use Sealed Secrets to encrypt them before committing to Git."

### 2. Only `pod-kill.yaml` committed
- **Interviewer:** "Your README mentions multiple chaos experiments, but I only see pod-kill."
- **Say:** "I started with pod-kill to establish a baseline for measuring MTTR. My next iterations, which I've designed but haven't committed, involve network latency injection to test timeouts, and CPU stress to validate the HPA tuning."

### 3. No CI Pipeline
- **Interviewer:** "You have CD with Argo, but where is your CI?"
- **Say:** "To focus deeply on Kubernetes and GitOps primitives, I mocked the CI side. A production setup would use GitHub Actions to run linting, pytest, build the Docker image, scan it with Trivy, push it to ECR, and then automatically update the `appVersion` tag in the Helm chart to trigger ArgoCD."

### 4. Prometheus Retention 2h
- **Interviewer:** "Why is retention only 2 hours?"
- **Say:** "Resource constraints on Minikube. Storing TSDB data locally consumes disk space fast. In a real environment, I'd set it to 15 days locally, and use Thanos or Cortex for long-term S3-backed storage."

### 5. Grafana Password `admin`
- **Interviewer:** "Grafana uses a default password."
- **Say:** "Yes, for local access ease. Production would use OAuth2/OIDC integration (like GitHub or Google Workspace SSO) and disable basic auth entirely."

### 6. topologySpreadConstraints: ScheduleAnyway
- **Interviewer:** "Why soft anti-affinity?"
- **Say:** "Minikube is often a single or 2-node cluster. Using a hard constraint (`DoNotSchedule`) would prevent pods from scheduling entirely if scaling beyond the node count. In AWS, spreading across 3 AZs, I would use `DoNotSchedule`."

### 7. Single Postgres Replica
- **Interviewer:** "Is this database highly available?"
- **Say:** "No, it's a single StatefulSet replica with a hostPath. It's a massive SPOF. In production, I would not run DBs in K8s if I could avoid it—I'd use a managed service like AWS RDS Multi-AZ. If I had to run it in K8s, I'd use an operator like Zalando Postgres Operator for clustering, leader election, and streaming replication."

### 8. Frontend has no HPA
- **Interviewer:** "Why does the backend scale but not the frontend?"
- **Say:** "The backend Python app is doing heavy compute/DB connections and is the bottleneck. The NGINX frontend is extremely lightweight. However, for a complete architecture, I should add HPA for the frontend based on CPU or network ingress."

---

## Section 4: ADJACENT CONCEPTS (Beyond the Repo)

### Minikube → EKS/GKE Migration Table

| Component | Minikube Setup | EKS / GKE Production Setup |
| :--- | :--- | :--- |
| **Ingress** | NodePort or minikube tunnel | AWS ALB Ingress Controller / NGINX Ingress with Route53 |
| **Storage** | `hostPath` PV | EBS CSI Driver (`gp3` StorageClass) / GCE PD |
| **Secrets** | Plain Secret in Helm | AWS Secrets Manager + External Secrets Operator |
| **Nodes** | Local VMs | Managed Node Groups or Karpenter / Autopilot |
| **Registry** | Local Docker daemon (`Never`) | ECR / GCR (`Always` or `IfNotPresent`) |

### Argo Rollouts
Standard K8s RollingUpdates (used here) replace pods slowly. Argo Rollouts enables:
- **Blue-Green:** Spinz up v2 alongside v1, flips traffic 100% instantly when tests pass.
- **Canary:** Routes 5% of traffic to v2, analyzes Prometheus metrics, and automatically promotes to 100% or rolls back if error rates spike.

### Service Meshes (Istio / Linkerd)
What would this add?
- **mTLS:** Encrypted traffic between NGINX and FastAPI.
- **Advanced Routing:** Retries on 502s, circuit breaking to prevent cascading failures.
- **Rich Metrics:** L7 metrics without needing code-level Prometheus instrumentation.

### HPA vs VPA vs Cluster Autoscaler
- **HPA:** Adds *more* pods.
- **VPA (Vertical):** Makes existing pods *bigger* (increases CPU/Mem requests). Conflicts with HPA on CPU metrics; usually, you use VPA to find baseline requests, and HPA to scale.
- **Cluster Autoscaler (Karpenter):** Adds *more nodes* to the cluster when pods are stuck in `Pending` due to lack of resources.

---

## Section 5: QUICK REVISION TABLE

Memorize these values. If asked "How is your HPA configured?", recite these exactly.

| Concept / Setting | Value in This Repo | Why That Value | What Changes in Production |
| :--- | :--- | :--- | :--- |
| Backend CPU Limit | `500m` | Prevents a rogue process from starving the node. | Might remove limits entirely to prevent throttling latency. |
| Backend Mem Request | `128Mi` | Baseline for Python/Uvicorn to start. | Profiled via actual usage metrics over 1 week. |
| DB Mem Limit | `512Mi` | Protects cluster from DB memory leaks. | Much higher, likely 4GB+, based on shared_buffers config. |
| HPA Target CPU | `60%` | Leaves 40% headroom for sudden bursts while new pods spin up. | Might lower to 50% for bursty traffic, or use custom metrics (RPS). |
| HPA Min Replicas | `2` | Minimum required for HA and zero-downtime rolling updates. | `3`, one for each Availability Zone. |
| HPA Max Replicas | `5` | Caps costs and protects DB from max_connection exhaustion. | Based on load testing and DB connection pool limits. |
| HPA Scale Up Window | `30s` | Reacts quickly to sudden traffic spikes. | Same or faster (down to 15s) depending on app boot time. |
| HPA Scale Down Window | `180s` | Prevents rapid thrashing when traffic fluctuates. | `300s` (5m) to ensure traffic drop is permanent. |
| PDB minAvailable | `1` | Ensures at least 1 pod is always up during voluntary node drains. | `50%` or `minAvailable: 2` depending on scale. |
| Rolling maxSurge | `1` | Creates 1 new pod before killing an old one. | `25%` for larger deployments to speed up rollouts. |
| Rolling maxUnavail | `0` | Ensures capacity never drops below 100% during updates. | Same, critical for zero downtime. |
| Liveness initialDelay | `20s` (Backend) | Gives app time to start before kubelet shoots it. | Tuned tightly based on 99th percentile startup times. |
| Liveness period | `15s` | Balances fast detection with low API overhead. | Same. |
| Readiness initialDelay | `15s` | Waits for DB connection pool to establish. | Optimized to be as fast as possible to reduce MTTR. |
| Readiness endpoint | `/ready` | Specific route checking DB, not just app server state. | Deep health checks testing downstream APIs and queues. |
| TermGracePeriod | `30s` (Backend) | Allows active HTTP requests to finish. | Depends on max request timeout. |
| TermGracePeriod (DB) | `60s` (Postgres) | Allows safe flushing of WAL and memory to disk. | `120s+` to prevent catastrophic data corruption. |
| topSpread maxSkew | `1` | Forces pods to be spread evenly across domains. | Same. |
| topSpread Key | `kubernetes.io/hostname` | Spreads across physical nodes (Minikube). | `topology.kubernetes.io/zone` for multi-AZ spreading. |
| ArgoCD Sync | `Automated` | Applies changes instantly. | Same for Dev/Staging. Maybe manual sync for Prod initially. |
| ArgoCD Prune | `true` | Cleans up deleted resources. | Same. |
| ArgoCD SelfHeal | `true` | Reverts manual kubectl tampering. | Same, enforces strict GitOps. |
| Image Pull Policy | `Never` | Uses local Minikube docker cache. | `IfNotPresent` or `Always` with strict sha256 image digests. |
| Uvicorn Workers | `1` | Container philosophy: 1 process per container, scale via K8s replicas. | Same. HPA handles concurrency, not Gunicorn/Uvicorn workers. |
| Prom Retention | `2h` | Saves local disk space on developer machine. | `15d` local, infinite in S3 via Thanos/Cortex. |
| DB Password | `values.yaml` (Plain) | Shortcut for local lab simplicity. | SealedSecrets or AWS Secrets Manager. |
| MTTR | `~30-60s` | Baseline achieved via probe tuning and replica configs. | Aim for < 10s with optimized probes, caching, and fast images. |
| Chaos Mesh mode | `one` | Kills a single pod per schedule. | Used in game days, occasionally randomized in prod (Chaos Monkey). |

---
*Document prepared for Chaos-Engineered Self-Healing GitOps Platform interview study.*
