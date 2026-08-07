# Kubernetes Mastery: Chapter 3 - Storage, Scaling, and Scheduling

Welcome to Chapter 3 of Kubernetes Mastery. This chapter dives deep into the intricate mechanisms of Kubernetes storage, advanced pod scheduling, and autoscaling. We will cover internal workings, production-grade scenarios, and prepare you for top-tier FAANG interviews.

---

## PART A: STORAGE

### 1. Storage Architecture Overview

Kubernetes decouples storage from the pods to ensure data persistence beyond a pod's lifecycle. The key components in this architecture are the PersistentVolume (PV), PersistentVolumeClaim (PVC), and StorageClass (SC).

#### Architecture Diagram
```text
+---------------------+
|     Pod             |
|  +---------------+  |
|  |   Container   |  |
|  | [ /data ] <---|--|---+ 
|  +---------------+  |   |
+---------------------+   |
                          | (Mounts)
+-------------------------v-+
|  PersistentVolumeClaim    |  <-- Request for storage by developer
|  (PVC)                    |
+-------------------------+-+
                          | (Binds)
+-------------------------v-+
|  PersistentVolume         |  <-- Actual storage resource in cluster
|  (PV)                     |
+-------------------------+-+
                          | (Provisioned by)
+-------------------------v-+
|  StorageClass             |  <-- Storage blueprint by admin
|  (SC)                     |
+---------------------------+
                          | (Cloud API)
+-------------------------v-+
| AWS EBS / GCP PD / EFS    |  <-- Physical/Cloud storage
+---------------------------+
```

#### Static vs Dynamic Provisioning
- **Static Provisioning:** A cluster administrator manually provisions a set of PersistentVolumes (PVs). Developers create PVCs that bind to these existing PVs if they match the requested capacity and access modes.
- **Dynamic Provisioning:** There are no pre-created PVs. When a developer creates a PVC requesting a specific StorageClass, Kubernetes automatically provisions a new PV (and the underlying cloud volume) on the fly.

#### Access Modes
- `ReadWriteOnce (RWO)`: Volume can be mounted as read-write by a single node. Most block storage (e.g., AWS EBS) supports this.
- `ReadOnlyMany (ROX)`: Volume can be mounted read-only by many nodes.
- `ReadWriteMany (RWX)`: Volume can be mounted as read-write by many nodes. Typical for file systems like NFS or AWS EFS.
- `ReadWriteOncePod (RWOP)`: Volume can be mounted as read-write by a single Pod. Introduced to prevent multiple pods on the *same* node from writing to the volume simultaneously.

#### Reclaim Policies
When a user deletes a PVC, what happens to the underlying PV and data?
- `Retain`: The PV becomes "Released" but is not deleted. The data remains. An admin must manually reclaim it. (Production default for critical data).
- `Delete`: The PV and the underlying cloud storage are automatically deleted. (Common for dynamic provisioning).
- `Recycle`: Deprecated. Performs a basic scrub (`rm -rf /thevolume/*`) and makes it available again.

#### Volume Lifecycle
1. **Provisioning**: Static or Dynamic creation of PV.
2. **Binding**: Control plane matches a PVC to a suitable PV and binds them exclusively.
3. **Using**: Pods mount the PVC as a volume.
4. **Releasing**: PVC is deleted. PV enters Released state.
5. **Reclaiming**: Based on Reclaim Policy, PV is retained, deleted, or scrubbed.

---

### 2. StorageClass Deep Dive

The `StorageClass` provides a way for administrators to describe the "classes" of storage they offer.

#### Parameters
Different provisioners accept different parameters. For `kubernetes.io/aws-ebs`, you might specify `type: gp3`, `iopsPerGB: "10"`, etc. For `kubernetes.io/gce-pd`, you might specify `type: pd-ssd`.

#### `volumeBindingMode`
- `Immediate`: (Legacy default). As soon as a PVC is created, a PV is dynamically provisioned and bound. **Problem:** It provisions the volume before knowing which node the pod will be scheduled on. If the volume is created in AZ `us-east-1a` but the pod can only run in `us-east-1b` (e.g., due to CPU constraints), the pod will stay Pending forever.
- `WaitForFirstConsumer`: (Production default). Delays the provisioning and binding of a PV until a Pod using the PVC is created. This ensures the storage is provisioned in the same AZ as the Node where the Pod is scheduled.

#### `allowVolumeExpansion`
Set this to `true` to allow users to resize volumes by editing the PVC's storage request.

#### Complete StorageClass YAML (AWS EBS gp3)
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
```
**Line-by-line explanation:**
- `apiVersion: storage.k8s.io/v1` and `kind: StorageClass`: Defines the object type.
- `metadata.name: ebs-sc`: The name used by PVCs to reference this class.
- `provisioner: ebs.csi.aws.com`: The CSI driver responsible for provisioning.
- `volumeBindingMode: WaitForFirstConsumer`: Wait for pod scheduling before creating the disk.
- `allowVolumeExpansion: true`: Allows increasing the PVC size later.
- `reclaimPolicy: Delete`: Delete the EBS volume when PVC is deleted.
- `parameters`: AWS-specific configs (gp3, 3000 IOPS, 125 MB/s).

#### Complete StorageClass YAML (Local Storage)
Local storage utilizes disks attached directly to the node.
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```
- `provisioner: kubernetes.io/no-provisioner`: Local volumes don't support dynamic provisioning.
- `volumeBindingMode: WaitForFirstConsumer`: Extremely important for local storage so the pod gets scheduled on the node that actually has the local volume!

#### Interview Q&A
**Q: "What is the difference between Immediate and WaitForFirstConsumer binding mode?"**
**A:** `Immediate` creates the cloud volume the moment the PVC is created, which may result in a zone mismatch if the pod is later scheduled to a different Availability Zone. `WaitForFirstConsumer` delays volume provisioning until the scheduler picks a node for the pod, ensuring the volume is created in the exact same zone as the chosen node.

---

### 3. CSI (Container Storage Interface)

CSI is a standard that allows third-party storage providers to write plugins for Kubernetes without having to merge their code into the core Kubernetes repository (out-of-tree plugins).

#### CSI Components
- **external-provisioner**: Watches for PVCs and calls the CSI driver to create the volume.
- **external-attacher**: Watches for VolumeAttachments and calls the driver to attach the volume to a node.
- **external-resizer**: Watches for PVC size updates and expands the volume.
- **node-plugin (DaemonSet)**: Runs on every node, formats the block device, and mounts it to the pod's directory.

#### Dynamic Provisioning Step-by-Step
1. User creates PVC requesting `StorageClass: ebs-sc`.
2. Pod is created referencing the PVC.
3. Scheduler assigns Pod to Node `worker-1` in `AZ-1a`.
4. The `external-provisioner` sees the PVC and scheduled Pod. It calls the CSI plugin via gRPC `CreateVolume`.
5. The CSI plugin (aws-ebs-csi-driver) calls AWS API to create an EBS volume in `AZ-1a`.
6. A PV is automatically created in k8s and bound to the PVC.
7. The `external-attacher` calls `ControllerPublishVolume` to attach the EBS volume to the EC2 instance `worker-1`.
8. The `kubelet` on `worker-1` sees the attached volume.
9. `kubelet` calls the CSI node-plugin via `NodeStageVolume` (mount device globally) and `NodePublishVolume` (bind mount into pod).

#### Troubleshooting
- **PVC stuck in Pending**: Check if the StorageClass exists and spelling is correct. If `WaitForFirstConsumer` is used, the PVC will stay Pending until a Pod uses it.
- **Pod stuck in ContainerCreating, Volume not attaching**: Check `kubectl describe pod <pod-name>`. Look for `Multi-Attach error` (RWO volume already attached to another node). Check the CSI controller pod logs (`kubectl logs -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver`).

---

### 4. Volume Snapshots

Volume snapshots let you create a copy of your volume at a specific point in time.

#### Objects
- `VolumeSnapshotClass`: Like StorageClass, defines the driver and parameters for taking snapshots.
- `VolumeSnapshot`: The user's request to take a snapshot of a specific PVC.
- `VolumeSnapshotContent`: The actual snapshot resource in the cluster (analogous to a PV).

#### Complete YAML: Taking a Snapshot
```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: my-db-snapshot
spec:
  volumeSnapshotClassName: csi-aws-vsc
  source:
    persistentVolumeClaimName: my-db-pvc
```
- `volumeSnapshotClassName`: The class defining how to snapshot.
- `source.persistentVolumeClaimName`: The PVC we are snapshotting.

#### Complete YAML: Restoring from a Snapshot
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restored-db-pvc
spec:
  storageClassName: ebs-sc
  dataSource:
    name: my-db-snapshot
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
```
- `dataSource`: Tells Kubernetes to populate this new PVC with the data from the snapshot.

#### Production Use Case
Before applying a major database schema migration (e.g., PostgreSQL upgrade), trigger a VolumeSnapshot. If the migration fails, delete the PVC and Pod, and recreate them using the snapshot as a dataSource to achieve near-instant rollback.

---

### 5. Stateful Application Patterns

Stateful applications require data persistence.

#### PostgreSQL on Kubernetes (StatefulSet)
A `StatefulSet` provides unique identities to its pods (`db-0`, `db-1`) and guarantees ordered deployment and scaling. It uses `volumeClaimTemplates` to provision a unique PVC for each pod.

#### Why Databases on K8s is Controversial
**Cons:**
- Databases rely heavily on predictable disk I/O. K8s introduces networking overhead (CNI, kube-proxy).
- Complex to manage HA, failover, and backups natively with basic K8s objects.
- Cloud managed services (RDS, Cloud SQL) are far easier to operate.

**When it's OK:**
- Using modern Kubernetes Operators.
- Multi-cloud or on-prem deployments avoiding vendor lock-in.

#### Operator Pattern
Operators encapsulate human operational knowledge into software. A Postgres Operator (like CrunchyData or Zalando) automatically handles:
- Provisioning Master/Replica pods.
- Setting up streaming replication.
- Performing leader election and failover on node crash.
- Taking continuous backups (WAL archiving) to S3.

---

## PART B: SCHEDULING

### 6. Kubernetes Scheduler Deep Dive

The `kube-scheduler` is responsible for finding the best Node for a newly created Pod.

#### Scheduler Phases
1. **PreFilter**: Check pod requirements (e.g., check if a requested PV exists).
2. **Filter**: Filter out nodes that cannot run the pod.
3. **PostFilter**: If no nodes remain, attempt to preempt (evict) lower-priority pods.
4. **PreScore**: Prepare data for scoring.
5. **Score**: Rank the remaining valid nodes.
6. **Reserve**: Assume the pod is scheduled on the highest-ranking node (cache the assignment).
7. **Permit**: Wait for external conditions (e.g., Dynamic Provisioning of volumes).
8. **PreBind**: Mount volumes, attach networks.
9. **Bind**: Update the API Server with the `nodeName`.
10. **PostBind**: Cleanup / notification phase.

#### Filter Plugins (Hard Constraints)
- `NodeResourcesFit`: Does the node have enough free CPU/RAM?
- `NodeAffinity`: Do the node labels match the pod's `nodeSelector`/`nodeAffinity`?
- `TaintToleration`: Does the pod tolerate all taints on the node?
- `PodTopologySpread`: Would placing the pod here violate spread constraints?
- `VolumeBinding`: Does the node belong to the same AZ as the PV?

#### Score Plugins (Soft Constraints)
- `NodeResourcesBalancedAllocation`: Favors nodes whose CPU/Memory fraction used will be balanced after placing the pod.
- `LeastAllocated`: Favors nodes with the most free resources.
- `ImageLocality`: Favors nodes that already have the container image pulled.

#### ASCII Scheduler Flowchart
```text
[ Pod Creation ] --> API Server --> [ Scheduler Queue ]
                                         |
                                         v
                            +-------------------------+
                            | 1. Filter Phase         |
                            | (Find feasible nodes)   |
                            +-------------------------+
                                         |
                       Nodes: [Node A, Node C] (Node B rejected)
                                         |
                            +-------------------------+
                            | 2. Score Phase          |
                            | (Rank feasible nodes)   |
                            +-------------------------+
                                         |
                       Node A: 95/100, Node C: 60/100
                                         |
                            +-------------------------+
                            | 3. Bind Phase           |
                            | (Assign to highest)     |
                            +-------------------------+
                                         |
                              API Server Updated:
                              Pod.Spec.NodeName = Node A
```

#### Interview Q&A
**Q: "How does the scheduler decide which node to place a pod on?"**
**A:** It uses a two-step process: Filtering and Scoring. In the Filtering phase, it eliminates nodes that cannot physically run the pod due to insufficient resources, mismatched node selectors, intolerable taints, or volume zone mismatches. In the Scoring phase, it ranks the remaining nodes using plugins like `LeastAllocated` and `ImageLocality`. The pod is bound to the node with the highest score.

---

### 7. Node Affinity and Node Selectors

These tools allow you to constrain a pod to only run on specific nodes based on labels.

#### nodeSelector
Simple, fast, exact key-value match.
```yaml
nodeSelector:
  disktype: ssd
```

#### nodeAffinity
More expressive than `nodeSelector`.
- `requiredDuringSchedulingIgnoredDuringExecution`: Hard requirement. The pod *must* match.
- `preferredDuringSchedulingIgnoredDuringExecution`: Soft requirement. The scheduler *tries* to match, but will schedule elsewhere if impossible.

#### Complete YAML: Node Affinity
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ml-job
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: instance-type
            operator: In
            values:
            - gpu-large
            - gpu-xlarge
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
          - key: cloud.google.com/gke-spot
            operator: Exists
  containers:
  - name: ml-container
    image: my-ml-app:1.0
```
**Explanation:**
- `required...`: The pod MUST run on nodes labeled `instance-type=gpu-large` OR `instance-type=gpu-xlarge`.
- `operator: In`: Logical OR. Other operators include `NotIn`, `Exists`, `DoesNotExist`, `Gt` (Greater than), `Lt` (Less than).
- `preferred...`: If multiple GPU nodes exist, prefer nodes that have the label `cloud.google.com/gke-spot` (with a weight of 100).
- `IgnoredDuringExecution`: If the node's labels change *after* the pod is scheduled, the pod is NOT evicted.

#### Production Use Case
Running CI/CD runners on preemptible (Spot) instances to save cost, while ensuring production databases run on reliable On-Demand instances.

#### Interview Q&A
**Q: "What is the difference between nodeSelector and nodeAffinity?"**
**A:** `nodeSelector` is an older, simpler feature that only supports exact key-value matches (AND logic). `nodeAffinity` is highly expressive, supporting soft preferences, logical operators (In, NotIn, Exists), and multiple selector terms.

---

### 8. Pod Affinity and Anti-Affinity

Constraints based on labels of pods *already running* on nodes, rather than node labels.

- `podAffinity`: "Place this pod on the same node/zone as pod X." (Useful for colocating frontend and cache).
- `podAntiAffinity`: "DO NOT place this pod on the same node/zone as pod X." (Crucial for High Availability).

#### TopologyKey
The `topologyKey` defines the boundary of the rule.
- `kubernetes.io/hostname`: The rule applies at the Node level.
- `topology.kubernetes.io/zone`: The rule applies at the Availability Zone level.

#### Complete YAML: Pod Anti-Affinity (HA Deployment)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: web
            topologyKey: kubernetes.io/hostname
      containers:
      - name: web
        image: nginx:1.19
```
**Explanation:**
- `podAntiAffinity`: We want to avoid other pods.
- `required...`: Hard requirement.
- `matchLabels: app: web`: Look for other pods belonging to this deployment.
- `topologyKey: kubernetes.io/hostname`: The boundary is the node.
**Result:** The 3 replicas will strictly be scheduled on 3 *different* nodes. If only 2 nodes exist in the cluster, the 3rd pod will remain Pending.

#### Interview Q&A
**Q: "How do you ensure your 3 replicas never land on the same node?"**
**A:** Use `podAntiAffinity` with a `requiredDuringSchedulingIgnoredDuringExecution` rule. Set the `labelSelector` to match the pod's own labels, and set the `topologyKey` to `kubernetes.io/hostname`.

---

### 9. Taints and Tolerations

Taints and tolerations work together to ensure pods are not scheduled onto inappropriate nodes.

- **Taint:** Applied to a NODE. It repels pods. ("No pod can run here unless it explicitly tolerates this taint.")
- **Toleration:** Applied to a POD. It acts as a key to bypass a taint.

#### Taint Effects
- `NoSchedule`: The scheduler will not place new pods here, but existing pods are left alone.
- `PreferNoSchedule`: Soft version of NoSchedule.
- `NoExecute`: The scheduler will not place new pods here AND will immediately evict any running pods that do not have the toleration.

#### Built-in Taints
Kubernetes automatically applies taints in bad conditions:
- `node.kubernetes.io/not-ready:NoExecute`
- `node.kubernetes.io/unreachable:NoExecute`
- `node.kubernetes.io/memory-pressure:NoSchedule`

#### Complete YAML: Taint and Toleration
**Command to taint the node:**
`kubectl taint nodes gpu-node-1 accelerator=nvidia-tesla:NoSchedule`

**Pod YAML to tolerate the taint:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-workload
spec:
  containers:
  - name: cuda
    image: nvidia/cuda:11.0-base
  tolerations:
  - key: "accelerator"
    operator: "Equal"
    value: "nvidia-tesla"
    effect: "NoSchedule"
```
**Explanation:**
- `key`, `value`, `effect`: Must perfectly match the taint.
- `operator: Equal`: The value must match. You can also use `Exists` to match any value for that key.

#### Production Use Case
Tainting dedicated GPU nodes so standard web apps don't accidentally get scheduled on them, wasting expensive resources.

#### Interview Q&A
**Q: "What is the difference between NoSchedule and NoExecute?"**
**A:** `NoSchedule` only affects *new* pods being scheduled; existing pods on the node are unaffected. `NoExecute` affects new pods AND aggressively evicts any currently running pods on the node that lack the corresponding toleration.

---

### 10. Topology Spread Constraints

A modern, highly flexible way to control pod distribution, superseding basic Anti-Affinity. It allows you to spread pods evenly across a cluster, rather than strictly rejecting placement.

#### Parameters
- `maxSkew`: The maximum allowed difference in pod count between any two topology domains (e.g., zones).
- `topologyKey`: The domain to spread across (zone, node).
- `whenUnsatisfiable`: What to do if the `maxSkew` can't be maintained.
  - `DoNotSchedule` (Hard)
  - `ScheduleAnyway` (Soft)
- `labelSelector`: Which pods to include in the counting calculation.

#### Complete YAML: Spread across AZs
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 6
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels:
            app: api
      containers:
      - name: api
        image: api:v2
```
**Explanation:**
- If you have 3 AZs and 6 replicas, the scheduler guarantees exactly 2 pods per AZ.
- `maxSkew: 1`: No zone can have >1 more pod than any other zone. (e.g., 3,2,1 is allowed. 4,1,1 is blocked).
- `whenUnsatisfiable: DoNotSchedule`: Ensures strict balance.

#### Interaction with Anti-Affinity
You can combine both! Use `topologySpreadConstraints` for Zone-level spreading (to balance across datacenters) and `podAntiAffinity` for Node-level spreading (to ensure HA within the datacenter).

---

### 11. Priority Classes and Preemption

What happens when your cluster is completely full, and a critical system component (like `coredns`) needs to scale up? Without Priority Classes, it stays Pending.

#### PriorityClass
A cluster-scoped object that maps a name to an integer value. Higher values = higher priority.

#### Preemption
If a high-priority pod is Pending, the scheduler will attempt to "preempt" (evict) lower-priority pods to make room for it.

#### Complete YAML: PriorityClass
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-app
value: 1000000
globalDefault: false
description: "Used for production revenue-generating services."
preemptionPolicy: PreemptLowerPriority
```
**Explanation:**
- `value: 1000000`: Arbitrary number. Kubernetes default pods are `0`.
- `globalDefault: false`: If true, all pods without a priority class get this value.
- `preemptionPolicy: PreemptLowerPriority`: The default. Can be set to `Never` if you want the pod to schedule before others in the queue, but NOT evict running pods.

**System Priorities:**
K8s reserves `system-node-critical` (2,000,001,000) and `system-cluster-critical` (2,000,000,000) for control plane components.

---

### 12. Pod Disruption Budget (PDB)

PDB limits the number of pods of a replicated application that are down simultaneously from **voluntary disruptions**.

#### Voluntary vs Involuntary
- **Involuntary**: Hardware failure, kernel panic, out-of-memory (OOM) kill. *PDB cannot prevent this.*
- **Voluntary**: `kubectl drain` for node upgrades, changing deployment replicas, Eviction API. *PDB prevents/delays this.*

#### Complete YAML: PDB
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: api
```
**Explanation:**
- `minAvailable: 2`: Kubernetes guarantees that at least 2 pods with `app: api` will always be running during voluntary disruptions.
- Alternatively, you can use `maxUnavailable: 1` (usually preferred as percentages, e.g., `maxUnavailable: 20%`).

#### The PDB Deadlock
If you set `minAvailable: 1` and your deployment only has 1 replica in total, `kubectl drain` will hang FOREVER. The system sees 1 pod running, knows it must maintain 1 pod, and therefore refuses to evict it.

#### Interview Q&A
**Q: "If my PDB says `minAvailable: 2` and I have 3 pods, how many can I drain simultaneously?"**
**A:** One. If you have 3 pods, you can safely evict 1 pod, leaving 2 pods running, which exactly meets the `minAvailable: 2` constraint. The node drain will wait until the evicted pod is recreated on another node before evicting further.

---

## PART C: AUTOSCALING

### 13. HPA (Horizontal Pod Autoscaler)

The HPA scales the number of replicas in a Deployment/StatefulSet based on observed metrics.

#### Internal Algorithm
Every 15 seconds (controlled by `--horizontal-pod-autoscaler-sync-period`), the `kube-controller-manager` checks metrics.
`desiredReplicas = ceil[currentReplicas * ( currentMetricValue / desiredMetricValue )]`

*Example:* Current replicas = 2. Current CPU = 100%. Desired CPU = 50%.
`desiredReplicas = ceil[2 * (100 / 50)] = 4 replicas.`

#### Stabilization Windows
Scaling up should be fast to handle load spikes. Scaling down should be slow to prevent "thrashing" (rapidly scaling up and down due to metric jitter).
- **Scale-Up Window**: Default 0s. (React instantly).
- **Scale-Down Window**: Default 300s (5 minutes). HPA waits 5 minutes after a peak before tearing down pods.

#### Complete YAML: HPA v2 (CPU + Custom Metric)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: External
    external:
      metric:
        name: sqs_queue_length
      target:
        type: AverageValue
        averageValue: 30
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```
**Explanation:**
- `scaleTargetRef`: Points to the Deployment to scale.
- `metrics.type: Resource`: Standard CPU check (keep average at 70%).
- `metrics.type: External`: Uses Custom Metrics API (e.g., via KEDA or Prometheus Adapter) to check AWS SQS queue length.
- `behavior.scaleDown`: The asymmetric 5-minute delay for scaling down.

#### Troubleshooting
- **HPA stuck at `<unknown>`**: Metrics-server is not installed, or the pod doesn't have CPU `requests` defined (HPA calculates utilization based on requests!).

---

### 14. VPA (Vertical Pod Autoscaler)

Instead of adding more pods, VPA adds more CPU/RAM to existing pods.

#### Components
- **Recommender**: Analyzes historical Prometheus/metrics-server data and calculates recommended CPU/RAM.
- **Updater**: Evicts running pods if their current resources differ significantly from recommendations.
- **Admission Plugin (Mutating Webhook)**: When the evicted pod is recreated, this webhook intercepts the creation and injects the new CPU/RAM values.

#### Modes
- `Off`: Only provides recommendations. Great for sizing new workloads.
- `Initial`: Only applies sizes when pods are first created.
- `Auto`: Will aggressively evict and resize running pods.

#### Complete YAML: VPA
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind:       Deployment
    name:       my-app
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: '*'
        minAllowed:
          cpu: 100m
          memory: 50Mi
        maxAllowed:
          cpu: 4000m
          memory: 4Gi
```
**Explanation:**
- `updateMode: "Auto"`: The Updater will evict pods to resize them.
- `minAllowed` / `maxAllowed`: Safety guardrails to prevent the VPA from giving a single pod the entire cluster's memory or shrinking it to zero.

#### Interview Q&A
**Q: "Can you run HPA and VPA on the same deployment?"**
**A:** Generally, NO, if they are using the same metric (like CPU). They will conflict. VPA will try to increase the CPU limit, causing CPU utilization to drop, which causes HPA to scale down replicas. You *can* use them together if HPA scales on a custom metric (like Request/sec) and VPA scales on CPU/Memory.

---

### 15. Cluster Autoscaler (CA)

While HPA/VPA scale pods, Cluster Autoscaler scales the physical/virtual Nodes.

#### How it Works
**Scale-Up:** CA watches for pods in the `Pending` state. If a pod is pending due to `Insufficient cpu/memory` or a nodeSelector mismatch, CA calls the Cloud Provider API (e.g., AWS Auto Scaling Group) to increase the desired node count.
**Scale-Down:** CA continuously checks node utilization. If a node is underutilized (default < 50% requested capacity) for a period (default 10 mins), CA verifies if the pods on that node can be moved. If yes, it cordons the node, evicts the pods, and terminates the cloud instance.

#### CA Limitations
CA is bound by Cloud Provider constructs (like AWS ASGs). An ASG must have nodes of identical size. If you need various instance types, you must manage dozens of ASGs and map them to CA.

#### Blocking Scale-Down
Certain pods block CA from removing a node:
- Pods with local storage (EmptyDir).
- Pods managed directly (no Deployment/ReplicaSet).
- Pods with strict PDBs.
- Pods in the `kube-system` namespace.
To force CA to ignore this, add the annotation: `cluster-autoscaler.kubernetes.io/safe-to-evict: "true"`.

---

### 16. Karpenter

Karpenter is an open-source node provisioning project built for Kubernetes, heavily championed by AWS, that bypasses Auto Scaling Groups entirely.

#### Why Karpenter replaces CA
- CA talks to ASGs. Karpenter talks directly to the EC2 Fleet API.
- **Just-In-Time Provisioning:** Karpenter looks at pending pods, evaluates their exact CPU, Memory, GPU, and architecture needs, and spins up the *exact right instance type* on the fly.
- **Consolidation:** Karpenter actively moves pods from fragmented nodes to smaller nodes to save costs.

#### Complete YAML: Karpenter NodePool
```yaml
apiVersion: karpenter.sh/v1beta1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64", "arm64"]
      nodeClassRef:
        name: default
  disruption:
    consolidationPolicy: WhenUnderutilized
    expireAfter: 720h # 30 days
```
**Explanation:**
- `requirements`: Karpenter is allowed to pick ANY instance type that is Spot or On-Demand, and AMD64 or ARM64. It will optimize for price and availability.
- `consolidationPolicy`: Continuously bin-pack pods to save money.
- `expireAfter`: Automatically recycle nodes every 30 days for security patching.

#### Interview Q&A
**Q: "What are the advantages of Karpenter over Cluster Autoscaler?"**
**A:** 1. Speed (provisions nodes in seconds by bypassing ASGs). 2. Flexibility (JIT instance selection based on pod requests instead of rigid ASG boundaries). 3. Advanced cost optimization through aggressive bin-packing and consolidation.

---

### 17. Resource Requests, Limits, and QoS

The bedrock of stability in Kubernetes.

#### Requests vs Limits
- **Requests:** Used by the Scheduler. "I guarantee this pod will get 500m CPU." The scheduler sums up requests to ensure a node isn't overbooked. Under the hood, this sets `cpu.shares` in Linux cgroups.
- **Limits:** The absolute ceiling. "This pod cannot exceed 1000m CPU." Under the hood, this sets `cpu.cfs_quota_us` in Linux cgroups.

#### The CPU Limit Debate
If a pod hits its CPU Limit, the Linux kernel **throttles** it. It pauses the application threads until the next quota period. This causes severe latency spikes in Java/Node.js apps, *even if the node has 80% free CPU*.
**Best Practice:** Set CPU Requests. Do NOT set CPU Limits (or set them very high). Let pods burst into unused CPU capacity.

#### The Memory Limit Reality
Memory is not compressible. If a pod hits its Memory Request, nothing happens. If a pod hits its Memory Limit, the Linux kernel invokes the `OOMKiller` (Out Of Memory) and instantly kills the container process.
**Best Practice:** Always set Memory Requests EQUAL to Memory Limits.

#### Quality of Service (QoS) Classes
Kubernetes assigns every pod a QoS class based on how you configure requests/limits. When a node runs out of memory, `kubelet` evicts pods based on this class.

1. **Guaranteed:** (Safest, last to be evicted)
   - Every container in the pod has CPU Request == CPU Limit AND Memory Request == Memory Limit.
2. **Burstable:** (Middle priority)
   - At least one container has a Request < Limit, or no limit is set for some resources.
3. **BestEffort:** (Most dangerous, first to be evicted)
   - No requests and no limits are set on any container.

#### Complete YAML: QoS Examples

**Guaranteed QoS:**
```yaml
containers:
- name: db
  resources:
    requests:
      memory: "4Gi"
      cpu: "2"
    limits:
      memory: "4Gi"
      cpu: "2"
```

**BestEffort QoS:**
```yaml
containers:
- name: random-script
  resources: {} # Blank! Will be killed immediately on node pressure.
```

#### Interview Q&A
**Q: "What is the difference between CPU throttling and OOMKill?"**
**A:** CPU throttling occurs when a container exceeds its CPU limit; the application isn't killed, but its execution is paused/slowed down by the kernel, causing latency. OOMKill occurs when a container exceeds its Memory limit; because memory cannot be throttled, the Linux kernel immediately terminates the process with Exit Code 137.

---

## END OF CHAPTER

### Scaling Decision Tree
- Need more instances of my application to handle traffic? **-> HPA**
- My application is single-threaded or needs a massive memory heap? **-> VPA**
- My pods are stuck in Pending state due to lack of resources? **-> CA or Karpenter**
- I want the fastest node scaling and cost optimization on AWS? **-> Karpenter**

### Scheduling Decision Tree
- Does the pod need specialized hardware (SSD/GPU)? **-> NodeSelector / NodeAffinity**
- Does the pod need to run near a database pod? **-> PodAffinity**
- Do the pods need to be highly available across different physical racks? **-> PodAntiAffinity / TopologySpreadConstraints**
- Do I need to keep standard pods away from my expensive GPU nodes? **-> Taints and Tolerations**

Keep this chapter handy. Mastering storage persistence, understanding the scheduler algorithm, and properly configuring autoscaling boundaries are the hallmarks of a Senior Kubernetes Engineer.
