# Chapter 7: Docker Mastery - Production Internals & Security

Welcome to Chapter 7 of the DevOps Mastery series. We are jumping straight into the deep end. You already know how to `docker build`, `docker run`, and write a basic `docker-compose.yml`. That's day one stuff. This chapter is about day two and beyond: how Docker *actually* works under the hood, how to build production-grade, secure, and optimized images, and how to debug containers when everything is on fire at 3 AM.

We will use the Feynman technique: we won't just learn *how* to do something, we will learn *why* it exists and *how* it works internally.

---

## SECTION 1: Docker Architecture Internals

### 1. Why it exists / problem it solves
In the early days of Docker (before version 1.11), the Docker Engine was a single massive monolith. The `dockerd` daemon handled everything: building images, pulling images, managing networks, volumes, and running the containers themselves.
If the daemon crashed or needed an update, all your running containers died. This was a nightmare for production.

To solve this, Docker split the architecture into specialized, decoupled components, donating the core runtime to the CNCF (Cloud Native Computing Foundation).

### 2. Internal working
Modern Docker architecture consists of four main layers:
1.  **Docker Client (`docker`)**: The CLI tool you type commands into. It sends REST API requests to the daemon.
2.  **Docker Daemon (`dockerd`)**: The API server. It handles image builds, volumes, networks, and routing requests to `containerd`.
3.  **`containerd`**: The container lifecycle manager. It pulls images, manages storage, and supervises containers via `containerd-shim`. It communicates with `dockerd` over gRPC.
4.  **`runc`**: The OCI (Open Container Initiative) compliant low-level runtime. Its *only* job is to create the container (namespaces, cgroups) using kernel features, start it, and exit.
5.  **`containerd-shim`**: Sits between `containerd` and the running container. It keeps the container's STDIN/STDOUT open so the daemon can be restarted without killing the container (daemonless containers).

### 3. ASCII architecture diagram

```text
+---------------------------------------------------+
|               Docker Client (CLI)                 |
|               (docker run ...)                    |
+---------------------------------------------------+
                         | REST API
+---------------------------------------------------+
|               Docker Daemon (dockerd)             |
|   (Builds, Networks, Volumes, API server)         |
+---------------------------------------------------+
                         | gRPC
+---------------------------------------------------+
|                 containerd                        |
|   (Image push/pull, Container lifecycle)          |
+---------------------------------------------------+
           |                          |
+----------------------+   +----------------------+
|  containerd-shim     |   |  containerd-shim     |
+----------------------+   +----------------------+
           |                          |
+----------------------+   +----------------------+
|       runc           |   |       runc           |
| (Creates container)  |   | (Creates container)  |
+----------------------+   +----------------------+
           |                          |
+----------------------+   +----------------------+
| Container Process    |   | Container Process    |
| (Namespaces, cgroups)|   | (Namespaces, cgroups)|
+----------------------+   +----------------------+
```

### 4. Production use case
At Google or Netflix, they don't run `dockerd` on their massive Kubernetes clusters. Because `containerd` was extracted and made independent, Kubernetes can talk *directly* to `containerd` (via the CRI - Container Runtime Interface), skipping `dockerd` entirely. This saves resources and reduces the attack surface.

### 5. Complete config/script (line-by-line explained)
You can manually interact with `containerd` bypassing Docker using the `ctr` CLI (mostly for debugging):

```bash
# 1. Pull an image directly using containerd
ctr images pull docker.io/library/nginx:alpine
# 2. Run a container named 'my-nginx' using the image
ctr run -d docker.io/library/nginx:alpine my-nginx
# 3. List running tasks (containers) in containerd
ctr tasks ls
```
*   Line 1: `ctr images pull` bypasses dockerd and pulls directly to containerd's storage.
*   Line 2: `ctr run` tells containerd to spin up a shim and invoke runc. `-d` is detached.
*   Line 3: Lists what's actually running at the containerd level.

### 6. Commands
*   `systemctl status docker`: See the daemon status.
*   `systemctl status containerd`: See the independent containerd service.

### 7. Common mistakes
*   Assuming `dockerd` runs the container processes. If `dockerd` is killed, containers continue running thanks to `containerd-shim`.

### 8. Best practices
*   Enable "Live Restore" in `/etc/docker/daemon.json` so that restarting `dockerd` (e.g., for updates) doesn't kill containers.

### 9. Troubleshooting
*   If Docker is hanging, check if `containerd` is responsive. They are separate processes.

### 10. Interview Q&A
**Q: "What is the difference between Docker, containerd, and runc?"**
**A:** Docker is the high-level platform (CLI, builds, API). `containerd` is the daemon that manages the container lifecycle (pulling images, execution). `runc` is the low-level CLI tool that actually interfaces with the Linux kernel to create the namespaces and cgroups, starts the process, and then exits.

---

## SECTION 2: Union File System and OverlayFS

### 1. Why it exists / problem it solves
If every container copied an entire 500MB Ubuntu OS to disk, starting 10 containers would take 5GB of storage. This is terribly inefficient. Union File Systems solve this by allowing multiple directories (layers) to be stacked on top of each other and appear as a single directory.

### 2. Internal working
A Docker image is a series of read-only layers. Each instruction in a Dockerfile (RUN, COPY, ADD) creates a new layer.
When you run a container, Docker adds a thin, read-write "container layer" on top of the image layers.

**OverlayFS (overlay2):**
*   **Lowerdir**: The read-only image layers.
*   **Upperdir**: The read-write container layer.
*   **Workdir**: Used by Linux to prepare files before moving them to the upperdir.
*   **Merged**: The unified view that the container actually sees.

**Copy-on-Write (CoW):**
If a container wants to modify a file that exists in a lower read-only layer, OverlayFS copies the file up to the `upperdir` (the writable layer) and modifies it there. The original file in the `lowerdir` is untouched.

**Whiteout files:**
If you delete a file in the container that exists in a lower layer, OverlayFS creates a "whiteout" file in the `upperdir`. The file isn't actually deleted from the lower layer (because it's read-only); the whiteout file just hides it in the `merged` view. This is why deleting a file in a later Dockerfile layer *doesn't* reduce the image size!

### 3. ASCII architecture diagram

```text
       +-----------------------------------------+
       |             Merged View                 | <--- What the container sees
       |          (/var/lib/mysql)               |
       +-----------------------------------------+
                           |
       +-----------------------------------------+
Upper  |       Writable Container Layer          | <--- (upperdir) Changes happen here
       | (e.g., modified file A, whiteout file B)|
       +-----------------------------------------+
                           |
       +-----------------------------------------+
Lower  |        Image Layer 3 (e.g., RUN ...)    | <--- Read-only
       +-----------------------------------------+
                           |
       +-----------------------------------------+
Lower  |        Image Layer 2 (e.g., COPY ...)   | <--- Read-only
       +-----------------------------------------+
                           |
       +-----------------------------------------+
Lower  |        Image Layer 1 (Base OS)          | <--- Read-only
       +-----------------------------------------+
```

### 4. Production use case
Because image layers are read-only, 100 Nginx containers on the same host share the exact same underlying image files on disk and in memory (page cache). This is how Uber scales thousands of microservices on a single node efficiently.

### 5. Complete config/script (line-by-line explained)
Let's inspect how Docker sees these layers:

```bash
docker inspect --format '{{json .GraphDriver}}' my-container | jq
```
*   `docker inspect`: Retrieves metadata.
*   `--format '{{json .GraphDriver}}'`: Extracts just the storage driver configuration and formats it as JSON.
*   `jq`: Pretty-prints the JSON.
*   Output will show `LowerDir` (colon-separated list of image layer paths), `UpperDir`, `WorkDir`, and `MergedDir`.

### 6. Commands
*   `docker history <image>`: See the layers of an image and their sizes.

### 7. Common mistakes
*   Doing `RUN apt-get install && rm -rf /var/lib/apt/lists/*` across *two different* RUN commands.
    *   `RUN apt-get install` (Creates Layer A, 50MB)
    *   `RUN rm -rf /var/lib/apt/lists/*` (Creates Layer B, adds whiteout files, Layer A remains 50MB. Net gain: 0 bytes saved).

### 8. Best practices
*   Always use `overlay2` storage driver (the default on modern Linux).
*   Chain commands in a single `RUN` layer using `&&` to clean up temporary files in the *same* layer they were created.

### 9. Troubleshooting
*   "No space left on device": Often caused by massive log files writing to the container layer (upperdir).

### 10. Interview Q&A
**Q: "Why does a Dockerfile instruction that deletes a file not reduce image size?"**
**A:** Because Docker uses a Union File System. Image layers are immutable (read-only). When you "delete" a file in a subsequent layer, the storage driver just creates a "whiteout" file in the new layer that hides the file in the merged view. The original file still exists in the lower layer, consuming disk space. To actually save space, the file creation and deletion must happen in the exact same `RUN` command.

---

## SECTION 3: Linux Namespaces and cgroups in Docker

### 1. Why it exists / problem it solves
Containers aren't VMs. They are just regular Linux processes. How do you prevent process A from seeing process B's files, killing its processes, or using 100% of the host's RAM?
The Linux kernel provides two mechanisms: **Namespaces** (for isolation/visibility) and **cgroups** (for resource limits). Docker is just a nice wrapper around these.

### 2. Internal working
**Namespaces (What a container can *see*):**
*   **PID**: Isolates process IDs. The container's init process is PID 1 inside, but PID 4321 on the host.
*   **NET**: Isolates network interfaces, IPs, and routing tables.
*   **MNT**: Isolates mount points (filesystems).
*   **UTS**: Isolates hostname and domain name.
*   **IPC**: Isolates inter-process communication (shared memory).
*   **USER**: Maps container root to an unprivileged host user (security).
*   **CGROUP**: Hides the host's cgroup hierarchy.
*   **TIME**: (New in kernel 5.6) Container can have its own system time.

**cgroups v2 (What a container can *use*):**
Control Groups limit CPU, Memory, Block I/O, and PIDs. When you run `docker run --memory 512m`, Docker translates this by writing "536870912" into a specific file in the Linux `/sys/fs/cgroup` virtual filesystem. The kernel enforces this limit.

### 3. ASCII architecture diagram

```text
Host OS (Linux Kernel)
+-------------------------------------------------------------------+
|                                                                   |
|   +-----------------------+           +-----------------------+   |
|   | Container A           |           | Container B           |   |
|   | Namespace: PID=1      |           | Namespace: PID=1      |   |
|   | Namespace: NET=eth0   |           | Namespace: NET=eth0   |   |
|   |                       |           |                       |   |
|   | cgroup: max RAM 1GB   |           | cgroup: max CPU 0.5   |   |
|   +-----------------------+           +-----------------------+   |
|                                                                   |
|   Kernel Namespaces (Isolation) & cgroups (Resource Limits)       |
+-------------------------------------------------------------------+
```

### 4. Production use case
If a Java container has a memory leak, cgroups ensure it hits its memory limit (OOM - Out of Memory) and is killed by the kernel *before* it crashes the entire host OS and takes down other containers.

### 5. Complete config/script (line-by-line explained)
Let's manually verify how Docker uses cgroups v2.

```bash
# 1. Run a container with a 100MB memory limit
docker run -d --name memtest --memory 100m nginx:alpine
# 2. Get the container ID
CID=$(docker inspect -f '{{.Id}}' memtest)
# 3. Read the cgroup v2 memory limit file directly from the host OS
cat /sys/fs/cgroup/system.slice/docker-${CID}.scope/memory.max
```
*   Line 1: We tell Docker to limit memory to 100MB.
*   Line 2: We grab the full 64-character container ID.
*   Line 3: We look at the virtual filesystem managed by the kernel. Docker created a scope for this container and wrote the limit there. The output will be `104857600` (100MB in bytes).

### 6. Commands
*   `lsns`: List all namespaces on the Linux host.
*   `systemd-cgtop`: Top-like tool for cgroups.

### 7. Common mistakes
*   Running a JVM (Java) inside a container without telling it about cgroup limits. Older JVMs look at the *host's* total RAM, try to allocate a heap that is too large, and instantly get OOMKilled by the kernel. (Modern Java 11+ respects cgroups automatically).

### 8. Best practices
*   Always set `--memory` and `--cpus` limits in production. Unbounded containers can starve the host OS.

### 9. Troubleshooting
*   If a container exits with code `137`, it means it was killed via SIGKILL (usually OOMKilled by the kernel due to hitting its cgroup memory limit). Check `docker inspect` for `OOMKilled: true`.

### 10. Interview Q&A
**Q: "How does Docker enforce memory limits?"**
**A:** Docker doesn't enforce limits; the Linux kernel does. Docker takes the `--memory` flag and writes that byte value into the `memory.max` (cgroup v2) or `memory.limit_in_bytes` (cgroup v1) file within the `/sys/fs/cgroup` virtual filesystem specific to that container's cgroup. The kernel's OOM killer monitors this and terminates the process if it exceeds the limit.

---

## SECTION 4: Image Optimization (Production Critical)

### 1. Why it exists / problem it solves
Large images (e.g., 2GB Node.js images) take forever to pull over the network, cost more in S3/ECR storage, and most importantly, have a massive attack surface. A large image contains curl, bash, compilers, and package managers—perfect tools for an attacker if they compromise your application.
Optimized images pull in seconds and contain *only* the compiled binary, dropping the attack surface to near zero.

### 2. Internal working
**Layer Caching:** Docker builds top-down. If a layer hasn't changed, it uses the cache. If a layer *has* changed, that layer and *every layer below it* must be rebuilt. Therefore, place commands that change frequently (like `COPY . .`) at the very bottom.
**Multi-stage builds:** Allow you to use a heavy image with compilers to build your app, and then `COPY` just the final binary into a tiny, empty image (`scratch` or `alpine`).

### 3. ASCII architecture diagram

```text
Multi-Stage Build Process:

Stage 1 (Builder): golang:1.21 (800MB)
[ Source Code ] -> [ go build main.go ] -> [ 'app' binary created ]
                                                  |
                                                  | (Only the binary is copied)
                                                  v
Stage 2 (Final): scratch (0MB)
[ Empty Filesystem ] -> [ 'app' binary added ] -> Final Image (15MB!)
```

### 4. Production use case
At Google, distroless images are heavily utilized. A distroless Python image contains the Python interpreter and your app—no shell (`/bin/sh`), no `apt`, no OS utilities.

### 5. Complete config/script (line-by-line explained)
Here is a production-grade multi-stage Dockerfile for a Go application using BuildKit cache mounts.

```dockerfile
# syntax=docker/dockerfile:1.4
# 1. Builder stage using a specific heavy image
FROM golang:1.21-alpine AS builder
# 2. Set working directory
WORKDIR /app
# 3. Copy only dependency files first to leverage layer caching
COPY go.mod go.sum ./
# 4. Download dependencies using BuildKit cache to speed up subsequent builds
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
# 5. Copy the rest of the source code (changes frequently)
COPY . .
# 6. Build the binary. CGO_ENABLED=0 ensures it's statically linked
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# 7. Final stage using distroless (no shell, highly secure)
FROM gcr.io/distroless/static:nonroot
# 8. Run as a non-root user (provided by the distroless image)
USER 65532:65532
# 9. Copy the binary from the builder stage
COPY --from=builder /app/main /main
# 10. Execute the binary directly (no shell wrap)
ENTRYPOINT ["/main"]
```
*   `# syntax=docker/dockerfile:1.4`: Enables BuildKit features.
*   Line 3/4: We copy `go.mod` and run `go mod download` *before* `COPY . .`. If we change `main.go`, layer 3 and 4 remain cached!
*   Line 4/6: `--mount=type=cache` tells BuildKit to keep a persistent cache directory on the host between builds. Massive speedup.
*   Line 7: Distroless static has no OS. It's essentially empty except for ca-certificates and timezone data.
*   Line 9: We pluck the compiled binary from the heavy `builder` stage. The final image size will be exactly the size of the binary (~10MB).

### 6. Commands
*   `DOCKER_BUILDKIT=1 docker build -t myapp .`: Force BuildKit (default in modern Docker).
*   `docker buildx build --platform linux/amd64,linux/arm64 -t myapp .`: Build for both Intel and Apple Silicon/AWS Graviton architectures simultaneously.

### 7. Common mistakes
*   Doing `COPY . .` *before* `RUN npm install`. This invalidates the `npm install` cache every time you change a CSS file, causing 5-minute builds instead of 5-second builds.
*   Leaving secrets in the Dockerfile (e.g., `ENV AWS_KEY=123`). This bakes the secret into the image layer forever. Use `--mount=type=secret` instead.

### 8. Best practices
*   Always use a `.dockerignore` file to exclude `.git`, `node_modules`, and local `.env` files from being sent to the Docker daemon build context.
*   Use specific tags (`node:18.16.0-alpine`) instead of `latest`.

### 9. Troubleshooting
*   If distroless containers crash, you cannot `docker exec -it <id> sh` because there is no `sh`. Use an ephemeral debug container: `docker debug <container_name>` (Docker Desktop) or `kubectl debug` in k8s.

### 10. Interview Q&A
**Q: "Explain multi-stage builds and why they are important."**
**A:** Multi-stage builds allow a single Dockerfile to use multiple `FROM` statements. You use a "builder" stage with all necessary compilers and SDKs to build your application. Then, you use a second, minimal `FROM` image (like alpine or scratch) and `COPY` only the final compiled artifact from the builder stage. This results in drastically smaller image sizes, faster pull times, and a significantly reduced security attack surface because build tools and shells are not included in the final production image.

---

## SECTION 5: Docker Networking Deep Dive

### 1. Why it exists / problem it solves
Containers are isolated in their own Network Namespaces. Without Docker networking, a container has no IP, no loopback, and cannot talk to the internet, the host, or other containers.

### 2. Internal working
**Default Bridge (`docker0`):**
When Docker starts, it creates a virtual Linux bridge interface called `docker0` on the host. When a container runs, Docker creates a `veth` (virtual ethernet) pair. One end goes into the container's network namespace (as `eth0`), and the other attaches to the `docker0` bridge.
Docker uses `iptables` (specifically the NAT table) to route traffic. When you use `-p 8080:80`, Docker adds a DNAT (Destination NAT) rule to `iptables` that says: "If traffic hits the host on port 8080, rewrite the destination IP to the container's IP on port 80".

**User-Defined Bridge Networks:**
The default bridge is legacy. If you create your own (`docker network create mynet`), Docker provides an embedded DNS server at `127.0.0.11` inside the container. This allows containers to resolve each other by container name (e.g., `curl http://backend:8080`). The default bridge does *not* have this DNS resolution.

### 3. ASCII architecture diagram

```text
Host OS
+-------------------------------------------------------------+
|                                                             |
|   Physical NIC (eth0: 192.168.1.50)                         |
|        |                                                    |
|     iptables (DNAT rule for port 8080 -> 172.17.0.2:80)     |
|        |                                                    |
|   docker0 Bridge (172.17.0.1)                               |
|        |                  |                                 |
|      vethA              vethB                               |
|        |                  |                                 |
| +------|------+    +------|------+                          |
| | Container 1 |    | Container 2 |                          |
| |  (eth0)     |    |  (eth0)     |                          |
| | 172.17.0.2  |    | 172.17.0.3  |                          |
| +-------------+    +-------------+                          |
+-------------------------------------------------------------+
```

### 4. Production use case
In Swarm or Kubernetes, an **Overlay Network** is used. It uses VXLAN encapsulation to create a virtual network spanning multiple physical servers, allowing a container on Node A to talk to a container on Node B as if they were on the same local switch.

### 5. Complete config/script (line-by-line explained)
Troubleshooting how a port mapping actually works under the hood.

```bash
# 1. Run a web server mapping host 8080 to container 80
docker run -d -p 8080:80 --name web nginx
# 2. View the iptables NAT rules Docker automatically created
sudo iptables -t nat -L DOCKER -n
# 3. View the embedded DNS configuration in a user-defined network
docker network create mynet
docker run --rm --net mynet alpine cat /etc/resolv.conf
```
*   Line 2: You will see a `DNAT` rule pointing TCP dpt:8080 to the container's IP (e.g., 172.17.0.2:80). This proves Docker networking relies heavily on Linux netfilter/iptables.
*   Line 3: The output will show `nameserver 127.0.0.11`, which is Docker's internal DNS resolver intercepting DNS queries.

### 6. Commands
*   `docker network create --driver bridge my-app-net`
*   `docker network inspect my-app-net`: See which containers are attached and their IPs.

### 7. Common mistakes
*   Trying to link containers using the default `bridge` network using IP addresses. IPs change on restart. Always create a user-defined network and use DNS names.

### 8. Best practices
*   Use `--network host` (Host networking) for high-performance applications like load balancers where bridging/NAT overhead is unacceptable. The container will use the host's actual network interfaces.

### 9. Troubleshooting
*   "Connection refused" between containers: Check if they are on the *same* user-defined network. Check if the destination service is actually listening on `0.0.0.0` inside its container, not just `127.0.0.1`.

### 10. Interview Q&A
**Q: "What is the difference between the default bridge network and a user-defined bridge network?"**
**A:** The main difference is DNS resolution. In a user-defined bridge network, Docker provides an embedded DNS server that allows containers to resolve each other by container name. On the default bridge, this automatic service discovery is disabled, and you have to rely on legacy `--link` flags or raw IPs. Additionally, user-defined networks provide better isolation.

---

## SECTION 6: Docker Volumes and Storage

### 1. Why it exists / problem it solves
Containers are ephemeral. When a container is deleted, its writable layer (upperdir) is destroyed. If you run a PostgreSQL database in a container and the container restarts, all your data is gone. Volumes provide persistent storage that exists outside the container's lifecycle.

### 2. Internal working
*   **Named Volumes:** Docker creates a directory on the host (usually `/var/lib/docker/volumes/`) and mounts it into the container. Docker completely manages this directory.
*   **Bind Mounts:** You specify an exact path on the host OS (e.g., `/home/user/code`) and mount it into the container.
*   **tmpfs:** Mounts a portion of the host's RAM into the container. Data is never written to disk. Great for sensitive secrets or high-performance temporary caches.

### 3. ASCII architecture diagram

```text
+-------------------------------------------------------+
|                       Host OS                         |
|                                                       |
|  /var/lib/docker/volumes/my_db/_data (Named Volume)   |
|         ^                                             |
|         | (Docker manages this)                       |
|         |                                             |
|  +------------------+                                 |
|  | Container (PG)   |                                 |
|  | /var/lib/postgresql/data                           |
|  +------------------+                                 |
|         |                                             |
|         | (Bind Mount)                                |
|         v                                             |
|  /home/developer/source_code (Bind Mount)             |
|                                                       |
+-------------------------------------------------------+
```

### 4. Production use case
Databases (MySQL, Mongo) in production containers *must* use Named Volumes. Developers writing code locally use Bind Mounts so that when they edit a file in VSCode on their Mac, the change instantly appears inside the running container.

### 5. Complete config/script (line-by-line explained)
Script to safely backup a named volume used by a database:

```bash
#!/bin/bash
VOLUME_NAME="postgres_data"
BACKUP_FILE="backup_$(date +%F).tar.gz"

# 1. Run an ephemeral alpine container, mount the volume, and mount a host dir
docker run --rm \
  -v ${VOLUME_NAME}:/volume-data:ro \
  -v $(pwd):/backup \
  alpine \
  tar -czf /backup/${BACKUP_FILE} -C /volume-data .

echo "Backup created at ./${BACKUP_FILE}"
```
*   Line 5: `docker run --rm` creates a temporary container that deletes itself upon exit.
*   Line 6: Mount the named volume `postgres_data` into `/volume-data` in the container, as Read-Only (`:ro`).
*   Line 7: Mount the current host directory into `/backup` in the container.
*   Line 9: Execute `tar` inside the container to compress the volume data and write it to the bind-mounted host directory.

### 6. Commands
*   `docker volume create my-vol`
*   `docker volume inspect my-vol`: Shows the exact path on the host (Mountpoint).

### 7. Common mistakes
*   Using bind mounts in production. It ties your container to a specific filesystem layout on a specific host node, breaking portability.
*   Not cleaning up volumes. `docker rm -v` deletes the volume with the container. Otherwise, volumes are left orphaned taking up disk space.

### 8. Best practices
*   Always use Named Volumes for production data. Use volume plugins (like Rex-Ray or AWS EFS drivers) if you need the volume to move between nodes in a cluster.

### 9. Troubleshooting
*   Permissions issues with bind mounts: If a file is owned by root on the host, a non-root user in the container can't read it. The UID/GID must match between host and container.

### 10. Interview Q&A
**Q: "When would you use a tmpfs mount?"**
**A:** You use a `tmpfs` mount when you have sensitive data, like database credentials or private keys, that the container needs to access, but you absolutely do not want that data to ever be written to the host's physical disk. It's stored entirely in memory and is destroyed as soon as the container stops.

---

## SECTION 7: Container Security

### 1. Why it exists / problem it solves
By default, the process inside a container runs as `root` (UID 0). Because the kernel is shared with the host, if an attacker breaks out of the container namespace (container escape), they are `root` on the host machine. You must lock down containers.

### 2. Internal working
*   **Capabilities:** Linux splits root privileges into ~40 distinct capabilities (e.g., `CAP_NET_BIND_SERVICE` allows binding ports < 1024, `CAP_SYS_ADMIN` is basically full root). Docker drops many by default, but you should drop them all and add back only what you need.
*   **Seccomp:** Secure Computing Mode. It's a kernel feature that restricts which system calls a process can make. Docker applies a default seccomp profile that blocks ~44 dangerous syscalls out of ~300.
*   **User Namespaces (Rootless Docker):** Maps the root user (UID 0) inside the container to an unprivileged user (e.g., UID 100000) on the host. Even if they escape, they are nobody on the host.

### 3. ASCII architecture diagram

```text
Security Layers in Depth:

[ Application Code ]
        |
[ Read-Only Filesystem (--read-only) ] -> Prevents downloading malware
        |
[ Non-Root User (USER 10001) ] -> Prevents system-level execution inside container
        |
[ Dropped Capabilities (--cap-drop ALL) ] -> Restricts kernel feature access
        |
[ Seccomp Profile ] -> Blocks malicious Linux system calls (e.g. ptrace)
        |
[ Host Kernel ]
```

### 4. Production use case
Financial institutions require automated image scanning in CI/CD. Before an image is deployed, Trivy scans the image layers for known CVEs (Common Vulnerabilities and Exposures). If a CRITICAL CVE is found, the build fails. Images are also cryptographically signed with Cosign.

### 5. Complete config/script (line-by-line explained)
Here is a highly secure, production-ready Dockerfile template.

```dockerfile
FROM alpine:3.18
# 1. Install necessary dependencies (e.g., curl)
RUN apk --no-cache add curl

# 2. Create a dedicated non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 3. Create app directory and set ownership
WORKDIR /app
RUN chown -R appuser:appgroup /app

# 4. Switch to the non-root user. ALL following commands run as appuser.
USER appuser

# 5. Copy application code (ensure it's owned by appuser)
COPY --chown=appuser:appgroup myapp.sh /app/

# 6. Run the application
ENTRYPOINT ["./myapp.sh"]
```
*   Line 4: This is the most important security line in any Dockerfile. If an attacker exploits your app, they land in a shell as an unprivileged user, vastly reducing the damage they can do.
*   Line 5: `--chown` ensures the copied files have the correct permissions so the non-root user can execute them.

Run command to maximize security:
```bash
docker run -d \
  --read-only \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  my-secure-image
```
*   `--read-only`: Mounts the container root filesystem as read-only.
*   `--cap-drop ALL`: Removes all root privileges.
*   `--security-opt no-new-privileges`: Prevents processes from gaining new privileges using `setuid` binaries.

### 6. Commands
*   `trivy image --severity CRITICAL myapp:latest`: Scan an image for critical vulnerabilities.
*   `cosign sign --key cosign.key myapp:latest`: Cryptographically sign an image.

### 7. Common mistakes
*   Running containers in `--privileged` mode. This disables all isolation, gives the container full access to all host devices, and bypasses seccomp/apparmor. It is a massive security risk.

### 8. Best practices
*   Integrate Trivy in your GitHub Actions pipeline.
*   Use "Rootless Docker" where the `dockerd` daemon itself runs as a non-root user on the host OS.

### 9. Troubleshooting
*   If your app fails to write logs or temp files when using `--read-only`, you must mount a `tmpfs` to the specific directories where writes are required: `--tmpfs /tmp --tmpfs /run`.

### 10. Interview Q&A
**Q: "How would you secure a Docker container in production?"**
**A:** First, build optimized images using multi-stage builds and distroless bases to reduce the attack surface. In the Dockerfile, create and switch to a non-root `USER`. Scan the image in CI/CD using Trivy. At runtime, run the container with `--read-only` root filesystem, drop all capabilities (`--cap-drop ALL`), and enforce `--security-opt no-new-privileges`. Finally, use user namespaces if possible to remap the container's root to an unprivileged host user.

---

## SECTION 8: Docker Compose Production Patterns

### 1. Why it exists / problem it solves
Docker CLI is imperative (run this, then run that). Docker Compose is declarative (Infrastructure as Code). It allows you to define complex, multi-container applications (app, database, cache, message queue) in a single YAML file, ensuring reproducible environments.

### 2. Internal working
Compose parses the `docker-compose.yml`, calculates the dependency graph (via `depends_on`), creates the required networks and volumes, and then uses the Docker Engine API to start the containers in the correct order.

### 3. ASCII architecture diagram

```text
docker-compose up -d
        |
        v
[ docker-compose.yml parsing ] --> Network "app-net" created
        |
        |--> Database Container Started
        |      |
        |      | (Healthcheck: pg_isready) --> Healthy!
        |      v
        |--> Backend Container Started (depends_on: db: condition: service_healthy)
        |      |
        |      v
        |--> Nginx Load Balancer Started
```

### 4. Production use case
While Kubernetes is standard for massive scale, single-node Docker Compose is incredibly popular for production deployments of self-hosted tools, internal APIs, or small startups. Using override files allows a single base config to adapt to Dev, Test, and Prod environments.

### 5. Complete config/script (line-by-line explained)
A production-ready Compose file leveraging health checks, resource limits, and secrets.

```yaml
version: '3.9'

services:
  api:
    image: my-backend:v1.2
    restart: unless-stopped
    depends_on:
      redis:
        condition: service_healthy
      postgres:
        condition: service_healthy
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - backend_net
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M

  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - pg_data:/var/lib/postgresql/data
    networks:
      - backend_net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

secrets:
  db_password:
    file: ./secrets/db_password.txt

volumes:
  pg_data:

networks:
  backend_net:
    driver: bridge
```
*   `restart: unless-stopped`: If the host reboots, this container will start automatically.
*   `depends_on: condition: service_healthy`: The API container will NOT start until Postgres is fully booted and accepting connections (based on the `healthcheck`). This prevents race conditions.
*   `secrets`: Reads a file from the host and mounts it into the container at `/run/secrets/db_password` as an in-memory `tmpfs` file. Highly secure.
*   `deploy.resources.limits`: Enforces cgroup limits directly via Compose.

### 6. Commands
*   `docker compose config`: Validates the YAML and prints the merged configuration (useful when using override files).
*   `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`: Merge configs.

### 7. Common mistakes
*   Using `depends_on` without `condition: service_healthy`. Standard `depends_on` only waits for the *container process* to start, not for the database to actually be ready to accept connections.

### 8. Best practices
*   Use `.env` files for environment-specific variables (like hostnames or feature flags), but use Docker Secrets for sensitive credentials.

### 9. Troubleshooting
*   If containers can't talk to each other, ensure they are on the same custom network defined in the `networks:` block at the bottom of the file.

### 10. Interview Q&A
**Q: "How do you manage configuration differences between Dev and Prod using Docker Compose?"**
**A:** I use multiple Compose files. A base `docker-compose.yml` defines the core services and images. Then, a `docker-compose.override.yml` (automatically read in dev) adds bind mounts for live-reloading and exposes ports to localhost. For production, I run `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`, where the prod file overrides restart policies, adds resource limits, and integrates proper logging drivers.

---

## SECTION 9: Docker Logging

### 1. Why it exists / problem it solves
In a distributed system, you can't SSH into 50 different containers to read log files. You need logs to be centralized. Docker manages the `stdout` and `stderr` streams of containers and routes them via Logging Drivers.

### 2. Internal working
By default, Docker uses the `json-file` logging driver. It captures `stdout`/`stderr` and writes them as JSON objects to `/var/lib/docker/containers/<id>/<id>-json.log`.
You can configure the Docker daemon to use other drivers like `awslogs` (CloudWatch), `fluentd`, or `syslog` to ship logs directly off the host without the container knowing.

### 3. ASCII architecture diagram

```text
[ Container App ]
   |
   | (Writes to STDOUT / STDERR)
   v
[ Docker Engine (dockerd) ]
   |
   +--> Logging Driver Configured?
          |
          |-- json-file (default) --> Local Disk (Subject to rotation)
          |
          |-- awslogs --> AWS CloudWatch
          |
          |-- fluentd --> ElasticSearch / Datadog
```

### 4. Production use case
An app outputs structured JSON logs to `stdout`. The Docker daemon is configured with the `fluentd` driver, which forwards the logs to a Fluent Bit sidecar, which parses them and ships them to Datadog for alerting.

### 5. Complete config/script (line-by-line explained)
Configure `/etc/docker/daemon.json` to prevent the default `json-file` driver from filling up the entire host disk (a very common production outage).

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```
*   `log-driver`: Set to `json-file`.
*   `max-size`: Once a log file hits 100MB, it is rotated.
*   `max-file`: Keep only 3 rotated files. Maximum log footprint per container is capped at 300MB. Without this, a chatty container will consume 100% of the host disk space.

### 6. Commands
*   `docker logs --follow --tail 100 --since 10m my-app`: Get real-time logs, last 100 lines, only from the last 10 minutes.
*   `docker logs -t my-app`: Add timestamps to the logs (useful if the app doesn't log timestamps).

### 7. Common mistakes
*   Writing logs to a file *inside* the container (e.g., `/var/log/nginx/access.log`). Docker cannot see these logs via `docker logs`, and they will bloat the container's writable layer until the disk is full. Applications in containers should *always* log to `stdout/stderr`.

### 8. Best practices
*   Applications must output Structured Logs (JSON). This makes parsing and querying logs in CloudWatch/Datadog trivial compared to regex parsing plain text.

### 9. Troubleshooting
*   If `docker logs` returns nothing, check if the application is buffering its standard output. For Python apps, set the environment variable `PYTHONUNBUFFERED=1`.

### 10. Interview Q&A
**Q: "A production host just crashed with 'No space left on device'. You find out Docker logs consumed all the space. How do you prevent this?"**
**A:** By default, the `json-file` logging driver keeps logs forever. I would configure the Docker daemon globally in `/etc/docker/daemon.json` to set `log-opts` with `max-size` (e.g., 50m) and `max-file` (e.g., 3) to enable log rotation. For enterprise production, I would change the log driver entirely to `fluentd` or `awslogs` to ship logs off the host completely.

---

## SECTION 10: Container Registry

### 1. Why it exists / problem it solves
Images built on a CI server need to be securely stored and distributed to production nodes. Registries (like Docker Hub, AWS ECR, Harbor) manage repositories of images, tag versioning, and access control.

### 2. Internal working
A registry stores two main things:
1.  **Blobs**: The actual compressed, hashed image layers.
2.  **Manifests**: JSON documents describing the image, listing the layer hashes, OS/Architecture details, and config.
When you `docker pull`, the daemon fetches the manifest first, checks which layer hashes it already has locally, and then downloads only the missing layer blobs.

### 3. ASCII architecture diagram

```text
[ CI Pipeline (GitHub Actions) ]
   |
   | 1. Build Image
   | 2. Tag (myapp:v1.2.3)
   | 3. docker push
   v
[ Private Registry (AWS ECR / Harbor) ]
   |  - Manifests (JSON)
   |  - Blobs (Compressed Layers)
   |  - Image Scanning (Trivy)
   |  - Role-Based Access Control (RBAC)
   v
[ Production Kubernetes / Docker Swarm ]
      (Pulls image securely via IAM roles)
```

### 4. Production use case
Large enterprises use an "Image Promotion Pipeline". Developers push to a `dev-registry`. QA tests it. If it passes, a CI job physically copies the immutable image from `dev-registry` to `prod-registry` and signs it with Cosign. Production nodes can *only* pull from `prod-registry` and *only* if the image has a valid signature.

### 5. Complete config/script (line-by-line explained)
Logging into AWS ECR and configuring a lifecycle policy.

```bash
# 1. Authenticate Docker CLI to AWS ECR using temporary STS credentials
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# 2. Tag local image for the registry
docker tag myapp:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0

# 3. Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp:v1.0
```

**ECR Lifecycle Policy (JSON):**
```json
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire untagged images after 1 day",
            "selection": {
                "tagStatus": "untagged",
                "countType": "sinceImagePushed",
                "countUnit": "days",
                "countNumber": 1
            },
            "action": { "type": "expire" }
        }
    ]
}
```
*   This policy is critical. Without it, every CI build pushes a new image, creating dangling untagged images that cost thousands of dollars in S3 storage over time. This automatically deletes them.

### 6. Commands
*   Use `docker-credential-helpers` to store registry passwords in macOS Keychain or Linux Secret Service instead of plain text in `~/.docker/config.json`.

### 7. Common mistakes
*   Relying on Docker Hub for production pulls without authentication. Docker Hub enforces strict rate limits (100 pulls / 6 hours). If a Kubernetes node scales up and hits this limit, your production deployment will fail with `TooManyRequests`. Always use authenticated pulls or a private registry/pull-through cache.

### 8. Best practices
*   Never use the `latest` tag in production. Images are mutable. `latest` today is not `latest` tomorrow. Always use semantic versioning (`v1.2.3`) or Git commit SHAs (`myapp:a1b2c3d`).

### 9. Troubleshooting
*   "unauthorized: authentication required": Ensure your token hasn't expired (AWS ECR tokens expire every 12 hours). Use a credential helper.

### 10. Interview Q&A
**Q: "Explain how Docker pulls an image and how registry rate limiting can break production."**
**A:** Docker pulls an image by first requesting the manifest from the registry, then pulling the compressed layer blobs in parallel. If using anonymous pulls from Docker Hub, they enforce an IP-based rate limit. In a cloud environment, many nodes might share the same NAT gateway IP. If Kubernetes triggers a scale-out event and tries to pull an image, it might hit the rate limit and fail to start containers. To prevent this, always authenticate with the registry, use a private registry like ECR, or configure a local Pull-Through Cache mirror.

---

## SECTION 11: Docker Debugging

### 1. Why it exists / problem it solves
Containers are black boxes. When an application crashes, hangs, or consumes 100% CPU, you need tools to introspect the namespaces, resource usage, and filesystem changes without destroying the state of the container.

### 2. Internal working
Docker CLI provides a suite of commands that query the Docker daemon API to fetch real-time cgroup metrics, inspect namespace configurations, and stream daemon events.

### 3. ASCII architecture diagram

```text
[ Debugging Toolkit ]

docker stats ----> Reads cgroup metrics (CPU, Mem, Net I/O)
docker top ------> Maps container PIDs to Host PIDs
docker diff -----> Compares OverlayFS upperdir against lowerdir
docker exec -----> Injects a new process (e.g. bash) into existing namespaces
```

### 4. Production use case
A container is exiting immediately on startup. `docker logs` shows nothing because the app crashes before stdout flushes. You need to inspect the exit code and potentially override the entrypoint to keep the container alive for debugging.

### 5. Complete config/script (line-by-line explained)
A step-by-step production debugging runbook.

```bash
# 1. Container keeps crashing. Find the exit code.
docker inspect -f '{{.State.ExitCode}} - {{.State.Error}}' crashing-app
# (If exit code is 137, it was OOMKilled. Check memory limits).

# 2. Override the entrypoint to stop it from crashing, so you can poke around
docker run -d --name debug-app --entrypoint sleep my-app-image 3600

# 3. Exec into the running container
docker exec -it debug-app /bin/sh

# 4. (Inside container) Manually run the app to see the raw error
./start_app.sh

# 5. Check what files the container has modified since it started
docker diff debug-app

# 6. Monitor real-time resource usage of all containers
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```
*   Line 2: `docker inspect` uses Go templates to extract exactly the data you need from the massive JSON output.
*   Line 5: Bypassing the baked-in `ENTRYPOINT` with `sleep` forces the container to stay alive.
*   Line 8: `docker exec` enters the container's namespaces, giving you a shell.
*   Line 14: `docker diff` shows `C` (Changed), `A` (Added), or `D` (Deleted) files in the read-write layer. Great for finding out if an app is writing massive logs locally.

### 6. Commands
*   `docker events`: Streams real-time events from the daemon (container start, stop, die, network connect). Great for finding out *when* something crashed.

### 7. Common mistakes
*   Trying to `docker exec` into a crashed (stopped) container. You can only exec into a *running* container. For stopped containers, use `docker logs` or `docker commit` to save the crashed state as an image, then run it with an overridden entrypoint.

### 8. Best practices
*   If using distroless images (no shell), use `docker debug` (in Docker Desktop) or `kubectl debug` (in k8s). These tools attach an ephemeral debug container (loaded with tools like busybox, curl, strace) to the target container's namespaces.

### 9. Troubleshooting
*   Exit Code 1: General application error.
*   Exit Code 137: SIGKILL (often Out of Memory).
*   Exit Code 143: SIGTERM (graceful shutdown requested by Docker).

### 10. Interview Q&A
**Q: "A container is consuming a massive amount of disk space, but you mapped volumes correctly. How do you find the culprit?"**
**A:** I would use `docker diff <container_name>`. This command inspects the OverlayFS container layer and lists all files that have been added or modified compared to the base image. It will immediately highlight if the application is writing log files or temp data directly into the container's writable layer instead of stdout or a tmpfs mount.

---

## SECTION 12: Container Lifecycle and Garbage Collection

### 1. Why it exists / problem it solves
Docker is a packrat. It caches every layer, keeps every stopped container, and retains every unused network and volume. Over months, a CI/CD builder node will accumulate hundreds of gigabytes of dead data, eventually crashing the node with "No space left on device". You must configure Garbage Collection (GC).

### 2. Internal working
*   **Dangling Images:** Images with no tag (shown as `<none>:<none>`). Created when you build a new image with the same name/tag as an existing one. The old one becomes dangling.
*   **Stopped Containers:** Containers that exited but weren't run with `--rm`.
*   **Unused Volumes:** Volumes not attached to any container. Docker will *never* automatically delete these, protecting your data.

### 3. ASCII architecture diagram

```text
Host Disk Over Time:

[ Base Image Layer (Ubuntu) ] -> Shared by many
[ Old App Layer (v1.0) ] ------> Dangling (Wasting space)
[ New App Layer (v1.1) ]
[ Stopped Container (Exit 0) ]-> Retains read-write layer state
[ Unused Named Volume ] -------> Retains old database data

Action: docker system prune -a --volumes
Result: Only Base Image and New App Layer (v1.1) remain.
```

### 4. Production use case
Every Kubernetes node (using containerd) and every Jenkins build server (using Docker) has an automated cron job or kubelet configuration that monitors disk pressure and actively prunes unused images and containers to maintain health.

### 5. Complete config/script (line-by-line explained)
A production cron job script for a Docker build server.

```bash
#!/bin/bash
# Save as /etc/cron.daily/docker-gc

# 1. Prune all stopped containers, unused networks, and dangling images
docker system prune --force

# 2. Aggressively prune ANY image not attached to a running container, older than 168 hours (7 days)
docker image prune --all --force --filter "until=168h"

# 3. (Optional & Dangerous) Prune unused volumes. Only do this on stateless build nodes!
# docker volume prune --force
```
*   Line 5: `docker system prune -f` cleans up the safe stuff automatically without asking for `y/n`.
*   Line 8: This is aggressive. It deletes *named* images (not just dangling) if they haven't been used in 7 days. This keeps the build cache fresh but prevents infinite disk growth.

### 6. Commands
*   `docker system df`: Shows Docker disk usage, broken down by Images, Containers, Local Volumes, and Build Cache. It also shows the "RECLAIMABLE" size.

### 7. Common mistakes
*   Running `docker system prune -a --volumes` on a production database node. This will delete all unused volumes. If a database container is temporarily stopped for maintenance, its volume is technically "unused". Pruning will delete all production data. Never automate volume pruning on stateful nodes.

### 8. Best practices
*   Always run ephemeral tasks (scripts, CI tests) with `docker run --rm` so the container deletes itself immediately upon exit.

### 9. Troubleshooting
*   If `docker system prune` doesn't free up space, the space might be consumed by the BuildKit cache. Run `docker builder prune -a` to clear the BuildKit cache.

### 10. Interview Q&A
**Q: "How do you manage Docker disk space on a heavily utilized CI/CD server?"**
**A:** First, I ensure all CI jobs run containers with the `--rm` flag. Second, I configure a daily cron job running `docker system prune -f` to clean up stopped containers and dangling images. For the BuildKit cache, I run `docker builder prune`. Finally, I implement a time-based filter (`docker image prune -a --filter "until=168h"`) to remove unused, tagged images older than a week, ensuring the disk doesn't fill up while preserving a recent cache.

---
## END OF CHAPTER

### One-Page Revision Sheet
*   **Architecture:** CLI -> dockerd -> containerd -> runc. `containerd` manages lifecycle, `runc` creates namespaces/cgroups.
*   **OverlayFS:** Immutable image layers + writable container layer. Modifying lower files triggers Copy-on-Write. Deleting lower files creates whiteouts.
*   **Namespaces/cgroups:** Namespaces isolate visibility (PID, NET). cgroups restrict usage (CPU, RAM).
*   **Optimization:** Use multi-stage builds. `COPY` source code *after* installing dependencies. Use distroless images.
*   **Networking:** Default bridge is legacy (no DNS). User-defined bridge has embedded DNS.
*   **Security:** Avoid root (`USER` directive), drop capabilities, use read-only root filesystems, scan with Trivy.

### Top 50 Docker Interview Takeaways
*(Summary of key points - refer to Q&A in sections)*
1. Difference between Docker, containerd, runc.
2. How Union File Systems (Overlay2) work.
3. How Copy-on-Write and whiteout files function.
4. Purpose of PID and NET namespaces.
5. How cgroups enforce memory limits.
6. The exact mechanism of multi-stage builds.
7. Advantages of distroless images.
8. How layer caching works and instruction ordering.
9. Bridge vs Host networking modes.
10. Embedded DNS in user-defined networks.
11. Named volumes vs Bind mounts.
12. When to use tmpfs mounts.
13. Principle of least privilege (non-root users).
14. Dropping Linux capabilities.
15. Use of seccomp and AppArmor.
16. Importance of image scanning (Trivy).
17. Docker Compose restart policies.
18. Healthchecks vs depends_on in Compose.
19. Managing secrets in Compose.
20. Docker logging drivers (json-file vs fluentd).
21. Preventing log-related disk exhaustion.
22. Registry manifests vs blobs.
23. Pull-through caches to avoid rate limits.
24. ECR lifecycle policies.
25. Debugging with `docker diff` and `docker stats`.
26. Overriding entrypoints for crash debugging.
27. Executing into namespaces.
28. Managing dangling images.
29. Safely using `docker system prune`.
30. The `--rm` flag for ephemeral containers.
... *(and all concepts covered in the sections above)*

### Common Production Mistakes Table
| Mistake | Consequence | Fix |
| :--- | :--- | :--- |
| Single-stage large Dockerfiles | Massive attack surface, slow pulls | Use multi-stage builds and distroless images |
| Running as root in container | Container escape leads to host root access | Use `USER` directive, drop capabilities |
| Unbounded logging | Host disk fills up, node crashes | Configure `max-size` in `daemon.json` |
| No memory/cpu limits | Container memory leak crashes entire host | Use `--memory` and `--cpus` |
| Using `latest` tag | Unpredictable deployments, breaks rollbacks | Use specific semantic tags or Git SHAs |
| Bind mounts in prod | Ties deployment to specific host filesystem | Use Named Volumes |
| Putting secrets in ENV | Secrets baked into immutable image history | Use Docker Secrets or tmpfs mounts |
| Installing updates (`apt upgrade`) | Non-reproducible builds over time | Pin versions, build fresh images |

### Hands-on Exercises (5 Labs)
1. **The Architecture Lab:** Bypass Docker completely. Use `ctr` to pull `nginx:alpine`, run it via containerd, and use `lsns` and `cat /sys/fs/cgroup/...` to manually verify the namespaces and cgroups created.
2. **The Size Lab:** Write a Node.js Dockerfile without multi-stage. Record the size. Rewrite it using multi-stage, copying only `node_modules` and source into an alpine image. Compare the sizes and `docker history`.
3. **The Networking Lab:** Create two containers on the default bridge and ping them by IP. Then create a user-defined network, attach two containers, and ping them by container name. Inspect the `iptables` NAT rules created on the host.
4. **The Security Lab:** Run a container with `--read-only` and `--cap-drop ALL`. Try to install a package or bind port 80. Observe the kernel denying the actions.
5. **The Debug Lab:** Write a script that writes a 1GB file into `/tmp` inside a container. Run it. Use `docker system df` and `docker diff` to identify the bloated layer, then fix the container to use a `--tmpfs` mount for `/tmp`.

### Mini Capstone Project
**Goal:** Build a production-grade multi-stage Dockerfile for a Python FastAPI app.
**Requirements:**
1.  Stage 1 (Builder): Use `python:3.11-slim`, install `pipenv` or `poetry`, generate a `requirements.txt`, and build a virtual environment. Use BuildKit cache mounts for `pip`.
2.  Stage 2 (Final): Use `gcr.io/distroless/python3`. Copy only the virtual environment and app code.
3.  Security: Set a non-root USER.
4.  CI/CD: Write a GitHub Action (mock script) that builds the image using `buildx` for `linux/amd64` and `linux/arm64`.
5.  Scan: Run `trivy` on the image. Fail if CRITICAL CVEs exist.
6.  Sign: Generate a Cosign keypair and sign the image.
7.  Push: Push to a mock ECR registry.

### Architecture Challenge
**Scenario:** Design the container image lifecycle from a Git commit to AWS ECR.
**Task:** Draw the architecture (using a tool or whiteboard).
1.  Developer pushes code to GitHub.
2.  GitHub Actions triggers.
3.  BuildKit builds the image leveraging remote layer caching.
4.  Trivy scans the image.
5.  Cosign signs the image.
6.  Image is pushed to `dev-ecr`.
7.  Integration tests run against `dev-ecr` image.
8.  Upon success, the exact same immutable image (by SHA) is promoted (copied) to `prod-ecr` and re-signed.
9.  Production Kubernetes cluster verifies the Cosign signature before allowing the pod to run.
