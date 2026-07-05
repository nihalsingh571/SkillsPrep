# Appendix B: Final Interview Preparation

This appendix provides **600 technical interview questions and answers** across eight domains. It is designed as a rapid-fire study guide for DevOps, SRE, Cloud, and Linux Systems Administrator interviews.

---

## Part 1: 100 Linux Interview Questions & Answers

1. **What is the Linux kernel?**
   * *Answer:* The core software component of the OS that sits between hardware and applications, managing CPU, memory, storage, and device drivers.
2. **Explain the difference between a hard link and a soft (symbolic) link.**
   * *Answer:* A hard link points directly to the file's physical data on disk (same inode). If the original file is deleted, the hard link remains functional. A soft link is a shortcut pointing to the file path (different inode). If the original file is deleted, the soft link breaks.
3. **What is an inode?**
   * *Answer:* An index node on a filesystem containing metadata about a file (permissions, size, owner, creation date, physical blocks location) but NOT the filename or actual data.
4. **How do you find the inode number of a file?**
   * *Answer:* Run `ls -i <filename>`.
5. **What is the difference between `/bin` and `/sbin`?**
   * *Answer:* `/bin` contains essential binaries for all users (e.g., `ls`, `cp`). `/sbin` contains system binaries reserved for the system administrator (`root`) for configurations and repairs (e.g., `fdisk`, `iptables`).
6. **Explain the boot process of a Linux system.**
   * *Answer:* BIOS/UEFI initializes hardware -> GRUB Bootloader loads kernel -> Kernel mounts root filesystem and starts PID 1 (`systemd`) -> `systemd` starts system services.
7. **What is `systemd`?**
   * *Answer:* The modern system initialization daemon and service manager in Linux. It runs with PID 1 and starts services in parallel using targets.
8. **How do you check the resource usage of a system in real-time?**
   * *Answer:* Run `top` or `htop`.
9. **Explain system load average.**
   * *Answer:* Represents the average number of active, runnable, or blocked processes over 1, 5, and 15 minutes.
10. **How do you check system uptime?**
    * *Answer:* Run the `uptime` command.
11. **What is swap space, and when is it used?**
    * *Answer:* A designated area on a storage drive used when physical RAM is fully depleted. The kernel moves inactive pages from RAM to swap space.
12. **How do you view partition sizes and disk space consumption?**
    * *Answer:* Run `df -h`.
13. **How do you check the disk usage of a specific folder?**
    * *Answer:* Run `du -sh <folder_path>`.
14. **What is the Out-Of-Memory (OOM) Killer?**
    * *Answer:* A kernel feature that monitors RAM. When memory is exhausted, it terminates processes using algorithms to avoid system-wide crashes.
15. **What does the command `free -m` do?**
    * *Answer:* Displays physical memory (RAM) and Swap usage in megabytes.
16. **How do you check kernel boot diagnostic logs?**
    * *Answer:* Run `dmesg`.
17. **What is `/proc` directory used for?**
    * *Answer:* A virtual filesystem exposing kernel configurations and active process states dynamically.
18. **Explain the difference between `ps aux` and `ps -ef`.**
    * *Answer:* Both display all running system processes. `aux` uses BSD syntax formatting, while `-ef` uses UNIX System V syntax.
19. **What is a zombie process?**
    * *Answer:* A defunct process that has finished executing but remains in the process table because its parent hasn't read its exit status.
20. **What is an orphan process?**
    * *Answer:* A running process whose parent has terminated. It is adopted by PID 1 (`systemd`), which handles its exit.
21. **How do you kill a process?**
    * *Answer:* Run `kill <PID>` (SIGTERM) or `kill -9 <PID>` (SIGKILL).
22. **What does signal code 9 represent?**
    * *Answer:* `SIGKILL` - immediately terminates the process.
23. **What does signal code 15 represent?**
    * *Answer:* `SIGTERM` - requests graceful shutdown.
24. **How do you reload a service configuration without restarting it?**
    * *Answer:* Run `sudo systemctl reload <service>` (sends `SIGHUP` signal).
25. **What is a daemon?**
    * *Answer:* A background process running detached from any active terminal window (e.g. `cron`, `sshd`).
26. **What is the purpose of the `/etc` directory?**
    * *Answer:* Stores system-wide configuration files.
27. **What is `/var/log`?**
    * *Answer:* The directory where system and application logs are saved.
28. **How do you list all active listening ports?**
    * *Answer:* Run `sudo ss -plnt` or `netstat -plnt`.
29. **What is the difference between `find` and `locate`?**
    * *Answer:* `find` walks the filesystem live (slower, up-to-date); `locate` searches a pre-built database (`mlocate.db`) (fast, needs database updates).
30. **Explain how `xargs` works.**
    * *Answer:* Reads items from standard input and builds and executes commands using those arguments.
31. **What is the sticky bit on a directory?**
    * *Answer:* A permission flag that ensures only the file owner or root can delete or rename files within that directory (e.g., `/tmp`).
32. **What are SUID and SGID permissions?**
    * *Answer:* SUID runs a file with the owner's privileges. SGID runs a file with the group's privileges or inherits parent folder group memberships.
33. **What does `chmod 755` do?**
    * *Answer:* Gives owner Read/Write/Execute, and Group/Others Read/Execute access.
34. **What does `chmod 600` do?**
    * *Answer:* Gives owner Read/Write access; denies all access to Group and Others.
35. **What is the role of `umask`?**
    * *Answer:* Defines default permissions subtracted from new files (base 666) and directories (base 777).
36. **How do you change file owner and group at once?**
    * *Answer:* Run `chown owner:group <file>`.
37. **What does `/dev/null` do?**
    * *Answer:* A virtual device file (black hole) that discards all data written to it.
38. **How do you suppress standard error output in a command?**
    * *Answer:* Append `2> /dev/null` to the command.
39. **What is the difference between `>` and `>>`?**
    * *Answer:* `>` overwrites file contents; `>>` appends to the end of the file.
40. **How do you monitor log updates live?**
    * *Answer:* Run `tail -f <logfile>`.
41. **Explain CPU Load averages on a multi-core processor.**
    * *Answer:* A load of 4.0 on a 4-core machine represents 100% CPU utilization.
42. **What does the `nice` command do?**
    * *Answer:* Sets priority for a command (-20 high to 19 low).
43. **What is `renice`?**
    * *Answer:* Changes the priority of an already running process.
44. **What is standard input, output, and error?**
    * *Answer:* File descriptors: stdin (0), stdout (1), stderr (2).
45. **What does `tar -czf archive.tar.gz folder/` do?**
    * *Answer:* Creates a gzip-compressed tar archive of the folder.
46. **What is a Cron job?**
    * *Answer:* A scheduled task run automatically by the `cron` daemon based on timing configurations.
47. **How do you view the current user's crontab tasks?**
    * *Answer:* Run `crontab -l`.
48. **What does `0 0 * * *` represent in crontab?**
    * *Answer:* Run daily at midnight.
49. **How do you check memory buffers and cache usage?**
    * *Answer:* Run `free -m` and check the "buff/cache" column.
50. **What is `/etc/fstab`?**
    * *Answer:* A configuration file mapping storage device UUIDs to filesystem mount points for startup mount automation.
51. **How do you mount a storage disk manually?**
    * *Answer:* Run `mount /dev/sdb1 /mnt/data`.
52. **What is the difference between hard reboot and soft reboot?**
    * *Answer:* Soft reboot sends shutdown signals to runlevels; hard reboot cuts power or forces instant reset.
53. **How do you check OS distribution details?**
    * *Answer:* Run `cat /etc/os-release`.
54. **What is the difference between `apt` and `yum`?**
    * *Answer:* `apt` manages packages on Debian/Ubuntu; `yum` (dnf) manages packages on RHEL/CentOS.
55. **How do you create a system group?**
    * *Answer:* Run `groupadd <group_name>`.
56. **How do you add a user to a group?**
    * *Answer:* Run `usermod -aG <group> <user>`.
57. **How do you show group members?**
    * *Answer:* Run `getent group <group_name>`.
58. **What is `/etc/shadow` file used for?**
    * *Answer:* Stores encrypted user passwords and password expiration dates. Accessible only by root.
59. **Explain the `su` vs `sudo` commands.**
    * *Answer:* `su` logs in as another user (requiring target's password); `sudo` runs commands with elevated root rights (requiring caller's password).
60. **What is page cache?**
    * *Answer:* System memory buffer holding recently read files from disk to optimize filesystem speeds.
61. **How do you clear RAM cache manually?**
    * *Answer:* Run `echo 3 > /proc/sys/vm/drop_caches` as root.
62. **What is the default filesystem for modern Ubuntu?**
    * *Answer:* ext4 (Extended filesystem version 4).
63. **Explain RAID in system storage.**
    * *Answer:* Redundant Array of Independent Disks - combines physical storage drives into logical units for speed/redundancy.
64. **Explain LVM (Logical Volume Manager).**
    * *Answer:* Standard disk allocation layer that permits resizing filesystems dynamically across multiple physical drives.
65. **How do you check LVM volume group sizes?**
    * *Answer:* Run `vgs` or `vgdisplay`.
66. **What does `df -i` show?**
    * *Answer:* Displays filesystem inode consumption instead of bytes.
67. **What is a filesystem corruption, and how do you fix it?**
    * *Answer:* Corruption due to power loss or hardware failure. Fix using `fsck` on an unmounted volume.
68. **What is an orphan file?**
    * *Answer:* A file without a valid owner UID or group GID.
69. **How do you check which command runs for a shortcut name?**
    * *Answer:* Run `type <name>` or `alias`.
70. **What is `/etc/security/limits.conf` used for?**
    * *Answer:* Limits system resource usages (open file descriptors, processes) per user.
71. **How do you check system limits for open files?**
    * *Answer:* Run `ulimit -n`.
72. **What is the significance of PID 1?**
    * *Answer:* The initialization daemon (`systemd`), the parent of all system processes.
73. **How do you run a command in the background?**
    * *Answer:* Append `&` to the command line.
74. **How do you bring a background job to the foreground?**
    * *Answer:* Run `fg %<job_id>`.
75. **What does `Ctrl+C` do to processes?**
    * *Answer:* Sends `SIGINT` interrupt signal.
76. **What does `Ctrl+Z` do?**
    * *Answer:* Sends `SIGTSTP` stop signal, suspending execution.
77. **How do you change system timezone?**
    * *Answer:* Run `timedatectl set-timezone <Zone>`.
78. **What is the purpose of `/srv`?**
    * *Answer:* Stores site-specific data served by the system (e.g. web assets).
79. **How do you verify if a directory is a mount point?**
    * *Answer:* Run `mountpoint /path/to/check`.
80. **What is the difference between `/tmp` and `/var/tmp`?**
    * *Answer:* `/tmp` is cleared on reboot; `/var/tmp` preserves data across boots.
81. **Explain the Linux runlevels.**
    * *Answer:* Operational states (0: Halt, 1: Single-user, 3: Multi-user CLI, 5: Multi-user GUI, 6: Reboot).
82. **How do you print shell commands as they are run?**
    * *Answer:* Run `set -x` in the shell script.
83. **What is the `dmesg` command checking?**
    * *Answer:* The kernel ring buffer.
84. **What is `/etc/hostname`?**
    * *Answer:* Holds the local machine name.
85. **Explain the `chattr` command.**
    * *Answer:* Sets file attributes (e.g. `+i` makes file immutable, preventing deletion even by root).
86. **What does `lsattr` show?**
    * *Answer:* Lists file attributes set by `chattr`.
87. **How do you check process trees?**
    * *Answer:* Run `pstree`.
88. **How do you display CPU info?**
    * *Answer:* Run `lscpu` or `cat /proc/cpuinfo`.
89. **How do you check hardware PCI details?**
    * *Answer:* Run `lspci`.
90. **How do you log out from shell?**
    * *Answer:* Run `exit` or `logout`.
91. **What is `/etc/resolv.conf`?**
    * *Answer:* Configures DNS resolvers (nameservers) for the system.
92. **What is the difference between `ping` and `telnet`?**
    * *Answer:* `ping` uses ICMP to check network host availability; `telnet` uses TCP to check connectivity on specific ports.
93. **How do you create an empty file quickly?**
    * *Answer:* Run `> file.txt` or `touch file.txt`.
94. **What is the `whoami` command?**
    * *Answer:* Outputs active login username.
95. **How do you list logged-in users?**
    * *Answer:* Run `w` or `who`.
96. **What is a shell?**
    * *Answer:* The CLI program interpreting user commands (e.g. Bash).
97. **What is `/etc/shells`?**
    * *Answer:* Lists valid system shell paths.
98. **How do you change your shell to zsh?**
    * *Answer:* Run `chsh -s $(which zsh)`.
99. **How do you run commands sequentially only if the prior succeeds?**
   * *Answer:* Use `&&` (e.g., `cmd1 && cmd2`).
100. **How do you run commands sequentially regardless of failure?**
    * *Answer:* Use `;` (e.g., `cmd1; cmd2`).

---

## Part 2: 100 Networking Interview Questions & Answers

101. **What is an IP address?**
    * *Answer:* A numerical identifier assigned to each device on a network.
102. **Explain the difference between IPv4 and IPv6.**
    * *Answer:* IPv4 is 32-bit (written in decimal, e.g. 192.168.1.1); IPv6 is 128-bit (written in hexadecimal, e.g. 2001:db8::).
103. **What is a subnet mask?**
    * *Answer:* A 32-bit number splitting an IP address into Network and Host portions.
104. **What does CIDR stand for?**
    * *Answer:* Classless Inter-Domain Routing.
105. **What is a Default Gateway?**
    * *Answer:* The router interface that handles traffic outside the local network.
106. **Explain Private IP addresses.**
    * *Answer:* IPs reserved for internal networks (e.g. `10.0.0.0/8`, `192.168.0.0/16`). They are not routed on the public internet.
107. **What is NAT?**
    * *Answer:* Network Address Translation - maps private IPs inside a local network to a single public IP.
108. **What is a MAC address?**
    * *Answer:* A unique physical hardware address burned into the Network Interface Card (NIC).
109. **Explain ARP.**
    * *Answer:* Address Resolution Protocol - resolves IPv4 addresses to physical MAC addresses.
110. **Explain the difference between TCP and UDP.**
    * *Answer:* TCP is reliable, connection-oriented, and guarantees packet delivery. UDP is fast, connectionless, and does not guarantee delivery.
111. **Explain the TCP 3-Way Handshake.**
    * *Answer:* Establishing a connection: SYN -> SYN-ACK -> ACK.
112. **How does TCP close a connection?**
    * *Answer:* 4-way termination handshake: FIN -> ACK -> FIN -> ACK.
113. **What is ICMP?**
    * *Answer:* Internet Control Message Protocol - used for error reporting and diagnostics (e.g. `ping`).
114. **What is a port number?**
    * *Answer:* A 16-bit number identifying specific application endpoints on a host.
115. **What is the port range?**
    * *Answer:* `0` to `65535` (Well-known: 0-1023, Registered: 1024-49151, Dynamic: 49152-65535).
116. **Which port does HTTPS run on?**
    * *Answer:* Port 443.
117. **Which port does HTTP run on?**
    * *Answer:* Port 80.
118. **Which port does SSH use?**
    * *Answer:* Port 22.
119. **What port does DNS listen on?**
    * *Answer:* Port 53 (both TCP and UDP).
120. **What is DHCP?**
    * *Answer:* Dynamic Host Configuration Protocol - automatically assigns IPs and network settings to joining hosts.
121. **What is DNS?**
    * *Answer:* Domain Name System - resolves domain names (google.com) to IP addresses.
122. **What is the DNS authoritative name server?**
    * *Answer:* The final server in the DNS resolution chain that holds the actual DNS records for a domain.
123. **What is a CNAME record?**
    * *Answer:* A canonical name record that points a subdomain alias to another domain name.
124. **What is an A record?**
    * *Answer:* Maps a domain name to an IPv4 address.
125. **What is a AAAA record?**
    * *Answer:* Maps a domain name to an IPv6 address.
126. **What is a TXT record?**
    * *Answer:* Stores descriptive text, often used for SSL/domain verification and email validation (SPF).
127. **What is an MX record?**
    * *Answer:* Mail Exchanger - defines the mail server handling email for a domain.
128. **What is an NS record?**
    * *Answer:* Lists the authoritative name servers for the domain.
129. **What is a reverse DNS lookup (PTR record)?**
    * *Answer:* Resolves an IP address to a domain name.
130. **Explain TTL in DNS.**
    * *Answer:* Time-To-Live - the duration DNS records should be cached by resolvers before querying again.
131. **What is the loopback IP?**
    * *Answer:* `127.0.0.1` (localhost).
132. **Explain the OSI Model layers.**
    * *Answer:* Physical (1), Data Link (2), Network (3), Transport (4), Session (5), Presentation (6), Application (7).
133. **Which layer do routers operate on in OSI?**
    * *Answer:* Layer 3 (Network).
134. **Which layer do switches operate on in OSI?**
    * *Answer:* Layer 2 (Data Link).
135. **What is the TCP/IP Model layers?**
    * *Answer:* Network Access, Internet, Transport, Application.
136. **Explain the difference between a hub, a switch, and a router.**
    * *Answer:* Hub broadcasts traffic to all ports; Switch forwards traffic to specific MAC addresses; Router routes traffic between different networks.
137. **What is VLAN?**
    * *Answer:* Virtual Local Area Network - groups devices logically on a single switch to isolate traffic.
138. **Explain ping.**
    * *Answer:* Sends ICMP Echo requests to verify if a remote host is online.
139. **Explain traceroute.**
    * *Answer:* Displays the path packets take to a destination, listing the hop IPs and response times.
140. **How does traceroute determine hops?**
    * *Answer:* Increments Time-to-Live (TTL) starting from 1. Routers discard expired packets and return ICMP Time Exceeded messages.
141. **What is a firewall?**
    * *Answer:* A security system filtering incoming/outgoing traffic based on rules.
142. **Explain Stateful vs Stateless firewalls.**
    * *Answer:* Stateful tracks the connection state (remembers outgoing requests); Stateless filters each packet individually based on header rules.
143. **What is dynamic routing?**
    * *Answer:* Routers dynamically share routes using protocols like OSPF or BGP.
144. **What is BGP?**
    * *Answer:* Border Gateway Protocol - the routing protocol of the internet, directing packets between Autonomous Systems (AS).
145. **What is a VPN?**
    * *Answer:* Virtual Private Network - creates an encrypted tunnel over a public network.
146. **What is SSL/TLS?**
    * *Answer:* Cryptographic protocols that secure communications over a network.
147. **Explain the difference between HTTP and HTTPS.**
    * *Answer:* HTTPS runs HTTP inside an encrypted TLS/SSL wrapper.
148. **Explain a Reverse Proxy.**
    * *Answer:* A proxy server sitting in front of application backends, managing incoming requests, caching, load balancing, and SSL termination.
149. **What is a Forward Proxy?**
    * *Answer:* A proxy server acting on behalf of internal clients, filtering outgoing traffic to the internet.
150. **What is a load balancer?**
    * *Answer:* Distributes network traffic across multiple servers to prevent overload.
151. **Explain Round Robin load balancing.**
    * *Answer:* Directs requests sequentially to servers in a loop.
152. **Explain Least Connections load balancing.**
    * *Answer:* Directs requests to the server with the fewest active connections.
153. **What is IP Anycast?**
    * *Answer:* Routes traffic from a single destination IP to the nearest physical server in a network topology.
154. **What is CIDR `/16` host count?**
    * *Answer:* $2^{16} - 2 = 65,534$ host IP addresses.
155. **Explain Subnetting CIDR `/28`.**
    * *Answer:* $2^4 - 2 = 14$ host IP addresses.
156. **What is loopback interface name in Linux?**
    * *Answer:* `lo`.
157. **How do you show route maps in Linux?**
    * *Answer:* Run `ip route` or `route -n`.
158. **How do you verify DNS settings in Linux?**
    * *Answer:* Inspect `/etc/resolv.conf`.
159. **Explain port forwarding.**
    * *Answer:* Forwards public ports on a router to a specific private IP and port on the local network.
160. **What is Keep-Alive in HTTP?**
    * *Answer:* Keeps the TCP connection open for subsequent requests to avoid handshake overhead.
161. **What is MTU?**
    * *Answer:* Maximum Transmission Unit - the largest packet size (in bytes) that can be sent over a network interface (typically 1500 bytes).
162. **What is latency?**
    * *Answer:* The delay (time taken) for data to travel from source to destination.
163. **What is bandwidth?**
    * *Answer:* The capacity of a network link to transmit data (e.g. Gbps).
164. **Explain packet loss.**
    * *Answer:* Occurs when packets fail to reach their destination, typically due to network congestion.
165. **What is jitter?**
    * *Answer:* The variance in arrival time (latency) of packets.
166. **What is CIDR `/32`?**
    * *Answer:* Represents a single IP address ($2^0 = 1$ host).
167. **What is CIDR `/0`?**
    * *Answer:* Represents the entire internet (`0.0.0.0/0`).
168. **What is the port for MySQL?**
    * *Answer:* Port 3306.
169. **What is the port for PostgreSQL?**
    * *Answer:* Port 5432.
170. **What is the port for Redis?**
    * *Answer:* Port 6379.
171. **What is the port for MongoDB?**
    * *Answer:* Port 27017.
172. **What is the port for Kubernetes API server?**
    * *Answer:* Port 6443.
173. **What is the port for Jenkins?**
    * *Answer:* Port 8080 (default).
174. **What is default port for secure shell?**
    * *Answer:* Port 22.
175. **What is TCP window size?**
    * *Answer:* The amount of data a sender can transmit before requiring an acknowledgment.
176. **Explain the TCP sliding window protocol.**
    * *Answer:* Manages flow control, dynamically adjusting window sizes based on network conditions.
177. **Explain TCP segmentation.**
    * *Answer:* Splits application data into segments matching the network's MTU.
178. **What is IP fragmentation?**
    * *Answer:* Occurs when routers split packets that exceed the next hop's MTU (inefficient).
179. **How do you disable IPv6 in Linux?**
    * *Answer:* Set `net.ipv6.conf.all.disable_ipv6 = 1` in `/etc/sysctl.conf`.
180. **What is a socket connection?**
    * *Answer:* The logical endpoint of a connection, defined by a Source IP, Source Port, Destination IP, and Destination Port.
181. **Explain the difference between a collision domain and a broadcast domain.**
    * *Answer:* Collision Domain: Group of devices where packet collisions can occur (hub). Broadcast Domain: Group of devices that receive broadcast traffic (switch/VLAN).
182. **What is Link Aggregation (bonding)?**
    * *Answer:* Combines multiple network interfaces into a single channel for redundancy and throughput.
183. **How do you check current ARP caches?**
    * *Answer:* Run `arp -a` or `ip neigh`.
184. **How do you flush DNS caches locally?**
    * *Answer:* Run `sudo systemd-resolve --flush-caches`.
185. **What port does NTP run on?**
    * *Answer:* Port 123 (UDP) - Network Time Protocol.
186. **What port does LDAP run on?**
    * *Answer:* Port 389 (LDAP) or Port 636 (LDAPS).
187. **What is SNMP?**
    * *Answer:* Simple Network Management Protocol (Ports 161/162) - used for monitoring network devices.
188. **What is the difference between a route table and an ARP table?**
    * *Answer:* Route Table maps destination IP ranges to gateways (Layer 3). ARP table maps IPs to local MAC addresses (Layer 2).
189. **What is a loopback loop in routing?**
    * *Answer:* Occurs when packets are routed back and forth between routers in a loop until their TTL reaches 0.
190. **What is split-horizon rule?**
    * *Answer:* Routing loop prevention rule: A router cannot advertise a route back out the interface it learned it from.
191. **What is DNSSEC?**
    * *Answer:* Secures DNS records by signing queries cryptographically to prevent spoofing.
192. **What is ephemeral port range?**
    * *Answer:* Temporary ports allocated for outgoing client connections (typically 32768-60999 in Linux).
193. **What is the difference between a host name and a domain name?**
    * *Answer:* Host Name: Specific machine name (e.g. `web01`). Domain Name: The parent directory label (e.g. `example.com`).
194. **Explain ICMP redirects.**
    * *Answer:* A message from a router notifying a host to use a better route gateway.
195. **What is the TCP Retransmission timeout?**
    * *Answer:* The duration a sender waits for an ACK before retransmitting the segment.
196. **What is TCP Congestion Control?**
    * *Answer:* Algorithms (like Tahoe, Reno, BBR) that adjust transmission rates to prevent network congestion.
197. **What is standard MTU of Ethernet?**
    * *Answer:* 1500 bytes.
198. **What are Jumbo Frames?**
    * *Answer:* Ethernet frames with MTU greater than 1500 bytes (typically 9000 bytes).
199. **How do you trace open ports using netcat?**
    * *Answer:* Run `nc -zv <host> <port>`.
200. **What is DNS propagation?**
    * *Answer:* The time it takes for DNS updates to sync globally across recursive resolvers (bounded by record TTLs).

---

## Part 3: 100 Bash Scripting Interview Questions & Answers

201. **What is the shebang line in Bash?**
    * *Answer:* The first line (`#!/bin/bash`) specifying the interpreter to run the script.
202. **How do you make a Bash script executable?**
    * *Answer:* Run `chmod +x <script.sh>`.
203. **What is the file extension of a Bash script?**
    * *Answer:* `.sh` (optional, but standard).
204. **How do you define a variable in Bash?**
    * *Answer:* `VAR="value"` (no spaces around `=`).
205. **How do you reference a variable?**
    * *Answer:* Use `$VAR` or `${VAR}`.
206. **Explain the difference between single quotes and double quotes.**
    * *Answer:* Single quotes treat all characters literally; double quotes permit variable substitution (`$`) and command evaluation (`` ` ``).
207. **How do you read arguments passed to a script?**
    * *Answer:* Positional variables: `$1` (first argument), `$2` (second argument), etc.
208. **What does `$0` represent?**
    * *Answer:* The name or path of the running script.
209. **What does `$@` represent?**
    * *Answer:* All arguments passed to the script.
210. **What does `$#` represent?**
    * *Answer:* The total number of arguments passed to the script.
211. **What does `$?` represent?**
    * *Answer:* The exit status code of the last run command.
212. **What does `$$` represent?**
    * *Answer:* The PID of the current shell session.
213. **How do you command-substitute in Bash?**
    * *Answer:* Use `$(command)` or `` `command` ``.
214. **How do you perform arithmetic operations in Bash?**
    * *Answer:* Use `$((expression))` (e.g., `$((5 + 3))`).
215. **What does `set -e` do?**
    * *Answer:* Exits the script immediately if any command returns a non-zero exit status.
216. **What does `set -x` do?**
    * *Answer:* Enables debug mode, printing commands and their arguments to stdout before executing them.
217. **What does `set -u` do?**
    * *Answer:* Exits the script if it attempts to expand an unbound (unassigned) variable.
218. **Explain exit status 0.**
    * *Answer:* Indicates successful command execution.
219. **Explain exit status 1.**
    * *Answer:* Indicates a general error occurred.
220. **Explain exit status 127.**
    * *Answer:* Indicates the command was not found.
221. **How do you define an array?**
    * *Answer:* `my_array=("val1" "val2")`.
222. **How do you access the first index of an array?**
    * *Answer:* `${my_array[0]}`.
223. **How do you list all items in an array?**
    * *Answer:* `${my_array[@]}`.
224. **How do you read user input inside a script?**
    * *Answer:* Use the `read` command (e.g. `read -p "Enter: " input`).
225. **How do you test if a variable is empty?**
    * *Answer:* `if [ -z "$VAR" ]`.
226. **How do you test if a file exists?**
    * *Answer:* `if [ -f "$file" ]`.
227. **How do you test if a directory exists?**
    * *Answer:* `if [ -d "$dir" ]`.
228. **What does the `-eq` operator compare?**
    * *Answer:* Integer equality.
229. **What operator is used for string equality?**
    * *Answer:* `=` or `==`.
230. **What does `[[` offer over `[`?**
    * *Answer:* Supports logical operators (`&&`, `||`), pattern matching, and regex without escaping brackets.
231. **How do you redirect standard error to standard output?**
    * *Answer:* Append `2>&1` to the command.
232. **What does `/dev/stdin` represent?**
    * *Answer:* The standard input stream file.
233. **Explain the `case` statement.**
    * *Answer:* A multi-branch conditional that compares a value against multiple patterns.
234. **How do you write a basic `for` loop?**
    * *Answer:* `for i in {1..5}; do echo $i; done`.
235. **How do you write a basic `while` loop?**
    * *Answer:* `while [ condition ]; do commands; done`.
236. **What is an infinite loop in Bash?**
    * *Answer:* `while true; do commands; done`.
237. **How do you define a function?**
    * *Answer:* `my_func() { commands; }`.
238. **How do you pass arguments to a function?**
    * *Answer:* By typing them after the function call (e.g. `my_func arg1 arg2`), read inside using `$1`, `$2`.
239. **What does the `local` keyword do inside a function?**
    * *Answer:* Restricts variable scope to that function only.
240. **How do you return values from a function?**
    * *Answer:* Functions return exit codes (`return 0-255`). For data returns, echo the value and capture it using command substitution: `res=$(my_func)`.
241. **How do you write output to a file and screen simultaneously?**
    * *Answer:* Pipe the command output to `tee` (e.g., `cmd | tee output.txt`).
242. **What does `export` do?**
    * *Answer:* Sets environment variables that are inherited by child shells and processes.
243. **How do you list all environment variables?**
    * *Answer:* Run `env` or `printenv`.
244. **What does the `shift` command do?**
    * *Answer:* Shifts command-line arguments to the left (e.g., `$2` becomes `$1`).
245. **What is the source command (`.`)?**
    * *Answer:* Executes a script's commands inside the current shell environment (preserving variables) instead of spawning a subshell.
246. **What is an alias?**
    * *Answer:* A shortcut command pointing to a longer command (e.g. `alias ll='ls -l'`).
247. **How do you remove an alias?**
    * *Answer:* Run `unalias <alias_name>`.
248. **Where is alias configurations saved?**
    * *Answer:* In `~/.bashrc` or `~/.bash_profile`.
249. **What is standard file pattern expansion called?**
    * *Answer:* Globbing (e.g. using `*.log`).
250. **What does `set -o pipefail` do?**
    * *Answer:* Forces pipeline commands to return the exit code of the first failing command instead of the last command.
251. **How do you check if a script is running as root?**
    * *Answer:* Check if `$EUID` or the output of `id -u` is `0`.
252. **How do you count characters in a variable?**
    * *Answer:* `${#VAR}`.
253. **How do you extract a substring?**
    * *Answer:* `${VAR:offset:length}`.
254. **How do you run commands in parallel inside a script?**
    * *Answer:* Append `&` to each command in the loop, followed by `wait` at the end of the script to block termination until they finish.
255. **What does the `wait` command do?**
    * *Answer:* Pauses script execution until all background jobs finish.
256. **What does the `until` loop do?**
    * *Answer:* Repeats commands until the condition becomes true.
257. **How do you check if a variable is defined?**
    * *Answer:* `if [ -v VAR ]`.
258. **How do you handle default variable values?**
    * *Answer:* `${VAR:-"default_value"}` (Uses default if variable is unset or empty).
259. **What does `exec` do in scripts?**
    * *Answer:* Replaces the current shell process with the target command without creating a new process.
260. **What is a trap?**
    * *Answer:* Captures signals (like SIGINT, EXIT) and executes clean-up functions when they occur.
261. **How do you trap script exits for cleanups?**
    * *Answer:* `trap cleanup_function EXIT`.
262. **How do you generate temporary files securely?**
    * *Answer:* Use the `mktemp` command.
263. **What is a Heredoc?**
    * *Answer:* Redirects multi-line text blocks into a command (e.g. using `<<EOF`).
264. **How do you parse flags using `getopts`?**
    * *Answer:* Loop `while getopts "ab:" opt; do ...done` inside the script.
265. **What does the `readlink -f` command do?**
    * *Answer:* Resolves absolute paths, following all symbolic links.
266. **How do you check if a file is executable?**
    * *Answer:* `if [ -x "$file" ]`.
267. **How do you check if a file is writable?**
    * *Answer:* `if [ -w "$file" ]`.
268. **How do you print text without newline?**
    * *Answer:* Run `echo -n "text"` or `printf "text"`.
269. **Why is `printf` preferred over `echo`?**
    * *Answer:* It provides consistent formatting options across different UNIX/Linux distributions.
270. **What does the double hyphen `--` represent in commands?**
    * *Answer:* Signifies the end of command options, allowing arguments that start with dashes (e.g., `rm -- -file`).
271. **How do you read configuration files into variables?**
    * *Answer:* Use `source config.env` or `export $(xargs < config.env)`.
272. **What does `$IFS` represent?**
    * *Answer:* Internal Field Separator - defines the delimiter characters for word splitting (defaults to space, tab, newline).
273. **How do you loop through comma-separated values?**
    * *Answer:* Temporarily set `IFS=","` before looping.
274. **How do you match strings using regex?**
    * *Answer:* Use the `=~` operator inside double brackets (e.g. `[[ "$VAR" =~ ^[0-9]+$ ]]`).
275. **How do you find the script's directory path?**
    * *Answer:* `DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`.
276. **What is a subshell?**
    * *Answer:* A child shell process spawned by the parent shell to execute commands (enclosed in parentheses `(cmds)`).
277. **How do you run commands block in parent context?**
    * *Answer:* Enclose commands in curly braces `{ cmds; }`.
278. **What does the command `history` do?**
    * *Answer:* Lists previous commands entered in the current shell session.
279. **How do you search command history quickly?**
    * *Answer:* Press `Ctrl+R` to search interactively.
280. **Explain how standard pipelines operate.**
    * *Answer:* Connects the stdout (1) of the left command to the stdin (0) of the right command.
281. **How do you count lines in standard output?**
    * *Answer:* Append `| wc -l` to the command.
282. **How do you check if user input is an integer?**
    * *Answer:* `[[ "$input" =~ ^[0-9]+$ ]]`.
283. **How do you print CPU cores count in script?**
    * *Answer:* `nproc`.
284. **How do you read the last line of a file into a variable?**
    * *Answer:* `line=$(tail -n 1 file.txt)`.
285. **What is `stdin` file descriptor?**
    * *Answer:* Descriptor `0`.
286. **What is `stdout` file descriptor?**
    * *Answer:* Descriptor `1`.
287. **What is `stderr` file descriptor?**
    * *Answer:* Descriptor `2`.
288. **How do you append both stdout and stderr to a file?**
    * *Answer:* `command >> file.txt 2>&1` or `command &>> file.txt`.
289. **What does `select` loop do?**
    * *Answer:* Automatically creates interactive menus in the console.
290. **How do you exit a loop early?**
    * *Answer:* Use the `break` statement.
291. **How do you skip to the next loop iteration?**
    * *Answer:* Use the `continue` statement.
292. **How do you compare strings lexicographically?**
    * *Answer:* Use `[[ "$A" < "$B" ]]`.
293. **What is standard output directory for cron logs?**
    * *Answer:* Cron sends execution outputs to the user's local mailbox unless redirected (`>/dev/null 2>&1`).
294. **What does the `bc` command do?**
    * *Answer:* Basic Calculator - handles floating-point math operations in the terminal.
295. **How do you perform floating-point divisions?**
    * *Answer:* `echo "scale=2; 5/2" | bc` (Output: 2.50).
296. **How do you display execution times of commands?**
    * *Answer:* Prefix the command with `time` (e.g. `time build.sh`).
297. **What is `env` shebang syntax?**
    * *Answer:* `#!/usr/bin/env bash` (searches system PATH for the bash binary, making it more portable).
298. **How do you clean up paths?**
    * *Answer:* Use `realpath <path>`.
299. **How do you check if a script parameter was omitted?**
    * *Answer:* `if [ -z "${1:-}" ]`.
300. **How do you check array sizes?**
    * *Answer:* `${#my_array[@]}`.

---

## Part 4: 100 Python Automation Interview Questions & Answers

301. **What are the built-in basic types in Python?**
    * *Answer:* `str`, `int`, `float`, `bool`.
302. **Explain mutable vs immutable objects in Python.**
    * *Answer:* Mutable objects (like lists, dicts, sets) can be changed after creation. Immutable objects (like strings, tuples, numbers) cannot be changed.
303. **How do you append to a list?**
    * *Answer:* `list_name.append(item)`.
304. **Explain lists vs tuples.**
    * *Answer:* Lists are mutable and enclosed in brackets `[]`. Tuples are immutable and enclosed in parentheses `()`.
305. **What is a dictionary?**
    * *Answer:* An unordered collection of key-value pairs (mutable, keys must be unique).
306. **How do you access keys of a dictionary?**
    * *Answer:* Use `dict.keys()`.
307. **How do you avoid KeyError in dictionaries?**
    * *Answer:* Use `dict.get("key", "default_value")` instead of `dict["key"]`.
308. **What is a set?**
    * *Answer:* An unordered collection of unique elements.
309. **How do you open files securely?**
    * *Answer:* Use the `with open("file.txt", "r") as f:` syntax to guarantee files are closed automatically.
310. **What is exception handling?**
    * *Answer:* `try-except` blocks that catch errors during execution to prevent application crashes.
311. **Explain the `finally` block.**
    * *Answer:* A code block that runs after `try-except`, regardless of whether an exception occurred. Often used for cleaning up resources.
312. **Which module is used to run OS terminal commands?**
    * *Answer:* The `subprocess` module.
313. **Why is `subprocess.run` preferred over `os.system`?**
    * *Answer:* It provides a modern, secure interface that captures stdout/stderr, supports argument lists, and handles error checks without shell injections.
314. **How do you read environment variables?**
    * *Answer:* `import os; val = os.environ.get("VAR_NAME")`.
315. **How do you list directory contents?**
    * *Answer:* `os.listdir(path)`.
316. **How do you create directories recursively?**
    * *Answer:* `os.makedirs(path, exist_ok=True)`.
317. **Which library is used to parse JSON structures?**
    * *Answer:* The built-in `json` module.
318. **Explain the difference between `json.loads` and `json.load`.**
    * *Answer:* `loads` parses a JSON string; `load` parses a JSON file buffer.
319. **Explain the difference between `json.dumps` and `json.dump`.**
    * *Answer:* `dumps` outputs a JSON string; `dump` writes JSON output directly to a file buffer.
320. **Which library is used to parse YAML?**
    * *Answer:* The third-party `PyYAML` library (`import yaml`).
321. **How do you load YAML configurations?**
    * *Answer:* `config = yaml.safe_load(file_stream)`.
322. **What library executes HTTP REST API queries?**
    * *Answer:* The third-party `requests` library.
323. **How do you send a GET request?**
    * *Answer:* `response = requests.get(url, timeout=5)`.
324. **How do you send a POST request with JSON payloads?**
    * *Answer:* `response = requests.post(url, json={"key": "val"})`.
325. **How do you extract JSON responses from `requests`?**
    * *Answer:* `data = response.json()`.
326. **What parameter protects requests from locking up indefinitely?**
    * *Answer:* The `timeout` parameter (e.g., `requests.get(url, timeout=3)`).
327. **What represents HTTP response codes in requests?**
    * *Answer:* `response.status_code`.
328. **How do you raise exceptions for failed HTTP requests?**
    * *Answer:* Call `response.raise_for_status()`.
329. **What is `pip`?**
    * *Answer:* The standard package installer for Python libraries.
330. **What is a virtual environment (venv)?**
    * *Answer:* An isolated environment that keeps project-specific dependencies separate to avoid global package conflicts.
331. **How do you create a virtual environment?**
    * *Answer:* Run `python -m venv myenv`.
332. **How do you activate a virtual environment on Linux?**
    * *Answer:* Run `source myenv/bin/activate`.
333. **What is `requirements.txt`?**
    * *Answer:* A text file listing all external dependencies required for the project, installed using `pip install -r requirements.txt`.
334. **How do you format strings dynamically?**
    * *Answer:* Use f-strings: `f"Service {name} is {status}"`.
335. **What does `if __name__ == "__main__":` do?**
    * *Answer:* Ensures the code block runs only when the script is executed directly, not when it is imported as a module.
336. **Explain list comprehensions.**
    * *Answer:* A concise syntax to create lists from existing iterables: `[x for x in list if condition]`.
337. **How do you handle logs in Python?**
    * *Answer:* Use the built-in `logging` module.
338. **What are the default logging levels?**
    * *Answer:* DEBUG, INFO, WARNING, ERROR, CRITICAL.
339. **How do you import custom modules?**
    * *Answer:* `import my_module` (where `my_module.py` is in the directory path).
340. **What is the `sys` module used for?**
    * *Answer:* Interacts with the interpreter (e.g. reading parameters `sys.argv`, exiting scripts `sys.exit()`).
341. **How do you read positional arguments?**
    * *Answer:* `sys.argv[0]` is the script name, `sys.argv[1]` is the first parameter.
342. **What does `shutil` module offer?**
    * *Answer:* High-level file operations (copying files, checking disk statistics `shutil.disk_usage`).
343. **How do you parse arguments cleanly?**
    * *Answer:* Use the built-in `argparse` module.
344. **How do you find files matching regex patterns?**
    * *Answer:* Use the `re` module (Regular Expressions) or `fnmatch`/`glob`.
345. **What does the `datetime` module do?**
    * *Answer:* Handles dates, times, and timezone formatting.
346. **How do you print the current local time?**
    * *Answer:* `datetime.datetime.now()`.
347. **How do you calculate resource execution times?**
    * *Answer:* `import time; start = time.time(); ...; duration = time.time() - start`.
348. **What does `boto3` represent?**
    * *Answer:* The official AWS SDK for Python, used to create, manage, and delete AWS resources programmatically.
349. **How do you list AWS S3 buckets using `boto3`?**
    * *Answer:* `s3 = boto3.resource('s3'); buckets = [b.name for b in s3.buckets.all()]`.
350. **What is the `__init__.py` file?**
    * *Answer:* Marks a directory as a Python package, allowing its modules to be imported.
351. **How do you join path directories safely?**
    * *Answer:* Use `os.path.join(path1, path2)`.
352. **How do you run shell command pipelines?**
    * *Answer:* Set `shell=True` in `subprocess` (use with caution) or connect subprocess pipes using `stdout=subprocess.PIPE`.
353. **How do you catch all exceptions?**
    * *Answer:* `except Exception as e:` (Best practice is to catch specific exceptions like `FileNotFoundError`).
354. **What does `pass` do in Python?**
    * *Answer:* A null statement used as a placeholder where syntax requires code but no action is needed.
355. **How do you convert strings to integers safely?**
    * *Answer:* Wrap `int(string_val)` in a `try-except ValueError` block.
356. **What library manages Kubernetes API calls in Python?**
    * *Answer:* The official `kubernetes` client library.
357. **How do you load local kubeconfig?**
    * *Answer:* `from kubernetes import client, config; config.load_kube_config()`.
358. **Explain generator functions.**
    * *Answer:* Functions that yield values one at a time using `yield`, memory-efficient for processing large logs.
359. **What does the `threading` module do?**
    * *Answer:* Executes multiple threads in parallel to handle I/O-bound tasks concurrently.
360. **What is the Global Interpreter Lock (GIL)?**
    * *Answer:* A mechanism in CPython preventing multiple threads from executing Python bytecodes at once (affects CPU-bound tasks).
361. **How do you handle CPU-bound parallel execution?**
    * *Answer:* Use the `multiprocessing` module instead of `threading`.
362. **How do you check if a file path is a directory?**
    * *Answer:* `os.path.isdir(path)`.
363. **How do you delete files?**
    * *Answer:* `os.remove(path)`.
364. **How do you delete empty folders?**
    * *Answer:* `os.rmdir(path)`.
365. **How do you delete non-empty folder trees?**
    * *Answer:* `shutil.rmtree(path)`.
366. **What does `import time; time.sleep(5)` do?**
    * *Answer:* Pauses process execution for 5 seconds.
367. **How do you strip whitespaces from string lines?**
    * *Answer:* Use `line.strip()`.
368. **How do you split strings by a delimiter?**
    * *Answer:* `line.split(",")`.
369. **How do you check if substrings exist inside strings?**
    * *Answer:* `if "substring" in main_string:`.
370. **Explain dictionary comprehensions.**
    * *Answer:* Concise syntax to generate dicts: `{key: val for key, val in iterable}`.
371. **How do you merge two dictionaries in Python 3.9+?**
    * *Answer:* Use the merge operator: `dict3 = dict1 | dict2`.
372. **What does `uuid` module do?**
    * *Answer:* Generates universally unique identifiers (UUIDs).
373. **How do you inspect function documentation?**
    * *Answer:* Access `func.__doc__` or run `help(func)`.
374. **How do you exit script executions?**
    * *Answer:* Call `sys.exit(code)` (0 for success, non-zero for error).
375. **What is standard output printing syntax?**
    * *Answer:* `print("message")`.
376. **How do you print to standard error stream?**
    * *Answer:* `import sys; print("error", file=sys.stderr)`.
377. **How do you read all lines from file as list?**
    * *Answer:* `lines = f.readlines()`.
378. **What does `dir()` function show?**
    * *Answer:* Returns a list of valid attributes and methods for the target object.
379. **What does `type()` show?**
    * *Answer:* Returns the type class of the target object.
380. **How do you get list length?**
    * *Answer:* `len(my_list)`.
381. **How do you get dictionary key count?**
    * *Answer:* `len(my_dict)`.
382. **Explain lambda functions.**
    * *Answer:* Anonymous, single-line functions: `lambda x: x + 1`.
383. **How do you sort lists?**
    * *Answer:* Use `my_list.sort()` (modifies inline) or `sorted(my_list)` (returns a new list).
384. **What library is used for scheduling Python tasks?**
    * *Answer:* The third-party `schedule` library or standard `cron`/`celery` triggers.
385. **What does `traceback` module offer?**
    * *Answer:* Formats and prints detailed stack traces for debug audits during exception handling.
386. **How do you copy files?**
    * *Answer:* `shutil.copy(source, destination)`.
387. **How do you move files?**
    * *Answer:* `shutil.move(source, destination)`.
388. **How do you check if path is symbolic link?**
    * *Answer:* `os.path.islink(path)`.
389. **What is `urllib`?**
    * *Answer:* Standard Python collection of modules for handling URLs (superseded by `requests` for ease of use).
390. **How do you create custom exceptions?**
    * *Answer:* Create a class inheriting from `Exception` (e.g. `class MyError(Exception): pass`).
391. **What is the difference between `==` and `is`?**
    * *Answer:* `==` checks for equality of values; `is` checks if both variables point to the exact same object in memory.
392. **How do you check memory footprint of objects?**
    * *Answer:* `import sys; sys.getsizeof(obj)`.
393. **What is the purpose of `mock` library in testing?**
    * *Answer:* Replaces system outputs and API endpoints with mock behaviors to test code in isolation.
394. **How do you check system CPU utilization in Python?**
    * *Answer:* Use the third-party `psutil` library (`psutil.cpu_percent()`).
395. **How do you list open files by process?**
    * *Answer:* `psutil.Process(pid).open_files()`.
396. **How do you read system memory usage via `psutil`?**
    * *Answer:* `psutil.virtual_memory()`.
397. **What is standard output format for requests body?**
    * *Answer:* JSON format or url-encoded form values.
398. **How do you verify if response contains valid JSON?**
    * *Answer:* Wrap `response.json()` in a `ValueError/JSONDecodeError` catch block.
399. **How do you check if dictionary key exists?**
    * *Answer:* `if "key" in my_dict:`.
400. **How do you run unit tests in Python?**
    * *Answer:* Use the built-in `unittest` module or third-party `pytest`.

---

## Part 5: 50 SSH Interview Questions & Answers

401. **What does SSH stand for?**
    * *Answer:* Secure Shell.
402. **What transport layer protocol and default port does SSH run on?**
    * *Answer:* TCP on Port 22.
403. **Explain asymmetric encryption in SSH.**
    * *Answer:* Uses a public key (to encrypt data) and a private key (to decrypt data).
404. **Where is local user SSH keys saved?**
    * *Answer:* In the user's home directory under `~/.ssh/`.
405. **What is the default filename of generated RSA private and public keys?**
    * *Answer:* Private: `id_rsa`; Public: `id_rsa.pub`.
406. **What is the purpose of `authorized_keys`?**
    * *Answer:* A file on the SSH server storing public keys of authorized clients allowed to connect to that account.
407. **Where is `authorized_keys` located on the server?**
    * *Answer:* In the target user's home directory: `~/.ssh/authorized_keys`.
408. **What permissions should `~/.ssh` folder have?**
    * *Answer:* `700` (Owner only: read, write, execute).
409. **What permissions should `authorized_keys` have?**
    * *Answer:* `600` (Owner only: read, write).
410. **What permissions should client private key (`id_rsa`) have?**
    * *Answer:* `600` (Owner only: read, write).
411. **What is `known_hosts`?**
    * *Answer:* A client-side file storing host keys of remote servers you have connected to, protecting against Man-in-the-Middle attacks.
412. **How does SSH protect against Man-in-the-Middle (MitM) attacks?**
    * *Answer:* By storing host keys in `known_hosts` and warning the user if the server's key changes on subsequent connections.
413. **How do you generate an SSH key pair?**
    * *Answer:* Run `ssh-keygen`.
414. **How do you copy public key to a remote server?**
    * *Answer:* Run `ssh-copy-id -i ~/.ssh/id_rsa.pub user@host`.
415. **What is the difference between `ssh` and `telnet`?**
    * *Answer:* `ssh` encrypts all communications; `telnet` transmits everything (including passwords) in plain text.
416. **How do you connect to server running on custom port 2222?**
    * *Answer:* Run `ssh -p 2222 user@host`.
417. **How do you execute command directly on remote host without entering interactive shell?**
    * *Answer:* Run `ssh user@host "command"` (e.g. `ssh ubuntu@10.0.0.5 "df -h"`).
418. **Explain SSH Agent.**
    * *Answer:* A background helper program that caches decrypted private keys so you don't have to re-enter passphrases.
419. **How do you start SSH Agent?**
    * *Answer:* Run `eval $(ssh-agent -s)`.
420. **How do you add keys to SSH Agent?**
    * *Answer:* Run `ssh-add ~/.ssh/id_rsa`.
421. **What is SSH Agent Forwarding?**
    * *Answer:* Allows you to use your local SSH keys on a remote server to authenticate further connections (e.g. hop through a bastion to a private repo).
422. **Explain the security risk of SSH Agent Forwarding.**
    * *Answer:* If the intermediate server is compromised, root users on that host can access the socket and authenticate connections using your keys.
423. **What is the SSH server configuration file path?**
    * *Answer:* `/etc/ssh/sshd_config`.
424. **How do you disable password-based log in?**
    * *Answer:* Set `PasswordAuthentication no` in `/etc/ssh/sshd_config` and restart SSH.
425. **How do you disable remote root logins?**
    * *Answer:* Set `PermitRootLogin no` in `/etc/ssh/sshd_config`.
426. **Which command transfers files over SSH interactively?**
    * *Answer:* `sftp`.
427. **How do you securely copy file `data.txt` to remote server?**
    * *Answer:* Run `scp data.txt user@host:/destination/path/`.
428. **Explain SSH tunnel port forwarding (Local forwarding).**
    * *Answer:* Forwards a local port to a remote host and port through an encrypted SSH tunnel (`ssh -L local_port:target_host:target_port user@ssh_server`).
429. **Explain SSH remote port forwarding.**
    * *Answer:* Forwards a port on the remote SSH server back to a local host and port (`ssh -R remote_port:local_host:local_port user@ssh_server`).
430. **Explain SSH client configuration file.**
    * *Answer:* The file `~/.ssh/config` containing server connection aliases, hostnames, user designations, and identity key paths.
431. **What does the option `StrictHostKeyChecking no` do?**
    * *Answer:* Automatically adds new host keys to `known_hosts` without prompting, useful for automation scripts (but reduces MitM protection).
432. **Which command restarts the SSH daemon on Ubuntu?**
    * *Answer:* `sudo systemctl restart ssh` or `ssh.service`.
433. **Which command restarts the SSH daemon on CentOS/RHEL?**
    * *Answer:* `sudo systemctl restart sshd`.
434. **What is the purpose of the `ProxyJump` parameter?**
    * *Answer:* Directly routes connections to isolated servers inside private networks through a bastion host.
435. **Why use Ed25519 keys over RSA?**
    * *Answer:* Ed25519 uses elliptic curve cryptography, which is faster and more secure than RSA with a much smaller key size.
436. **What does the command `ssh-add -l` do?**
    * *Answer:* Lists all fingerprints of keys currently cached in the SSH Agent.
437. **How do you remove cached keys from SSH Agent?**
    * *Answer:* Run `ssh-add -D`.
438. **How do you check SSH server logs on Ubuntu?**
    * *Answer:* Run `sudo tail -f /var/log/auth.log` or `journalctl -u ssh`.
439. **What is a Bastion Host?**
    * *Answer:* A hardened, public-facing server used as a gateway to access private instances inside a VPC.
440. **How do you debug an SSH connection failure?**
    * *Answer:* Run SSH in verbose mode: `ssh -vvv user@host`.
441. **What does "Connection refused" on Port 22 indicate?**
    * *Answer:* The remote host is offline, the port is blocked by a firewall, or the SSH daemon is not running.
442. **What does "Permission denied (publickey)" indicate?**
    * *Answer:* The server rejected your key. The public key is not in `authorized_keys`, or the client is not presenting the correct private key.
443. **Explain SSH Multiplexing.**
    * *Answer:* Shares a single TCP connection for multiple SSH sessions to avoid handshake overhead.
444. **What is the role of `/etc/ssh/ssh_config`?**
    * *Answer:* Configures client-side SSH settings system-wide for all local users.
445. **What is SSH Escaping?**
    * *Answer:* Special key sequences (starting with `~`) used to manage active SSH sessions (e.g. `~.` terminates a hung session).
446. **How do you run a GUI application over SSH?**
    * *Answer:* Enable X11 forwarding: `ssh -X user@host`.
447. **How do you test SSH configurations without applying?**
    * *Answer:* Run `/usr/sbin/sshd -t` on the server to check for syntax errors.
448. **How do you restrict SSH logins to a specific user group?**
    * *Answer:* Add `AllowGroups devops` or `AllowUsers administrator` to `/etc/ssh/sshd_config`.
449. **What does `ssh-keygen -R <host_ip>` do?**
    * *Answer:* Removes all keys belonging to the host IP from the client's `known_hosts` file.
450. **What is SSH Banner message?**
    * *Answer:* A warning message displayed to users before they log in, configured via the `Banner` directive in `sshd_config`.

---

## Part 6: 50 DNS Interview Questions & Answers

451. **What is DNS?**
    * *Answer:* Domain Name System - translates domain names to IP addresses.
452. **What port and transport protocol does DNS use?**
    * *Answer:* TCP/UDP on Port 53.
453. **What is a DNS Resolver?**
    * *Answer:* A server (usually run by your ISP or a public provider like Cloudflare `1.1.1.1`) that queries other DNS servers to resolve domains for clients.
454. **What is Root DNS server?**
    * *Answer:* The top level of the DNS hierarchy, directing resolvers to TLD servers based on the domain extension.
455. **How many Root DNS server IPs exist globally?**
    * *Answer:* 13 logical root server IP addresses (managed by hundreds of physical locations worldwide using Anycast).
456. **What is a TLD DNS server?**
    * *Answer:* Top-Level Domain server (e.g. managing `.com`, `.org`, `.net`).
457. **Explain the difference between Recursive and Iterative queries.**
    * *Answer:* In a recursive query, the resolver queries other servers until it returns the final IP to the client. In an iterative query, the queried server returns the address of the next DNS server to ask.
458. **What does DNS cache poisoning mean?**
    * *Answer:* A vulnerability where malicious DNS data is injected into a resolver's cache, redirecting users to fake websites.
459. **Explain Authoritative Name Server.**
    * *Answer:* The server that holds the definitive DNS records for a specific domain.
460. **What is DNS zone file?**
    * *Answer:* A text file containing the mapping between domain names, IPs, and other resources.
461. **What is an A record?**
    * *Answer:* Maps hostnames to IPv4 addresses.
462. **What is a AAAA record?**
    * *Answer:* Maps hostnames to IPv6 addresses.
463. **What is CNAME?**
    * *Answer:* Canonical Name - points one domain alias to another domain name.
464. **Explain the difference between CNAME and Alias records.**
    * *Answer:* A CNAME points to another domain name; an Alias record points directly to a resource (like an AWS Load Balancer) and can be used on the root domain.
465. **What is an MX record?**
    * *Answer:* Mail Exchanger - routes incoming emails to the designated mail servers.
466. **What is a TXT record?**
    * *Answer:* Holds descriptive text data, often used to verify domain ownership and configure email security policies (SPF, DKIM).
467. **What is an NS record?**
    * *Answer:* Lists the authoritative name servers for a domain.
468. **What is a PTR record?**
    * *Answer:* Pointer record - maps an IP address to a domain name (Reverse DNS lookup).
469. **What does TTL represent?**
    * *Answer:* Time-To-Live - the duration resolvers cache a DNS record before querying the name server again.
470. **What happens if you set a very high DNS TTL?**
    * *Answer:* Resolvers cache the record longer, reducing name server load but delaying updates if the server IP changes.
471. **What happens if you set a very low DNS TTL?**
    * *Answer:* DNS updates propagate quickly, but the authoritative name servers experience higher query load.
472. **What is Split-Horizon DNS?**
    * *Answer:* A setup returning different IPs for the same domain name depending on the client's network (internal vs. external).
473. **Explain DNS Round Robin.**
    * *Answer:* Responds with multiple IP addresses in a rotating list to distribute traffic across servers (basic load balancing).
474. **What is DNSSEC?**
    * *Answer:* Adds cryptographic signatures to DNS records to protect against cache poisoning and spoofing.
475. **What is DDNS?**
    * *Answer:* Dynamic DNS - automatically updates DNS records when a device's IP changes.
476. **How do you check DNS records on the CLI?**
    * *Answer:* Run `dig` or `nslookup`.
477. **How do you retrieve MX records for a domain using `dig`?**
    * *Answer:* Run `dig <domain> MX`.
478. **How do you perform a reverse DNS lookup using `dig`?**
    * *Answer:* Run `dig -x <IP_address>`.
479. **What is DNS propagation delay?**
    * *Answer:* The time it takes for DNS updates to sync across recursive resolvers globally.
480. **What is the local DNS configuration file in Linux?**
    * *Answer:* `/etc/resolv.conf`.
481. **What is the role of `/etc/hosts`?**
    * *Answer:* A local text file mapping domains to IPs. The OS checks this file before querying DNS.
482. **What is the default DNS lookup order in Linux?**
    * *Answer:* Usually checks `/etc/hosts` first, then queries DNS servers listed in `/etc/resolv.conf` (configured in `/etc/nsswitch.conf`).
483. **How do you test if local DNS resolution is working?**
    * *Answer:* Run `ping` or `nslookup` on a known domain.
484. **What does NXDOMAIN represent?**
    * *Answer:* Non-Existent Domain - a DNS response indicating the domain name does not exist.
485. **What does SERVFAIL indicate?**
    * *Answer:* The resolver could not get a response from the authoritative name servers.
486. **What does REFUSED indicate?**
    * *Answer:* The authoritative name server refused to process the query, often due to security settings.
487. **What is DNS wildcard record?**
    * *Answer:* A record using `*` to match any subdomain requests (e.g. `*.example.com`).
488. **What is an SOA record?**
    * *Answer:* Start of Authority - contains administrative details about the DNS zone (administrator email, refresh timers, serial numbers).
489. **What does the Serial Number in an SOA record represent?**
    * *Answer:* A version number updated whenever the zone file changes, letting secondary DNS servers know when to sync.
490. **What is DNS Zone Transfer (AXFR)?**
    * *Answer:* The mechanism secondary DNS servers use to replicate the zone file from the primary server.
491. **Why should AXFR queries be restricted?**
    * *Answer:* Unrestricted zone transfers allow anyone to list all subdomains and hosts, leaking infrastructure layout.
492. **What is the role of CoreDNS in Kubernetes?**
    * *Answer:* The default DNS server that handles internal name resolution for Kubernetes services and pods.
493. **What domain suffix do Kubernetes services get?**
    * *Answer:* `<service_name>.<namespace>.svc.cluster.local`.
494. **What is DoH?**
    * *Answer:* DNS over HTTPS - encrypts DNS queries inside standard HTTPS traffic to improve privacy.
495. **What is DoT?**
    * *Answer:* DNS over TLS - encrypts DNS queries inside a secure TLS tunnel (Port 853).
496. **How do you check DNS resolution latency?**
    * *Answer:* Check the "Query time" field in the `dig` output.
497. **How do you query a specific DNS server using `dig`?**
    * *Answer:* Append `@<nameserver_ip>` to the query (e.g. `dig @8.8.8.8 google.com`).
498. **What is an SRV record?**
    * *Answer:* Service record - defines the host name and port of servers for specific services (used by Kubernetes and Active Directory).
499. **What is an CAA record?**
    * *Answer:* Certification Authority Authorization - specifies which Certificate Authorities (CAs) are allowed to issue SSL certificates for the domain.
500. **How do you flush the DNS cache on modern Linux?**
    * *Answer:* Run `sudo resolvectl flush-caches` or `sudo systemd-resolve --flush-caches`.

---

## Part 7: 50 HTTP/HTTPS Interview Questions & Answers

501. **What is HTTP?**
    * *Answer:* Hypertext Transfer Protocol - an application-layer protocol used to transmit web resources.
502. **What port does HTTP use?**
    * *Answer:* Port 80.
503. **What is HTTPS?**
    * *Answer:* Hypertext Transfer Protocol Secure - HTTP encrypted using SSL/TLS.
504. **What port does HTTPS use?**
    * *Answer:* Port 443.
505. **Explain SSL/TLS.**
    * *Answer:* Cryptographic protocols that secure communications over a network using encryption, authentication, and integrity checks.
506. **Explain the TLS Handshake.**
    * *Answer:* Negotiates cryptographic keys and validates identity: ClientHello -> ServerHello -> Certificate Exchange -> Key Generation -> Finished.
507. **What is an SSL Certificate?**
    * *Answer:* A digital document signed by a Certificate Authority (CA) that binds a public key to an organization's domain.
508. **What is a Certificate Authority (CA)?**
    * *Answer:* A trusted third-party organization that issues and signs digital SSL/TLS certificates.
509. **What is Let's Encrypt?**
    * *Answer:* A free, automated, open Certificate Authority providing free domain-validated SSL certificates.
510. **Explain a wild-card SSL certificate.**
    * *Answer:* An SSL certificate that secures a domain and all its subdomains (e.g. `*.example.com`).
511. **Explain the GET method.**
    * *Answer:* Retrieves resources from a server; should not modify state.
512. **Explain the POST method.**
    * *Answer:* Submits data to a server to create a new resource.
513. **Explain the PUT method.**
    * *Answer:* Replaces the target resource completely with the request payload.
514. **Explain the PATCH method.**
    * *Answer:* Applies partial modifications to a resource.
515. **Explain the DELETE method.**
    * *Answer:* Deletes the specified resource from the server.
516. **What is the difference between GET and POST?**
    * *Answer:* GET passes parameters in the URL query string (visible, size limits); POST passes parameters in the request body (hidden, no size limits).
517. **What does a 200 status code mean?**
    * *Answer:* OK - the request succeeded.
518. **What does a 201 status code mean?**
    * *Answer:* Created - the resource was successfully created on the server.
519. **What does a 301 status code mean?**
    * *Answer:* Moved Permanently - redirections.
520. **What does a 302 status code mean?**
    * *Answer:* Found (Moved Temporarily) - redirection.
521. **What does a 400 status code mean?**
    * *Answer:* Bad Request - the server could not understand the request due to malformed syntax.
522. **What does a 401 status code mean?**
    * *Answer:* Unauthorized - client authentication credentials are missing or invalid.
523. **What does a 403 status code mean?**
    * *Answer:* Forbidden - client is authenticated but lacks permission to access the resource.
524. **What does a 404 status code mean?**
    * *Answer:* Not Found - the requested URL path does not exist on the server.
525. **What does a 500 status code mean?**
    * *Answer:* Internal Server Error - the server encountered a general error.
526. **What does a 502 status code mean?**
    * *Answer:* Bad Gateway - an intermediate server (like a reverse proxy) received an invalid response from the upstream application.
527. **What does a 503 status code mean?**
    * *Answer:* Service Unavailable - the server is down for maintenance or overloaded.
528. **What does a 504 status code mean?**
    * *Answer:* Gateway Timeout - the proxy server timed out waiting for the upstream application to respond.
529. **What is an HTTP Header?**
    * *Answer:* Key-value metadata sent with requests and responses (e.g. `Content-Type: application/json`).
530. **What is the User-Agent header?**
    * *Answer:* Identifies the client software (browser, version, OS) making the request.
531. **What is the Content-Type header?**
    * *Answer:* Indicates the media type of the request or response body (e.g. `text/html`, `application/json`).
532. **What is the Authorization header?**
    * *Answer:* Contains credentials (like API keys or Bearer tokens) to authenticate the client.
533. **What is a Cookie?**
    * *Answer:* A key-value string stored in the browser by the server and sent automatically with subsequent requests.
534. **What is Session tracking?**
    * *Answer:* A mechanism to track a user's state across requests (HTTP is stateless), often using a Session ID stored in a cookie.
535. **What does JWT stand for?**
    * *Answer:* JSON Web Token.
536. **Explain the structure of a JWT.**
    * *Answer:* Three dot-separated parts: Header (algorithm), Payload (claims), and Signature (cryptographic verification).
537. **What is CORS?**
    * *Answer:* Cross-Origin Resource Sharing - a browser security mechanism that restricts web pages from making requests to a different domain.
538. **Explain a preflight request in CORS.**
    * *Answer:* An initial `OPTIONS` request sent by the browser to verify if the server permits cross-origin requests.
539. **What is HSTS?**
    * *Answer:* HTTP Strict Transport Security - forces browsers to communicate with the domain exclusively over HTTPS.
540. **How do you inspect HTTP headers using `curl`?**
    * *Answer:* Run `curl -I <URL>`.
541. **What is the difference between HTTP/1.1 and HTTP/2?**
    * *Answer:* HTTP/1.1 processes requests sequentially on TCP connections; HTTP/2 supports multiplexing, allowing multiple requests over a single TCP connection.
542. **What is HTTP/3?**
    * *Answer:* The latest version of HTTP, running over **QUIC** (UDP-based transport) to reduce connection latency.
543. **What does the header `Cache-Control` do?**
    * *Answer:* Specifies caching policies for clients and proxy servers (e.g. `max-age=3600`).
544. **What is the difference between asymmetric and symmetric encryption in SSL/TLS?**
    * *Answer:* Asymmetric encryption (public/private keys) is used to verify identity and securely exchange symmetric keys. Symmetric encryption (same key) is then used to encrypt the actual session data (faster).
545. **What is a Certificate Revocation List (CRL)?**
    * *Answer:* A list of digital certificates revoked by the Certificate Authority before their expiration date.
546. **What is OCSP?**
    * *Answer:* Online Certificate Status Protocol - checks the validity of an SSL certificate in real-time.
547. **What is SNI?**
    * *Answer:* Server Name Indication - an extension to TLS that allows a server to host multiple secure websites on a single IP address.
548. **What does the header `X-Forwarded-For` do?**
    * *Answer:* Appended by reverse proxies to identify the original client's IP address.
549. **What does the header `X-Frame-Options` do?**
    * *Answer:* Prevents clickjacking attacks by blocking the page from loading inside frames/iframes.
550. **What does the header `Content-Security-Policy` (CSP) do?**
    * *Answer:* Restricts the sources of content (scripts, images, stylesheets) the browser is allowed to load.

---

## Part 8: 50 Log Analysis Interview Questions & Answers

551. **Why are logs critical in DevOps and system administration?**
    * *Answer:* They provide a chronological record of system events, which is essential for troubleshooting, security auditing, and root cause analysis.
552. **Name the standard log directory on Linux.**
    * *Answer:* `/var/log`.
553. **What is syslog?**
    * *Answer:* A system-wide logging protocol and daemon collecting events from applications and operating system layers.
554. **Where are general system log files saved?**
    * *Answer:* `/var/log/syslog` (Ubuntu/Debian) or `/var/log/messages` (CentOS/RHEL).
555. **Where are security and authentication logs stored?**
    * *Answer:* `/var/log/auth.log` (Ubuntu/Debian) or `/var/log/secure` (CentOS/RHEL).
556. **What is stored in `/var/log/kern.log`?**
    * *Answer:* Kernel logs, hardware errors, and firewall blocks.
557. **How do you read the kernel ring buffer?**
    * *Answer:* Run `dmesg`.
558. **Where are default Nginx logs located?**
    * *Answer:* `/var/log/nginx/access.log` and `/var/log/nginx/error.log`.
559. **What information is typically found in an access log?**
    * *Answer:* Client IP, timestamp, HTTP request method, URL path, response status code, and user agent.
560. **What is the purpose of log rotation?**
    * *Answer:* Prevents disk space exhaustion by compressing, renaming, and deleting old log files.
561. **Which utility manages log rotation on Linux?**
    * *Answer:* `logrotate`.
562. **Where is `logrotate` configured?**
    * *Answer:* In `/etc/logrotate.conf` and `/etc/logrotate.d/`.
563. **Explain how `journalctl` works.**
    * *Answer:* The CLI tool used to query binary logs managed by the systemd journal service.
564. **How do you view logs for a specific service using `journalctl`?**
    * *Answer:* Run `journalctl -u <service_name>`.
565. **How do you show logs in real-time using `journalctl`?**
    * *Answer:* Run `journalctl -f`.
566. **How do you filter journalctl logs by priority?**
    * *Answer:* Run `journalctl -p <priority>` (e.g. `journalctl -p err`).
567. **How do you search for a specific string inside logs?**
    * *Answer:* Use `grep` (e.g. `grep "ERROR" /var/log/syslog`).
568. **What does the command `tail -f /var/log/syslog | grep "systemd"` do?**
    * *Answer:* Follows the syslog output and prints only lines containing "systemd" in real-time.
569. **Explain how `awk` is used in log analysis.**
    * *Answer:* Extracts specific columns (like status codes or IP addresses) and aggregates them.
570. **What is the command to get the top 5 requesting IPs from nginx access logs?**
    * *Answer:* `awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 5`.
571. **How do you find OOM (Out of Memory) events in syslog?**
    * *Answer:* Run `grep -i "oom" /var/log/syslog` or search kernel outputs `dmesg | grep -i "oom-killer"`.
572. **What does an OOM Killer log look like?**
    * *Answer:* Contains "Out of memory: Killed process <PID> (<process_name>)".
573. **How do you find failed SSH login attempts in auth.log?**
    * *Answer:* Run `grep "Failed password" /var/log/auth.log`.
574. **Where do you look if Nginx returns a 502 Bad Gateway status?**
    * *Answer:* Check `/var/log/nginx/error.log` to see why Nginx cannot connect to the backend server.
575. **What does "bind() to 0.0.0.0:80 failed (98: Address already in use)" in Nginx logs indicate?**
    * *Answer:* Another process is already running and listening on Port 80.
576. **How do you find out which process is using Port 80?**
    * *Answer:* Run `sudo ss -plnt | grep :80` or `sudo lsof -i :80`.
577. **What is structured logging?**
    * *Answer:* Outputting logs in structured formats (like JSON) to make parsing and ingestion easier for log aggregators.
578. **What is Elasticsearch?**
    * *Answer:* A distributed search and analytics engine used to index and search logs.
579. **What is Logstash?**
    * *Answer:* A data processing pipeline that collects, parses, and sends logs to Elasticsearch.
580. **What is Filebeat?**
    * *Answer:* A lightweight log shipper that reads log files from servers and forwards them to Logstash or Elasticsearch.
581. **What is Kibana?**
    * *Answer:* A visualization dashboard used to search, view, and analyze logs stored in Elasticsearch.
582. **Explain the ELK stack.**
    * *Answer:* Elasticsearch, Logstash, and Kibana combined to collect, store, and visualize logs in one central system.
583. **What is EFK stack?**
    * *Answer:* Elasticsearch, Fluentd (as log collector), and Kibana.
584. **What is Loki?**
    * *Answer:* A lightweight, cost-effective log aggregation system designed by Grafana.
585. **How does Loki differ from Elasticsearch?**
    * *Answer:* Loki indexes only metadata (labels) rather than the entire log message, reducing storage costs.
586. **What is Auditd?**
    * *Answer:* The Linux Audit daemon, tracking system-level actions and security changes.
587. **How do you view logs for a Docker container?**
    * *Answer:* Run `docker logs <container_id>`.
588. **How do you follow Docker logs live?**
    * *Answer:* Run `docker logs -f <container_id>`.
589. **Where does Docker store logs on the host by default?**
    * *Answer:* In `/var/lib/docker/containers/<container_id>/<container_id>-json.log`.
590. **How do you view logs for a Kubernetes pod?**
    * *Answer:* Run `kubectl logs <pod_name>`.
591. **How do you view logs for a failed container inside a pod?**
    * *Answer:* Run `kubectl logs <pod_name> -c <container_name>`.
592. **How do you view logs of a previously crashed container?**
    * *Answer:* Run `kubectl logs <pod_name> --previous` or `-p`.
593. **What is log parsing?**
    * *Answer:* Converting unstructured log lines into structured fields (e.g. mapping IP, Timestamp, and URL).
594. **What are Grok patterns?**
    * *Answer:* Regex patterns used in Logstash to parse unstructured log messages into structured fields.
595. **What is Log ingestion?**
    * *Answer:* The process of transmitting logs from hosts to a central logging system.
596. **What does the command `journalctl --since "1 hour ago"` do?**
    * *Answer:* Displays systemd logs generated within the last hour.
597. **How do you check current logs using `journalctl` showing only errors?**
    * *Answer:* Run `journalctl -p err -e` (e indicates jump to end).
598. **How do you inspect kernel crash dumps?**
    * *Answer:* Inspect `/var/log/crash/` or use the `kdump` diagnostic tool.
599. **How do you check who ran the command `sudo rm -rf /var`?**
    * *Answer:* Search `/var/log/auth.log` for lines containing "COMMAND=/usr/bin/rm -rf /var".
600. **What is a log retention policy?**
    * *Answer:* Rules defining how long logs must be kept (for compliance/debugging) before being deleted or archived.
