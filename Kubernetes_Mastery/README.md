# ☸️ Kubernetes Mastery Notes
### The Most Comprehensive Production Kubernetes Guide Ever Written

> Built for **Senior DevOps / Platform Engineer / SRE interviews** at Google, Amazon, Microsoft, Netflix, Uber, LinkedIn, Goldman Sachs, and any startup.
> Every concept explained with **internal working**, **control plane flows**, **ASCII diagrams**, **production-grade YAML**, **kubectl commands**, **troubleshooting**, and **FAANG-level interview Q&A**.

---

## 📁 Chapters

| # | Chapter | File | Focus |
|---|---|---|---|
| 1 | **Kubernetes Internal Architecture** | [Chapter1_Internal_Architecture.md](./Chapter1_Internal_Architecture.md) | API Server, etcd, Scheduler, Controller Manager, Kubelet, CRI, Operators, CRDs, `kubectl apply` internal flow |
| 2 | **Advanced Workloads & Networking** | [Chapter2_Workloads_Networking.md](./Chapter2_Workloads_Networking.md) | StatefulSets, DaemonSets, Jobs, Pod lifecycle, CNI, eBPF, Cilium, Calico, CoreDNS, NetworkPolicy, packet flow |
| 3 | **Storage, Scaling & Scheduling** | [Chapter3_Storage_Scaling_Scheduling.md](./Chapter3_Storage_Scaling_Scheduling.md) | CSI, StorageClass, HPA, VPA, Karpenter, Cluster Autoscaler, Affinity, Taints, QoS, PDB, eviction |
| 4 | **Security, Observability & Operations** | [Chapter4_Security_Observability.md](./Chapter4_Security_Observability.md) | RBAC, OPA, Falco, Cosign, Trivy, Prometheus, Loki, Tempo, debugging CrashLoopBackOff/OOMKilled/Pending |
| 5 | **Production Kubernetes Architecture** | [Chapter5_Production_Architecture.md](./Chapter5_Production_Architecture.md) | EKS HA design, Karpenter, GitOps, Velero, multi-region, cost optimization, Netflix/Uber/Swiggy architectures |
| 6 | **Interview Mastery** | [Chapter6_Interview_Mastery.md](./Chapter6_Interview_Mastery.md) | 50 deep-analysis Q&A + 30 Beginner + 20 Intermediate + 20 Advanced + 20 Scenario + 10 Debug + 10 Architecture + 20 YAML + 50 Rapid-fire |

---

## 🎯 Target Interviews

| Company | Focus Chapters |
|---|---|
| **Google / DeepMind** | Ch1 (internals) + Ch4 (security) + Ch6 advanced |
| **Amazon (EKS team)** | Ch5 (EKS production) + Ch3 (scaling) + Ch6 EKS questions |
| **Microsoft (AKS)** | Ch1 + Ch2 (networking) + Ch6 |
| **Netflix / Uber / LinkedIn** | Ch5 (production architecture) + Ch4 (observability) + Ch6 scenario |
| **Goldman Sachs / Morgan Stanley** | Ch4 (security/RBAC) + Ch6 |
| **Startups** | Ch3 + Ch5 + Ch6 beginner/intermediate |
| **Senior DevOps / SRE / Platform Eng** | All 6 chapters |

---

## ⚡ Quick Revision Path

| Time | What to Read |
|---|---|
| **1 week** | All 6 chapters in order |
| **3 days** | Ch1 internals + Ch4 security + Ch6 all Q&A |
| **1 day** | Ch6 only (50 deep + all categories) |
| **1 hour** | Ch6 Rapid-fire + cheat sheets from each chapter |
