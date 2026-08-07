# Chapter 2: Advanced Workloads and Networking

Welcome to Chapter 2 of the Kubernetes Mastery series. In this chapter, we will take a deep dive into advanced workloads and networking in Kubernetes. This is designed for engineers preparing for production environments and FAANG interviews. We'll explore the internal workings of components, real-world scenarios, complete YAML definitions, and how packets traverse the cluster.

---

## PART A: ADVANCED WORKLOADS

### 1. StatefulSet — Deep Internals

While `Deployment` is perfect for stateless applications like web servers, it is fundamentally unsuitable for stateful applications like databases (PostgreSQL, Cassandra, MongoDB) or distributed systems (Kafka, ZooKeeper). 

#### Why Deployment isn't enough for databases
1. **No Stable Network Identity:** Deployment pods get random names (e.g., `web-6b7d9b7f58-abcde`). When they restart, they get new names and new IPs. Distributed databases rely on peers having stable identities.
2. **No Ordered Operations:** Deployments scale up and down in parallel (or randomly). Databases often require a primary node to start before replicas can join.
3. **No Stable Storage:** Deployments typically share the same PersistentVolumeClaim (PVC) or rely on local storage. Databases need independent, dedicated storage for each instance.

#### StatefulSet Guarantees
StatefulSets solve these problems by providing:
1. **Stable Network Identity:** Pods are named sequentially (`pod-0`, `pod-1`, `pod-2`). This identity persists across rescheduling.
2. **Stable Storage:** Using `volumeClaimTemplates`, each pod automatically gets its own distinct PVC and PV. If `pod-1` crashes, it is recreated as `pod-1` and reattached to its exact same PVC.
3. **Ordered Deployment and Scaling:** Pods are created sequentially. `pod-0` must be in `Running` and `Ready` state before `pod-1` is created. Scaling down happens in reverse order.

#### The Headless Service
A StatefulSet requires a Headless Service (a Service with `clusterIP: None`) to control the network domain. 
Instead of load balancing traffic (like a regular ClusterIP), a Headless Service creates DNS A records for each pod in the StatefulSet.
The FQDN for a pod becomes: `{pod-name}.{headless-service-name}.{namespace}.svc.cluster.local`.
For example: `db-0.postgres-svc.default.svc.cluster.local`.

```text
       +-------------------+
       | Headless Service  | ---> Returns A Records
       | (clusterIP: None) |
       +-------------------+
          /      |      \
         /       |       \
    db-0       db-1      db-2
   (IP 1)     (IP 2)    (IP 3)
```

#### Complete Production StatefulSet YAML
Here is a complete, production-ready StatefulSet for a PostgreSQL-like stateful application.

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: database
  labels:
    app: postgres
spec:
  # The name of the Headless Service
  serviceName: "postgres-svc"
  replicas: 3
  # RollingUpdate ensures updates happen one by one (db-2, then db-1, then db-0)
  updateStrategy:
    type: RollingUpdate
  # OrderedReady is default. Parallel can be used if order doesn't matter (faster startup).
  podManagementPolicy: OrderedReady
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      # Anti-affinity ensures pods aren't scheduled on the same node
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - postgres
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: postgres
        image: postgres:14-alpine
        ports:
        - containerPort: 5432
          name: postgres
        # Liveness/Readiness probes are critical for OrderedReady to work
        readinessProbe:
          exec:
            command: ["pg_isready", "-U", "postgres"]
          initialDelaySeconds: 5
          periodSeconds: 10
        volumeMounts:
        - name: pg-data
          mountPath: /var/lib/postgresql/data
  # Dynamically provisions PVCs for each replica
  volumeClaimTemplates:
  - metadata:
      name: pg-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast-storage"
      resources:
        requests:
          storage: 50Gi
```

**Line-by-line breakdown:**
- `serviceName: "postgres-svc"`: Links the StatefulSet to the headless service for DNS creation.
- `updateStrategy: RollingUpdate`: Upgrades pods starting from the highest ordinal (db-2, db-1, db-0).
- `podManagementPolicy: OrderedReady`: `db-1` waits for `db-0` to be Ready.
- `podAntiAffinity`: A production best practice to prevent single-node failures from taking down the cluster.
- `volumeClaimTemplates`: Creates `pg-data-postgres-0`, `pg-data-postgres-1`, etc.

#### Troubleshooting
- **Pod stuck in Pending:** Check PVCs. Is the StorageClass valid? Are there enough PersistentVolumes available?
- **Pod-1 not starting:** Is `pod-0` Ready? If the readiness probe fails on `pod-0`, `pod-1` will never be created.

#### Interview Q&A
**Q:** Why can't you use a Deployment for a distributed database?
**A:** Deployments don't provide stable network identities or independent stable storage. If a database primary pod restarts, peers need to find it at the exact same DNS address, and it needs its exact data volume back. Deployments use random hashes for names and share volumes, leading to split-brain or data corruption.

---

### 2. DaemonSet — Deep Internals

A DaemonSet ensures that a copy of a specific Pod runs on *all* (or some matching) Nodes in the cluster.

#### How the DaemonSet Controller Works
Unlike Deployments which rely on the standard Scheduler to place pods on nodes, the DaemonSet controller actively monitors the cluster's Node list. 
- When a new node is added to the cluster, the DaemonSet controller detects it and creates a pod for that node.
- When a node is removed, the controller handles garbage collection.
- Historically (before 1.12), the DaemonSet controller bypassed the default scheduler entirely by directly setting the `nodeName` on the Pod object. Now, it uses NodeAffinity, allowing the default scheduler to place the pod while respecting other constraints (like taints and tolerations).

#### Use Cases
- **Logging/Monitoring:** Fluentbit, Filebeat, Datadog agents, Node Exporter.
- **Networking/Storage:** Calico/Cilium CNI pods, Kube-proxy, Ceph storage daemons.

#### Complete DaemonSet YAML
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentbit
  namespace: logging
  labels:
    app: fluentbit
spec:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      app: fluentbit
  template:
    metadata:
      labels:
        app: fluentbit
    spec:
      # Tolerations allow it to run on Master/Control-Plane nodes
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      - operator: Exists # Tolerate everything to ensure it runs EVERYWHERE
      # nodeSelector restricts it to specific nodes (optional)
      nodeSelector:
        env: production
      containers:
      - name: fluentbit
        image: fluent/fluent-bit:2.1
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      # HostPath mounts the actual node's filesystem into the pod
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

#### Interview Q&A
**Q:** How does a DaemonSet ensure a pod runs on every new node automatically?
**A:** The DaemonSet Controller constantly watches the Kubernetes API for Node events. When it sees a Node added that matches the DaemonSet's nodeSelector (or all nodes if none is specified), it dynamically generates a Pod manifest with a NodeAffinity rule binding it to that specific Node and submits it to the API.

---

### 3. Jobs and CronJobs

While Deployments are for long-running services, Jobs are for short-lived, run-to-completion tasks.

#### Job Types
1. **Non-Indexed Jobs:** A standard job. It runs pods until `completions` number of pods succeed.
2. **Indexed Jobs:** Each pod gets an index (0 to N-1) injected via the `JOB_COMPLETION_INDEX` environment variable, useful for batch processing where each pod processes a specific shard of data.

#### Key Parameters
- `completions`: How many total successful pods are needed to mark the Job as Complete.
- `parallelism`: How many pods can run simultaneously.
- `backoffLimit`: How many times the Job controller will retry a failed pod before marking the entire Job as Failed.
- `activeDeadlineSeconds`: Hard timeout for the Job. If it exceeds this, the system terminates it.

#### CronJob Deep Dive
A CronJob creates Jobs on a time-based schedule (standard cron format).
- `concurrencyPolicy`: 
  - `Allow` (default): If the previous job hasn't finished, start the next one anyway. (Beware: Can cause OOM or DB connection exhaustion!).
  - `Forbid`: Skip the new run if the old one is still running.
  - `Replace`: Kill the old running job and start the new one.
- `startingDeadlineSeconds`: If the CronJob controller is down and misses the schedule, it will look back this many seconds. If the deadline has passed, it skips the execution.

#### Complete CronJob YAML
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-db-backup
spec:
  # Runs at 2:00 AM every day
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      backoffLimit: 2 # Only retry twice on failure
      ttlSecondsAfterFinished: 86400 # Clean up job object after 1 day
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: pg-dump
            image: postgres:14-alpine
            command:
            - /bin/sh
            - -c
            - "pg_dump -U postgres -h db-svc > /backup/db.sql"
```

---

### 4. Init Containers

Init containers run to completion sequentially *before* any app containers start. 

#### Rules & Guarantees
- If an init container fails, the Pod restarts (depending on `restartPolicy`), and the init containers run *again*. Therefore, init container logic MUST be idempotent.
- They do not support `lifecycle`, `livenessProbe`, `readinessProbe`, or `startupProbe`.
- Resource Calculation: The Pod's effective resource request is the *maximum* of:
  - The highest request of all init containers.
  - The sum of the requests of all app containers.

#### Complete YAML (Wait for DB)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  initContainers:
  - name: wait-for-db
    image: busybox:1.28
    command: ['sh', '-c', "until nslookup postgres-svc; do echo waiting for postgres; sleep 2; done"]
  containers:
  - name: app
    image: my-web-app:1.0
```

---

### 5. Sidecar Containers (Kubernetes 1.29+)

Historically, sidecars were just regular containers running alongside the main app. This caused lifecycle issues (e.g., a Job would never Complete because the logging sidecar never exited).

In K8s 1.29+, Sidecars are officially supported as a special type of `initContainer` with `restartPolicy: Always`.

#### Lifecycle Guarantees
- They start sequentially with other init containers, but do not block subsequent containers from starting once they reach the `Started` state.
- During Pod termination, they are the *last* to receive SIGTERM, ensuring they can still route traffic/logs for the main container as it shuts down.

#### Complete Sidecar YAML
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  initContainers:
  - name: envoy-proxy
    image: envoyproxy/envoy:v1.28.0
    restartPolicy: Always # <--- This magic field makes it a native sidecar
  containers:
  - name: app
    image: my-app:1.0
```

---

### 6. Ephemeral Containers

Ephemeral containers are added dynamically to an already-running pod. They are meant strictly for debugging.
Since distroless images contain no shell (like `/bin/sh`), you cannot `kubectl exec` into them. Instead, you attach an ephemeral container (like busybox) that shares the process namespace of the distroless container.

**Command:**
```bash
kubectl debug -it web-pod --image=busybox --target=web-container
```

Because they are added dynamically, ephemeral containers cannot have ports, probes, or resource reservations.

---

### 7. Pod Lifecycle

#### Pod Phases
- **Pending:** Accepted by API, but not yet scheduled or pulling images.
- **Running:** Scheduled, at least one container is running.
- **Succeeded:** All containers exited with code 0.
- **Failed:** All containers terminated, at least one with non-zero code.

#### Termination Sequence
When a pod is deleted, Kubernetes initiates a graceful shutdown:
1. Pod state is set to `Terminating`.
2. Pod is removed from Service Endpoints (stops receiving new traffic).
3. `preStop` hook executes (if defined).
4. `SIGTERM` is sent to PID 1 in the container.
5. Kubernetes waits for `terminationGracePeriodSeconds` (default 30s).
6. If the container is still running, `SIGKILL` is sent, destroying the process forcefully.

*Why 30s is often not enough:* If your app takes 45 seconds to gracefully drain long-lived WebSockets or process queue messages, it will be forcefully killed at 30s. You must increase `terminationGracePeriodSeconds`.

---

## PART B: KUBERNETES NETWORKING — COMPLETE DEEP DIVE

### 8. The Kubernetes Networking Model

Kubernetes mandates a flat network model defined by three fundamental rules:
1. **Pod-to-Pod without NAT:** All pods can communicate with all other pods across the entire cluster without Network Address Translation.
2. **Node-to-Pod without NAT:** Agents on a node (like kubelet) can communicate with all pods on that node.
3. **Pod sees its own IP:** The IP that a pod sees itself having is the exact same IP that others see it having.

#### Internals: Network Namespaces
Linux Network Namespaces isolate networking stacks (interfaces, routing tables, iptables). Every pod gets its own network namespace.
To connect the pod's isolated namespace to the host, a `veth` (Virtual Ethernet) pair is created. It acts like a pipe: one end is inside the pod (`eth0`), the other is on the node's root namespace (e.g., `veth1234`).
The node end is attached to a Linux bridge (`cbr0` or `docker0`), connecting the pod to the wider network.

```text
+-----------------------+           +-----------------------+
| NODE 1                |           | NODE 2                |
|                       |           |                       |
| +-------------------+ |           | +-------------------+ |
| | POD A (10.1.1.2)  | |           | | POD B (10.1.2.2)  | |
| | eth0              | |           | | eth0              | |
| +--+----------------+ |           | +--+----------------+ |
|    | (veth pair)      |           |    | (veth pair)      |
| +--+----------------+ |           | +--+----------------+ |
| | vethA             | |           | | vethB             | |
| |     Bridge        | |           | |     Bridge        | |
| +-------+-----------+ |           | +-------+-----------+ |
|         |             |           |         |             |
|    eth0 (Node IP)     | <=======> |    eth0 (Node IP)     |
+-----------------------+  Overlay  +-----------------------+
```

---

### 9. CNI — Container Network Interface

Kubernetes itself does not implement networking; it delegates it to CNI plugins.
When a Pod is scheduled, the kubelet executes the CNI binary. The CNI provisions the network namespace, creates the veth pair, assigns an IP address, and configures routing.

#### Leading CNI Options
- **Flannel:** Very simple. Uses VXLAN to create an overlay network. Does NOT support NetworkPolicies.
- **Calico:** Production standard. Can use BGP for pure unencapsulated routing (very fast) or VXLAN. Fully supports NetworkPolicy.
- **Cilium:** Next-generation. Uses eBPF instead of iptables for extreme performance. Completely replaces kube-proxy. Offers L7 observability (Hubble).

#### VXLAN vs BGP
- **VXLAN (Overlay):** Encapsulates pod packets inside node UDP packets. Works on ANY network (cloud, on-prem), but adds overhead.
- **BGP (Underlay):** Routers natively understand pod IPs. No encapsulation overhead. Requires control over physical network hardware.

---

### 10. Services Deep Dive

Pods are ephemeral; their IPs change. Services provide a stable IP (ClusterIP) that load balances across a dynamic set of Pod IPs.

#### Service Types
1. **ClusterIP:** Default. Accessible only from within the cluster. kube-proxy writes iptables rules to perform Destination NAT (DNAT). When a pod pings `10.96.0.10`, iptables intercepts it and rewrites the destination IP to a pod IP `10.1.1.5`.
2. **NodePort:** Opens a port (30000-32767) on EVERY node's IP. Traffic hitting `NodeIP:NodePort` is SNAT/DNAT routed to the pod.
3. **LoadBalancer:** Provisions a cloud load balancer (AWS ALB, GCP TCP LB) that forwards traffic to NodePorts.
4. **ExternalName:** Creates a CNAME DNS record. Useful for mapping internal cluster names to external managed databases (e.g., AWS RDS).
5. **Headless:** `clusterIP: None`. No iptables rules. DNS returns the raw Pod IPs.

#### EndpointSlices
Historically, Services used `Endpoints` objects. If a Service had 1,000 pods, every time one pod restarted, the entire 1,000-IP list was updated and shipped to every kube-proxy, causing massive etcd and network strain.
`EndpointSlices` break this into smaller chunks (e.g., 100 IPs per slice), dramatically improving scalability.

#### Complete Service YAML
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-backend-svc
spec:
  type: ClusterIP
  # Session affinity routes the same client IP to the same pod
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 80        # The port the service exposes
    targetPort: 8080 # The port the container is listening on
```

---

### 11. Ingress Deep Dive

Services provide L4 (TCP/UDP) routing. Ingress provides L7 (HTTP/HTTPS) routing based on hostnames and paths.

#### Ingress vs Ingress Controller
- **Ingress:** Just a Kubernetes API object (a YAML file). It does nothing by itself.
- **Ingress Controller:** A running pod (like NGINX, Traefik). It reads Ingress objects from the API and dynamically reconfigures itself (e.g., updating `nginx.conf` and reloading).

#### Complete Production Ingress YAML
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  annotations:
    # Requires cert-manager to provision Let's Encrypt certs
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    # NGINX-specific annotations
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/limit-rps: "50"
spec:
  ingressClassName: nginx # Explicitly choose the controller
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls-secret
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /v1/users
        pathType: Prefix
        backend:
          service:
            name: users-svc
            port:
              number: 80
      - path: /v1/auth
        pathType: Exact
        backend:
          service:
            name: auth-svc
            port:
              number: 80
```

---

### 12. Gateway API

The Gateway API is the modern evolution of Ingress. Ingress became bloated with custom annotations because its spec was too simple. Gateway API provides native L7 routing and introduces Role-Based Access Control.

- **GatewayClass:** Managed by Cluster Admin. Defines the underlying infrastructure (e.g., AWS ALB).
- **Gateway:** Managed by Platform Team. Defines listeners and ports (e.g., listen on 443 with TLS).
- **HTTPRoute:** Managed by App Developers. Defines the actual path routing.

#### Complete HTTPRoute YAML
```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: store-route
  namespace: store
spec:
  parentRefs:
  - name: shared-gateway
    namespace: platform
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /checkout
    backendRefs:
    - name: checkout-svc
      port: 8080
      weight: 90 # Native Canary Deployments!
    - name: checkout-svc-v2
      port: 8080
      weight: 10
```

---

### 13. CoreDNS

CoreDNS runs as a Deployment in `kube-system`. It translates DNS requests from pods into Service IPs.

#### ndots:5 Configuration
When you run `cat /etc/resolv.conf` inside a pod, you will see `ndots:5`.
This means: If a DNS query contains fewer than 5 dots (e.g., `google.com`), CoreDNS will append the search domains first.
It will try:
1. `google.com.default.svc.cluster.local` (Fail)
2. `google.com.svc.cluster.local` (Fail)
3. `google.com.cluster.local` (Fail)
4. `google.com.ec2.internal` (Fail)
5. Finally: `google.com` (Success)
This causes massive DNS overhead. If an app makes high external calls, set `ndots:1` or `ndots:2` in the pod's `dnsConfig`.

---

### 14. Network Policies

Network policies implement zero-trust security inside the cluster. They are a whitelist mechanism. If no policy selects a pod, it allows all traffic. If a policy selects a pod, it **denies all traffic** except what is explicitly allowed.

#### Complete NetworkPolicy Example (Strict Isolation)
This policy secures a PostgreSQL database. It ONLY allows incoming traffic on port 5432 from pods labeled `app: backend`.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-postgres
  namespace: production
spec:
  # Target the database pod
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
  - Ingress # We are controlling incoming traffic
  ingress:
  - from:
    - podSelector: # Only allow from pods with this label
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432
```

---

### 15. Complete Packet Flow Diagram

How does a request travel from a user's browser to the database inside Kubernetes?

```text
1. [Browser] User types app.example.com
      |
      | (DNS Resolution via Route53)
      v
2. [Cloud Load Balancer] (External IP: 203.0.113.5)
      |
      | (Load Balancer forwards to Node IP on NodePort 32145)
      v
3. [Kubernetes Node eth0]
      |
      | (iptables SNAT/DNAT rules)
      v
4. [Ingress Controller Pod (NGINX)]
      |
      | (NGINX matches Host: app.example.com and Path: /)
      | (NGINX looks up Service ClusterIP for "backend-svc")
      v
5. [iptables / eBPF (kube-proxy)]
      |
      | (DNAT: 10.96.10.10 -> Pod IP 10.1.2.55)
      v
6. [CNI Network (Flannel/Calico)]
      |
      | (Overlay encap or BGP route to Target Node)
      v
7. [Target Node veth pair]
      |
      v
8. [Backend App Pod eth0]
      |
      | (App logic processes request, needs database)
      | (App queries "postgres-svc:5432")
      v
9. [CoreDNS] Resolves postgres-svc -> 10.96.20.20
      |
      v
10. [iptables (kube-proxy)] DNAT to Database Pod IP
      |
      v
11. [PostgreSQL Pod] -> Returns data back up the chain!
```

---

### 16. Network Troubleshooting Toolkit

1. **Verify Service Endpoints:**
   ```bash
   kubectl get endpoints frontend-svc
   # If output is <none>, your pod labels don't match the service selector, or pods are crashing.
   ```
2. **Test DNS from inside the cluster:**
   ```bash
   kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash
   nslookup backend-svc
   ```
3. **Test Connectivity:**
   ```bash
   curl -v http://backend-svc:8080
   ```
4. **Check iptables on Node (Advanced):**
   ```bash
   iptables -t nat -L KUBE-SERVICES | grep backend-svc
   ```

---

### Interview Q&A (Top 5 Networking)

1. **Explain exactly how a ClusterIP service routes traffic.**
   A ClusterIP is a virtual IP that exists only in iptables/IPVS rules on each node (managed by kube-proxy). When a pod sends a packet to the ClusterIP, the node's kernel intercepts it, randomly selects a healthy backend Pod IP from the EndpointSlice, and performs Destination NAT (DNAT).
   
2. **Why does a pod sometimes take 5 seconds to resolve a DNS name?**
   This is the classic Alpine Linux + `ndots:5` bug. Alpine's `musl libc` handles DNS resolution differently than `glibc`. When combined with K8s `ndots:5`, it attempts multiple failed DNS lookups simultaneously over IPv4 and IPv6. The DNS server drops packets to prevent DDoS, causing a 5-second timeout before the pod retries.

3. **How does NetworkPolicy work internally?**
   The Kubernetes API just stores the YAML. The actual enforcement is done by the CNI plugin (e.g., Calico). Calico reads the API and converts the NetworkPolicy into complex iptables chains or eBPF programs attached to the pod's `veth` interface, dropping unauthorized packets at the kernel level before they reach the container.

4. **What is the difference between LoadBalancer and NodePort?**
   NodePort opens a port on every Node's IP. LoadBalancer *includes* a NodePort, but additionally makes an API call to the cloud provider (AWS/GCP) to provision a physical/virtual Load Balancer outside the cluster, which then sends traffic to the NodePorts.

5. **Why use Gateway API over Ingress?**
   Ingress mixes all concerns (TLS, routing, infrastructure) into one object, making multi-tenant clusters hard to manage. Gateway API splits this into GatewayClass (Infra), Gateway (Ports/TLS), and HTTPRoute (Paths), allowing proper RBAC between Cloud Admins, Platform Teams, and Developers.

---
End of Chapter 2.
