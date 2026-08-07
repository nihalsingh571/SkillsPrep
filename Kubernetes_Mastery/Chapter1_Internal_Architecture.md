# Chapter 1: Kubernetes Internal Architecture — The Definitive Deep Dive

Welcome to the internal architecture deep dive. If you're reading this, you already know how to write a Pod spec, create a Deployment, and expose it via a Service. This chapter isn't about that. This chapter is about what happens *under the hood*. 

We are going to dissect the Kubernetes control plane and worker node components with the rigor expected of a seasoned Site Reliability Engineer or Kubernetes administrator operating at scale. You will learn not just *what* the components are, but *how* they communicate, *why* they were designed this way, and how to debug them when they inevitably break in production.

This knowledge is what separates a user of Kubernetes from a master of Kubernetes. Let's begin.

---

## SECTION 1: Control Plane Components — Deep Internals

The Control Plane is the brain of the cluster. It makes global decisions, detects and responds to cluster events, and maintains the cluster's desired state. In a production HA (High Availability) setup, the control plane components run across multiple dedicated master nodes.

### 1.1 kube-apiserver: The Universal Gateway

The `kube-apiserver` is the most critical component in the cluster. **It is the ONLY entry point to the cluster.** Every single component—whether it's the kubelet on a node, the controller-manager, the scheduler, or a user running `kubectl`—must communicate through the API server. No component talks directly to etcd or to each other.

#### The REST API and State
The API server is a stateless REST HTTP(S) server. Its primary job is to provide a CRUD interface for Kubernetes objects, validate those objects, and persist them to `etcd`. Because it is stateless, scaling the API server is as simple as adding more replicas behind a load balancer.

#### API Request Lifecycle
When a request hits the API server, it goes through a strict, multi-stage pipeline:

1.  **Authentication (AuthN):** "Who are you?" (e.g., x509 client certs, Bearer Tokens, OIDC).
2.  **Authorization (AuthZ):** "Are you allowed to do this?" (typically RBAC).
3.  **Mutating Admission:** Webhooks that can modify the incoming object (e.g., injecting sidecar containers).
4.  **Schema Validation:** "Is this JSON/YAML valid for this object type?"
5.  **Validating Admission:** Webhooks that can reject the object based on custom policies (e.g., OPA Gatekeeper preventing privileged pods).
6.  **Storage:** Writing the final state to `etcd`.

#### Communication and Watch Mechanism
Kubernetes is a declarative system, which means components need to know when the state changes. Instead of polling (which doesn't scale), Kubernetes uses the **Watch** mechanism.
Controllers open long-lived HTTP connections (chunked transfer encoding) to the API server. When a resource is updated in etcd, the API server streams the event to all watching clients.

#### Aggregation Layer
The API server can be extended natively using the Aggregation Layer. If you install the `metrics-server`, it registers an API service. When you hit `/apis/metrics.k8s.io/v1beta1`, the core API server acts as a reverse proxy, forwarding the request to the `metrics-server` pod.

#### Production Configuration (kubeadm snippet)
In production, you pass extensive flags to configure auditing, auth, and admission:

```yaml
# Snippet from /etc/kubernetes/manifests/kube-apiserver.yaml
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.0.0.10
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction,MutatingAdmissionWebhook,ValidatingAdmissionWebhook
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-servers=https://127.0.0.1:2379
    - --secure-port=6443
    - --audit-log-path=/var/log/kubernetes/audit.log
    - --audit-policy-file=/etc/kubernetes/audit-policy.yaml
```

#### Debugging and Operations
*   **Check logs:** `crictl logs <apiserver-container-id>` (since it runs as a static pod).
*   **Check metrics:** `curl -k https://localhost:6443/metrics` (often used to monitor request latencies).

> **Interview Q&A**
> **Q:** What happens when the API server goes down? Can existing pods keep running?
> **A:** Yes, existing pods will continue to run without interruption. The `kubelet` and container runtime manage the running processes. `kube-proxy` keeps the networking rules intact. However, you cannot create new pods, scale deployments, or read logs/metrics. If a node fails while the API server is down, the pods on that node cannot be rescheduled elsewhere because the scheduler and controller-manager cannot function without the API server.

---

### 1.2 etcd: The Source of Truth

`etcd` is a strongly consistent, distributed key-value store built by CoreOS (now Red Hat). It holds the absolute state of the cluster. If it's not in etcd, it doesn't exist in Kubernetes.

#### Raft Consensus Algorithm
`etcd` uses the Raft consensus algorithm to maintain High Availability. Raft works by electing a **Leader**. All writes MUST go to the leader. If a write hits a follower, it forwards it to the leader. 
The leader appends the write to its log and sends an `AppendEntries` RPC to the followers. Once a **Quorum** (majority) of nodes acknowledge the write, it is committed.

**Why an odd number of nodes?**
Quorum is `(N/2) + 1`.
*   A 3-node cluster needs 2 nodes for quorum. It can tolerate 1 failure.
*   A 4-node cluster needs 3 nodes for quorum. It can STILL only tolerate 1 failure, but increases network overhead.
*   A 5-node cluster needs 3 nodes for quorum. It can tolerate 2 failures.
Therefore, always use 3, 5, or 7 nodes.

#### ASCII: Raft Log Replication

```text
      [ Client ]
          | (Write: key=value)
          v
+-------------------+
|  etcd Node 1      |
|  (LEADER)         |  --1. Appends to local log-->
+-------------------+
  |               |
  | 2. Replicate  | 2. Replicate
  v               v
+---------+   +---------+
| etcd 2  |   | etcd 3  |
| (Follow)|   | (Follow)|
+---------+   +---------+
  |               |
  | 3. Ack        | 3. Ack
  v               v
 (Once majority ack, leader commits and replies to client)
```

#### Data Storage Structure
Objects are stored as JSON strings in an etcd hierarchy:
`/registry/{group}/{kind}/{namespace}/{name}`

Example: A pod named `web` in `default` namespace:
`/registry/pods/default/web`

*Important distinction:* Only object specs and statuses are stored. Ephemeral data like pod logs or metrics are NOT stored in etcd.

#### Compaction and Defragmentation
Kubernetes uses MVCC (Multi-Version Concurrency Control) in etcd. When you update a deployment, etcd doesn't overwrite the old value; it writes a new revision. This allows `watch` clients to replay history if they disconnect.
However, this means etcd grows infinitely. `kube-apiserver` runs a periodic compaction process (usually every 5 mins) to discard old revisions.
Even after compaction, the disk space is not returned to the OS. You must run defragmentation manually or via cronjob to reclaim space, especially if etcd hits its strict 2GB or 8GB quota.

#### Backup and Restore
In production, you MUST back up etcd.

```bash
# Snapshot Backup
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /backup/etcd-snapshot.db

# Snapshot Status
ETCDCTL_API=3 etcdctl --write-out=table snapshot status /backup/etcd-snapshot.db
```

#### Encryption at Rest
By default, Secrets in Kubernetes are base64 encoded and stored in plain text in etcd. If someone steals your etcd data file, they have all your passwords. Production clusters must enable Encryption at Rest using an `EncryptionConfiguration` passed to the API server.

> **Interview Q&A**
> **Q:** What is the minimum etcd cluster size for HA and why?
> **A:** 3 nodes. Raft requires a majority quorum `(N/2 + 1)` to elect a leader and commit writes. A 1-node cluster has no fault tolerance. A 2-node cluster needs 2 nodes for quorum, meaning if 1 fails, the cluster loses quorum and becomes read-only. A 3-node cluster requires 2 nodes for quorum, meaning it can tolerate 1 node failure while maintaining HA.

---

### 1.3 kube-scheduler: The Matchmaker

The scheduler's job is deceptively simple: find an unscheduled Pod, find the best Node for it, and assign it.
It operates in a continuous loop, watching the API server for Pods where `spec.nodeName == ""`.

#### Two-Phase Scheduling
The scheduling algorithm is divided into two distinct phases: Filtering and Scoring.

**Phase 1: Filtering (Predicates / Feasibility)**
The scheduler eliminates nodes that CANNOT run the pod.
*   `NodeResourcesFit`: Does the node have enough allocatable CPU/RAM?
*   `NodeAffinity` / `NodeSelector`: Does the node match the required labels?
*   `TaintToleration`: Does the pod tolerate the node's taints?
*   `NodeUnschedulable`: Is the node cordoned?
If no nodes pass the filters, the pod remains `Pending`.

**Phase 2: Scoring (Priorities)**
For the nodes that passed Phase 1, the scheduler scores them from 0 to 100 to find the *optimal* fit.
*   `NodeResourcesBalancedAllocation`: Prefers nodes that will have a balanced CPU/RAM utilization after scheduling.
*   `ImageLocality`: Prefers nodes that already have the container image pulled.
*   `InterPodAffinity`: Scores higher if the node satisfies preferred affinity rules.
The node with the highest score wins.

#### Binding
Once a node is selected, the scheduler does NOT tell the node to run the pod. It simply issues a `Binding` API request to the `kube-apiserver`, which updates the `spec.nodeName` of the Pod in etcd.

#### ASCII: Scheduler Flow

```text
[ Unscheduled Pod Queue ]
         |
         v
+-----------------------+
|  Filtering (Hard)     | --> Rejects Node C (Full RAM)
+-----------------------+
         |
         v (Node A, Node B left)
+-----------------------+
|  Scoring (Soft)       | --> Node A: 90, Node B: 50
+-----------------------+
         |
         v
[ Select Node A ]
         |
         v
[ API Server Binding Request ] -> updates spec.nodeName="Node-A"
```

#### Scheduler Cache
To make decisions quickly, the scheduler maintains an in-memory cache of the cluster state (nodes, pods). It doesn't query etcd for every decision.

> **Interview Q&A**
> **Q:** Walk me through exactly how the scheduler picks a node for a new pod.
> **A:** The scheduler watches the API server for Pods without a `nodeName`. When it sees one, it runs it through a two-phase cycle: Filtering and Scoring. In Filtering, it applies plugins like ResourceFit and TaintToleration to remove unsuitable nodes. If no nodes remain, the pod stays Pending. For remaining nodes, Scoring applies plugins like ImageLocality to rank them. The highest-scoring node is selected. Finally, the scheduler sends a Binding object to the API server to update the Pod's `nodeName`. The kubelet on that node will then notice the assignment and start the pod.

---

### 1.4 kube-controller-manager: The Reconciler

Kubernetes is built on the concept of controllers. A controller watches the current state, compares it to the desired state, and takes action to reconcile the two.
The `kube-controller-manager` is a single binary that bundles dozens of core controllers together. They run as independent goroutines inside the same process.

#### Key Controllers
*   **Deployment Controller:** Watches Deployments. When you create one, it creates a ReplicaSet. If you update the image, it creates a *new* ReplicaSet and scales the old one down.
*   **ReplicaSet Controller:** Watches ReplicaSets. If `replicas: 3` but only 2 pods exist, it creates a new Pod object. If 4 exist, it deletes one.
*   **Node Controller:** Watches node heartbeats. If a node stops reporting for 40s, it marks it `NotReady`. If it's down for 5 mins (pod eviction timeout), it evicts the pods on that node.
*   **Job Controller:** Watches Jobs and creates Pods to execute them.
*   **EndpointSlice Controller:** Watches Services and Pods. When a Pod matching a Service's selector becomes Ready, it adds the Pod's IP to the Service's EndpointSlice.

#### The Reconciliation Loop
Controllers operate on level-triggered logic (reacting to the current *state*, not just *events*).
`for { observe -> diff -> act }`

#### Leader Election
If you run 3 controller-managers for HA, they would fight over who gets to create pods. To prevent this, they use Leader Election. Only one controller-manager is "active". The others are on standby. They acquire a `Lease` object in the `kube-system` namespace. If the active leader dies, the lock expires, and another replica takes over.

> **Interview Q&A**
> **Q:** What happens to pods if the controller manager crashes?
> **A:** Existing pods continue to run fine. However, the self-healing mechanisms break. If a pod crashes, it won't be replaced. If a node fails, its pods won't be rescheduled. If you create a new Deployment, no ReplicaSet or Pods will be created because the controllers responsible for generating those downstream objects are offline.

---

### 1.5 cloud-controller-manager (CCM)

Historically, cloud provider code (AWS, GCP, Azure) was baked directly into the Kubernetes core binaries (in-tree). This meant Kubernetes releases were tied to cloud provider updates.
The `cloud-controller-manager` extracts this logic.

*   **Node Controller:** Determines if a node was deleted in the cloud (e.g., an EC2 instance terminated) and removes it from Kubernetes. Updates node labels with instance types and zones.
*   **Service Controller:** When you create a Service of type `LoadBalancer`, this controller talks to the cloud provider API to provision an ALB/NLB, configure security groups, and route traffic to the worker nodes.
*   **Route Controller:** Configures VPC route tables so pods on different nodes can communicate.

---

## SECTION 2: Worker Node Components

Worker nodes are where the actual workloads run. They take instructions from the control plane.

### 2.1 kubelet: The Node Agent

The `kubelet` is the primary "node agent" that runs on every node. It is the ONLY component that interacts directly with the container runtime. **The API server NEVER talks to Docker or containerd directly.**

#### Pod Assignment and Execution
The kubelet watches the API server for Pods assigned to its node (`spec.nodeName == my-hostname`).
When it sees a new pod, it doesn't just run it. It runs an internal admission check (e.g., verifying it still has enough allocatable resources, handling AppArmor/Seccomp profiles).
Then, it translates the Pod spec into imperative API calls over gRPC to the Container Runtime Interface (CRI).

#### Static Pods
The kubelet can manage pods independently of the API server! If you place a YAML manifest in `/etc/kubernetes/manifests/`, the kubelet will run it.
This is how the control plane is bootstrapped. `kubeadm` places the apiserver, etcd, etc., in that directory. The kubelet starts them. It then creates a "Mirror Pod" on the API server so they are visible to `kubectl`, but they cannot be deleted via API.

#### Probes and Health Checks
The kubelet, NOT the control plane, is responsible for running Liveness, Readiness, and Startup probes. It executes the `exec` commands or makes the HTTP `GET` requests against the containers and reports the status back to the API server.

#### Node Eviction
The kubelet monitors node resources (RAM, disk). If memory drops below a threshold (e.g., `< 100Mi` configured via `evictionHard`), the kubelet will aggressively terminate pods to save the node from kernel panics (OOM Killer).

> **Interview Q&A**
> **Q:** What happens if kubelet crashes on a node?
> **A:** The existing containers keep running (the container runtime manages them). However, the node stops sending heartbeats to the API server. After 40 seconds, the Node Controller marks the node `NotReady`. After 5 minutes, it evicts the pods. The Service endpoints will be removed. Since the kubelet is dead, it cannot stop the containers, so the pods might actually still be running network traffic if their IPs are hardcoded, but they are logically dead to the cluster.

---

### 2.2 kube-proxy: The Network Plumber

`kube-proxy` is a network proxy that runs on every node. It is responsible for implementing Kubernetes Services.

Pods are ephemeral; their IPs change. Services provide a stable Virtual IP (VIP). `kube-proxy` makes that VIP work.

#### Modes of Operation
1.  **iptables (Default):** `kube-proxy` watches the API Server for `EndpointSlices`. For every Service, it writes hundreds of `iptables` NAT rules in the kernel. When a packet destined for a Service VIP hits the kernel, `iptables` intercepts it, uses a random probability stat to load balance, and changes the destination IP (DNAT) to a specific Pod IP.
    *   *Problem:* `iptables` evaluates rules sequentially `O(n)`. In clusters with 10,000 services, routing becomes extremely slow.
2.  **IPVS:** Uses the Linux IP Virtual Server. It uses hash tables `O(1)` instead of sequential lists, making it vastly more scalable and performant for large clusters.
3.  **eBPF:** Modern networking solutions like Cilium completely replace `kube-proxy`. They compile network policies into eBPF bytecode loaded directly into the kernel for unmatched performance, bypassing iptables entirely.

> **Interview Q&A**
> **Q:** Can you run a cluster without kube-proxy? When would you?
> **A:** Yes. `kube-proxy` is only required to route traffic to Service VIPs. If you use a CNI plugin that replaces kube-proxy functionality with eBPF (like Cilium), you run the cluster entirely without kube-proxy. You also don't strictly need it if you only use headless services or node-level routing, though that is rare.

---

### 2.3 Container Runtime (CRI + OCI)

Kubernetes doesn't run containers. It tells the runtime to run them.

*   **CRI (Container Runtime Interface):** The gRPC specification defining how kubelet talks to a runtime.
*   **OCI (Open Container Initiative):** The standard for container image formats and runtime execution. `runc` is the reference implementation.

Common runtimes: `containerd` (the modern standard, extracted from Docker), `CRI-O`.

#### The Container Lifecycle (CRI calls from Kubelet)
1.  `RunPodSandbox`: Instructs containerd to set up the environment. It creates a Linux network namespace and runs a lightweight `pause` container to hold the network namespace open.
2.  `CreateContainer`: containerd pulls the image and prepares the root filesystem and config.
3.  `StartContainer`: containerd tells `runc` to execute the application process.

> **Interview Q&A**
> **Q:** What is the difference between Docker, containerd, and runc?
> **A:** Docker is a full developer platform (CLI, builder, daemon). When Docker runs a container, it passes it to `containerd`. `containerd` is a daemon that manages the image lifecycle and APIs. But `containerd` doesn't run the process—it passes it to `runc`. `runc` is the low-level CLI tool that actually talks to the Linux kernel (namespaces/cgroups) to spawn the isolated process. Kubernetes deprecated Docker (dockershim) because it only needed `containerd`.

---

## SECTION 3: The Complete kubectl apply Journey

This is the ultimate interview question: "What happens when I run `kubectl apply -f deployment.yaml`?"

Here is the exact step-by-step trace of a declarative rollout:

```text
[User] kubectl apply -f deployment.yaml
```

**1. Client Processing**
`kubectl` reads your `~/.kube/config`. It discovers the API server URL and your credentials. It performs client-side validation (syntax). It determines if this is a Create or Patch operation, then constructs a REST POST/PATCH request with the YAML converted to JSON.

**2. Authentication**
The request hits the `kube-apiserver`. The server checks the x509 certificate or Bearer Token to identify the user (e.g., `User: nihal`, `Group: system:masters`).

**3. Authorization**
The API server passes the identity to the RBAC module. "Does `nihal` have the `create` verb permission on the `deployments` resource in the `apps` apiGroup in the `default` namespace?" Yes.

**4. Mutating Admission**
The request goes through Mutating Webhooks. For example, an Istio webhook intercepts the request and injects the Envoy sidecar container configuration into the deployment template.

**5. Object Validation**
The API server validates the mutated JSON against the OpenAPI schema for Deployments. (Are replica counts integers? Are labels strings?).

**6. Validating Admission**
The request goes through Validating Webhooks. For example, OPA Gatekeeper checks a policy: "Does this deployment run as root?" If yes, it denies the request. Let's assume it passes.

**7. Storage in etcd**
The API server persists the Deployment object to etcd.
etcd responds with success and a new `resourceVersion` (e.g., `10542`).
The API server returns a `201 Created` HTTP response to `kubectl`.
*At this point, nothing is running yet.*

**8. Deployment Controller loop**
The Deployment Controller, running in `kube-controller-manager`, receives a watch event from the API server: "New Deployment created".
It reconciles state: It creates a `ReplicaSet` object and POSTs it to the API server.

**9. ReplicaSet Controller loop**
The API server saves the ReplicaSet to etcd.
The ReplicaSet Controller receives a watch event.
It notices `desired=3`, `current=0`. It creates 3 `Pod` objects and POSTs them to the API server. The pod objects have `spec.nodeName=""`.

**10. Scheduler loop**
The Scheduler notices 3 Pods with no `nodeName`.
It runs Filtering (finding nodes with enough resources) and Scoring (ranking them).
It selects `worker-node-1` for a pod.
It sends a `Binding` object to the API server: "Update Pod A to run on worker-node-1".

**11. Kubelet notices assignment**
The `kubelet` on `worker-node-1` receives a watch event: "A Pod was assigned to me."

**12. Container Execution (CRI)**
Kubelet calls `containerd` via gRPC:
*   `RunPodSandbox`: Create the network namespace.
*   `PullImage`: Download the image.
*   `StartContainer`: Start the application.

**13. Networking (CNI)**
The CRI calls the CNI (Container Network Interface) plugin (e.g., Calico, Flannel). CNI creates a `veth` pair, connects the pod to the node's bridge, and assigns an IP address (e.g., `10.244.1.5`).

**14. Probes and Status**
Kubelet starts running the Readiness probe. Once it passes, kubelet PATCHes the Pod status to `Ready=True` on the API server.

**15. Endpoint Updating**
The `EndpointSlice` controller sees the Pod is `Ready` and has an IP. It updates the `Service`'s `EndpointSlice` to include `10.244.1.5`.

**16. Network Routing**
`kube-proxy` on every node sees the updated EndpointSlice. It updates local `iptables` rules so traffic to the Service VIP routes to `10.244.1.5`.

**[Running]**
The Pod is live.

---

## SECTION 4: API Objects Internals

### 4.1 Desired State and Reconciliation Loop
Kubernetes is a declarative, **level-triggered** system. It is not edge-triggered.
*   *Edge-triggered:* Reacts to events (e.g., "Scale up by 1"). If a message is lost, the system is out of sync permanently.
*   *Level-triggered:* Reacts to the current observed state vs desired state (e.g., "I want 3. I see 2. I will add 1"). If an event is missed, the next sync loop will catch it. This makes reconciliation idempotent.

**Garbage Collection and OwnerReferences:**
When a Deployment creates a ReplicaSet, it injects an `OwnerReference` into the ReplicaSet's metadata. When the RS creates Pods, it sets itself as the owner.
If you delete the Deployment, the `kube-controller-manager`'s Garbage Collector sees the cascade and deletes the dependent objects automatically.

### 4.2 Custom Resources (CRDs)
You can extend the Kubernetes API dynamically.
By applying a CustomResourceDefinition (CRD), you tell the API server to create new endpoints for your custom objects.

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.company.com
spec:
  group: company.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                engine:
                  type: string
                  enum: [postgres, mysql]
  scope: Namespaced
  names:
    plural: databases
    singular: database
    kind: Database
```

Once applied, you can run `kubectl create -f db.yaml` and the API server will store it in etcd at `/registry/company.com/databases/...`.

### 4.3 Operators
A CRD just stores data. To make it do something, you need a controller.
**Operator = CRD + Custom Controller**.
You write a controller (often using Go and Kubebuilder) that watches your Custom Resource and performs complex domain-specific logic.
Example: The `prometheus-operator` watches `Prometheus` CRDs and dynamically configures and deploys Prometheus statefulsets and configmaps.

> **Interview Q&A**
> **Q:** What is an Operator and how is it different from a Helm chart?
> **A:** A Helm chart is a templating engine. It renders YAML and submits it to the API server once. It has no active lifecycle management. An Operator is an active software process running in the cluster. It watches for changes to Custom Resources and actively manages the lifecycle, backups, upgrades, and failovers of a complex application on an ongoing basis.

---

## SECTION 5: Admission Controllers Deep Dive

Admission controllers intercept requests *after* auth, but *before* persistence. They are the gatekeepers of the cluster.

### Built-in vs Dynamic
*   **Built-in:** Compiled into the API server (e.g., `LimitRanger` which enforces default resource limits).
*   **Dynamic (Webhooks):** HTTP callbacks to external services.

### Mutating vs Validating
1.  **MutatingWebhookConfiguration:** Runs first. It can modify the object.
2.  **ValidatingWebhookConfiguration:** Runs second. It can only say "Yes" or "No".

Why order matters: You want to validate the *final* object, after all mutations (like sidecar injections) have occurred.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: strict-security
webhooks:
  - name: verify-root.example.com
    clientConfig:
      service:
        name: validator
        namespace: default
        path: "/validate"
      caBundle: "base64-encoded-ca-cert"
    rules:
      - operations: ["CREATE", "UPDATE"]
        apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods"]
    failurePolicy: Fail
    sideEffects: None
```

**Failure Policy (`Fail` vs `Ignore`):**
If the webhook service is down, what should the API server do?
*   `Fail`: The API request is rejected. Secure, but risks cluster availability if the webhook crashes.
*   `Ignore`: The request is allowed through. High availability, but risks security violations.

> **Interview Q&A**
> **Q:** What is the order of admission controller execution?
> **A:** Mutating admission webhooks execute first, because they can alter the object. After mutations are applied, the object schema is validated again. Finally, validating admission webhooks execute to strictly accept or reject the final proposed state.

---

## SECTION 6: Leader Election for HA

In an HA cluster, you run 3 `kube-controller-manager` pods and 3 `kube-scheduler` pods. If all 3 scheduled the same pod, chaos would ensue.
They use the Kubernetes API itself to coordinate via a `Lease` object in the `kube-system` namespace.

1.  All 3 instances try to create/update the Lease object.
2.  Thanks to etcd's optimistic concurrency (`resourceVersion`), only one succeeds. That instance is the Leader.
3.  The leader continually renews the lease (e.g., every 2 seconds).
4.  The followers simply watch the lease.
5.  If the leader crashes, the lease expires. A follower grabs the lease and becomes the new leader.

---

## END OF CHAPTER

### Cheat Sheet: Component Matrix

| Component | Runs On | Main Responsibility | Stateful? |
| :--- | :--- | :--- | :--- |
| **API Server** | Master | Front-door API, auth, validation | No |
| **etcd** | Master | Key-value store, cluster state | **Yes** |
| **Scheduler** | Master | Assigning Pods to Nodes | No |
| **Controller Mgr** | Master | Running reconciliation loops | No (Leader Elect) |
| **Kubelet** | Node | Managing container lifecycle via CRI | No |
| **Kube-proxy** | Node | Network routing for Services (iptables) | No |
| **Containerd** | Node | Running the actual processes | No |

### Control Plane Debugging Commands
```bash
# Check if core components are healthy
kubectl get componentstatuses (deprecated but still used)
kubectl get pods -n kube-system

# See API server logs (static pod)
crictl logs $(crictl ps --name=kube-apiserver -q)

# See kubelet logs (systemd service)
journalctl -u kubelet -f

# Trace a pod scheduling decision
kubectl describe pod <name> | grep -A 5 Events
```

*Proceed to Chapter 2 for Advanced Networking and CNI Plugins.*
