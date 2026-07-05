# Appendix A: DevOps Roadmap Technologies

Understanding foundational Linux, Networking, and Scripting is essential because modern cloud-native tools are built directly on top of these primitives. This section serves as a technical roadmap showing exactly how these foundations connect to the industry's primary DevOps technologies.

---

## 1. Docker (Containerization)
* **What it is:** A platform that packages applications and their dependencies into lightweight, standalone containers.
* **How it connects to Core Fundamentals:**
  * **Linux:** Docker runs containers by sharing the host kernel. It relies directly on Linux **Namespaces** (to isolate mount points, users, process IDs, and networks) and **Control Groups (cgroups)** (to set hard limits on memory, CPU, and disk I/O). If you don't understand how Linux allocates processes, you will struggle to debug container crashes or set limits.
  * **Networking:** Docker configures virtual interfaces, local bridge networks (`docker0`), and uses **IPtables** (Linux firewalls) rules to forward external host ports to internal container ports.
  * **Scripting:** Entrypoints and configuration checks inside Dockerfiles are almost always written as Bash shell scripts.

---

## 2. Jenkins & GitHub Actions (CI/CD Pipelines)
* **What they are:** Automation servers and orchestrators that build, test, and deploy code changes when developers push updates to repositories.
* **How they connect to Core Fundamentals:**
  * **Linux:** Build agents/runners are almost always Linux VMs or containers. The configuration files (e.g., `.github/workflows/deploy.yml` or a `Jenkinsfile`) define commands that run on these agents.
  * **Networking:** Runners must securely connect to repositories, pull dependencies from registry APIs, and push builds to servers using SSH, TLS, and DNS.
  * **Scripting:** While pipeline syntax is defined in YAML or Groovy, the actual build, testing, and deployment commands are shell execution statements. A CI/CD pipeline is essentially an automated Bash runner.

---

## 3. Kubernetes & Helm (Orchestration)
* **What they are:** Kubernetes manages container clusters across machines, handling scaling and healing. Helm is the package manager used to bundle and deploy Kubernetes configurations.
* **How they connect to Core Fundamentals:**
  * **Linux:** Kubernetes worker nodes are Linux servers. Processes inside containers run as isolated Linux processes. Linux security features like **Seccomp** profiles and **AppArmor** policies are used to lock down containers.
  * **Networking:** Kubernetes has a strict network model where every pod gets a unique IP. Understanding IP routing, subnet masks, DNS resolution (CoreDNS), proxying (Kube-Proxy using IPVS/IPtables), and load balancing is required to debug pod-to-pod communication.
  * **Scripting:** Helm templates use Go templating and shell-like logic. InitContainers utilize shell scripts to wait for databases or run migrations before the main application pod boots.

---

## 4. Terraform (Infrastructure as Code)
* **What it is:** A declarative configuration tool used to provision cloud infrastructure (virtual machines, networks, databases) across cloud providers.
* **How it connects to Core Fundamentals:**
  * **Linux:** Terraform is used to provision virtual machine operating systems. When provisioning, you use Linux **Cloud-Init** scripts to perform initial server bootstrapping (installing git, docker, starting services).
  * **Networking:** Defining Terraform files requires configuring subnets, CIDR blocks (`10.0.0.0/16`), Routing Tables, Security Groups (Firewalls), and DNS records. Without networking knowledge, you cannot secure your cloud infrastructure.
  * **Scripting:** Automation pipelines invoke Terraform CLI commands (`terraform plan`, `terraform apply`) sequentially using Bash scripts, capturing outputs to verify deployment steps.

---

## 5. Amazon Web Services (AWS)
* **What it is:** The world's leading public cloud platform, offering virtual servers, managed databases, and scalable networks.
* **How it connects to Core Fundamentals:**
  * **Linux:** Most AWS EC2 (Elastic Compute Cloud) instances run Linux distros. Understanding file paths, services management, and storage mounting is required to run workloads.
  * **Networking:** AWS VPC (Virtual Private Cloud) configurations are built on traditional networking principles: subnets, CIDRs, Network Access Control Lists (NACLs), gateways, and route tables.
  * **Scripting:** Interacting with cloud resources at scale is done using the AWS CLI or AWS Python SDK (**Boto3**). Writing automation scripts is required for backup rotations, instance scaling, or cleanups.

---

## 6. Prometheus & Grafana (Monitoring & Observability)
* **What they are:** Prometheus scrapes and stores time-series metrics. Grafana query engines convert this raw metrics data into rich dashboards and charts.
* **How they connect to Core Fundamentals:**
  * **Linux:** To monitor servers, you run exporters (like `Node Exporter`) which collect kernel and operating system data (CPU usage, disk read/write rates, memory allocations) directly from the virtual `/proc` and `/sys` file systems.
  * **Networking:** Exporters expose endpoints on specific ports (e.g., `9100`). Prometheus retrieves this data over HTTP/HTTPS connections.
  * **Scripting:** Custom exporters or metric alerting checks (e.g., alerting when disk usage is > 85%) are written using Python or Bash scripts.

---

## 7. ELK Stack (Elasticsearch, Logstash, Kibana)
* **What it is:** A centralized log aggregation platform. Filebeat/Logstash collects logs, Elasticsearch indexes them, and Kibana provides a visualization UI.
* **How it connects to Core Fundamentals:**
  * **Linux:** Collectors scan standard system log files directly from `/var/log` paths.
  * **Networking:** Logs are transmitted over encrypted network channels to the Elasticsearch cluster.
  * **Scripting:** To digest complex, unstructured logs, you must write log shippers' parsing filters using regular expressions (Regex), which are identical to `grep` and `sed` filters.

---

## 8. ArgoCD (GitOps CD)
* **What it is:** A declarative GitOps continuous delivery tool for Kubernetes, keeping cluster states synchronized with git repositories.
* **How it connects to Core Fundamentals:**
  * **Linux:** ArgoCD runs as system processes inside Kubernetes pods on Linux nodes.
  * **Networking:** Syncs state via HTTPS/SSH Git queries and calls the Kubernetes API server (Port 6443) to reconcile cluster structures.
  * **Scripting:** GitOps pipelines incorporate shell hooks to execute verification tasks, run security scanners, and check deployment health status post-sync.
