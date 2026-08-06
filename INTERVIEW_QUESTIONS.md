# INTERVIEW_QUESTIONS.md
# Chaos-Engineered Self-Healing GitOps Platform — 50 Interview Questions

> All questions are grounded in the actual repo content.
> File names, values, and numbers cited are real, not hypothetical.
> Format: Q + one-line hint. Practice articulating the full answer yourself.

---

## CATEGORY 1: Project Overview & Architecture (Q1–Q10)

**Q1. Walk me through what happens end-to-end when a user opens a browser and hits `gitops.local` on your platform.**

*Hint: Touch minikube tunnel → NGINX Ingress controller → NodePort 30080 → frontend Service → NGINX container → /api/* proxy → backend ClusterIP Service (port 8000) → FastAPI → Postgres ClusterIP (port 5432) → response back up the chain.*

---

**Q2. Your README architecture diagram shows ArgoCD polling GitHub every 3 minutes. What is actually triggering that poll — is it a cron inside ArgoCD, a webhook, or something else? And what is the trade-off between the two approaches?**

*Hint: Default is a cron-style poll loop inside the ArgoCD application controller. Webhooks from GitHub (push events) give near-instant sync but require a publicly reachable ArgoCD endpoint. On local Minikube there is no public IP, so polling is the only option.*

---

**Q3. You chose a 3-tier architecture: NGINX frontend, FastAPI backend, Postgres StatefulSet. Why not just serve the API from the frontend container, or combine all three into one Docker image?**

*Hint: Separation of concerns — each tier scales independently (frontend scales for static serving, backend scales for CPU, Postgres is a StatefulSet with sticky storage). Combining them creates a single-replica bottleneck, makes HPA impossible, and conflates deployment lifecycles.*

---

**Q4. The frontend uses `pullPolicy: Never` and the backend uses `pullPolicy: Never`. What does that mean, and what would break if you changed it to `Always` on Minikube?**

*Hint: Never = only use the image already loaded into Minikube's internal container runtime. Always would tell Kubernetes to pull from a remote registry; since there is no registry in this setup, the pod would fail with ImagePullBackOff.*

---

**Q5. Your `values.yaml` is the single source of truth for the entire platform. But it also contains the database password on line 163. How would you explain this trade-off to a hiring manager, and what would you change first with more time?**

*Hint: Acknowledge it is a deliberate portfolio shortcut with a comment in the file. First change: integrate Sealed Secrets (kubeseal) so the encrypted SealedSecret is in Git but the plaintext never is.*

---

**Q6. You have a 2-node Minikube cluster (`minikube` as control-plane, `minikube-m02` as worker). The Postgres StatefulSet has a `nodeSelector` pinning it to `minikube`. Walk me through exactly why, and what the consequence is if you remove that selector.**

*Hint: Minikube hostPath provisioner creates the PV directory on the control-plane node only. Removing the nodeSelector risks Postgres scheduling to minikube-m02, where /tmp/hostpath-provisioner/... does not exist, causing CreateContainerConfigError.*

---

**Q7. If someone on your team runs `kubectl scale deployment backend --replicas=10` directly against the cluster, what happens? Be specific about the timeline.**

*Hint: Kubernetes immediately scales to 10. ArgoCD detects drift in its next reconciliation loop (up to 3 minutes). Because selfHeal: true is set in application.yaml, ArgoCD reverts the Deployment back to replicaCount: 2 (from values.yaml). The team member's change is silently undone.*

---

**Q8. Your backend has `replicaCount: 2` in `values.yaml` with a comment "2 replicas → PDB will protect at least 1 during disruptions." But the frontend has `replicaCount: 3` with a comment "Changed from 2 to 3 to trigger auto-sync." What does that comment reveal about your workflow, and is 3 the right number for the frontend?**

*Hint: The comment reveals you used a replica count change as a GitOps demo trigger, not a capacity decision. For a static-file NGINX server, 2 replicas are sufficient for HA; 3 is arbitrary. A better demo would change a label or annotation, not a capacity value.*

---

**Q9. What would you change about this architecture if you had two more weeks to work on it?**

*Hint: Strong answers include: (1) CI pipeline with GitHub Actions to build/push to GHCR, (2) custom Alertmanager rules, (3) network-delay and cpu-stress chaos YAML files committed to /chaos, (4) Sealed Secrets for DB credentials instead of plaintext in values.yaml, (5) NetworkPolicy for pod-to-pod traffic restriction.*

---

**Q10. How would you demonstrate to a recruiter who has never seen Kubernetes that this project is impressive? What is the one thing you would show them first?**

*Hint: Show the ArgoCD UI — commit a change (e.g., increment frontend replicaCount), let them watch the cluster state update in real time without any kubectl command. Then show Chaos Mesh killing a pod and the ReplicaSet replacing it automatically. Visual proof of self-healing is the most impressive demo.*

---

## CATEGORY 2: Kubernetes Resilience Internals (Q11–Q20)

**Q11. Explain the exact difference between the liveness probe and readiness probe you set on the backend, using the actual endpoint paths and thresholds from your repo.**

*Hint: Liveness is GET /health (returns {"status":"alive"}, fast, cheap), initialDelaySeconds: 20, failureThreshold: 3, failure triggers container restart. Readiness is GET /ready (opens a live psycopg2 DB connection every call), initialDelaySeconds: 15, failureThreshold: 3, failure removes pod from Service endpoints, no restart.*

---

**Q12. Your `/ready` endpoint in `main.py` opens a new psycopg2 connection to Postgres on every single readiness probe call, rather than checking a startup flag. Why did you design it that way? What bug does a startup flag introduce?**

*Hint: A startup flag (_db_ready) only flips once at boot. If Postgres goes down and comes back up after startup, the startup flag stays True — the readiness endpoint keeps returning 200 even though the DB is unreachable. A live connection check always reflects current DB state.*

---

**Q13. The HPA in your repo is set to `targetCPUUtilizationPercentage: 60` and `requests.cpu: 100m` for the backend. At what actual CPU usage in millicores does the HPA trigger a scale-out? How does it calculate this?**

*Hint: 60% of 100m = 60m. When average actual CPU across all backend pods exceeds 60 millicores, HPA triggers scale-out. Formula: desiredReplicas = ceil(currentReplicas * currentMetric / targetMetric).*

---

**Q14. Your HPA has `stabilizationWindowSeconds: 30` for scale-up and `stabilizationWindowSeconds: 180` for scale-down. Why the asymmetry? What real-world problem does `180` on scale-down prevent?**

*Hint: Scaling up fast prevents user-facing latency during load spikes. Scaling down slowly prevents flapping — if you scale down too quickly and load spikes again, you immediately scale back up, wasting resources and causing pod churn. 180s is the standard SRE anti-flap guard.*

---

**Q15. Your `PodDisruptionBudget` has `minAvailable: 1`. If the backend HPA scales down to exactly 2 pods and you simultaneously run `kubectl drain minikube-m02`, what sequence of events occurs? Does the drain succeed or block?**

*Hint: The drain tries to evict the pod on minikube-m02. The Eviction API checks the PDB: 2 pods running, minAvailable: 1, so 1 can be evicted. Drain evicts it. Kubernetes reschedules the pod to minikube (control-plane). Once the replacement passes readiness (15+ seconds), traffic resumes. Drain succeeds.*

---

**Q16. What is the difference between a voluntary and involuntary disruption in Kubernetes? Give me one example of each from your actual setup.**

*Hint: Voluntary = mediated by the Eviction API (kubectl drain, Chaos Mesh pod-kill, ArgoCD rolling update). Involuntary = node crash, OOM kill, power failure. PDB governs voluntary only. Example voluntary: chaos/pod-kill.yaml. Example involuntary: minikube-m02 runs out of RAM and the kernel OOMKills a backend container.*

---

**Q17. Walk me through exactly what happens during a rolling deployment when ArgoCD syncs a new image tag for the backend. Reference the `maxSurge` and `maxUnavailable` values in your Deployment.**

*Hint: maxSurge: 1, maxUnavailable: 0. With replicaCount: 2, Kubernetes creates pod 3 (new version), waits for it to pass readiness (15+ seconds for backend). Only then terminates pod 1 (old version). Then creates pod 4 (new version), waits for readiness, terminates pod 2. At no point are fewer than 2 pods serving traffic.*

---

**Q18. Your Postgres uses `terminationGracePeriodSeconds: 60` while the backend uses `30` and the frontend uses `15`. What is this setting, and why is Postgres's value higher?**

*Hint: After Kubernetes sends SIGTERM, it waits terminationGracePeriodSeconds before sending SIGKILL. Postgres needs more time to finish WAL writes, flush buffers, and checkpoint cleanly — 60 seconds. FastAPI/uvicorn drains in-flight HTTP requests quickly (30s). NGINX drains even faster (15s). Too-short grace period risks data corruption for Postgres.*

---

**Q19. You set `topologySpreadConstraints` with `whenUnsatisfiable: ScheduleAnyway` for the backend. What would happen if you changed this to `DoNotSchedule`, and why did you NOT do that?**

*Hint: DoNotSchedule would leave new backend pods in Pending state whenever they cannot be evenly spread (e.g., one node full). On a 2-node cluster with limited resources, this would cause scale-out pods from the HPA to get stuck Pending and never serve traffic — defeating the entire purpose of HPA.*

---

**Q20. What happens to the backend pods if the Postgres StatefulSet pod crashes and is being restarted? Walk through the probe logic step by step.**

*Hint: Backend /ready probes start failing (psycopg2 connection refused). After 3 failures x 10s = 30s, all backend pods are removed from the backend Service endpoints. Frontend NGINX /api/* requests get 502. Backend /health probes still pass (process alive). No restarts. When Postgres comes back (30s initialDelaySeconds on its own readiness probe), backend /ready probes pass again and pods re-enter the Service endpoints.*

---

## CATEGORY 3: GitOps / ArgoCD (Q21–Q28)

**Q21. What is the `resources-finalizer.argocd.argoproj.io` finalizer in your `argocd/application.yaml` actually doing? What goes wrong if you remove it and then delete the Application?**

*Hint: The finalizer registers a pre-delete hook. When the Application is deleted, ArgoCD cascades the deletion to all managed cluster resources (Deployments, Services, PVCs) before removing the Application object itself. Without it, the Application disappears from ArgoCD but orphaned pods, services, and the Postgres PVC remain in the cluster.*

---

**Q22. Your ArgoCD Application's `syncPolicy` has `prune: true`. What is the scenario where forgetting to set this flag causes a real operational problem?**

*Hint: You commit a mistake — say, a typo in an Ingress template that creates a broken resource. You fix it by deleting the template from Git. Without prune: true, ArgoCD never deletes the broken Ingress from the cluster. You have to manually kubectl delete it, violating the GitOps model.*

---

**Q23. ArgoCD tracks `targetRevision: main`. If a colleague force-pushes to main and rewrites history, what happens to ArgoCD's sync behaviour?**

*Hint: ArgoCD tracks the current HEAD of main. After a force push, HEAD points to a different commit. ArgoCD compares the cluster state to the new HEAD. If the new HEAD has different manifests, ArgoCD will sync to them (potentially destructively if the colleague removed resources). Force pushes to main in a GitOps repo are extremely dangerous.*

---

**Q24. You have inline `helm.values` in your `argocd/application.yaml` that override `values.yaml`. What would you put here for a production environment vs a staging environment?**

*Hint: Production overrides might include: replicaCount: 3 for backend, pullPolicy: IfNotPresent with a specific image tag (not "latest"), resource limits tuned for production node sizes, a production Ingress hostname, and Sealed Secrets references. Staging would have lower replicas and a staging hostname.*

---

**Q25. If you wanted to run a database migration (`alembic upgrade head`) automatically before every ArgoCD sync, how would you implement that without breaking the GitOps model?**

*Hint: Use an ArgoCD sync hook — a Kubernetes Job with annotation argocd.argoproj.io/hook: PreSync. ArgoCD runs the Job before syncing other resources. The Job must complete successfully or the sync is aborted. This keeps the migration declarative and version-controlled in Git.*

---

**Q26. What is the difference between ArgoCD "OutOfSync" and "Degraded" application health statuses? Which one would you see if the HPA could not reach the metrics-server?**

*Hint: OutOfSync = Git state differs from cluster state (drift detected). Degraded = the app is deployed per Git, but the resources themselves are unhealthy (e.g., pods not ready). If metrics-server is down, the HPA cannot calculate current utilization and enters an unknown state — ArgoCD would likely report the app as Degraded.*

---

**Q27. Your ArgoCD polls every 3 minutes by default. A critical security patch needs to be deployed in under 30 seconds. How would you do this without breaking the GitOps model?**

*Hint: Two options: (1) Set up a GitHub webhook that triggers ArgoCD to sync immediately on push — this requires your ArgoCD to be reachable from GitHub (not possible on local Minikube without tunnelling). (2) Manually trigger sync via argocd app sync gitops-platform from the CLI — this is still GitOps because the desired state is in Git; you are just forcing an immediate reconciliation.*

---

**Q28. What exactly does ArgoCD check when it determines that a resource is "in sync"? Is it comparing the raw YAML bytes?**

*Hint: ArgoCD renders the Helm chart from Git (values.yaml + templates) and compares the output to the live Kubernetes resource manifests using a semantic diff (not raw byte comparison). It ignores server-side fields like resourceVersion, uid, creationTimestamp. It uses a three-way merge similar to kubectl apply.*

---

## CATEGORY 4: Observability (Q29–Q36)

**Q29. Your backend Deployment has Prometheus scrape annotations (`prometheus.io/scrape: "true"`, `prometheus.io/port: "8000"`, `prometheus.io/path: "/metrics"`). How does Prometheus actually discover and use these — walk through the full scrape path.**

*Hint: Prometheus runs a kubernetes-pods scrape config that watches the Kubernetes API for pods. When it finds a pod with prometheus.io/scrape: "true", it adds pod-IP:8000/metrics to its scrape targets. prometheus_fastapi_instrumentator exposes http_requests_total, http_request_duration_seconds_bucket, etc. on that endpoint in Prometheus text format.*

---

**Q30. You have `retention: 2h` in your `monitoring-values.yaml`. What does this mean operationally, and what is the minimum retention needed to track a weekly SLO?**

*Hint: 2h means Prometheus drops metric data older than 2 hours. For a weekly SLO (e.g., 99.9% uptime over 7 days), you need at least 7 days of retention. For monthly SLO tracking, at least 30 days. In production, you either extend retention or use Thanos/Cortex for long-term storage.*

---

**Q31. You implemented metrics but not logs or traces. Describe a real debugging scenario on this platform where metrics alone would be insufficient and you would need logs.**

*Hint: Suppose /items GET endpoint returns 500 errors. Metrics tell you the error rate and count. But they cannot tell you WHY — was it a bad SQL query? An unexpected item format? A connection pool exhaustion? Logs from uvicorn would show the stack trace and exact exception. Without Loki or EFK, you can only get logs via kubectl logs — not queryable across restarts.*

---

**Q32. If the backend is returning 503 errors for 5 minutes and you only have Grafana, walk me through how you would diagnose the root cause using only the panels available to you.**

*Hint: Check pod readiness status panel (are backend pods in the endpoint list?). Check pod CPU/memory (are they being throttled or OOMKilled?). Check Postgres pod status (is the StatefulSet pod Running?). Check http_requests_total by status code. If all pods are Ready and Postgres is up but 503s persist, the issue is likely inside the application logic — need logs.*

---

**Q33. You enabled Alertmanager in `monitoring-values.yaml` but wrote no custom alert rules. What is the minimum alert you would add to make this platform "production-minimally-viable," and what PromQL would you write for it?**

*Hint: PodRestartingTooFast: `increase(kube_pod_container_status_restarts_total{namespace="gitops-app"}[15m]) > 5`. This catches crash loops before they become prolonged outages. Also useful: `kube_deployment_status_replicas_available{namespace="gitops-app"} < kube_deployment_spec_replicas` for under-replicated deployments.*

---

**Q34. What is the difference between `kube-state-metrics` and `node-exporter` in the kube-prometheus-stack you installed? Both are listed in your `monitoring-values.yaml` with resource constraints.**

*Hint: kube-state-metrics watches the Kubernetes API and exports metrics about Kubernetes objects (pod counts, deployment status, HPA replica counts, PDB status). node-exporter runs on each node as a DaemonSet and exports hardware/OS-level metrics (CPU, memory, disk, network). You need both: one for cluster objects, one for underlying node health.*

---

**Q35. Explain what a Prometheus histogram metric is, and why latency is measured as a histogram rather than a gauge in `prometheus_fastapi_instrumentator`.**

*Hint: A gauge is a single value at a point in time (e.g., current temperature). A histogram buckets observations (e.g., "how many requests took less than 0.1s? less than 0.5s? less than 1s?"). Histograms let you calculate percentiles (P50, P95, P99) across time ranges. A gauge of "average latency" loses distribution information — two systems with the same average can have very different tail latency.*

---

**Q36. What would you add to this observability stack to get "full three pillars" coverage? Be specific about the tools and how they would integrate with what you already have.**

*Hint: Logs: add Loki (Grafana's log aggregation) deployed via helm install grafana/loki-stack, then configure Promtail as a DaemonSet to tail container logs. Traces: instrument main.py with opentelemetry-sdk and configure an exporter to Tempo (Grafana's trace backend). All three would then be queryable from the same Grafana instance.*

---

## CATEGORY 5: Chaos Engineering (Q37–Q44)

**Q37. Why is chaos engineering called "engineering" and not "testing"? What is the philosophical difference between a chaos experiment and a unit test?**

*Hint: Unit tests verify known behaviour under known conditions. Chaos engineering explores unknown failure modes in complex systems — you hypothesise about what should happen, inject a fault, measure what actually happens, and update your mental model. Chaos is about learning, not assertion. The output is an improved system understanding and architectural change, not a pass/fail result.*

---

**Q38. Your `pod-kill.yaml` uses `mode: one`. What would change if you changed it to `mode: all`? Would the PDB prevent it?**

*Hint: mode: all would attempt to kill ALL pods with label app=backend simultaneously. Chaos Mesh uses the Eviction API, so the PDB (minAvailable: 1) would block the second eviction request, leaving one pod alive. However, depending on timing, both pods might receive eviction calls before the PDB blocks the second — behaviour depends on Chaos Mesh's eviction ordering. mode: one is the safe, controlled choice.*

---

**Q39. You state your MTTR is approximately 30-60 seconds for the pod-kill experiment. How did you measure that? What specifically starts the clock and what ends it?**

*Hint: Clock starts when Chaos Mesh kills the pod (visible in kubectl get pods output — pod shows Terminating). Clock ends when the replacement pod passes its readiness probe and is added back to the backend Service endpoints (kubectl get endpoints backend shows the new pod IP). You can verify via Grafana: the moment the pod count dips and recovers.*

---

**Q40. If you wanted to design a fourth chaos experiment targeting the Postgres StatefulSet, what hypothesis would you write, and what resilience gap would it expose?**

*Hint: Hypothesis: "When Postgres pod is killed, backend /ready probes fail within 30 seconds and all backend pods are removed from Service endpoints, causing frontend 502s. When Postgres recovers, backend /ready probes pass and traffic resumes within 60 seconds without any container restarts." Resilience gap: the frontend has no circuit breaker — it keeps accepting requests and returning 502s during the outage rather than failing fast.*

---

**Q41. The README says you have three chaos experiments: pod-kill, network-delay, and CPU-stress. But only `pod-kill.yaml` exists in the `/chaos` folder. If an interviewer opens your repo right now and asks about the other two, what do you say?**

*Hint: Be honest: "I ran network-delay and cpu-stress experiments manually through the Chaos Mesh UI/CLI to validate HPA scaling and network degradation, but I did not commit the YAML files to the repo. That is a gap I would close. Here is what those experiments would have looked like..." Then describe the hypotheses.*

---

**Q42. Your `pod-kill.yaml` has `duration: '60s'`. What does this actually control — is it how long the pod stays dead, or how long the experiment runs?**

*Hint: Duration controls how long the chaos experiment is active. For pod-kill, Chaos Mesh kills the pod and considers the experiment done after the duration. Kubernetes immediately starts replacing the pod (ReplicaSet controller does not wait for the experiment to end). The pod replacement typically completes in 30-45s, well within the 60s experiment window.*

---

**Q43. How does Chaos Mesh actually kill a pod? Does it run `kubectl delete pod`? And why does this distinction matter for the PDB?**

*Hint: Chaos Mesh uses the Kubernetes Eviction API (same as kubectl drain). This is crucial: the Eviction API respects PodDisruptionBudgets. If Chaos Mesh used kubectl delete pod directly, it would bypass the PDB and could kill all pods simultaneously, regardless of minAvailable. The PDB's protection only works when the Eviction API is used.*

---

**Q44. What is "blast radius" in chaos engineering, and list every mechanism in your current setup that limits it.**

*Hint: Blast radius = the maximum possible impact if an experiment goes wrong or runs longer than intended. Your controls: (1) mode: one limits to exactly one pod, (2) duration: '60s' auto-terminates, (3) labelSelector scopes to app=backend only (not frontend or Postgres), (4) namespace: gitops-app scopes to this app's namespace, (5) PDB minAvailable: 1 prevents complete backend unavailability.*

---

## CATEGORY 6: Curveball / Scaling Questions (Q45–Q50)

**Q45. You built this on Minikube. If you had to deploy this exact platform to AWS EKS for a production workload, list every single change you would need to make — walk through each component.**

*Hint: (1) Remove nodeSelector from Postgres StatefulSet, change storageClassName to gp2/gp3 (EBS). (2) Change frontend Service from NodePort to ClusterIP, add an AWS Load Balancer Controller Ingress. (3) Change pullPolicy to IfNotPresent, push images to ECR. (4) Add cluster-autoscaler to the node group. (5) Change topologyKey to topology.kubernetes.io/zone for multi-AZ spread. (6) Use AWS Secrets Manager + External Secrets Operator instead of values.yaml credentials. (7) Increase Prometheus retention to 15+ days or add Thanos. (8) Add NetworkPolicy.*

---

**Q46. Your platform currently handles one team's traffic. How would you architect this if you needed to deploy it for 50 different tenant teams, each isolated from each other?**

*Hint: Use ArgoCD ApplicationSets with a list generator (one entry per tenant). Each tenant gets its own namespace. NetworkPolicy isolates namespaces. A shared Prometheus instance with namespace-scoped scraping, or per-tenant Prometheus with a federation layer. Tenant-specific values files in a directory per tenant. Shared Postgres is replaced by a database-per-tenant or tenant-isolation via Postgres schemas.*

---

**Q47. Your backend runs `uvicorn --workers 1`. At 10x your current traffic, what breaks first, and what is your mitigation strategy?**

*Hint: Single uvicorn worker means single-threaded async event loop. At high load, it maxes out. HPA scales out pods (up to maxReplicas: 5), so you get 5 single-worker pods. That is the hard ceiling in this config. Mitigations: (1) Increase maxReplicas, (2) Switch to Gunicorn with multiple uvicorn workers per pod (e.g., --workers 4), (3) Add connection pooling (PgBouncer) in front of Postgres since each uvicorn call opens a new psycopg2 connection.*

---

**Q48. How would you secure this platform for a real production environment? Assume a threat model of: external attacker, malicious internal user, and accidental operator error.**

*Hint: External attacker: TLS termination at Ingress (cert-manager + Let's Encrypt), NetworkPolicy to restrict inter-pod traffic, RBAC limiting who can exec into pods. Malicious internal user: Sealed Secrets or Vault for credentials, ArgoCD RBAC limiting who can trigger syncs, audit logs. Accidental operator error: selfHeal: true reverts manual changes, PDB prevents accidental total drain, Helm rollback for bad releases, alert on drift detection.*

---

**Q49. A competitor of yours built the same project but used Kustomize instead of Helm. They argue that Kustomize is better because it is built into `kubectl`. How would you defend your Helm choice, and when would you concede that Kustomize is the better choice?**

*Hint: Helm wins for: parameterised multi-environment deployments (a single chart serves dev/staging/prod via --set or -f overrides), packaged dependencies (you could add a Helm dependency for a Redis subchart), chart versioning and helm rollback. Concede Kustomize when: you only need to patch a few fields across environments (Kustomize overlay is simpler), when you want no templating abstraction, or when you need kubectl-native workflow without Helm installed.*

---

**Q50. Imagine this platform goes down completely at 2am — ArgoCD is not syncing, the frontend returns 503, and you have no access to Grafana. Walk me through your step-by-step debugging process using only `kubectl`.**

*Hint: (1) kubectl get pods -n gitops-app (are pods running?). (2) kubectl describe pod <name> -n gitops-app (check Events for scheduling, image, or probe failures). (3) kubectl logs <name> -n gitops-app (application errors). (4) kubectl get endpoints backend -n gitops-app (is the backend Service routing anywhere?). (5) kubectl get events -n gitops-app --sort-by=.metadata.creationTimestamp (recent cluster events). (6) kubectl top nodes (are nodes out of resources?). (7) kubectl get hpa -n gitops-app (is HPA scaling?). (8) For ArgoCD: kubectl get pods -n argocd, check ArgoCD controller logs.*

---

*Total: 50 questions across 6 categories.*
*Files referenced: values.yaml, argocd/application.yaml, chaos/pod-kill.yaml, backend-hpa.yaml, backend-pdb.yaml, backend-deployment.yaml, postgres-statefulset.yaml, main.py, monitoring-values.yaml, nginx.conf, README.md*
