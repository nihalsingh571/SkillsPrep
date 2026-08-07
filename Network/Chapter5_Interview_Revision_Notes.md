# Chapter 5: Networking Interview Revision Notes

**A high-density, scannable revision guide for placement interviews at top tech companies.**

---

## SECTION 1: ALL COMPARISON TABLES

### 1. OSI 7 Layers
| Layer # | Name | PDU | Key Protocols | Devices | Primary Function |
|:---|:---|:---|:---|:---|:---|
| 7 | Application | Data | HTTP, FTP, SMTP, DNS, SSH | Gateways, Firewalls | Network applications, user interface |
| 6 | Presentation | Data | TLS, SSL, JPEG, ASCII | Gateways, Firewalls | Data formatting, encryption, compression |
| 5 | Session | Data | NetBIOS, PPTP | Gateways, Firewalls | Establish, manage, and terminate sessions |
| 4 | Transport | Segment(TCP)/Datagram(UDP)| TCP, UDP | Load Balancers, Firewalls | End-to-end reliability, flow control, ports |
| 3 | Network | Packet | IP, ICMP, IPsec, IGMP | Routers, L3 Switches | Logical addressing (IP), routing, path determination |
| 2 | Data Link | Frame | Ethernet, MAC, ARP, VLAN | Switches, Bridges, WAPs | Physical addressing (MAC), error detection (FCS) |
| 1 | Physical | Bit | 100BASE-T, 802.11 | Hubs, Repeaters, Cables | Transmitting raw bits over physical medium |

### 2. TCP vs UDP (20 Differences)
| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |
|:---|:---|:---|
| Connection Type | Connection-oriented | Connectionless |
| Reliability | Highly reliable | Unreliable (best effort) |
| Speed | Slower (overhead) | Faster (low overhead) |
| Handshake | Requires 3-way handshake | No handshake |
| Delivery Guarantee | Guaranteed | Not guaranteed |
| Order of Packets | Ordered (sequencing) | Unordered |
| Error Checking | Extensive (Checksum & Recovery) | Basic (Checksum only) |
| Retransmission | Retransmits lost packets | No retransmission |
| Header Size | 20-60 bytes | 8 bytes |
| Flow Control | Yes (Sliding Window) | No |
| Congestion Control| Yes | No |
| Broadcast/Multicast| Unicast only | Unicast, Broadcast, Multicast |
| Weight | Heavyweight | Lightweight |
| State | Stateful | Stateless |
| Acknowledgement | Requires ACKs | No ACKs |
| Data Unit | Segments | Datagrams |
| Use Case | Web, Email, File Transfer | Streaming, VoIP, DNS, Gaming |
| Protocols | HTTP, HTTPS, FTP, SMTP, SSH | DNS, DHCP, TFTP, SNMP, RIP |
| Overhead | High | Low |
| Data Boundary | Byte-stream oriented | Message-oriented |

### 3. Hub vs Switch vs Router
| Feature | Hub | Switch | Router |
|:---|:---|:---|:---|
| Layer | Layer 1 (Physical) | Layer 2 (Data Link) | Layer 3 (Network) |
| Function | Repeats signal to all ports | Forwards frames based on MAC | Routes packets based on IP |
| Collision Domain | 1 (All ports in same domain) | 1 per port | 1 per port |
| Broadcast Domain| 1 | 1 (unless VLANs used) | 1 per port (breaks broadcast domains) |
| Addressing | None | MAC Address | IP Address |
| Transmission | Half-duplex | Full-duplex | Full-duplex |
| Intelligence | Dumb | Smart | Very Smart |

### 4. Static vs Dynamic Routing
| Feature | Static Routing | Dynamic Routing |
|:---|:---|:---|
| Configuration | Manual | Automatic (via protocols) |
| Complexity | Simple for small networks | Complex, suitable for large networks |
| CPU/RAM Usage | Low | High |
| Adaptability | Fails if link goes down | Automatically finds alternate paths |
| Security | High (predictable) | Lower (routes exchanged, can be spoofed) |
| Use Case | Stub networks, default routes | Enterprise networks, Internet |

### 5. RIP vs OSPF vs BGP vs EIGRP
| Protocol | Type | Metric | AD | Max Hops | Convergence | Use Case |
|:---|:---|:---|:---|:---|:---|:---|
| RIPv2 | Distance Vector | Hop count | 120 | 15 | Slow | Small legacy networks |
| OSPF | Link-State | Cost (Bandwidth)| 110 | Unlimited| Fast | Large enterprise (Internal) |
| EIGRP | Advanced DV | Bandwidth/Delay | 90 | 255 | Very Fast | Cisco-only enterprise networks|
| BGP | Path Vector | Path attributes | 20 (e), 200 (i)| Unlimited| Slow | Internet backbone (External) |

### 6. IPv4 vs IPv6
| Feature | IPv4 | IPv6 |
|:---|:---|:---|
| Address Length | 32 bits (4 bytes) | 128 bits (16 bytes) |
| Representation | Decimal (192.168.1.1) | Hexadecimal (2001:0db8::1) |
| Number of Addresses| ~4.3 billion | ~3.4 × 10^38 |
| Header Size | Variable (20-60 bytes) | Fixed (40 bytes) |
| Broadcast | Yes | No (Uses Multicast/Anycast) |
| Checksum | In header | Removed from header (relies on L4) |
| IPsec | Optional | Built-in (Mandatory implementation) |

### 7. Application Layer Protocols
| Protocol | HTTP | HTTPS | FTP | SFTP | SSH | Telnet |
|:---|:---|:---|:---|:---|:---|:---|
| Port | 80 | 443 | 20 (Data), 21 (Control)| 22 | 22 | 23 |
| Secure? | No | Yes (TLS/SSL) | No | Yes (over SSH) | Yes | No |
| Function | Web browsing| Secure web browsing | File transfer | Secure file transfer | Secure remote login| Insecure remote login|

### 8. Firewall Types
| Type | How it Works | Layer | Pros | Cons |
|:---|:---|:---|:---|:---|
| Packet Filter | Inspects headers (IP, Port, Protocol) | L3, L4 | Fast, low impact | Weak, stateless (allows spoofing) |
| Stateful | Remembers connection state (TCP handshake) | L3, L4 | Better security | Slower than packet filter |
| Application (Proxy)| Deep packet inspection (payload) | L7 | Very secure, blocks malware | Slow, high CPU usage |
| NGFW | Stateful + IPS + App awareness | L3-L7 | Comprehensive | Expensive, complex |

### 9. IDS vs IPS
| Feature | IDS (Intrusion Detection System) | IPS (Intrusion Prevention System) |
|:---|:---|:---|
| Function | Detects and alerts | Detects, alerts, and blocks |
| Placement | Out-of-band (promiscuous mode) | In-line (in the traffic path) |
| Impact on Traffic | None (passive) | Can drop or delay packets (active) |
| False Positives | Alerts only (annoying) | Blocks legitimate traffic (disruptive) |

### 10. TCP vs TLS Handshake
| Step | TCP 3-Way Handshake | TLS 1.2 Handshake (Simplifed) |
|:---|:---|:---|
| 1 | Client: SYN | Client: ClientHello (Cipher suites supported) |
| 2 | Server: SYN-ACK | Server: ServerHello + Certificate + ServerHelloDone |
| 3 | Client: ACK | Client: ClientKeyExchange + ChangeCipherSpec + Finished |
| 4 | Data transfer begins | Server: ChangeCipherSpec + Finished |
| 5 | - | Data transfer begins (Encrypted) |

### 11. FLSM vs VLSM
| Feature | FLSM (Fixed Length Subnet Mask) | VLSM (Variable Length Subnet Mask) |
|:---|:---|:---|
| Subnet Size | All subnets are equal size | Subnets can be different sizes |
| IP Waste | High (e.g., /24 for a point-to-point link) | Low (e.g., /30 for a point-to-point link) |
| Routing Protocols | RIPv1, IGRP (Classful) | RIPv2, OSPF, EIGRP (Classless) |

### 12. Network Types
| Type | Span | Example |
|:---|:---|:---|
| PAN (Personal) | Few meters | Bluetooth devices around a desk |
| LAN (Local) | Single building | Office network, home WiFi |
| MAN (Metropolitan)| City | City-wide cable TV network |
| WAN (Wide) | Global/Countries | The Internet, corporate WAN |

### 13. ARP Types
| Type | Purpose |
|:---|:---|
| Normal ARP | Find MAC address for a known IP address |
| RARP (Reverse) | Find IP address for a known MAC (Legacy, replaced by DHCP) |
| Proxy ARP | Router answers ARP on behalf of another device (hides topology) |
| Gratuitous ARP | Device announces its IP/MAC without being asked (for IP conflict detection/HA) |

### 14. Standard vs Extended ACL
| Feature | Standard ACL | Extended ACL |
|:---|:---|:---|
| Number Range | 1-99, 1300-1999 | 100-199, 2000-2699 |
| Filters Based On | Source IP address only | Source IP, Dest IP, Protocol, Port |
| Placement Rule | Place near the DESTINATION | Place near the SOURCE |

### 15. VPN Types
| Feature | Site-to-Site VPN | Remote Access VPN |
|:---|:---|:---|
| Purpose | Connects two networks (Branch to HQ) | Connects single user to network (WFH) |
| Endpoints | Router/Firewall to Router/Firewall | VPN Client Software to VPN Gateway |
| User Action | Transparent to users | User must authenticate/login |

### 16. Email Protocols
| Protocol | Port | Function |
|:---|:---|:---|
| SMTP | 25, 587 | Sending emails (Client to Server, Server to Server) |
| POP3 | 110, 995 | Downloading emails (Deletes from server by default) |
| IMAP | 143, 993 | Syncing emails (Keeps on server, multiple devices) |

### 17. VLAN Ports
| Port Type | Function | Tagging |
|:---|:---|:---|
| Access Port | Connects end devices (PC, Printer) | Untagged (Device doesn't know about VLAN) |
| Trunk Port | Connects switches/routers | Tagged (802.1Q inserts VLAN ID into frame) |

---

## SECTION 2: ALL MEMORY TRICKS

*   **OSI Layer Order (Bottom-Up):** **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way (Physical, Data Link, Network, Transport, Session, Presentation, Application)
*   **OSI Layer Order (Top-Down):** **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
*   **TCP Flags Order:** SYN, ACK, FIN, RST, PSH, URG $\rightarrow$ "**S**oldiers **A**re **F**ighting **R**ebels **P**retty **U**rgently"
*   **IP Class Ranges:**
    *   Class A: 1 - 126
    *   Class B: 128 - 191
    *   Class C: 192 - 223
    *   Class D: 224 - 239
    *   Class E: 240 - 255
    *   *Trick:* **A** **B**oy **C**ame **D**ancing **E**very **F**riday (128, 192, 224, 240)
*   **Powers of 2 (Memorize for subnetting):** 
    *   1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096
*   **Private IP Ranges:**
    *   Class A: 10.0.0.0 (1 network)
    *   Class B: 172.16.x.x to 172.31.x.x (16 networks)
    *   Class C: 192.168.x.x (256 networks)
*   **Administrative Distance (AD) - Lower is better:**
    *   Connected = 0
    *   Static = 1
    *   EBGP = 20
    *   EIGRP = 90
    *   OSPF = 110
    *   RIP = 120
    *   *Trick:* **C**ats **S**ee **E**very **O**bject **R**eally (Connected 0, Static 1, EIGRP 90, OSPF 110, RIP 120)
*   **Port Numbers Categories:**
    *   Well-Known: 0 - 1023 (Reserved for system services)
    *   Registered: 1024 - 49151 (Registered by vendors)
    *   Dynamic/Ephemeral: 49152 - 65535 (Used randomly by clients)
*   **HTTP Status Codes:**
    *   1xx: Informational
    *   2xx: Success
    *   3xx: Redirect
    *   4xx: Client Error
    *   5xx: Server Error
    *   *Trick:* "**I** **S**hould **R**eally **C**ome **A**gain"
*   **DNS Record Types:**
    *   A = IPv4 Address
    *   AAAA = IPv6 Address
    *   MX = Mail Exchange
    *   CNAME = Canonical Name (Alias)
    *   PTR = Pointer (Reverse DNS)
    *   NS = Name Server
*   **TTL (Time to Live):** 
    *   Decremented by 1 at every router hop. Prevents infinite routing loops. Traceroute uses this by sending packets with TTL=1, then 2, then 3, mapping routers that reply with "Time Exceeded".

---

## SECTION 3: FREQUENTLY CONFUSED CONCEPTS

**1. NAT vs PAT**
*   **NAT (Network Address Translation):** Maps one private IP to one public IP (1:1).
*   **PAT (Port Address Translation / NAT Overload):** Maps many private IPs to one public IP (Many:1) using source port numbers to distinguish sessions.

**2. Router vs Gateway**
*   **Router:** Forwards packets between networks using IP addresses.
*   **Gateway:** Specifically translates between completely different protocols (e.g., connecting an IP network to an IBM SNA network), though commonly used synonymously with "Default Router".

**3. Hub vs Switch**
*   **Hub:** Dumb Layer 1 device. Floods electrical signals out all ports. 1 collision domain.
*   **Switch:** Smart Layer 2 device. Forwards frames based on MAC address table. 1 collision domain per port.

**4. Collision Domain vs Broadcast Domain**
*   **Collision Domain:** A network segment where simultaneous transmissions cause collisions. Separated by switch ports and router ports.
*   **Broadcast Domain:** A logical division where a broadcast frame (FFFF.FFFF.FFFF) reaches all nodes. Separated by router ports or VLANs.

**5. IPv4 vs IPv6**
*   **IPv4:** 32-bit, decimal, running out of addresses, relies on NAT.
*   **IPv6:** 128-bit, hexadecimal, essentially infinite addresses, built-in IPsec, no NAT needed.

**6. TCP vs UDP**
*   **TCP:** Guaranteed delivery, ordered, handshake required, slow (Web, Email).
*   **UDP:** Best-effort delivery, unordered, no handshake, fast (Streaming, DNS).

**7. IDS vs IPS**
*   **IDS (Detection):** Watches traffic and sends an alert if malicious. Cannot stop the attack.
*   **IPS (Prevention):** Sits inline. Can actively drop malicious packets.

**8. Firewall vs IPS**
*   **Firewall:** Enforces access control policies (IPs/Ports).
*   **IPS:** Inspects allowed traffic for malicious payloads/signatures.

**9. HTTP vs HTTPS**
*   **HTTP:** Plaintext web traffic (Port 80). Vulnerable to sniffing.
*   **HTTPS:** Encrypted web traffic using TLS (Port 443). Secure.

**10. FTP vs SFTP vs FTPS**
*   **FTP:** Cleartext file transfer (Port 20/21).
*   **SFTP:** File transfer over SSH (Port 22). Secure, single port.
*   **FTPS:** FTP wrapped in TLS. Uses multiple ports, firewall unfriendly.

**11. VLAN vs Subnet**
*   **VLAN:** Layer 2 concept. Logically isolates broadcast domains on a switch.
*   **Subnet:** Layer 3 concept. Logically isolates IP networks. (1 VLAN usually equals 1 Subnet).

**12. Static NAT vs Dynamic NAT vs PAT**
*   **Static NAT:** 1 Private $\rightarrow$ 1 specific Public (Used for hosting servers).
*   **Dynamic NAT:** 1 Private $\rightarrow$ 1 available Public from a pool.
*   **PAT:** Many Private $\rightarrow$ 1 Public IP (Used for home Wi-Fi).

**13. ARP vs RARP**
*   **ARP:** I know the IP, what is your MAC?
*   **RARP:** I know my MAC, what is my IP? (Legacy, DHCP does this now).

**14. Link-state vs Distance-vector routing**
*   **Distance-vector:** Routing by rumor. Knows distance (hops) and direction. (RIP).
*   **Link-state:** Every router has a complete map of the topology. Calculates shortest path. (OSPF).

**15. STP vs RSTP**
*   **STP (Spanning Tree):** Prevents Layer 2 loops. Slow convergence (50 seconds).
*   **RSTP (Rapid STP):** Faster version of STP. Convergence in seconds.

**16. SSH vs Telnet**
*   **SSH:** Secure, encrypted remote CLI access (Port 22).
*   **Telnet:** Insecure, plaintext remote CLI access (Port 23). Never use in prod.

**17. POP3 vs IMAP**
*   **POP3:** Downloads email and deletes from server. Good for 1 device.
*   **IMAP:** Syncs email, leaves on server. Good for multiple devices.

**18. OSPF Area 0 vs non-backbone areas**
*   **Area 0 (Backbone):** The core of an OSPF network.
*   **Non-backbone:** Other areas. *Rule: All non-backbone areas must connect directly to Area 0.*

**19. Standard ACL vs Extended ACL placement**
*   **Standard (Source only):** Place near the destination, or you'll block traffic too early.
*   **Extended (Source+Dest):** Place near the source to save bandwidth.

**20. Full-duplex vs Half-duplex**
*   **Half-duplex:** Can send OR receive, not both simultaneously (Hubs/Walkie-talkies).
*   **Full-duplex:** Can send AND receive simultaneously (Switches/Phones).

---

## SECTION 4: COMMON INTERVIEW TRAPS

1. **Does IPv6 have broadcast?**
   *NO — It uses multicast and anycast instead.*
2. **Can a MAC address be changed?**
   *YES — While burned into hardware (BIA), it can be spoofed/changed in OS software.*
3. **Which OSI layer does a switch work at?**
   *Layer 2 (Data Link), but Layer 3 (Multilayer) switches exist which route IP.*
4. **Is 127.0.0.1 a Class A address?**
   *Technically falls in the Class A range, but it is exclusively reserved for loopback (localhost).*
5. **What happens if you ping 255.255.255.255?**
   *It is a limited broadcast. It reaches all devices on the local subnet but routers will NOT forward it.*
6. **Can two devices have the same private IP?**
   *YES — If they are on completely separate, unconnected private networks behind different NAT routers.*
7. **Does DNS use TCP or UDP?**
   *BOTH! UDP for standard client queries, TCP for zone transfers and responses > 512 bytes.*
8. **Which layer does encryption happen?**
   *Officially Layer 6 (Presentation), but practically TLS operates between Transport and Application.*
9. **What is the subnet mask of /0?**
   *0.0.0.0 — It matches everything. Used for the default route (`0.0.0.0/0`).*
10. **Can a router be in the same broadcast domain as two different networks?**
    *NO — By definition, every router interface creates a separate broadcast domain.*
11. **Is ping TCP or UDP?**
    *NEITHER — Ping uses ICMP (Internet Control Message Protocol), which is an L3 protocol.*
12. **Can you ping a MAC address?**
    *NO — Ping uses IP addresses. You use ARP to find MACs.*
13. **What is the difference between a stateful and stateless firewall?**
    *Stateful remembers the connection (e.g., knows an inbound packet belongs to an outbound request). Stateless treats every packet independently.*
14. **Why do we need a default gateway?**
    *To send traffic to devices that are NOT on the local subnet.*
15. **What happens if two devices have the same IP on a LAN?**
    *IP Conflict. Usually, the first device keeps it, and the second gets an error and loses network access.*
16. **How does a computer know if an IP is on its local network?**
    *It performs a bitwise AND operation between the destination IP and its own Subnet Mask.*
17. **What is MTU?**
    *Maximum Transmission Unit. The largest packet size allowed (typically 1500 bytes for Ethernet). Larger packets get fragmented.*
18. **What is an APIPA address?**
    *169.254.x.x — Assigned automatically by Windows if a DHCP server cannot be reached.*
19. **What port does Ping use?**
    *Ping does NOT use ports. Ports are Layer 4 (TCP/UDP). Ping is Layer 3 (ICMP).*
20. **Can a Layer 2 switch stop a broadcast storm?**
    *NO — Layer 2 switches forward broadcasts. You need STP to prevent the loops that cause the storms, or a Layer 3 device to block them.*
21. **What is the maximum length of a Cat6 Ethernet cable?**
    *100 meters (328 feet).*
22. **What protocol does Traceroute use?**
    *Windows `tracert` uses ICMP. Linux `traceroute` uses UDP by default (but can use ICMP).*
23. **What is a VLAN tag?**
    *A 4-byte header inserted into an Ethernet frame (802.1Q) to identify the VLAN.*
24. **Does HTTPS hide the website domain you are visiting?**
    *NO — The domain name (SNI) is visible in the TLS handshake. Only the path/payload is encrypted.*
25. **What is a proxy server?**
    *A server that makes requests on behalf of a client (masks client IP, can cache, can filter).*
26. **What is BGP split horizon?**
    *Rule: An iBGP router will not advertise a route learned from one iBGP peer to another iBGP peer (prevents loops).*
27. **What is the network address of 192.168.1.130/25?**
    *192.168.1.128 (Since /25 gives block sizes of 128).*
28. **Why is UDP faster than TCP?**
    *No 3-way handshake, no acknowledgments, smaller header, no error recovery overhead.*
29. **What is port forwarding?**
    *Configuring a NAT router to forward incoming traffic on a specific public port to a specific private IP/port inside the network.*
30. **Is DHCP broadcast or unicast?**
    *Broadcast initially (Client discovers server), unicast later in the process.*

---

## SECTION 5: SHORTCUT SUBNETTING METHODS

**1. The Magic Number Trick (Block Size)**
*   Formula: `Magic Number = 256 - [last non-zero octet of subnet mask]`
*   *Example:* Mask is 255.255.255.192.
*   `256 - 192 = 64`.
*   Your block size is 64. The subnets will be: 0, 64, 128, 192.

**2. Quick CIDR /Notation to Hosts Table (MEMORIZE THESE 8)**
*   /24 = 254 hosts (1 subnet)
*   /25 = 126 hosts (2 subnets)
*   /26 = 62 hosts (4 subnets)
*   /27 = 30 hosts (8 subnets)
*   /28 = 14 hosts (16 subnets)
*   /29 = 6 hosts (32 subnets)
*   /30 = 2 hosts (Point-to-point link)
*   /31 & /32 = Special cases

**3. How to find which subnet an IP belongs to instantly**
*   *Example Question:* What subnet is 192.168.1.100/26 in?
*   *Step 1:* Find block size. /26 = 255.255.255.192. Magic number = 256 - 192 = 64.
*   *Step 2:* Divide the target octet by block size. `100 / 64 = 1.something`.
*   *Step 3:* Multiply the integer by block size. `1 * 64 = 64`.
*   *Answer:* The subnet is 192.168.1.64. The broadcast is 192.168.1.127 (next subnet - 1).

**4. 3-Step Interview Subnetting Shortcut**
1.  Write down the CIDR (/X).
2.  Calculate how many bits are borrowed (Host bits = 32 - X).
3.  Number of Hosts = $2^{\text{Host bits}} - 2$.

---

## SECTION 6: IMPORTANT NETWORKING COMMANDS

**`ping`**
*   *Syntax:* `ping google.com`
*   *Shows:* Latency (ms), packet loss.
*   *Use:* Test basic Layer 3 connectivity. Uses ICMP Echo Request/Reply.

**`tracert` (Windows) / `traceroute` (Linux)**
*   *Syntax:* `tracert 8.8.8.8`
*   *Shows:* Every router (hop) between you and the destination.
*   *Use:* Find where a network connection is failing. Uses TTL expiration.

**`ipconfig` (Windows)**
*   *Syntax:* `ipconfig`
*   *Shows:* IP address, Subnet Mask, Default Gateway.
*   *Use:* Basic IP verification.

**`ipconfig /all` (Windows)**
*   *Syntax:* `ipconfig /all`
*   *Shows:* MAC address (Physical Address), DHCP Server IP, DNS Server IP.
*   *Use:* Detailed network interface info.

**`ipconfig /release` and `/renew`**
*   *Syntax:* `ipconfig /release` then `ipconfig /renew`
*   *Use:* Force computer to drop its current IP and request a new one from DHCP.

**`ifconfig` / `ip addr` (Linux)**
*   *Syntax:* `ip addr show`
*   *Shows:* IP addresses, MACs, interface states (UP/DOWN).
*   *Use:* Linux equivalent of ipconfig.

**`netstat -an`**
*   *Syntax:* `netstat -an`
*   *Shows:* All active TCP/UDP connections and listening ports, in numeric format.
*   *Use:* Check if a server is listening on a port, or find malware connections.

**`netstat -r` / `route print`**
*   *Syntax:* `netstat -r`
*   *Shows:* The host's local routing table.
*   *Use:* Verify the default gateway route (`0.0.0.0`).

**`arp -a`**
*   *Syntax:* `arp -a`
*   *Shows:* The ARP cache (mapping of IP addresses to MAC addresses).
*   *Use:* Check if device knows the MAC of the default gateway.

**`nslookup`**
*   *Syntax:* `nslookup google.com`
*   *Shows:* The IP address returned by the DNS server.
*   *Use:* Troubleshoot DNS resolution issues.

**`dig` (Linux)**
*   *Syntax:* `dig google.com`
*   *Shows:* Detailed DNS records (A, MX, NS), query time.
*   *Use:* Advanced DNS troubleshooting.

**`ss -tuln` (Linux)**
*   *Syntax:* `ss -tuln`
*   *Shows:* TCP/UDP listening ports numerically. (Modern replacement for netstat).
*   *Use:* Verify which services are running on a Linux server.

**`tcpdump` (Linux)**
*   *Syntax:* `tcpdump -i eth0 port 80`
*   *Shows:* Raw packet capture.
*   *Use:* Deep network analysis, verifying packets actually reach the server.

**`nmap -sn`**
*   *Syntax:* `nmap -sn 192.168.1.0/24`
*   *Shows:* Which hosts are alive on a network.
*   *Use:* Network discovery (Ping sweep).

**`curl` / `wget`**
*   *Syntax:* `curl -I https://google.com`
*   *Shows:* HTTP headers.
*   *Use:* Test web servers from the command line without a browser.

---

## SECTION 7: REAL-WORLD SCENARIOS

**1. What happens when you type google.com in your browser? (The Complete Flow)**
1.  **DNS Resolution:** Browser checks cache $\rightarrow$ OS cache $\rightarrow$ Local DNS server requests IP for google.com (UDP 53).
2.  **ARP:** If gateway MAC is unknown, PC sends ARP broadcast.
3.  **TCP Handshake:** PC sends SYN to Google's IP on port 443. Google replies SYN-ACK. PC replies ACK.
4.  **TLS Handshake:** PC and Google establish encryption keys.
5.  **HTTP Request:** PC sends encrypted `GET / HTTP/1.1`.
6.  **Response:** Google sends encrypted HTML payload.
7.  **Render & Teardown:** Browser renders page, connection closed with FIN packets.

**2. What happens when you connect a laptop to a corporate WiFi?**
1.  **Association:** Laptop authenticates via 802.1X (RADIUS) or WPA2/3.
2.  **DHCP DORA:**
    *   **D**iscover: Laptop broadcasts requesting an IP.
    *   **O**ffer: DHCP server offers an IP.
    *   **R**equest: Laptop requests that specific IP.
    *   **A**ck: Server acknowledges. Laptop now has IP, Mask, Gateway, DNS.
3.  **Network Access:** Laptop can now route traffic.

**3. How does a Zoom call work at the network level?**
*   Uses **UDP** (mostly via RTP protocol).
*   Why? Speed is critical. If a voice packet is dropped, we don't want TCP to wait and retransmit it (causes lag). We just accept a brief glitch in audio.
*   Susceptible to **Jitter** (variation in latency) and **Packet Loss**.

**4. Why does Netflix buffer?**
*   Unlike Zoom, Netflix uses **TCP** (HTTP/TLS).
*   Buffering occurs because of TCP Congestion Control. If packets drop, TCP cuts transmission speed in half (halves the sliding window) and slowly ramps back up.
*   Netflix mitigates this using **CDNs** (Content Delivery Networks) placing servers close to ISPs.

**5. Company's internal website is unreachable from external. Possible causes?**
*   NAT/Port Forwarding not configured on the edge firewall.
*   Firewall ACL blocking inbound port 80/443.
*   Internal server is down or service stopped.
*   Public DNS record is pointing to the wrong IP.
*   ISP is blocking web ports.

**6. All users in the office suddenly have 169.254.x.x IPs. What happened?**
*   The DHCP server went down, or the link to it broke.
*   169.254.x.x is APIPA (Automatic Private IP Addressing). Windows assigns this when DHCP fails.

**7. After adding a new VLAN, devices in it can't reach the internet. Why?**
*   No Default Gateway assigned via DHCP for that VLAN.
*   Router (Router-on-a-stick or L3 switch) missing an IP interface for the new VLAN.
*   NAT pool not updated on the firewall to translate the new VLAN's subnet.
*   Switch port connecting the router is an Access port instead of a Trunk port.

**8. Two branch offices need to communicate securely over the internet. What do you set up?**
*   A **Site-to-Site IPsec VPN**.
*   Configured on the edge routers/firewalls of both branches. Encrypts traffic transparently between the two LANs.

**9. Users can access HTTP sites but not HTTPS. What's wrong?**
*   Firewall is blocking outbound TCP Port 443.
*   A web proxy is failing to handle SSL interception/decryption.

**10. Server is pingable but the web page is not loading. Possible causes?**
*   Layer 3 is fine (Ping works). Issue is Layer 4 or 7.
*   Web service (Apache/Nginx/IIS) is stopped/crashed.
*   Server's local firewall (iptables/Windows Firewall) is blocking TCP port 80/443.
*   Application error (Code 500).

---

## SECTION 8: ONE-DAY REVISION SHEET

**OSI Model (7 Layers - 1 Line Each):**
7. **Application:** User interface (HTTP/DNS).
6. **Presentation:** Encryption, formatting (TLS/JPEG).
5. **Session:** Setup/teardown connections.
4. **Transport:** Reliability, Ports, TCP/UDP.
3. **Network:** IP Addressing, Routing (Routers).
2. **Data Link:** MAC Addressing, Switching, VLANs.
1. **Physical:** Cables, bits, hubs.

**TCP/IP Model (4 Layers):**
4. Application (maps to OSI 5,6,7)
3. Transport (maps to OSI 4)
2. Internet (maps to OSI 3)
1. Network Access (maps to OSI 1,2)

**Top 10 Port Numbers to Memorize:**
*   20/21: FTP
*   22: SSH
*   23: Telnet
*   25: SMTP
*   53: DNS (UDP/TCP)
*   80: HTTP
*   110: POP3
*   143: IMAP
*   443: HTTPS
*   3389: RDP

**Top 5 Subnetting Shortcuts:**
1. Block size = 256 - Mask.
2. /24 = 254 hosts.
3. /30 = 2 hosts (Point-to-Point).
4. Subnet IP = Network Address (All host bits 0).
5. Broadcast IP = Subnet IP + Block Size - 1 (All host bits 1).

**Key Protocols Summary:**
*   **ARP:** IP $\rightarrow$ MAC.
*   **DNS:** Name $\rightarrow$ IP.
*   **DHCP:** Automates IP assignment.
*   **ICMP:** Pings and error messages.
*   **NAT:** Private IP $\rightarrow$ Public IP.

**Routing Protocols At a Glance:**
*   **OSPF:** Link-State, Metric=Cost, AD=110, Internal.
*   **BGP:** Path-Vector, Internet Protocol, External.
*   **Static:** Manual, AD=1.

**Top 5 Security Concepts:**
1. **Firewall:** Blocks by IP/Port.
2. **IPS:** Blocks by malicious payload.
3. **VPN:** Encrypted tunnel over public net.
4. **ACL:** Rules dictating what is allowed.
5. **TLS:** Certificate-based encryption for web.

---

## SECTION 9: LAST-HOUR REVISION SHEET

**1. The 7 Layers:**
Application $\rightarrow$ Presentation $\rightarrow$ Session $\rightarrow$ Transport $\rightarrow$ Network $\rightarrow$ Data Link $\rightarrow$ Physical.

**2. The 5 Ports:**
22 (SSH), 53 (DNS), 80 (HTTP), 443 (HTTPS), 3389 (RDP).

**3. TCP 3-Way Handshake:**
*   SYN
*   SYN-ACK
*   ACK

**4. Subnetting Formula:**
Hosts = $2^n - 2$ (where n = number of host bits).

**5. The 3 Tables:**
*   **Hub vs Switch vs Router:** (L1/Flood vs L2/MAC vs L3/IP).
*   **TCP vs UDP:** (Reliable/Handshake vs Unreliable/Fast).
*   **IPv4 vs IPv6:** (32-bit vs 128-bit).

**6. The 5 Traps:**
*   Ping is ICMP (Not TCP/UDP).
*   Switch is Layer 2 (Uses MAC, not IP).
*   VLANs break broadcast domains.
*   Routers break broadcast domains.
*   127.0.0.1 is loopback.

---

## SECTION 10: MOST FREQUENTLY ASKED CONCEPTS IN INTERVIEWS

1. **OSI Model Layers:** Mention PDUs (Frame, Packet, Segment) and hardware at L2/L3.
2. **TCP vs UDP:** TCP guarantees delivery via handshakes/ACKs; UDP is fire-and-forget for streaming.
3. **TCP 3-Way Handshake:** SYN $\rightarrow$ SYN-ACK $\rightarrow$ ACK.
4. **What happens when you type a URL:** DNS $\rightarrow$ ARP $\rightarrow$ TCP $\rightarrow$ TLS $\rightarrow$ HTTP $\rightarrow$ HTML.
5. **Subnetting (/24, /26, /30):** Know how to calculate block sizes using 256 minus the mask.
6. **Ping & Traceroute:** Ping = ICMP Echo; Traceroute = ICMP/UDP manipulating the TTL field.
7. **MAC vs IP Address:** MAC is physical/L2/LAN; IP is logical/L3/WAN.
8. **Hub vs Switch vs Router:** Hub floods, Switch learns MACs, Router forwards IPs.
9. **Collision vs Broadcast Domains:** Switches separate collisions, Routers separate broadcasts.
10. **ARP (Address Resolution Protocol):** Resolves known IP to unknown MAC on a local network.
11. **DNS (Domain Name System):** Resolves hostname to IP. Uses UDP 53 for queries.
12. **DHCP (DORA process):** Discover, Offer, Request, Acknowledge.
13. **NAT / PAT:** NAT translates private to public IP; PAT uses ports to allow many-to-one translation.
14. **IPv4 vs IPv6:** 32-bit vs 128-bit, IPv6 has no broadcasts, built-in IPSec.
15. **VLANs:** Layer 2 logical separation. Requires a router (or L3 switch) to communicate between them.
16. **Static vs Dynamic Routing:** Manual configuration vs automatic exchange via protocols.
17. **OSPF vs BGP:** OSPF is interior/link-state/fast; BGP is exterior/path-vector/internet.
18. **Default Gateway:** The IP of the router interface that leads off the local subnet.
19. **Firewall vs IPS:** Firewall blocks ports/IPs; IPS deep-inspects payloads for malware.
20. **VPN (IPsec / SSL):** Creates secure encrypted tunnels over public networks.
21. **HTTP vs HTTPS:** Port 80 plaintext vs Port 443 encrypted via TLS/SSL certificates.
22. **Private IP Ranges:** 10.x.x.x, 172.16-31.x.x, 192.168.x.x.
23. **APIPA (169.254.x.x):** Self-assigned IP when DHCP server is unreachable.
24. **Ports (Well-Known):** Know SSH, Telnet, SMTP, DNS, HTTP, HTTPS by heart.
25. **STP (Spanning Tree):** Prevents Layer 2 broadcast storms by blocking redundant links.

---
*End of Chapter 5*
