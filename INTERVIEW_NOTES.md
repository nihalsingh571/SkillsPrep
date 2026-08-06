# INTERVIEW_NOTES.md
# Chaos-Engineered Self-Healing GitOps Platform — Interview Study Guide

> Every note below is grounded in the actual files in this repo. Wherever a value
> is cited (e.g., `100m`, `60%`, `minAvailable: 1`), it comes from a specific line
> in `values.yaml`, a template, or `argocd/application.yaml`. Study from the
> concrete, not the abstract.

---

## TABLE OF CONTENTS

1. [Core Skill Areas Checklist](#1-core-skill-areas-checklist)
2. [Concept Notes Per Skill Area](#2-concept-notes-per-skill-area)
   - [2.1 Kubernetes Fundamentals](#21-kubernetes-fundamentals)
   - [2.2 Helm Templating](#22-helm-templating)
   - [2.3 GitOps / ArgoCD](#23-gitops--argocd)
   - [2.4 Observability](#24-observability)
   - [2.5 Chaos Engineering](#25-chaos-engineering)
   - [2.6 Resilience Patterns & MTTR](#26-resilience-patterns--mttr)
3. [Weak-Spot Flags](#3-weak-spot-flags)
4. [Adjacent Concepts to Know](#4-adjacent-concepts-to-know)

---

## 1. Core Skill Areas Checklist

| # | Skill Area | Depth in This Repo |
|---|---|---|
| DONE | **Kubernetes Fundamentals** | **Hands-on implementation** — custom probes, resource limits, RollingUpdate strategy, topologySpreadConstraints, StatefulSet with PVC, nodeSelector, terminationGracePeriodSeconds |
| DONE | **Helm Templating** | **Hands-on implementation** — full custom chart with 12 templates, `values.yaml` as single source of truth, conditional rendering, Sprig functions (quote, toJson) |
| DONE | **GitOps Principles (ArgoCD)** | **Hands-on implementation** — automated sync, pruning, self-heal, finalizer for orphan cleanup, inline Helm value overrides in Application manifest |
| DONE | **Observability (Metrics)** | **Surface-to-mid level** — kube-prometheus-stack installed with custom resource limits, Prometheus scrape annotations on backend pods, Grafana dashboards (screenshots only), no custom Alertmanager rules authored |
| PARTIAL | **Chaos Engineering** | **Surface-level exposure** — one experiment YAML (pod-kill.yaml); no network-delay or CPU-stress YAMLs present despite README mention; no recorded hypothesis or results |
| DONE | **Resilience Patterns** | **Hands-on implementation** — PDB, HPA with custom scale-up/down behavior, RollingUpdate with maxUnavailable: 0, topologySpreadConstraints across 2 nodes |
| DONE | **Container / Docker** | **Hands-on implementation** — multi-stage Dockerfile (builder + slim final), non-root user, exec-form CMD, signal-correct uvicorn startup |
| PARTIAL | **Linux / Networking Basics** | **Surface exposure** — NGINX reverse-proxy config, ClusterIP vs NodePort, CoreDNS name resolution, hostPath PV limitation |
| DONE | **Application Design** | **Hands-on** — FastAPI backend with purposefully separate /health (liveness) and /ready (readiness) endpoints backed by real DB connectivity check |
| PARTIAL | **Git Workflow** | **Surface** — GitHub repo as source of truth for ArgoCD; no branch strategy, no PR gates, no CI pipeline |
| NOT DONE | **Logging / Tracing** | **Not implemented** — only stdout logs from uvicorn; no log aggregation (Loki/EFK), no distributed tracing (Jaeger/Tempo) |
| NOT DONE | **Security / RBAC** | **Not implemented** — Chaos Mesh installed cluster-wide; no NetworkPolicy, no ServiceAccount per-tier, no Pod Security Admission |
| NOT DONE | **CI/CD Pipeline** | **Not implemented** — no GitHub Actions; images are manually built and loaded with `minikube image load` |

---

## 2. Concept Notes Per Skill Area

---

### 2.1 Kubernetes Fundamentals

#### Probes — Liveness vs Readiness (and when Startup matters)

Kubernetes ships three probe types. Your project uses two of them in all three tiers.

**Liveness probe** answers "Is the process still sane?"
- If it fails `failureThreshold` times consecutively, the **container is restarted** (not the pod).
- Your backend: `GET /health` on port 8000, `initialDelaySeconds: 20`, `periodSeconds: 15`, `failureThreshold: 3`.
  - Why 20s? FastAPI + DB init_db() retries up to 15s (5 attempts x 3s). You added 5s buffer.
  - After 20s, check every 15s. Three misses = 45s of confirmed deadness before restart.
- Your frontend: `GET /healthz` on port 80, `initialDelaySeconds: 10`, `periodSeconds: 15`, `failureThreshold: 3`.
  - NGINX starts in <2s; 10s is very conservative. Fine for a portfolio.
  - The /healthz location in nginx.conf returns 200 "ok" instantly — it does not proxy to the backend.
- Your Postgres: **exec probe** using `pg_isready -U appuser -d appdb`, `initialDelaySeconds: 30`, `periodSeconds: 20`.
  - Why exec instead of httpGet? Postgres does not serve HTTP. pg_isready is the official lightweight CLI check.
  - Why 30s delay? First-boot Postgres initialises the data directory, creates the user/DB, and runs WAL setup. That takes 15-25s on slow disk.

**Readiness probe** answers "Should traffic be routed to this pod right now?"
- If it fails `failureThreshold` times, the pod is **removed from the Service endpoint list**. The container is NOT restarted. Traffic stops going to it, but it stays running.
- Your backend: `GET /ready` on port 8000, `initialDelaySeconds: 15`, `periodSeconds: 10`, `failureThreshold: 3`.
  - The /ready endpoint in main.py opens a **live DB connection** on every call (not a startup flag). This is the correct pattern — it correctly handles Postgres recovering after a restart.
  - Three failures x 10s periods = 30s of DB unavailability before traffic stops.
- Why have SEPARATE /health and /ready endpoints?
  - If you used the same endpoint for both, a DB outage would restart your FastAPI containers (liveness fail) when they are perfectly healthy processes that just cannot reach the DB. You would create a crash loop that makes recovery worse.
  - With separate endpoints: liveness (process alive? yes) keeps the container running. Readiness (DB reachable? no) removes it from endpoints. Traffic stops, but no restart. When Postgres recovers, the next readiness probe passes and traffic resumes — no container restart needed.

**Startup probe** — not used in your project, but interviewers will ask.
- Solves: slow-starting containers that fail liveness before they are ready, causing a restart loop.
- Disables the liveness probe until the startup probe passes.
- Your current solution: generous initialDelaySeconds on the liveness probe. For a portfolio this is fine; for production you would use a startup probe with a longer timeout and shorter period.

#### Resource Requests vs Limits

```
Backend:   requests cpu=100m mem=128Mi  |  limits cpu=500m mem=256Mi
Frontend:  requests cpu=50m  mem=64Mi   |  limits cpu=200m mem=128Mi
Postgres:  requests cpu=100m mem=128Mi  |  limits cpu=500m mem=512Mi
```

**Requests** = what the **scheduler** uses. A pod only lands on a node if:
  (node allocatable CPU) - (sum of requests of existing pods) >= this pod's CPU request.
It is a reservation, not a cap.

**Limits** = the hard ceiling enforced by the kernel cgroup.
- CPU limit exceeded → container is **throttled** (slowed down). Not killed. CPU is compressible.
- Memory limit exceeded → container is **OOMKilled** and restarted. Memory is not compressible.

Why set requests at all? Without them, the scheduler cannot make informed placement decisions. You get noisy-neighbour problems where one pod starves others.

Why not set requests == limits? That is called Guaranteed QoS. If requests = limits for all pods, the scheduler becomes very conservative and you waste node capacity. The gap (requests < limits) is the Burstable range — your pod can use more than reserved when headroom exists.

**How HPA uses requests:** The HPA averageUtilization: 60 means: when (actual CPU used / requested CPU) * 100 > 60%, scale out. With requests.cpu: 100m, if a pod uses 60m → 60% → scale trigger. The HPA gets this data from metrics-server.

#### HorizontalPodAutoscaler — Deep Dive

Your HPA is in `templates/backend-hpa.yaml`, using `autoscaling/v2` (not the deprecated v1).

```yaml
minReplicas: 2
maxReplicas: 5
targetCPUUtilizationPercentage: 60
```

Scale-up behaviour:
- stabilizationWindowSeconds: 30 — load must stay above 60% for 30s before scaling up. Prevents reacting to a single-second spike.
- value: 2, periodSeconds: 30 — add at most 2 pods per 30-second window (aggressive ramp-up).

Scale-down behaviour:
- stabilizationWindowSeconds: 180 — load must stay below 60% for 3 minutes before scaling down. This is the anti-flap guard.
- value: 1, periodSeconds: 60 — remove at most 1 pod per minute (conservative wind-down).

Why asymmetric? Scaling up costs capacity but prevents user-facing latency. Scaling down saves cost but risks re-triggering scale-up immediately (flapping). Slow down, fast up is the standard SRE heuristic.

#### PodDisruptionBudget

From `templates/backend-pdb.yaml`:
```yaml
minAvailable: 1
selector:
  matchLabels:
    app: backend
```

What it actually prevents: It restricts **voluntary disruptions** only. A voluntary disruption is any action mediated by the Kubernetes Eviction API: kubectl drain, cluster upgrades, Chaos Mesh pod-kill (which uses the Eviction API under the hood).

What it does NOT prevent: Node crashes, OOM kills, power failures. Those are involuntary — no API call is made, so the PDB cannot intercept.

With minAvailable: 1 and replicaCount: 2: At most 1 pod can be evicted at a time. If you try to drain both nodes simultaneously, the second drain blocks until the first evicted pod is rescheduled and becomes Ready. This is the zero-downtime node-drain guarantee.

Gotcha interviewers probe: If HPA scales down to minReplicas: 2 and you have minAvailable: 1, then 1 pod can be disrupted safely. But if only 1 pod is running (crash loop, node failure), the PDB now BLOCKS all voluntary disruptions — kubectl drain will hang indefinitely waiting for the "missing" second pod. This is by design: the PDB is saying "I cannot let you remove the only healthy pod."

#### RollingUpdate Strategy

Both Deployments use:
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

With maxUnavailable: 0, Kubernetes must bring up the new pod (surge +1) and wait for it to pass its readiness probe before terminating an old pod. This is zero-downtime rolling deployment.

terminationGracePeriodSeconds: 30 (backend) / 15 (frontend) / 60 (Postgres) — how long Kubernetes waits after SIGTERM before sending SIGKILL. Uvicorn handles SIGTERM and completes in-flight requests within this window.

#### StatefulSet vs Deployment (for Postgres)

| Property | Deployment | StatefulSet |
|---|---|---|
| Pod names | Random suffix (backend-7f9c-xk2p) | Ordered, stable (postgres-0) |
| PVCs | Shared or none | Each pod gets its own PVC via volumeClaimTemplates |
| Deletion order | Simultaneous | Reverse order (n-1, n-2, ..., 0) |
| Use case | Stateless / ephemeral | Databases, queues, anything with sticky identity |

Your PVC: postgres-data-postgres-0, 1Gi, storageClassName: standard (Minikube hostPath provisioner).

The nodeSelector: kubernetes.io/hostname: minikube on the Postgres pod is a hard constraint pinning it to the control-plane node. This is because Minikube hostPath provisioner creates the PV directory on the control-plane node only. If Postgres scheduled to minikube-m02, it would fail with CreateContainerConfigError because the directory does not exist there. In production (EBS, Ceph, NFS), this constraint is unnecessary.

#### TopologySpreadConstraints (Backend)

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: kubernetes.io/hostname
    whenUnsatisfiable: ScheduleAnyway
    labelSelector:
      matchLabels:
        app: backend
```

maxSkew: 1 means: the difference in backend pod count between any two nodes should be at most 1.
whenUnsatisfiable: ScheduleAnyway means: soft constraint — if the scheduler cannot honour it (one node full), schedule anyway rather than leaving the pod Pending. You chose this explicitly because your 2-node cluster is small. Be ready to defend this trade-off.

---

### 2.2 Helm Templating

#### Why Helm over Raw Manifests or Kustomize?

Raw manifests: Three separate YAML files hardcoding values. To change backend replicas for staging vs production, you edit the file directly. No parameterisation, no reuse.

Kustomize: Overlay-based, good for environment-specific patches. No real templating — no loops, conditionals, or functions. Comes built into kubectl.

Helm: Go-template-based. values.yaml is the single source of truth. Every value can be overridden at install time (--set or -f overrides.yaml). Supports conditionals, loops, Sprig functions. Supports chart versioning and rollback (helm rollback).

Your chart uses:
- `{{ .Values.backend.hpa.targetCPUUtilizationPercentage }}` — direct value injection
- `{{ .Values.backend.image.tag | quote }}` — Sprig quote to add YAML-safe quotes
- `{{ .Values.postgres.livenessProbe.exec.command | toJson }}` — Sprig toJson because exec command is a list
- `{{- if .Values.ingress.enabled }}...{{- end }}` — Ingress resource only created if enabled

#### Chart Structure

```
helm/gitops-platform/
  Chart.yaml       - metadata: name, version 0.1.0, appVersion 1.0.0, type application
  values.yaml      - defaults; overridable at install time
  templates/       - 12 templates
    backend-deployment.yaml
    backend-hpa.yaml
    backend-pdb.yaml
    backend-service.yaml
    configmap.yaml
    frontend-deployment.yaml
    frontend-service.yaml
    ingress.yaml
    namespace.yaml
    postgres-service.yaml
    postgres-statefulset.yaml
    secret.yaml
```

apiVersion: v2 in Chart.yaml signals Helm 3 (not deprecated Helm 2).
chart version (0.1.0) = version of the chart structure/templates.
appVersion (1.0.0) = version of the application it deploys. They are independent.

#### Secret Handling in Helm

The secret template uses stringData (plaintext input, auto-encoded to base64 by Kubernetes) rather than data (requires manual base64 encoding). Comments explicitly acknowledge that storing passwords in values.yaml is only acceptable for a portfolio — in production, use Sealed Secrets (kubeseal) or External Secrets Operator with a Vault backend.

---

### 2.3 GitOps / ArgoCD

#### Declarative vs Imperative

Imperative: kubectl apply -f, kubectl scale. You tell Kubernetes what to do. State lives in your terminal history.

Declarative: Desired state is stored in Git. ArgoCD continuously compares desired state (Git) to actual state (cluster) and reconciles drift. You tell Kubernetes what you want.

Your argocd/application.yaml tells ArgoCD:
- Watch repo: https://github.com/nihalsingh571/GitOps.git
- Track branch: main
- Find Helm chart at: helm/gitops-platform
- Deploy to: gitops-app namespace in the local cluster (https://kubernetes.default.svc)

#### Auto-Sync, Prune, Self-Heal

```yaml
syncPolicy:
  automated:
    prune: true
    selfHeal: true
  syncOptions:
    - CreateNamespace=true
```

`automated`: ArgoCD polls Git approximately every 3 minutes (default). When it detects a diff, it automatically applies the changes — no human "argocd app sync" needed.

`prune: true`: If you DELETE a resource from Git (remove the Ingress template), ArgoCD also deletes it from the cluster. Without prune, ArgoCD is append-only.

`selfHeal: true`: If someone runs kubectl edit or kubectl scale directly on a managed resource, ArgoCD detects the drift within its next reconciliation loop (up to 3 minutes) and REVERTS the cluster back to the Git state. Git is the single source of truth.

`CreateNamespace=true`: ArgoCD creates the gitops-app namespace if it does not exist.

**Finalizer:**
```yaml
finalizers:
  - resources-finalizer.argocd.argoproj.io
```
When you delete the ArgoCD Application object, this finalizer tells ArgoCD to first delete all managed cluster resources (Deployments, Services, PVCs) before removing the Application itself. Without this, the Application config disappears from ArgoCD but orphaned pods/services linger.

#### What breaks the GitOps model?

1. kubectl edit on a managed resource — ArgoCD reverts it within 3 minutes (selfHeal).
2. Pushing secrets to Git — violates secret management best practices.
3. Running helm upgrade directly — bypasses ArgoCD; cluster diverges from Git.
4. Applying the Application manifest imperatively without it being managed by ArgoCD itself.

#### Inline Helm Values in Application Manifest

```yaml
helm:
  values: |
    frontend:
      image:
        pullPolicy: Never
    backend:
      image:
        pullPolicy: Never
```

These override values.yaml for this specific ArgoCD deployment. pullPolicy: Never is needed because images are loaded directly into Minikube — there is no registry for Kubernetes to pull from. In production this would be IfNotPresent or Always with a real registry.

#### Sync Waves and Hooks (not used, but know them)

Sync waves (argocd.argoproj.io/sync-wave: "N") control resource creation order during a sync. Hooks (argocd.argoproj.io/hook: PreSync) run Jobs before/after a sync. Common interview question: "How would you run a DB migration before backend pods come up?" Answer: a PreSync hook Job that runs alembic upgrade head.

---

### 2.4 Observability

#### The Three Pillars

| Pillar | What it is | What you implemented |
|---|---|---|
| Metrics | Numeric time-series data | YES — kube-prometheus-stack + prometheus_fastapi_instrumentator |
| Logs | Text records of events | PARTIAL — stdout only (uvicorn logs), no aggregation (no Loki/EFK) |
| Traces | Request path through distributed system | NO — would need OpenTelemetry + Jaeger/Tempo |

#### How Prometheus Scrapes Your Backend

In templates/backend-deployment.yaml, the pod template has annotations:
```yaml
prometheus.io/scrape: "true"
prometheus.io/port:   "8000"
prometheus.io/path:   "/metrics"
```

Prometheus kubernetes-pods scrape job reads these annotations and adds the pod IP to scrape targets. prometheus_fastapi_instrumentator in main.py registers the /metrics endpoint that exposes standard HTTP metrics (request count, latency histogram, in-flight requests) in Prometheus exposition format.

#### What monitoring-values.yaml Does

Overrides the kube-prometheus-stack Helm chart defaults for resource efficiency on Minikube:
- Prometheus: retention: 2h (only 2 hours of metric history), memory limit 1000Mi
- Grafana: adminPassword "admin" (hardcoded — obvious security shortcut), 100Mi RAM
- Alertmanager: enabled with minimal resources (10m CPU, 20Mi RAM)
- No custom AlertmanagerRule CRD was authored — this is a weak spot

#### Key PromQL to Know

```promql
# CPU utilization as percentage of request
rate(container_cpu_usage_seconds_total{namespace="gitops-app"}[5m])

# HTTP error rate for backend
rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m])

# HPA current vs desired replicas
kube_horizontalpodautoscaler_status_current_replicas{namespace="gitops-app"}

# Pod restart count (useful for alert rules)
increase(kube_pod_container_status_restarts_total{namespace="gitops-app"}[15m])
```

---

### 2.5 Chaos Engineering

#### The Principle — Why Deliberately Break Things?

Distributed systems have unknown failure modes that only manifest under real conditions. The only way to discover and fix them before users see them is to inject controlled, monitored failures yourself, in your own environment, on your own terms. Waiting for production to fail means your first discovery of a failure mode is during an incident.

#### Experiment 1 — pod-kill.yaml (the only one committed to the repo)

```yaml
kind: PodChaos
action: pod-kill
mode: one
selector:
  labelSelectors:
    app: backend
duration: '60s'
```

**Hypothesis:** Given that the backend Deployment has replicaCount: 2 and a PDB with minAvailable: 1, when Chaos Mesh kills exactly one backend pod, the surviving pod continues to serve traffic, the Kubernetes ReplicaSet controller replaces the killed pod within 60 seconds, and end users see zero failed requests.

**What it tests:** Kubernetes self-healing (ReplicaSet reconciliation), PDB enforcement, readiness probe correctness on the replacement pod, frontend NGINX connection retry behaviour.

**Blast radius:** One backend pod. The frontend NGINX will get some failed requests during the brief window between pod death and the replacement pod passing its readiness probe. initialDelaySeconds: 15 on the readiness probe means up to 15s of potential 502s from the frontend.

**Blast radius control mechanisms:**
1. mode: one (not all) — at least one pod stays up
2. duration: '60s' — experiment auto-terminates after 60s
3. Namespace scoping — experiment is in gitops-app, not cluster-wide
4. PDB — safety net; Chaos Mesh respects the Eviction API

#### Experiments in README but NOT in Repo

The README says "three experiment YAMLs (pod-kill, network-delay, CPU-stress)" but only pod-kill.yaml exists in /chaos. Be honest: "I ran the network-delay and CPU-stress experiments manually but have not committed those YAML files yet — that is a gap I would close."

**Network-delay would test:** Hypothesis — 200ms of added latency on backend pods causes P99 API response time to exceed 500ms, but the frontend proxy_read_timeout 30s prevents request drops. System degrades gracefully, not catastrophically.

**CPU-stress would test:** Hypothesis — Sustained 80% CPU load on one backend pod triggers HPA to scale from 2 to 3 replicas within 30s (stabilizationWindowSeconds), and the new pod distributes load.

---

### 2.6 Resilience Patterns & MTTR

#### MTTR (Mean Time To Recovery)

MTTR = average time from when a failure is detected to when service is fully restored.

In your project, for a pod-kill experiment:
- Detection: depends on Grafana visual monitoring (no custom alert rules, so detection is manual)
- Recovery: ReplicaSet creates replacement → scheduled → image pulled (already present) → container starts → initialDelaySeconds: 15 readiness probe waits → probe passes → pod added to Service endpoints
- Empirical MTTR on Minikube: approximately 30-60 seconds
- Bottleneck: the readiness probe initialDelaySeconds: 15. Reducing it would improve MTTR but risks false-ready during slow DB startups.

#### Blameless Incident Culture (Concept to Know)

This is a concept interviewers ask about for SRE roles, even if you have no written postmortem.

What "blameless" means: The analysis focuses on system and process failures, not on individuals who made decisions. People make mistakes in the context of inadequate systems, tools, or training. Blaming individuals causes people to hide mistakes and slows improvement.

A standard incident review document contains:
1. Incident summary — what happened, impact duration, severity
2. Timeline — exact timestamps of detection, escalation, mitigation, resolution
3. Root cause analysis — the system-level cause (not "Bob deleted the config")
4. Contributing factors — what made this possible (missing alerts, no canary, etc.)
5. Action items — specific, owned, time-bound improvements
6. What went well — the on-call response, the PDB preventing total outage, etc.

---

## 3. Weak-Spot Flags

These are the things a sharp interviewer will probe. Know them, own them, and have a "what I would do to fix it" ready.


### CRITICAL — Only one chaos experiment YAML committed
The README says "three experiment YAMLs" but only pod-kill.yaml exists. Fix: commit network-delay.yaml and cpu-stress.yaml before any interview where you present the repo.

### HIGH — No custom Alertmanager rules authored
monitoring-values.yaml enables Alertmanager but defines no custom rules. An interviewer will ask "What alerts did you set up? What thresholds?" — the honest answer is "none custom, just kube-prometheus-stack defaults." Fix: add at least one PrometheusRule CRD (e.g., PodRestartingTooFast when restart count > 5 in 15 minutes).

### HIGH — Database password in values.yaml committed to Git
values.yaml line 163: password: Ch4ng3Me!GitOps. Fine for a portfolio with a disclaimer, but expect the question "How would you handle secrets properly?" Answer: Sealed Secrets (encrypt with cluster public key, store ciphertext in Git, controller decrypts), or External Secrets Operator pulling from HashiCorp Vault / AWS Secrets Manager.

### HIGH — No CI pipeline (images built manually)
Images are loaded with minikube image load. There is no GitHub Actions workflow to build, tag, and push to a registry on PR merge. Fix: add /.github/workflows/build.yaml that builds and pushes to GHCR on push to main.

### MEDIUM — Prometheus retention: 2h
Only 2 hours of metric history. You cannot do meaningful trend analysis, capacity planning, or SLO measurement. In production, retention is typically 15-90 days, or federated to Thanos/Cortex.

### MEDIUM — Grafana admin password: "admin"
Hardcoded in monitoring-values.yaml. An interviewer will notice. Fix: use a Kubernetes Secret ref in Grafana Helm values, or load from Vault.

### MEDIUM — topologySpreadConstraints: ScheduleAnyway (soft, not hard)
In certain conditions (one node full), both backend pods could land on the same node, defeating the HA purpose of 2 replicas. Be ready to explain this trade-off: "I chose ScheduleAnyway because DoNotSchedule would leave pods Pending on a 2-node cluster."

### MEDIUM — Single Postgres replica, no HA
replicas: 1 in the StatefulSet. Single point of failure. In production: Patroni, CloudNativePG, or a managed DB (RDS, Cloud SQL).

### MEDIUM — No NetworkPolicy
Any pod in the cluster can reach any other pod. In a real environment, you would add a NetworkPolicy enforcing: frontend → backend, backend → postgres, but frontend cannot directly reach postgres.

### MEDIUM — uvicorn --workers 1
Single worker limits throughput. In production: run multiple workers, or use Gunicorn as the process manager. The HPA scaling-out strategy compensates at the pod level, but within a single pod, throughput is limited.

### LOW — Frontend has no HPA
Frontend has a fixed replicaCount: 3. The comment "Changed from 2 to 3 to trigger auto-sync" reveals this was a demo decision, not a production sizing decision.

---

## 4. Adjacent Concepts to Know

These topics are NOT in the repo but will come up in any interview starting from this project.

---

### From Minikube to Managed Cluster (EKS/GKE/AKS)

| Minikube decision | What changes on EKS/GKE |
|---|---|
| pullPolicy: Never (local image load) | pullPolicy: IfNotPresent or Always with ECR/GCR |
| nodeSelector: minikube for Postgres | Remove; use a network StorageClass (EBS gp3, Filestore) |
| storageClassName: standard (hostPath) | storageClassName: gp3 (EBS) or standard (GCE PD) |
| type: NodePort for frontend | type: LoadBalancer or type: ClusterIP + Ingress with cloud LB |
| Manual minikube tunnel for Ingress | Cloud load balancer automatically provisioned |
| 2-node cluster, single-AZ | Multi-AZ node groups; topologyKey: topology.kubernetes.io/zone |

### Secrets Management

**Sealed Secrets:** kubeseal CLI encrypts a Secret using the cluster public key. The ciphertext (SealedSecret) is committed to Git. The Sealed Secrets controller in the cluster decrypts it using the private key. Anyone reading Git sees only ciphertext — useless without the private key.

**External Secrets Operator:** A controller that reads from an external secret store (Vault, AWS SSM, Azure Key Vault, GCP Secret Manager) and projects values into Kubernetes Secrets. Secrets never touch Git at all.

### Argo Rollouts (vs plain Deployment)

Your project uses plain Deployments with RollingUpdate. Production GitOps often uses Argo Rollouts for:
- Canary deployments: Route 10% of traffic to new version, observe error rate, gradually increase if healthy.
- Blue-green deployments: Run old and new versions in parallel, flip traffic all at once.
- Automated rollback: If Prometheus analysis shows elevated error rate, rollback automatically.

### ArgoCD ApplicationSets

Instead of one Application manifest per environment, an ApplicationSet generates multiple Application objects from a template + a generator (list of clusters, list of directories). Enables multi-cluster GitOps from a single manifest.

### Chaos Mesh vs Litmus vs Gremlin

| Tool | Open source? | Strengths | Weaknesses |
|---|---|---|---|
| Chaos Mesh (yours) | Yes (CNCF) | Kubernetes-native, rich experiment types, CRD-based | Requires cluster access |
| Litmus | Yes (CNCF) | Workflow-based, templates (ChaosHub), better scheduling | More complex to set up |
| Gremlin | No (commercial) | SaaS, team collaboration, audit trail | Costly, requires agent install |

### Service Meshes (Istio / Linkerd)

Not in your repo. If asked "how would you do canary deployments or mTLS?":
- Istio: Envoy sidecar per pod; rich traffic management (weight-based routing, circuit breaking, retries), mTLS, telemetry.
- Linkerd: Lighter-weight, simpler to operate; automatic mTLS.
- Your version: label on pod templates is a hook for Istio traffic splitting — it is unused today but shows awareness.

### SLI / SLO / SLA / Error Budget

- SLI (Service Level Indicator): A metric that measures reliability. E.g., "the fraction of HTTP requests that return 2xx within 200ms."
- SLO (Service Level Objective): A target for the SLI. E.g., "99.9% of requests succeed within 200ms over a 30-day window."
- SLA (Service Level Agreement): A contractual commitment to the SLO with consequences for breach.
- Error Budget: 1 - SLO. If your SLO is 99.9%, your error budget is 0.1% = 43.8 minutes/month of acceptable downtime. Chaos engineering deliberately spends error budget in a controlled way to discover failure modes before customers spend it unintentionally.

### Horizontal vs Vertical vs Cluster Autoscaling

- HPA (yours): Scale pods horizontally (add/remove replicas). Good for stateless services.
- VPA (Vertical Pod Autoscaler): Automatically adjusts CPU/memory requests based on observed usage. Cannot be used with HPA on the same resource metric simultaneously.
- Cluster Autoscaler: Adds/removes nodes when pods are Pending due to insufficient resources. Works with HPA: HPA demands more pods → pods Pending → CA adds a node.

---

*Last updated: generated from repo state as of August 2026.*
*Files read: values.yaml, Chart.yaml, argocd/application.yaml, chaos/pod-kill.yaml, all 12 Helm templates, backend/main.py, backend/Dockerfile, frontend/nginx.conf, monitoring-values.yaml, README.md*
