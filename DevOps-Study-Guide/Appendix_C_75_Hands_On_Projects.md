# Appendix C: 75 Hands-On Projects

This appendix contains **75 hands-on projects** divided into three skill tiers: Beginner, Intermediate, and Advanced. They are designed to build your practical skills in Linux, Networking, Bash, Python, SSH, Logs, and DevOps.

---

## 🚀 Part 1: 25 Beginner Projects

### Project 1: System Info Reporter
* **Objective:** Extract and write system specs (Hostname, CPU, OS, RAM) to a file.
* **Steps:**
  1. Write a script `sys_report.sh` that gathers info using `hostname`, `uname -r`, and `free -h`.
  2. Redirect output using `>` to `/tmp/sys_report.txt`.

### Project 2: Interactive User Creator
* **Objective:** Create a script prompting for username and password, then creates the user.
* **Steps:** Use `read` for inputs, run `sudo useradd` and `chpasswd` to set the password.

### Project 3: Password Strength Validator
* **Objective:** Check if a user-supplied string has $\ge 8$ characters.
* **Steps:** Calculate string length using `${#password}` and evaluate inside `if-else`.

### Project 4: Simple Local HTTP Server
* **Objective:** Serve a folder of local HTML files over the network.
* **Steps:** Navigate to a target folder containing `index.html` and start Python's built-in server: `python3 -m http.server 8000`.

### Project 5: Automated Log Grep Utility
* **Objective:** Filter and count "ERROR" lines in a log folder.
* **Steps:** Run `grep -ri "error" /var/log/ 2>/dev/null | wc -l`.

### Project 6: Static File Backup
* **Objective:** Archive the local website directory.
* **Steps:** Run `tar -czf /tmp/www_backup.tar.gz /var/www/html/`.

### Project 7: Inode Exhaustion Check
* **Objective:** Alert if inode consumption of the system exceeds 80%.
* **Steps:** Parse `df -i` output using `awk` and compare value in shell.

### Project 8: Shell Variable Config Loader
* **Objective:** Load environment config values from a `.env` file and print them.
* **Steps:** Use `source config.env` inside a script and reference the loaded variables.

### Project 9: Running Process Count Monitor
* **Objective:** Log the total count of running processes to a file every minute.
* **Steps:** Create a script running `ps ax | wc -l` and register it in `crontab`.

### Project 10: Port Availability Validator
* **Objective:** Check if Port 80 is currently open on the local host.
* **Steps:** Run `nc -zv 127.0.0.1 80` and check exit status.

### Project 11: Host Down Alerter
* **Objective:** Ping a target server IP and output a warning if unreachable.
* **Steps:** Run `ping -c 2 <IP>`, if status code is non-zero, print "Down".

### Project 12: Directory Size Alert
* **Objective:** Warning if a specific folder exceeds 500MB.
* **Steps:** Check size using `du -s <folder>`, parse size value, and evaluate against threshold.

### Project 13: Temporary Directory Cleaner
* **Objective:** Delete files in `/tmp` older than 3 days.
* **Steps:** Run `find /tmp -type f -mtime +3 -delete`.

### Project 14: SSH Key-pair Initializer
* **Objective:** Set up SSH keys on a local machine without prompts.
* **Steps:** Run `ssh-keygen -t ed25519 -f ~/.ssh/id_test -N ""`.

### Project 15: Website Ping and Response Header Logger
* **Objective:** Verify website status and log headers.
* **Steps:** Run `curl -I https://example.com > /tmp/headers.txt`.

### Project 16: File Hash integrity checker
* **Objective:** Generate and verify SHA256 file checksums.
* **Steps:** Create hash `sha256sum file.txt > file.sha256`, and verify with `sha256sum -c file.sha256`.

### Project 17: User Command Auditer
* **Objective:** Read history and output the top 5 most used commands.
* **Steps:** Run `history | awk '{print $2}' | sort | uniq -c | sort -nr | head -n 5`.

### Project 18: File Permission Auditor
* **Objective:** Find any files inside a folder containing permissions `777`.
* **Steps:** Run `find /opt/app -perm 777`.

### Project 19: Log Cleanup Script
* **Objective:** Truncate all `.log` files inside `/tmp/logs` to 0 bytes.
* **Steps:** Loop files, run `cat /dev/null > "$file"`.

### Project 20: Simple DNS Lookup Utility
* **Objective:** Print A records for a domain list.
* **Steps:** Loop domain list and execute `host -t A $domain`.

### Project 21: Python Hello World API Caller
* **Objective:** Query a public API and print the JSON response.
* **Steps:** Use Python's `requests` library to fetch `https://httpbin.org/get`.

### Project 22: JSON Syntax Validator
* **Objective:** Validate if a file contains valid JSON structure.
* **Steps:** Run `python3 -m json.tool config.json >/dev/null`.

### Project 23: Disk Utilization Tracker
* **Objective:** Check disk usage and print a message: "Disk Healthy" or "Disk Warning".
* **Steps:** Run `df -h /`, extract percentage, and evaluate inside an `if` block.

### Project 24: SSH Config File Builder
* **Objective:** Automatically append custom server aliases to `~/.ssh/config`.
* **Steps:** Use `cat <<EOF >> ~/.ssh/config` to append host connection definitions.

### Project 25: Simple Docker Container Runner
* **Objective:** Start a detached Nginx container mapping port 80.
* **Steps:** Run `docker run -d -p 80:80 --name web nginx`.

---

## 🛠️ Part 2: 25 Intermediate Projects

### Project 26: Log Shipper to S3 Simulator
* **Objective:** Compress and upload daily logs to a backup folder or AWS bucket.
* **Steps:** Create a Bash script running `tar` and calling `aws s3 cp`.

### Project 27: Nginx Access Log Traffic Analyzer
* **Objective:** Count request distributions by HTTP Status Code.
* **Steps:** Run `awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c`.

### Project 28: Process Supervisor Watchdog
* **Objective:** Check if `nginx` service is running; if not, restart it and log the event.
* **Steps:** Use `pgrep` check in shell script, call `systemctl start nginx` if down.

### Project 29: Weekly Automated Database Backup Rotation
* **Objective:** Keep only the last 4 database backups, deleting older files.
* **Steps:** Run backup, then find and delete: `find /backups -mtime +28 -delete`.

### Project 30: Multi-Host Ping Checker
* **Objective:** Loop through a list of servers and print a status dashboard.
* **Steps:** Read `/etc/hosts` or list, execute ping in parallel, output results to a markdown table.

### Project 31: DNS Zone Record Validator
* **Objective:** Compare domain records against expected target IPs.
* **Steps:** Use Python script with `subprocess` to dig records and compare strings.

### Project 32: CPU load Average Alert via Email/Slack
* **Objective:** Scan CPU usage and trigger alerts if load average exceeds core count.
* **Steps:** Read `/proc/loadavg` values, compare to `nproc`, and call curl webhooks if high.

### Project 33: Secure SSH Port Swapper
* **Objective:** Relocate server SSH port to 2222 and verify access.
* **Steps:** Modify `/etc/ssh/sshd_config` Port line, open firewall port, restart SSH.

### Project 34: XML to JSON Parser Converter
* **Objective:** Convert configuration files.
* **Steps:** Write a Python script using `xml.etree.ElementTree` and the `json` module.

### Project 35: JSON config template generator
* **Objective:** Read configuration template and populate environment secrets.
* **Steps:** Read `template.json`, replace keywords using `sed` or Python dictionary updates.

### Project 36: Docker Logs Exporter
* **Objective:** Fetch logs from all running docker containers and save them to host log folders.
* **Steps:** Run `docker ps -q`, loop and run `docker logs --tail 100 $id > /var/log/docker/$name.log`.

### Project 37: Git Untracked File Guard
* **Objective:** Fail a CI build script if untracked files are found in the working tree.
* **Steps:** Check if `git status --porcelain` is non-empty; if so, exit with code 1.

### Project 38: HTTP API Latency Monitor
* **Objective:** Perform requests to endpoints and write response times to a CSV file.
* **Steps:** Use Python `requests` and `time` modules inside a loop, writing values to a CSV.

### Project 39: Automated SSL certificate expiry checker
* **Objective:** Query a list of domains and warn if their SSL certs expire within 14 days.
* **Steps:** Use `openssl s_client` command inside a script to query dates.

### Project 40: Multi-user home folder auditor
* **Objective:** Scan `/home` and report folders violating standard permissions (e.g. visible to others).
* **Steps:** Find permissions using `stat -c "%a %n" /home/*` and verify they are `700` or `750`.

### Project 41: System Port Scanner (Port Sweep)
* **Objective:** Test a target IP for open ports between 1 and 1024.
* **Steps:** Run a loop in Python using `socket.connect_ex`.

### Project 42: YAML syntax parser validator
* **Objective:** Read and validate Kubernetes deployment manifests.
* **Steps:** Write a Python script loading YAML files via `yaml.safe_load`.

### Project 43: System Resource utilization dashboard
* **Objective:** Print a dynamic system status summary.
* **Steps:** Create a shell script running `top`, `free`, and `df` once, displaying output in a clean terminal window.

### Project 44: Host ARP Spoofing Defender
* **Objective:** Watch for MAC address changes for a static IP in the network ARP cache.
* **Steps:** Compare IP/MAC associations in `arp -n` against a verified static database.

### Project 45: Cron job monitor checker
* **Objective:** Scan `/var/log/syslog` to verify if cron tasks executed at scheduled intervals.
* **Steps:** Match cron job triggers using `grep "CRON" /var/log/syslog`.

### Project 46: Docker volume cleanup daemon
* **Objective:** Clean up unused Docker storage volumes to reclaim disk space.
* **Steps:** Execute `docker volume prune -f` weekly via cron.

### Project 47: Static HTML asset compiler
* **Objective:** Read text templates and output compiled HTML pages.
* **Steps:** Use Python script with file operations to build layout templates.

### Project 48: Local network subnet calculator
* **Objective:** Calculate host ranges and broadcast IPs from a CIDR input.
* **Steps:** Write a Python script using the standard `ipaddress` module.

### Project 49: SSH Key Rotation automation
* **Objective:** Replace user authorized keys on remote hosts.
* **Steps:** Copy new public keys, append to `authorized_keys`, and delete old key configurations.

### Project 50: Upstream API Health Checker Proxy
* **Objective:** Return a health status page indicating if upstream services are healthy.
* **Steps:** Configure Nginx with status checks, or write a Python web script querying upstream APIs.

---

## 🏆 Part 3: 25 Advanced Projects

### Project 51: Multi-Tier Network Service Topology Simulation
* **Objective:** Set up an isolated multi-subnet network using VPC/CIDR concepts or local virtual interfaces.
* **Steps:** Define routing rules, setup IP forwarding, and isolate database subnets from public traffic.

### Project 52: Kubernetes Pod CrashLoopBackOff Alerter
* **Objective:** Monitor cluster status and send alerts for crash looping pods.
* **Steps:** Run `kubectl get pods -A -o json` in Python, check for `CrashLoopBackOff` status, and send a webhook alert.

### Project 53: Production-ready automated SSL Certificate renewer (Certbot client)
* **Objective:** Manage domain certificate registration, challenges, and renewals.
* **Steps:** Write a Python orchestrator running Certbot DNS-01 validation challenges.

### Project 54: Git Commit Secrets Scan Guard
* **Objective:** A pre-commit hook that scans modified files for passwords, private keys, or API credentials.
* **Steps:** Write a shell script matching key regex strings, configured as a Git hook under `.git/hooks/pre-commit`.

### Project 55: High-speed Log Parsing Daemon
* **Objective:** Monitor active access logs, parse events to JSON, and stream to a secondary metrics endpoint.
* **Steps:** Write a Python script using generator patterns to tail logs without locking system memory.

### Project 56: Auto-Healing Host Watchdog
* **Objective:** Monitor system services and automatically restart dependencies, clean up logs, or adjust resources based on errors.
* **Steps:** Set up automated systemd targets, custom event traps, and automated shell recoveries.

### Project 57: Continuous Integration Lint and Test Orchestration Runner
* **Objective:** A script executing code check tools (flake8, shellcheck, syntax check) and packaging successful builds.
* **Steps:** Write a Shell runner script managing workspace setups, environment isolations, and exit code validations.

### Project 58: AWS EC2 Custom AMI builder automation
* **Objective:** Provision, install configurations, clean logs, and register custom system images.
* **Steps:** Automate instances deployment using Terraform, execute build scripts via SSH, and run image registration commands.

### Project 59: Dynamic IP Firewall Blacklister (DDoS Shield)
* **Objective:** Parse access logs in real-time, count request rates, and block IPs exceeding 100 requests per minute.
* **Steps:** Extract IPs using `awk` in a loop, check request limits, and run `iptables -A INPUT -s $ip -j DROP` for violators.

### Project 60: Multi-Host System Status Matrix Dashboard
* **Objective:** Collect CPU, RAM, and disk metrics from a list of servers over SSH and compile them into a central webpage.
* **Steps:** Execute remote commands in parallel using Python `multiprocessing` and SSH keys, compiling the metrics into a static HTML report.

### Project 61: Python-based Kubernetes Operator
* **Objective:** Watch custom resources in a Kubernetes cluster and automatically provision namespaces, services, and deployments.
* **Steps:** Implement a Python script using the Kubernetes API to watch and reconcile resource states.

### Project 62: Database Master-Slave Replication Validator
* **Objective:** Connect to database nodes, compare transaction log IDs, and verify replication health.
* **Steps:** Write a Python validator executing database queries and checking lag metrics.

### Project 63: Multi-VPC Peer Routing Manager
* **Objective:** Automate VPC peering connection configurations and routing table updates.
* **Steps:** Implement a Terraform configuration and Python script using the AWS SDK to verify route connectivity.

### Project 64: Automated Disaster Recovery System Failover
* **Objective:** Detect endpoint outages and update DNS records to route traffic to a secondary region.
* **Steps:** Write a monitor checking endpoints, which calls Route 53 or Cloudflare APIs to update A records on failure.

### Project 65: Git Repository Configuration Auditor
* **Objective:** Scan organizations to find repositories with weak configurations (e.g., missing branch protections).
* **Steps:** Write a Python automation script using GitHub API payloads to generate compliance reports.

### Project 66: Containerized Application Deployer (Kubernetes Helm Deployer)
* **Objective:** Package application configurations, lint Helm charts, and deploy to a cluster.
* **Steps:** Create a shell execution runner validating chart syntax before executing upgrade commands.

### Project 67: Automated AWS Cost Auditor
* **Objective:** Query billing metrics and alert when daily expenditures exceed thresholds.
* **Steps:** Write a Python script querying AWS Cost Explorer and alerting over Slack.

### Project 68: Multi-Subnet CIDR Allocator API
* **Objective:** Manage IP allocations, returning the next available subnet size for a VPC request.
* **Steps:** Implement a Python automation utility tracking assigned IP blocks.

### Project 69: Container Image Vulnerability Scanner
* **Objective:** Scan container images for vulnerabilities, failing builds if critical issues are found.
* **Steps:** Integrate Trivy or Grype scans into a pipeline script, parsing JSON outputs to check for vulnerabilities.

### Project 70: Host Port Connection Sniffer
* **Objective:** Monitor host traffic on a port, log header payloads, and identify anomalies.
* **Steps:** Write a Python script using `scapy` or raw sockets to capture and parse network packets.

### Project 71: Prometheus Metric Exporter Daemon
* **Objective:** Collect custom system stats and expose them on an endpoint in Prometheus format.
* **Steps:** Write a Python daemon running a basic HTTP server to expose custom metrics.

### Project 72: Real-time File System Integrity Monitor
* **Objective:** Watch directories and log notifications immediately if any files are modified or deleted.
* **Steps:** Implement a Python automation daemon using the `watchdog` library.

### Project 73: Secure Bastion User Auditing System
* **Objective:** Record terminal session keystrokes of users logging into bastion hosts.
* **Steps:** Configure SSH with shell wrapper scripts utilizing the `script` utility.

### Project 74: Automated Chaos Monkey Daemon
* **Objective:** Randomly terminate non-critical server processes or containers to test system resilience.
* **Steps:** Create an automated task randomly terminating Docker containers or stopping systemd services.

### Project 75: Kubernetes Cluster Backup and Recovery System
* **Objective:** Export all cluster resource manifests to a Git backup repository daily.
* **Steps:** Write a Python automation script looping through API groups, exporting resources as YAML, and pushing changes to Git.
