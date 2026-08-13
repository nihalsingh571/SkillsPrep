# System Engineer Final Interview Preparation & Cheatsheets
**Candidate Profile:** CSE Graduate, DevOps Knowledge (Linux, Docker, K8s, AWS, CI/CD, Terraform, Git)
**Target Role:** System Engineer (0-1 year experience), Gurugram
**Strategy:** Leverage DevOps as a strong foundation for modern infrastructure without appearing overqualified or disconnected from core System Administration tasks.

---

## PART 1: TOP INTERVIEW QUESTIONS (CURATED)

### Top 20 Linux Questions (with complete answers)

1. **What is the Linux file system hierarchy? Explain 10 important directories.**
   The Linux file system is organized in a hierarchical tree structure starting from the root directory (`/`). Everything in Linux is considered a file, including hardware devices.
   - `/bin`: Essential user command binaries (e.g., `ls`, `ping`).
   - `/sbin`: Essential system binaries, usually run by root (e.g., `fdisk`, `reboot`).
   - `/etc`: Configuration files for the system and installed programs.
   - `/var`: Variable data files like logs (`/var/log`) and databases.
   - `/home`: Personal directories for users.
   - `/root`: The home directory for the root user.
   - `/tmp`: Temporary files created by system and users, cleared on reboot.
   - `/dev`: Device files representing hardware (e.g., `/dev/sda`).
   - `/proc`: Virtual filesystem providing system and process information in memory.
   - `/opt`: Optional add-on application software packages.

2. **What does `chmod 755` mean?**
   `chmod` changes file permissions. The numbers represent User (Owner), Group, and Others.
   - `4` = Read (r), `2` = Write (w), `1` = Execute (x).
   - `7` (User) = 4+2+1 = Read, Write, Execute.
   - `5` (Group) = 4+1 = Read, Execute.
   - `5` (Others) = 4+1 = Read, Execute.
   So `755` means the owner can do anything, while group and others can read and execute, but not modify the file. Commonly used for scripts and directories.

3. **How do you find all files larger than 100MB on a Linux system?**
   I would use the `find` command:
   `find / -type f -size +100M -exec ls -lh {} \;`
   This searches from the root directory `/` for files (`-type f`) larger than 100 Megabytes (`-size +100M`) and executes `ls -lh` to show human-readable sizes.

4. **How do you check which process is using a specific port?**
   We can use `ss`, `netstat`, or `lsof`.
   - `ss -tulnp | grep :80` (Shows listening TCP/UDP ports and the process using port 80).
   - `lsof -i :80` (Lists open files/processes associated with port 80).

5. **How do you check disk usage on Linux?**
   - For partition space: `df -h` (Disk Free, human-readable).
   - For directory space: `du -sh /var/log` (Disk Usage, summary, human-readable).

6. **What is the difference between hard link and soft link?**
   - **Soft (Symbolic) Link (`ln -s target linkname`):** Acts like a shortcut in Windows. It points to the original file's path. If the original file is deleted, the soft link breaks (dangling link). Can link across different filesystems.
   - **Hard Link (`ln target linkname`):** Points to the exact same inode (physical data on disk) as the original file. If you delete the original file, the data is still accessible via the hard link. Cannot link across different filesystems or link to directories.

7. **How do you schedule a cron job? Give an example.**
   You edit the cron table using `crontab -e`.
   The format is: `Minute Hour DayOfMonth Month DayOfWeek Command`
   Example: To run a backup script every day at 2:30 AM:
   `30 2 * * * /opt/scripts/backup.sh`

8. **How do you check system resource usage in real time?**
   I primarily use `top` or `htop`. These tools show real-time CPU, memory usage, load average, and a dynamic list of running processes. I can also use `vmstat 1` for CPU/memory stats updating every second, or `free -h` for a snapshot of memory.

9. **What is the difference between `kill -9` and `kill -15`?**
   - `kill -15` (SIGTERM): The default termination signal. It asks the process to stop gracefully, allowing it to save data and clean up temporary files.
   - `kill -9` (SIGKILL): A forceful kill sent directly to the kernel, bypassing the process. The process stops immediately without cleanup. Should only be used if SIGTERM fails.

10. **How do you add a new user and give them sudo access on Linux?**
    1. Create user: `sudo adduser johndoe`
    2. Grant sudo (Ubuntu/Debian): `sudo usermod -aG sudo johndoe`
    3. Grant sudo (RHEL/CentOS): `sudo usermod -aG wheel johndoe`

11. **What is `/etc/fstab` used for?**
    The File System Table (`fstab`) configuration file defines how disk partitions, various other block devices, or remote file systems should be mounted into the filesystem automatically at boot time.

12. **How do you check logs for a systemd service?**
    Use `journalctl`.
    - For a specific service: `journalctl -u nginx.service`
    - To follow logs in real-time: `journalctl -fu nginx.service`

13. **What is the difference between `ps aux` and `top`?**
    - `ps aux` provides a static snapshot of all currently running processes at the exact moment the command is executed.
    - `top` provides an interactive, real-time, constantly updating view of system processes and resource utilization.

14. **How do you find a file named "config.txt" in `/etc` directory?**
    `find /etc -name "config.txt"`
    If case-insensitive is needed: `find /etc -iname "config.txt"`

15. **How do you compress and extract a tar.gz file?**
    - Compress: `tar -czvf archive_name.tar.gz /path/to/directory` (Create, Zip, Verbose, File)
    - Extract: `tar -xzvf archive_name.tar.gz -C /destination/path` (eXtract)

16. **What does the `free -h` command show?**
    It displays the total amount of free and used physical (RAM) and swap memory in the system, as well as the buffers and caches used by the kernel, in a human-readable format (MB/GB).

17. **How do you change file ownership?**
    Use the `chown` (change owner) command.
    Example: `chown username:groupname filename.txt`
    To do it recursively for a folder: `chown -R username:groupname /var/www/html`

18. **How do you SSH to a remote server using a key file?**
    `ssh -i /path/to/private_key.pem username@server_ip_or_hostname`

19. **What is the `/proc` directory?**
    It's a pseudo-filesystem maintained in the system's memory. It contains runtime system information (e.g., system memory, mounts, hardware configuration) and a directory for every running process (named by its PID) containing process-specific details.

20. **How do you check which ports are listening on a Linux server?**
    `ss -tulnp` or `netstat -tulpn`. This shows TCP (`t`), UDP (`u`), listening ports (`l`), numeric addresses/ports (`n`), and the associated process (`p`).

### Top 20 Networking Questions (with complete answers)

1. **What happens when you type google.com in a browser? (complete flow)**
   - **DNS Resolution:** Browser checks its cache, OS cache, router cache, then queries the ISP DNS server to resolve google.com to an IP address.
   - **TCP Handshake:** The browser initiates a 3-way TCP handshake (SYN, SYN-ACK, ACK) with the Google server on port 443 (HTTPS).
   - **TLS Handshake:** The browser and server establish a secure, encrypted connection using SSL/TLS.
   - **HTTP Request:** The browser sends an HTTP GET request for the webpage.
   - **HTTP Response:** The server processes the request and sends back an HTTP response containing the HTML content.
   - **Rendering:** The browser parses the HTML, fetches additional resources (CSS, JS, images), and renders the page for the user.

2. **What is the DORA process in DHCP?**
   DORA explains how a device gets an IP address dynamically:
   - **Discover:** Client broadcasts a message looking for a DHCP server.
   - **Offer:** DHCP server responds with an offered IP address.
   - **Request:** Client requests to use that offered IP.
   - **Acknowledge:** Server acknowledges and finalizes the IP lease.

3. **What is the difference between TCP and UDP? Name protocols for each.**
   - **TCP (Transmission Control Protocol):** Connection-oriented, reliable, guarantees delivery and order (via handshakes and acknowledgments), but slower. Protocols: HTTP, HTTPS, FTP, SSH.
   - **UDP (User Datagram Protocol):** Connectionless, unreliable, no guarantee of delivery or order, but much faster. Protocols: DNS, DHCP, SNMP, Video Streaming, VoIP.

4. **What is the OSI model? Which layer does a router operate on? A switch?**
   The OSI model is a conceptual framework that standardizes network communication into 7 layers:
   7. Application
   6. Presentation
   5. Session
   4. Transport
   3. Network
   2. Data Link
   1. Physical
   - A **Router** operates at Layer 3 (Network) using IP addresses.
   - A standard **Switch** operates at Layer 2 (Data Link) using MAC addresses.

5. **What is subnetting? What is the subnet for 192.168.1.0/24?**
   Subnetting is dividing a large network into smaller, more manageable logical networks to improve performance and security.
   For `192.168.1.0/24`, the subnet mask is `255.255.255.0`. It provides 256 IPs, with 254 usable for hosts (network ID `.0`, broadcast `.255`).

6. **What is NAT and why is it used?**
   Network Address Translation (NAT) modifies IP address information in IP packet headers while in transit across a traffic routing device. It's primarily used to allow multiple devices on a private network to share a single public IP address to access the internet, thus conserving public IPv4 addresses.

7. **What is the difference between a public and private IP?**
   - **Public IP:** Routable on the internet, unique globally, assigned by ISP.
   - **Private IP:** Non-routable on the public internet, used within local networks (LAN). Specified by RFC 1918 (e.g., 10.x.x.x, 192.168.x.x, 172.16.x.x to 172.31.x.x).

8. **What does `ipconfig /flushdns` do and when would you use it?**
   It clears the local DNS resolver cache on a Windows machine. You use it when a website changes its IP address, or when you are facing DNS resolution issues (e.g., a site isn't loading but you know it's up), forcing the machine to query the DNS server again.

9. **What is ARP and how does it work?**
   Address Resolution Protocol (ARP) maps an IP address (Layer 3) to a physical MAC address (Layer 2). When a machine wants to communicate with an IP on the local network, it broadcasts an "ARP Request" asking "Who has this IP?". The machine with that IP replies with its MAC address, which is then cached.

10. **What is the difference between `ping` and `traceroute`?**
    - `ping` uses ICMP Echo Requests to test basic connectivity and latency to a single destination.
    - `traceroute` (or `tracert` in Windows) maps the exact path (hop-by-hop) a packet takes to reach the destination, showing the latency at each router along the way. Useful for finding exactly where a connection drops.

11. **What is port 80 vs port 443 vs port 22?**
    - **Port 80:** HTTP (Unencrypted web traffic)
    - **Port 443:** HTTPS (Encrypted web traffic)
    - **Port 22:** SSH (Secure Shell for remote CLI administration)

12. **What is a MAC address? How is it different from an IP address?**
    A MAC (Media Access Control) address is a physical, unique, permanent address burned into a network interface card (NIC) by the manufacturer. It operates at Layer 2. An IP address is a logical address assigned dynamically or statically, used for routing across different networks (Layer 3).

13. **What is the 3-way TCP handshake?**
    The process to establish a reliable TCP connection:
    1. **SYN:** Client sends a SYN (Synchronize) packet to the server.
    2. **SYN-ACK:** Server acknowledges receipt and sends its own SYN.
    3. **ACK:** Client acknowledges the server's SYN. Connection established.

14. **What is DNS caching?**
    Storing recent DNS lookups (IP to domain mapping) locally (in browser, OS, or local router) for a set Time-To-Live (TTL). This speeds up subsequent requests for the same domain and reduces load on DNS servers.

15. **What is the difference between hub, switch, router?**
    - **Hub:** Layer 1. Dumb device. Broadcasts all data to all connected ports. Causes collisions.
    - **Switch:** Layer 2. Smart device. Learns MAC addresses and forwards data only to the specific intended port.
    - **Router:** Layer 3. Connects different networks together (e.g., LAN to WAN). Routes packets based on IP addresses.

16. **What is a VLAN?**
    Virtual Local Area Network. It allows you to logically segment a single physical switch into multiple isolated networks. This improves security and broadcast traffic management without needing separate hardware switches for each department.

17. **What is the default gateway?**
    The default gateway is the IP address of the router interface on the local network. It is the "door" that devices use to send traffic to devices outside their own local subnet (e.g., to the internet).

18. **What does 169.254.x.x mean?**
    It is an APIPA (Automatic Private IP Addressing) address. If a Windows machine is configured to use DHCP but cannot reach the DHCP server, it automatically assigns itself an IP in this range. It indicates a DHCP failure or network connectivity issue to the server.

19. **What is MTU?**
    Maximum Transmission Unit. It defines the maximum size of a packet (in bytes) that can be sent over a network connection. Standard Ethernet MTU is 1500 bytes. If a packet is larger, it must be fragmented.

20. **What is latency vs bandwidth vs throughput?**
    - **Bandwidth:** The maximum theoretical capacity of a pipe (e.g., 100 Mbps).
    - **Throughput:** The actual amount of data successfully transferred over the link (usually less than bandwidth).
    - **Latency:** The time delay it takes for a packet to travel from source to destination (ping time).

### Top 10 Windows Questions (with complete answers)

1. **What is Active Directory at a basic level?**
   Active Directory (AD) is a centralized database and identity management service created by Microsoft. It stores information about users, computers, and groups within a domain, authenticates logins via Kerberos, and enforces security policies across the network.

2. **What is Group Policy and how does `gpupdate /force` work?**
   Group Policy (GPO) allows administrators to manage and configure operating systems, applications, and users' settings remotely from Active Directory. `gpupdate /force` manually forces a Windows client to immediately contact the domain controller and re-apply all Group Policy objects, skipping the normal background refresh interval.

3. **How do you check Windows Event Viewer for a service crash?**
   I would open `eventvwr.msc`, navigate to Windows Logs > Application or System. I'd filter the log for "Error" or "Critical" levels, particularly looking for Event IDs related to Service Control Manager (like Event ID 7034: Service terminated unexpectedly).

4. **What does `sfc /scannow` do?**
   System File Checker is a Windows utility that scans all protected system files for corruption and replaces corrupted or missing files with a cached copy located in a compressed folder at `%WinDir%\System32\dllcache`. It's a go-to command for OS stability issues.

5. **How do you force quit a frozen application from CMD?**
   I would use `tasklist` to find the Image Name or PID, then use `taskkill`.
   Example: `taskkill /F /IM notepad.exe` (Force kill by Image Name)
   or `taskkill /F /PID 1234` (Force kill by Process ID).

6. **What is the difference between local admin and domain admin?**
   - **Local Admin:** Has full control only over that specific single computer.
   - **Domain Admin:** Has full control over all computers, servers, and user accounts within the entire Active Directory domain. It is a highly privileged account.

7. **How do you map a network drive in Windows?**
   - GUI: Open "This PC", click "Map network drive", select a letter, and enter the path `\\ServerIP\SharedFolder`.
   - CMD: `net use Z: \\ServerName\ShareName`

8. **What does `ipconfig /release` and `/renew` do?**
   - `/release` drops the currently assigned DHCP IP address.
   - `/renew` broadcasts a new DHCP request to the network to obtain a fresh IP address lease from the DHCP server. Useful for fixing IP conflicts or moving networks.

9. **How do you check startup programs in Windows?**
   - Task Manager -> "Startup" tab.
   - For deeper inspection, the `msconfig` utility or the Sysinternals tool "Autoruns".

10. **What are the most important Windows Event IDs?**
    - 4624: Successful Logon
    - 4625: Failed Logon
    - 7036: Service started/stopped
    - 4720: User account created

### Top 20 Command-Based Questions (with complete answers)

*See Part 3 Cheat Sheets for detailed command breakdowns.*

### Top 15 Security Questions (with complete answers)

1. **How do you secure a Linux server? (practical checklist)**
   - Disable direct root login via SSH (`PermitRootLogin no`).
   - Use SSH Key-based authentication and disable password auth.
   - Change default SSH port (optional but reduces bot spam).
   - Configure a firewall (ufw or firewalld) to only allow necessary ports (22, 80, 443).
   - Keep the system updated (`apt update && apt upgrade`).
   - Implement fail2ban to block brute-force attacks.
   - Enforce Principle of Least Privilege for users.

2. **What is the principle of least privilege?**
   Giving a user, program, or process only the bare minimum permissions necessary to perform its intended function, and nothing more. This limits the blast radius if an account is compromised.

3. **What is SSH key-based authentication vs password auth?**
   Password auth requires a text string that can be brute-forced or intercepted. Key-based auth uses a cryptographic keypair (Public key on server, Private key on client). It is mathematically almost impossible to brute-force and much more secure.

4. **How do you configure ufw (uncomplicated firewall) on Ubuntu?**
   - `sudo ufw default deny incoming`
   - `sudo ufw default allow outgoing`
   - `sudo ufw allow ssh` (or `sudo ufw allow 2222/tcp` if changed)
   - `sudo ufw allow http`
   - `sudo ufw enable`
   - `sudo ufw status verbose`

5. **What is sudo and how does `/etc/sudoers` work?**
   `sudo` (Superuser DO) allows permitted users to execute a command as root or another user. The `/etc/sudoers` file defines exactly who can run what commands. It should always be edited using `visudo` to prevent syntax errors that could lock you out.

6. **What are the most dangerous permissions in Linux?**
   `777` (Read, Write, Execute for Everyone). This allows any user on the system or any compromised service to modify or execute a file, leading to severe security breaches.

7. **What is fail2ban?**
   It's an intrusion prevention software framework. It monitors log files (e.g., `/var/log/auth.log` for SSH) for too many failed login attempts and dynamically updates firewall rules to temporarily or permanently ban the attacking IP address.

8. **How do you detect unauthorized logins on a Linux server?**
   Check the `last` command for login history. Review `/var/log/auth.log` (Ubuntu) or `/var/log/secure` (CentOS) for accepted or failed login attempts. Check `who` or `w` for currently logged-in users.

9. **What is SSL/TLS?**
   Secure Sockets Layer and its modern successor Transport Layer Security are cryptographic protocols designed to provide communications security over a computer network (like HTTPS). They encrypt data in transit so man-in-the-middle attackers cannot read it.

10. **What is the difference between antivirus and EDR?**
    - **Antivirus (AV):** Signature-based, looks for known bad files and malware.
    - **EDR (Endpoint Detection and Response):** Behavior-based. It monitors endpoint activity in real-time, looking for anomalous behavior (like an innocent-looking word doc trying to launch powershell) and allows security teams to investigate and isolate threats.

11. **How would you respond to a suspected ransomware attack?**
    1. **Isolate:** Immediately disconnect the infected machine(s) from the network (pull the cable/disable NIC) to prevent lateral movement. Do not power it off immediately as RAM data might be needed for forensics.
    2. **Report:** Notify the security team and management.
    3. **Identify:** Determine the strain of ransomware.
    4. **Restore:** Rebuild the machine from scratch and restore data from isolated, immutable backups. Never pay the ransom.

12. **What is patch management and why is it important?**
    The process of testing, acquiring, and installing updates (patches) on systems and software. It is critical because attackers constantly exploit known, publicly disclosed vulnerabilities in unpatched software.

13. **What is 2FA and how does it work?**
    Two-Factor Authentication requires two different forms of identification before granting access. Usually: Something you know (password) + Something you have (a code from a phone app like Google Authenticator or a hardware token).

14. **What are signs that a Windows machine might be compromised?**
    Unexpected high CPU/network usage, antivirus being disabled, unknown startup programs in Task Manager, strange pop-ups, inability to access certain files, or unauthorized accounts created.

15. **What is a firewall rule and how does iptables work basically?**
    A rule defines what traffic is allowed or blocked based on IP, port, or protocol. `iptables` is the traditional Linux kernel firewall. It uses chains (INPUT, OUTPUT, FORWARD) and rules evaluated top-to-bottom. If a packet matches a rule, the target action (ACCEPT, DROP, REJECT) is taken.

---

## PART 2: CONNECTING DEVOPS TO SYSTEM ENGINEERING

As a fresher with DevOps knowledge applying for a SysEng role, your strategy is to frame DevOps not as "I want to be a developer," but as "I know how modern IT operations work."

1. **"How would you monitor a Linux server?"**
   → *Sysadmin Answer:* "I would use `top` or `htop` for live CPU/RAM usage, `df -h` for disk space, and check `/var/log/syslog` for errors."
   → *DevOps Add:* "While I'm comfortable doing that manually, in my projects I've also set up Prometheus with node_exporter to scrape these metrics and Grafana to visualize them, which gives a better historical view of server health."

2. **"How would you automate repetitive system administration tasks?"**
   → *Sysadmin Answer:* "I write Bash scripts and schedule them using `cron` jobs."
   → *DevOps Add:* "Bash is great for local tasks, but for configuring multiple servers simultaneously, I've learned the basics of Ansible, which allows for declarative configuration management."

3. **"How do you manage server configuration?"**
   → *Sysadmin Answer:* "I document changes, backup `/etc` configuration files before editing them with `nano` or `vim`, and restart the service."
   → *DevOps Add:* "I also believe in treating configurations like code. Pushing config files to a private Git repository ensures we have version history and can rollback easily if a change breaks the system."

4. **"What experience do you have with virtualization?"**
   → *Sysadmin Answer:* "I have used VMware Workstation and Oracle VirtualBox to create and manage Windows and Linux VMs, configuring their network adapters."
   → *DevOps Add:* "I'm also familiar with containerization using Docker. While full VMs are great for isolating whole operating systems, Docker has taught me how to isolate applications efficiently using shared kernel resources."

5. **"How would you handle deploying an application update on a server?"**
   → *Sysadmin Answer:* "I would schedule a maintenance window, take a backup of the current app and database, transfer the new files via SFTP, and restart the web server."
   → *DevOps Add:* "I understand that modern teams automate this using CI/CD pipelines like Jenkins or GitHub Actions to deploy with zero downtime, which reduces manual errors."

6. **"What is containerization?"**
   → *Sysadmin/DevOps Answer:* "It's a way to package an application and all its dependencies into a single image (like Docker). As a system engineer, I see it as a huge benefit because it solves the 'it works on my machine' problem, making deploying software to our servers much more predictable."

7. **"How do you manage logs at scale?"**
   → *Sysadmin Answer:* "I ensure `logrotate` is configured correctly so logs don't fill up the disk, and use `grep` or `awk` to search through them."
   → *DevOps Add:* "For larger environments, I'm aware of centralized logging solutions like the ELK stack (Elasticsearch, Logstash, Kibana) which aggregate logs from all servers into one dashboard."

8. **"What is Infrastructure as Code?"**
   → *Sysadmin/DevOps Answer:* "IaC, like Terraform, is writing code to provision servers and networks instead of clicking through a cloud console. It's highly relevant to system engineering because it allows us to build disaster recovery environments in minutes, consistently."

9. **"How do you ensure a server is always running?"**
   → *Sysadmin Answer:* "I configure services to start on boot using `systemctl enable`, set up hardware RAID for disk redundancy, and ensure dual power supplies."
   → *DevOps Add:* "I also understand the shift towards high availability architectures, where we might use a load balancer to distribute traffic across multiple servers, or Kubernetes to automatically restart failed containers."

10. **"What is CI/CD and is it relevant to System Engineering?"**
    → *Answer:* "Continuous Integration/Continuous Deployment automates software delivery. For a System Engineer, it's highly relevant. Even if we aren't writing application code, we can use CI/CD to automatically test and deploy infrastructure scripts, OS patches, or configuration changes securely."

---

## PART 3: COMPLETE COMMAND CHEAT SHEETS

### Linux Command Cheat Sheet

| Command | Purpose | Quick Example | Troubleshooting Use |
| :--- | :--- | :--- | :--- |
| **FILE OPERATIONS** | | | |
| `ls -lah` | List files with hidden and details | `ls -lah /var/log` | Checking file permissions & sizes |
| `cd` | Change directory | `cd /etc/nginx` | Navigating filesystem |
| `pwd` | Print working directory | `pwd` | Finding exactly where you are |
| `cp -r` | Copy files/folders | `cp -r /var/www /backup` | Making config backups before changes |
| `mv` | Move or rename files | `mv config.bak config.txt` | Restoring backups |
| `rm -rf` | Remove forcefully (Careful!) | `rm -rf /tmp/cache` | Clearing bad cache |
| `mkdir -p` | Create nested directories | `mkdir -p /opt/app/data` | Prepping paths for apps |
| `touch` | Create empty file / update timestamp | `touch trigger.txt` | Testing write permissions |
| `find` | Search for files | `find / -name "*.log"` | Locating missing config files |
| `tar` | Archive files | `tar -czvf logs.tar.gz /var/log` | Compressing logs to send to vendor |
| **USER & PERMISSIONS** | | | |
| `chmod` | Change permissions | `chmod 755 script.sh` | Fixing "permission denied" execution |
| `chown` | Change owner | `chown nginx:nginx /var/www` | Fixing web server 403 errors |
| `passwd` | Change user password | `passwd johndoe` | Password resets |
| `sudo` | Run as root | `sudo systemctl restart` | Escalate privileges safely |
| `usermod` | Modify user account | `usermod -aG docker user` | Adding users to admin groups |
| `whoami` | Show current user | `whoami` | Verifying active session context |
| `w` | Show who is logged in | `w` | Checking for unauthorized active sessions |
| **PROCESS MANAGEMENT** | | | |
| `top` / `htop`| Real-time process monitor | `top` | Finding CPU/RAM hogging processes |
| `ps aux` | Snapshot of all processes | `ps aux \| grep apache` | Finding PID of a hung service |
| `kill -9` | Force kill process | `kill -9 1234` | Stopping a frozen process via PID |
| `killall` | Kill process by name | `killall nginx` | Stopping all workers at once |
| `systemctl` | Manage system services | `systemctl status sshd` | Checking if service crashed |
| **DISK & STORAGE** | | | |
| `df -h` | Show disk free space | `df -h` | Diagnosing "No space left on device" |
| `du -sh` | Show directory usage | `du -sh /var/log/*` | Finding which folder ate the disk |
| `lsblk` | List block devices (disks) | `lsblk` | Viewing attached disks and mounts |
| `fdisk -l` | List partition tables | `sudo fdisk -l` | Checking new disk recognition |
| `mount` | Mount a filesystem | `mount /dev/sdb1 /data` | Accessing secondary drives |
| **NETWORK** | | | |
| `ping` | Check connectivity | `ping 8.8.8.8` | Testing outside internet access |
| `ip a` | Show IP addresses | `ip a` | Finding the server's IP |
| `ss -tulnp` | Show listening ports | `ss -tulnp` | Checking if a webserver bound to port 80 |
| `netstat` | Network statistics | `netstat -an` | Looking for established connections |
| `curl` | Transfer data from URL | `curl -I http://localhost` | Testing local web server response |
| `wget` | Download file | `wget url.com/file.zip` | Pulling patches/software directly |
| `traceroute`| Trace network path | `traceroute google.com` | Finding where connection drops |
| `dig` / `nslookup`| DNS lookup | `dig google.com` | Troubleshooting DNS resolution |
| **LOG ANALYSIS** | | | |
| `tail -f` | Follow log file in real-time | `tail -f /var/log/syslog` | Watching for errors during app start |
| `grep -i` | Search text in files | `grep -i "error" /var/log` | Finding specific crash strings |
| `less` | View files interactively | `less /var/log/messages` | Scrolling through huge log files |
| `journalctl` | Query systemd journal | `journalctl -xe` | Deep-diving into service start failures |

### Windows CMD & PowerShell Cheat Sheet

| Command / Cmdlet | Purpose | Example / When to Use |
| :--- | :--- | :--- |
| `ipconfig /all` | Full network config | Finding MAC, DHCP, DNS details |
| `ipconfig /flushdns` | Clear DNS cache | Fix "website not found" but internet works |
| `ping -t` | Continuous ping | `ping -t 8.8.8.8` (Ctrl+C to stop) |
| `tracert` | Windows traceroute | `tracert 8.8.8.8` (Find routing loops) |
| `netstat -anob` | Ports with executable | Find which exe is using port 80 (Run as Admin) |
| `nslookup` | Query DNS | `nslookup domain.com` |
| `tasklist` | Show running processes| Look up memory usage |
| `taskkill /f /im` | Force kill by name | `taskkill /f /im excel.exe` (Frozen app) |
| `sfc /scannow` | System File Checker | Fix corrupt Windows OS files |
| `chkdsk /f /r` | Check/Repair Disk | Fix bad sectors or NTFS file system errors |
| `gpupdate /force` | Update Group Policy | Apply AD policies immediately |
| `systeminfo` | Detailed OS/Hardware info | Check boot time, OS version, RAM |
| `Test-NetConnection` | (PS) Advanced ping | `Test-NetConnection 8.8.8.8 -Port 443` |
| `Get-Service` | (PS) List services | `Get-Service -Name "Spooler"` |
| `Restart-Service`| (PS) Restart service | `Restart-Service -Name "Spooler"` (Fix printer) |
| `Get-Process` | (PS) List processes | `Get-Process \| Sort-Object CPU -Descending` |

---

## PART 4: ONE-PAGE LAST-MINUTE REVISION SHEET

### 🐧 TOP 10 LINUX FACTS
1. **Everything is a file** (even hardware in `/dev`).
2. **Root (/)** is the base; `/etc` is configs, `/var` is logs, `/home` is users.
3. **Permissions:** `r=4, w=2, x=1`. `755` = owner all, group/others read+exec.
4. **sudo:** Runs commands as root; configured in `/etc/sudoers`.
5. **cron:** Time-based job scheduler.
6. **systemd:** Modern init system (`systemctl start/stop/status/enable`).
7. **SSH:** Secure Shell (Port 22), best secured with Key Pairs, not passwords.
8. **Package Managers:** `apt` (Debian/Ubuntu), `yum/dnf` (RHEL/CentOS).
9. **SIGTERM (15)** asks nicely; **SIGKILL (9)** assassinates immediately.
10. **Logs:** Mostly live in `/var/log` (syslog, auth.log, messages).

### 🪟 TOP 10 WINDOWS FACTS
1. **Active Directory:** Centralized DB for Users, Computers, Policies (Kerberos/LDAP).
2. **Group Policy (GPO):** Centralized configuration management.
3. **Registry (regedit):** Hierarchical DB storing OS/App low-level settings.
4. **Event Viewer:** The source of truth for troubleshooting (App, Security, System logs).
5. **Services.msc:** Manage background processes (Start, Stop, Automatic).
6. **NTFS:** Default file system (supports permissions, encryption, large files).
7. **Local vs Domain:** Local accounts only exist on one PC; Domain on all AD PCs.
8. **PowerShell:** Object-oriented shell, far superior to legacy CMD.
9. **Task Manager:** Quick look at processes, performance, startups.
10. **RDP:** Remote Desktop Protocol (Port 3389).

### 🌐 NETWORKING & PORTS
**OSI Model:**
7. Application (HTTP, DNS)
6. Presentation (SSL/TLS)
5. Session (NetBIOS)
4. Transport (TCP, UDP) -> *Segments*
3. Network (IP, ICMP, Routers) -> *Packets*
2. Data Link (MAC, Switches) -> *Frames*
1. Physical (Cables, Hubs) -> *Bits*

**Must-Know Ports:**
- **21:** FTP
- **22:** SSH
- **23:** Telnet (Insecure)
- **25:** SMTP (Email Out)
- **53:** DNS (UDP for query, TCP for zone transfer)
- **80:** HTTP
- **443:** HTTPS
- **3389:** RDP

### 🛠️ UNIVERSAL TROUBLESHOOTING (The 5 Steps)
1. **Identify the Problem:** Ask the user, replicate the issue. "Is it just you or everyone?"
2. **Check the Basics:** Are cables plugged in? Is there power? Is the IP valid?
3. **Establish a Theory:** (Bottom-up OSI approach) Ping local -> Ping gateway -> Ping 8.8.8.8 -> DNS check.
4. **Test & Fix:** Apply the fix (e.g., restart service, flush DNS).
5. **Verify & Document:** Ensure it works, tell the user, document the fix in ticketing system.

---

## PART 5: INTERVIEW BEHAVIORAL ANSWERS

### 60-Second Self-Introduction
"Good morning, my name is Nihal Kumar Singh. I’m a Computer Science graduate passionate about IT infrastructure and operations. During my academic journey, while I studied programming, I found myself much more interested in the servers, networks, and environments that make code run. I've built a strong foundation in Linux administration, networking, and Windows troubleshooting.

To prepare for the modern IT landscape, I also trained myself in DevOps tools like Docker, AWS, and CI/CD pipelines. Rather than just building applications, my goal is to maintain, secure, and automate the infrastructure they run on. I'm applying for this System Engineer role because it allows me to apply my core sysadmin skills in a hands-on way while bringing a modern, automation-focused mindset to the team."

### "Why Should We Hire You?"
"You should hire me because I offer a strong blend of traditional IT fundamentals and modern infrastructure practices. I have a solid grip on Linux, Windows OS, and networking, which means I can handle day-to-day troubleshooting and system administration immediately. However, my background in DevOps tools like Docker and scripting means I bring an 'automation-first' mindset. I don't just want to fix a problem manually ten times; I want to fix it, document it, and script it so it doesn't happen an eleventh time. I’m eager to learn your specific environment and contribute quickly."

### "Why System Engineer When You Know DevOps?"
"I get this question often! The truth is, DevOps isn't just a title, it's a culture, and its foundation is rock-solid system engineering. You can't effectively automate a server, containerize an application, or secure a network pipeline if you don't deeply understand Linux, DNS, and file systems first. I see the System Engineer role as the perfect place to master the fundamentals of enterprise IT infrastructure. I want to build a deep understanding of production systems, and over time, leverage my DevOps knowledge to help automate operations right here on this team."

### "Why Do You Want This Job?" (Gurugram Specific)
"I am highly interested in this role because your company has a strong reputation for maintaining robust IT infrastructure in Gurugram’s tech hub. As a fresher, I am looking for a dynamic environment where I can handle a high volume of diverse IT challenges—from basic Windows troubleshooting to managing Linux servers. This role perfectly aligns with my goal to get hands-on enterprise experience, and being in Gurugram means being part of a fast-paced, high-growth professional ecosystem where I can rapidly accelerate my learning curve."

### "Where Do You See Yourself in 3 Years?"
"In three years, I see myself as a highly reliable senior member of this infrastructure team. I want to have mastered the specifics of your environment to the point where I am the go-to person for complex critical escalations. Furthermore, I hope to have successfully introduced some automation initiatives—perhaps using scripts or Ansible to reduce the team's manual workload—transitioning naturally into a Site Reliability Engineering or platform-focused capability within the company."

### "Tell Me About a Technical Challenge You Solved"
*(Use the STAR Method - Situation, Task, Action, Result. Adapt this to a real project if you have one)*
**Situation:** "While setting up a multi-tier application project on AWS, my web server couldn't communicate with my database server."
**Task:** "I needed to troubleshoot and restore connectivity without exposing the database to the internet."
**Action:** "I took a systematic approach. First, I verified the database was running and listening on port 3306 using `ss -tulnp`. Then, I tried to ping the DB server from the web server and it failed. I checked the AWS Security Groups (firewall rules) and realized the DB security group was only allowing traffic from my personal IP, not the web server's subnet. I modified the rule to allow port 3306 only from the web server's security group."
**Result:** "The connection was established, the application worked, and I learned a vital lesson about network segmentation and firewall troubleshooting in cloud environments."

### "What Do You Know About Active Directory?"
"As a fresher, my hands-on enterprise experience with AD is limited, but I have a strong conceptual understanding. I know Active Directory is a centralized directory service by Microsoft. It's essentially the 'source of truth' for identity management in an organization. It allows administrators to create users, assign them to security groups, authenticate them via Kerberos, and apply configurations across hundreds of machines simultaneously using Group Policy. If a user needs password resets, or a department needs mapped network drives, it's handled through AD."

### "Have You Worked in a Production Environment?"
"I haven't worked in a corporate production environment yet, but I have treated my academic and personal projects with production-level standards. I use Git for version control on all my configuration files, I document my architectures, and I’ve practiced using CI/CD pipelines to deploy code safely rather than manual uploads. I'm very aware that in a real production environment, downtime costs money, changes require approvals, and taking backups before touching anything is mandatory. I am ready to adapt to those strict enterprise protocols."

### Questions to Ask the Interviewer (Pick 2-3)
1. "Can you describe the typical infrastructure stack I would be supporting in my first six months?"
2. "How does the team handle out-of-hours critical alerts or server downtime?"
3. "Are there opportunities in this role to implement automation for repetitive tasks?"
4. "What is the biggest technical challenge your IT infrastructure team is facing right now?"
5. "What ticketing system and monitoring tools do you currently use?"

---

## PART 6: MOCK TECHNICAL INTERVIEW

**Interviewer:** Let's get started. Tell me about yourself.
**Strong Answer:** My name is Nihal Kumar Singh, a CSE graduate with a passion for IT infrastructure. I've built a solid foundation in Linux, networking, and Windows systems. Beyond the basics, I've upskilled in DevOps practices like Docker, AWS, and scripting. I'm looking for a System Engineer role where I can handle day-to-day operations while bringing an automation-focused mindset to the team.
**Score:** 9/10
**What's correct:** Confident, mentions CSE, highlights both core sysadmin and modern DevOps skills.
**What to add:** Keep it under 60 seconds and sound conversational.

**Interviewer:** Great. What is Linux and why is it so heavily used in servers compared to Windows?
**Strong Answer:** Linux is an open-source operating system kernel. It's preferred for servers because it is highly stable, secure, consumes fewer hardware resources (as it can run without a GUI), and is completely free. It also offers incredible flexibility and powerful command-line tools for automation.
**Score:** 10/10

**Interviewer:** What is the difference between TCP and UDP?
**Strong Answer:** TCP is connection-oriented; it uses a 3-way handshake to establish a connection, guarantees data delivery, and ensures packets arrive in order. It's used for HTTP, SSH, etc. UDP is connectionless; it just sends packets without checking if they arrived. It's faster but unreliable, used for DNS, video streaming, and VoIP.
**Score:** 10/10

**Interviewer:** A user complains their computer has no internet. What is your first step?
**Strong Answer:** First, I'd check physical layer basics: is the network cable plugged in or Wi-Fi connected? If yes, I'd open CMD and run `ipconfig` to check if they have a valid IP address.
**Score:** 8/10
**Improved answer:** Add the OSI model troubleshooting approach. "I'd use the bottom-up approach. Layer 1: Check the physical cable/Wi-Fi. Layer 3: Run `ipconfig` to ensure they have a valid IP, not a 169.254 APIPA address. Then try to ping the default gateway, and finally ping an external IP like 8.8.8.8."

**Interviewer:** What does the command `df -h` show?
**Strong Answer:** `df` stands for Disk Free. The `-h` flag makes it human-readable. It shows the amount of free and used disk space on all mounted filesystems.
**Score:** 10/10

**Interviewer:** What is DHCP and how does it work?
**Strong Answer:** DHCP stands for Dynamic Host Configuration Protocol. It automatically assigns IP addresses to devices on a network. It works using the DORA process: the client broadcasts a Discover message, the server Offers an IP, the client sends a Request for it, and the server sends an Acknowledgment.
**Score:** 10/10

**Interviewer:** What is the difference between a router and a switch?
**Strong Answer:** A switch operates at Layer 2 and connects devices within the same local network, using MAC addresses to forward frames. A router operates at Layer 3 and connects different networks together, like a LAN to the internet, routing packets based on IP addresses.
**Score:** 10/10

**Interviewer:** How do you check which process is consuming the most CPU on a Linux server?
**Strong Answer:** I would use the `top` or `htop` command. By default, it sorts processes by CPU usage, so the top process is the one consuming the most. Alternatively, I could use `ps aux --sort=-%cpu | head`.
**Score:** 10/10

**Interviewer:** What does `chmod 755 filename` do?
**Strong Answer:** It sets file permissions. The owner gets full rights (Read, Write, Execute - 7). The group and others get read and execute rights only (5).
**Score:** 10/10

**Interviewer:** A user got an IP of 169.254.x.x. What does this mean and what will you do?
**Strong Answer:** That is an APIPA address. It means the computer is set to DHCP but cannot communicate with the DHCP server to get an IP. I would check physical connectivity to the switch, verify the DHCP server is running, and try `ipconfig /release` and `ipconfig /renew`.
**Score:** 10/10

**Interviewer:** How do you restart a service on modern Linux?
**Strong Answer:** I would use `systemctl restart <servicename>`. For example, `systemctl restart sshd`.
**Score:** 9/10
**Follow-up:** Also mention checking status afterward with `systemctl status <servicename>`.

**Interviewer:** What is the OSI model? Name the 7 layers.
**Strong Answer:** It's a conceptual model for network communication. The layers from bottom to top are: Physical, Data Link, Network, Transport, Session, Presentation, Application. (Please Do Not Throw Sausage Pizza Away).
**Score:** 10/10

**Interviewer:** A Linux server disk is 100% full. What do you do?
**Strong Answer:** First, I'd run `df -h` to confirm which partition is full. Then I'd use `du -sh /*` to find the largest directories, drilling down to find the culprit. It's usually massive log files in `/var/log`. I'd delete or compress old logs, then look into configuring `logrotate`.
**Score:** 10/10

**Interviewer:** What is Active Directory?
**Strong Answer:** Active Directory is a Microsoft centralized identity management system. It authenticates users, manages permissions, and enforces security policies via Group Policy across all Windows machines in a domain.
**Score:** 10/10

**Interviewer:** How would you secure SSH access on a Linux server?
**Strong Answer:** I would disable root login, change the default port from 22, configure the firewall to only allow SSH from specific IP ranges, and most importantly, disable password authentication and mandate SSH Key-based authentication.
**Score:** 10/10

**Interviewer:** What is the difference between `ps aux` and `top`?
**Strong Answer:** `ps aux` takes a static snapshot of processes at that exact moment. `top` provides an interactive, real-time, continuously updating dashboard of processes and resource usage.
**Score:** 10/10

**Interviewer:** What is a firewall? How is it different from a router?
**Strong Answer:** A firewall is a security device or software that monitors and filters incoming and outgoing network traffic based on predefined security rules (like allowing port 80, dropping port 22). While a router just moves packets between networks to get them to their destination, a firewall inspects the packets to decide if they are allowed to pass at all.
**Score:** 10/10

**Interviewer:** How do you troubleshoot a slow Windows PC?
**Strong Answer:** I'd open Task Manager to check if CPU, Memory, or Disk is maxed out. If Disk is at 100%, it might be a failing HDD or Windows Update running. I'd check the Startup tab to disable unnecessary programs. I'd also check system uptime and ask the user to do a full restart, not just a shutdown, to clear RAM.
**Score:** 10/10

**Interviewer:** Given your DevOps background, how is Docker relevant to System Engineering?
**Strong Answer:** Docker allows us to package an application with all its dependencies into an isolated container. For a System Engineer, this means no more "dependency hell" where an app breaks because the server has the wrong Python version. It makes deploying, updating, and scaling applications on our servers much more predictable and cleaner.
**Score:** 10/10

**Interviewer:** What questions do you have for us?
**Strong Answer:** Yes! Could you tell me about the most common types of infrastructure issues your team faces daily? And what monitoring tools do you currently use?
**Score:** 10/10

---

## PART 7: TOP 5 TROUBLESHOOTING SCENARIOS (Interview-Ready)

### Scenario 1: "No internet on 5 machines simultaneously this morning."
**How to answer:**
"Since it's 5 machines simultaneously, the issue is highly likely network-wide, not localized to a single OS.
1. **User Comm:** I would inform the users we are investigating a network issue.
2. **Isolate:** I'd find out if these 5 machines are in the same physical area (same switch) or different areas.
3. **Check Switch/Router:** I'd log into the local switch to check for power issues, port errors, or loops.
4. **IP Check:** I'd have one user run `ipconfig`. If they have a `169.254.x.x` address, the DHCP server is down or unreachable. If they have a valid IP, I'd ping the default gateway.
5. **Resolution:** If the gateway is unreachable, I'd restart the switch or check the uplink. If the gateway replies but `ping 8.8.8.8` fails, our ISP link or edge firewall might be down. I'd systematically trace the path outwards."

### Scenario 2: "A critical Linux server is unreachable and team can't SSH."
**How to answer:**
"1. **Ping Test:** First, I'll ping the server IP. If it replies, the network is fine but the SSH service might have crashed or a firewall rule changed.
2. **Console Access:** Since SSH is down, I would log into the server via the hypervisor console (like vSphere) or physical KVM.
3. **Check Service:** Once in, I'd run `systemctl status sshd` to see if the service crashed. If it did, I'd check `journalctl -u sshd` to find out why.
4. **Check Resources:** If the server was entirely unresponsive to ping, the server might have kernel panicked, run out of memory (OOM killer), or powered off. I'd check the hypervisor level.
5. **Fix:** Restart the SSH service or gracefully reboot the server if it's completely frozen."

### Scenario 3: "Disk alert: Server at 100% capacity. Application team unavailable."
**How to answer:**
"1. **Verify:** I'd SSH into the server and run `df -h` to confirm which partition is 100% full.
2. **Locate:** I'd run `du -sh /*` to find the largest directories, then drill down (e.g., `du -sh /var/*`, then `du -sh /var/log/*`) to find the exact files consuming space.
3. **Safe Cleanup:** It's usually runaway log files. Since the app team isn't there, I will not delete application data. Instead, I will find old rotated log files (like `syslog.1.gz`) and delete them, or truncate the current massive log file using `> /var/log/hugeapp.log` without deleting the file itself, to immediately free up space and stop the server from crashing.
4. **Document:** I'd document exactly what was cleared and notify the app team."

### Scenario 4: "A user's application keeps crashing after a Windows update."
**How to answer:**
"1. **Replicate & Isolate:** I'd ask the user to demonstrate the crash. I'd check if it happens for other users (to rule out a network app issue).
2. **Event Viewer:** I'd open `eventvwr.msc`, go to Windows Logs > Application, and look for red Error events at the exact time of the crash. This usually names the faulty `.dll` or module.
3. **Compatibility:** Since it happened after an update, the update likely broke compatibility. I'd check if there's a patch available from the application vendor.
4. **Resolution:** If no patch exists, I would use Control Panel to uninstall the specific recent Windows KB Update that caused the issue, reboot, verify the app works, and temporarily pause updates for that machine while opening a ticket with the app vendor."

### Scenario 5: "A user suspects their machine has malware — behaving strangely."
**How to answer:**
"1. **Immediate Action:** Containment is priority one. I would instruct the user to immediately unplug their Ethernet cable and disconnect from Wi-Fi to prevent lateral movement of the malware to the rest of the network.
2. **Investigate Offline:** I would physically go to the machine. I'd check Task Manager for unfamiliar high-resource processes. I'd check Startup apps.
3. **Scan:** I would run a full, deep scan using our enterprise Antivirus/EDR solution (which should have offline definitions).
4. **Resolution:** If a severe infection is found (like ransomware signs or rootkits), standard practice is not to trust the OS anymore. I would back up only their user files (after scanning them), wipe the drive, and reimage the machine from a clean baseline image."
