# Chapter 5: Computer Networking for DevOps

## 5.1 What is Networking?
**Computer Networking** is the practice of connecting computers together so they can share resources, communicate, and exchange data.

Let's start with a simple analogy:
> **Analogy:** Imagine the global postal system. 
> * **Computers** are houses.
> * **Data packets** are letters.
> * **IP addresses** are the home street addresses.
> * **Routers** are the postal transit hubs that read the addresses and route the mail.
> * **Protocols (TCP/IP)** are the agreed-upon postal formatting rules (e.g., placing the stamp on the top-right and writing the zip code).

```
               [LOCAL LAN SUBNET A]                      [LOCAL LAN SUBNET B]
           ┌─────────────────────────┐               ┌─────────────────────────┐
           │  ┌───────┐   ┌───────┐  │               │  ┌───────┐   ┌───────┐  │
           │  │Host A1│   │Host A2│  │               │  │Host B1│   │Host B2│  │
           │  └───┬───┘   └───┬───┘  │               │  └───┬───┘   └───┬───┘  │
           │      └─────┬─────┘      │               │      └─────┬─────┘      │
           │            ▼            │               │            ▼            │
           │      [Switch A]         │               │      [Switch B]         │
           └────────────┬────────────┘               └────────────┬────────────┘
                        │                                         │
                        ▼                                         ▼
                 [Router A (GW)]                          [Router B (GW)]
                        │                                         │
                        └───────────────►[INTERNET]◄──────────────┘
                                    (Public Routing)
```

---

## 5.2 IP Addresses & Subnetting

An **IP (Internet Protocol) Address** is a unique logical identifier assigned to every device connected to a network.

### IPv4 vs IPv6
* **IPv4:** 32-bit address format written as four decimal segments separated by dots (e.g., `192.168.1.1`). Total combinations: ~4.3 billion (run out).
* **IPv6:** 128-bit address format written in hexadecimal separated by colons (e.g., `2001:db8::ff00:42:8329`). Exposes practically infinite IP addresses.

### IPv4 Structure & Classes
An IPv4 address is divided into a **Network ID** (identifying the subnet) and a **Host ID** (identifying the specific machine on that subnet).

| Class | Range | Default Subnet Mask | Purpose |
| :--- | :--- | :--- | :--- |
| **Class A** | `1.0.0.0` - `127.255.255.255` | `255.0.0.0` | Very large networks. |
| **Class B** | `128.0.0.0` - `191.255.255.255` | `255.255.0.0` | Medium networks. |
| **Class C** | `192.0.0.0` - `223.255.255.255` | `255.255.255.0` | Small local networks. |

### Private IP vs Public IP
* **Public IPs:** Globally unique. Directly reachable over the public internet (e.g., web server hosting google.com).
* **Private IPs:** Used inside local area networks (LANs). They are not routed on the public internet. This allows companies to reuse the same IP pools locally.
  * **Private IP Ranges (RFC 1918):**
    * Class A: `10.0.0.0` to `10.255.255.255` (Common in cloud VPCs).
    * Class B: `172.16.0.0` to `172.31.255.255` (Common default for Docker networks).
    * Class C: `192.168.0.0` to `192.168.255.255` (Common in home Wi-Fi networks).

### Subnetting and CIDR Notation
**Subnetting** is the process of splitting a single large network into smaller, isolated sub-networks (subnets). 
**CIDR (Classless Inter-Domain Routing)** specifies how many bits of the 32-bit IP address represent the network.
* **Example: `10.0.0.0/24`**
  * The `/24` means the first 24 bits are fixed for the network ID.
  * Subnet Mask: `255.255.255.0` ($8 \times 3 = 24$ bits).
  * Host range: `10.0.0.1` to `10.0.0.254`.
  * Total host IPs available: $2^{(32-24)} - 2 = 254$ hosts. (Subtract 2: one for network address `10.0.0.0` and one for broadcast address `10.0.0.255`).

---

## 5.3 DNS (Domain Name System)
**DNS** is the phonebook of the internet. It translates human-friendly names (like `google.com`) into computer-friendly IP addresses (like `142.250.190.46`).

### The DNS Resolution Process

```
 [User Client]    ───1. Request: web.example.com? ───>  [Local DNS Resolver]
               ◄───8. Resolve: IP 192.168.1.10 ────   (e.g., ISP or 8.8.8.8)
                                                               │
     ┌─────────────────────────────────────────────────────────┤
     │ Ask Root Server (".")                                   │ Ask TLD Server (".com")
     ▼ 2.                                                      ▼ 4.
 [Root Server] ──3. Go to TLD for .com ──>                [TLD Server] ──5. Go to NameServer ──>
                                                               │
     ┌─────────────────────────────────────────────────────────┘
     │ Ask Authoritative Name Server
     ▼ 6.
 [Authoritative NameServer] ──7. Record exists at IP 192.168.1.10 ──>
```

### DNS Record Types
* **A Record:** Maps a domain to an IPv4 address (e.g., `app.com -> 54.210.12.5`).
* **AAAA Record:** Maps a domain to an IPv6 address.
* **CNAME (Canonical Name):** Alias record mapping a domain to another domain (e.g., `www.app.com -> app.com`).
* **TXT Record:** Holds arbitrary text data. Often used for domain ownership validation (e.g., SSL validation or SPF mail security).
* **MX Record (Mail Exchanger):** Specifies mail servers responsible for receiving email.
* **NS Record (Name Server):** Identifies which servers hold the authoritative DNS records for the domain.

### DNS Commands

#### 1. `dig` (Domain Information Groper)
* **Definition:** Detailed DNS lookup tool.
* **Syntax:** `dig <domain> [record_type]`
* **Example:**
  ```bash
  dig google.com A
  ```
* **Expected Output:**
  ```text
  ;; ANSWER SECTION:
  google.com.             300     IN      A       142.250.190.46
  ```

#### 2. `nslookup` (Name Server Lookup)
* **Definition:** Basic cross-platform query tool.
* **Syntax:** `nslookup <domain>`
* **Example:**
  ```bash
  nslookup web.example.com
  ```
* **Expected Output:**
  ```text
  Server:         127.0.0.53
  Address:        127.0.0.53#53

  Non-authoritative answer:
  Name:   web.example.com
  Address: 192.168.1.10
  ```

#### 3. `host` (Quick Lookup)
* **Definition:** Minimal lookup utility.
* **Example:** `host google.com`

---

## 5.4 Ports and Protocols

### TCP vs UDP vs ICMP
* **TCP (Transmission Control Protocol):** Connection-oriented. Ensures reliable delivery through error checking, packet sequencing, and a **3-Way Handshake** (SYN -> SYN-ACK -> ACK). Used for HTTP, SSH, databases.
* **UDP (User Datagram Protocol):** Connectionless. Fast and lightweight. No guarantee of packet delivery. Used for video streaming, DNS queries, and gaming.
* **ICMP (Internet Control Message Protocol):** Used by network devices to send error messages and operational info (e.g., used by `ping` and `traceroute`).

### Well-Known Port Table

| Port | Protocol | Usage | Description |
| :--- | :--- | :--- | :--- |
| **22** | TCP | SSH | Secure remote command shell. |
| **21** | TCP | FTP | File Transfer Protocol (unsecure). |
| **25** | TCP | SMTP | Simple Mail Transfer Protocol. |
| **53** | TCP/UDP | DNS | Domain Name System inquiries. |
| **80** | TCP | HTTP | Hypertext Transfer Protocol (unencrypted web). |
| **110** | TCP | POP3 | Post Office Protocol v3 (email retrieval). |
| **143** | TCP | IMAP | Internet Message Access Protocol. |
| **443** | TCP | HTTPS | Secure encrypted web traffic. |
| **3306** | TCP | MySQL | MySQL Database server. |
| **5432** | TCP | PostgreSQL | PostgreSQL Database server. |
| **27017**| TCP | MongoDB | MongoDB NoSQL database. |
| **6379** | TCP | Redis | Redis Cache / Key-Value store. |
| **8080** | TCP | HTTP-Alt | Alternate web server port / default for Jenkins. |
| **6443** | TCP | K8s API | Kubernetes API server control plane. |

---

## 5.5 HTTP & HTTPS Deep-Dive
**HTTP (Hypertext Transfer Protocol)** is the underlying communication protocol for the web. **HTTPS** is HTTP encapsulated in an encrypted SSL/TLS tunnel.

### Client-Server Lifecycle Flow
1. Client establishes a TCP connection to Server on Port 80 (HTTP) or 443 (HTTPS).
2. For HTTPS: Handshake exchanges SSL certificates and negotiates session symmetric keys.
3. Client sends request (Method, Path, Headers, Body).
4. Server parses request, executes backend code, and returns response (Status Code, Headers, Body).
5. TCP connection is closed or kept alive for reuse.

```
 [CLIENT]                                                        [SERVER]
    │                                                               │
    │ ─── 1. TCP 3-Way Handshake (Port 443) ──────────────────────> │
    │ ◄── 2. TCP Handshake Complete ─────────────────────────────── │
    │                                                               │
    │ ─── 3. TLS ClientHello ─────────────────────────────────────> │
    │ ◄── 4. TLS ServerHello + Certificate ──────────────────────── │
    │ ─── 5. Key Exchange & Verification ─────────────────────────> │
    │ ◄── 6. Encryption Secure Channel Active ───────────────────── │
    │                                                               │
    │ ─── 7. HTTPS GET /index.html (Headers) ─────────────────────> │
    │ ◄── 8. HTTPS 200 OK (HTML Body) ───────────────────────────── │
```

### HTTP Methods
* **GET:** Retrieve data from the server. (No request body).
* **POST:** Submit data to the server to create a new resource.
* **PUT:** Replace an existing resource completely.
* **PATCH:** Partially modify an existing resource.
* **DELETE:** Remove a resource from the server.

### Common HTTP Status Codes
* **200 OK:** Request succeeded.
* **201 Created:** Resource successfully created (common on POST/PUT requests).
* **301 Moved Permanently:** Domain redirect.
* **302 Found:** Temporary redirect.
* **400 Bad Request:** Malformed request payload.
* **401 Unauthorized:** Missing credentials or token authentication.
* **403 Forbidden:** Authenticated, but lacks permissions to access resource.
* **404 Not Found:** Requested URL path does not exist.
* **500 Internal Server Error:** Generic application crash or server code failure.
* **502 Bad Gateway:** Intermediary proxy server (like Nginx) cannot connect to upstream application server (like Node.js/Python).
* **503 Service Unavailable:** Server overloaded or down for maintenance.

### Headers, Cookies, JWT
* **Headers:** Metadata key-value pairs (e.g., `Content-Type: application/json`, `Authorization: Bearer <token>`).
* **Cookies:** Key-value pairs stored in the browser by the server, sent with every request to maintain state.
* **JWT (JSON Web Token):** A secure, signed string encoding payload claims (like user permissions), verified cryptographically without database hits.

### Nginx Reverse Proxy & SSL Configuration
In production, a reverse proxy sits in front of your applications to terminate SSL, compress content, and distribute load.

#### Nginx Reverse Proxy Config `/etc/nginx/sites-available/default`:
```nginx
server {
    listen 80;
    server_name app.example.com;

    # Redirect all HTTP traffic to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name app.example.com;

    # SSL Certificates (obtained via Let's Encrypt Certbot)
    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    
    # Modern TLS Security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        # Forward traffic to upstream application server
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5.6 Network Troubleshooting commands

### 1. `ping`
* **Definition:** Checks remote host reachability using ICMP Echo requests.
* **Syntax:** `ping [options] <destination>`
* **Example:** `ping -c 3 google.com`
* **Expected Output:**
  ```text
  64 bytes from 142.250.190.46: icmp_seq=1 ttl=116 time=12.4 ms
  --- google.com ping statistics ---
  3 packets transmitted, 3 received, 0% packet loss, time 2003ms
  rtt min/avg/max/mdev = 12.42/12.85/13.20/0.38 ms
  ```

### 2. `traceroute` & `tracepath`
* **Definition:** Traces the path packets take to reach the destination, showing intermediate router hops.
* **Example:** `traceroute google.com`

### 3. `curl`
* **Definition:** Transfer data to or from a server using various protocols (HTTP, HTTPS, FTP). Excellent for REST API testing.
* **Syntax:** `curl [options] <URL>`
* **Options:**
  * `-I` (Fetch headers only).
  * `-X <METHOD>` (Specify request method).
  * `-d` (Pass request body data).
  * `-k` (Insecure: bypass SSL checks).
* **Example:**
  ```bash
  curl -I https://google.com
  ```
* **Expected Output:**
  ```text
  HTTP/2 200
  content-type: text/html; charset=ISO-8859-1
  date: Mon, 01 Jun 2026 09:25:00 GMT
  ```

### 4. `wget`
* **Definition:** File downloader from web servers.
* **Example:** `wget https://example.com/installer.sh`

### 5. `telnet` & `nc` (Netcat)
* **Definition:** Network testing utilities. `nc` is known as the networking swiss-army knife.
* **Example:** Check if port 3306 on database host is open:
  ```bash
  nc -zv 10.0.1.15 3306
  ```
* **Expected Output:**
  ```text
  Connection to 10.0.1.15 3306 port [tcp/mysql] succeeded!
  ```

### 6. `ss` & `netstat`
* **Definition:** Displays active socket connections, listening ports, and routing tables.
* **Syntax:** `ss -plnt` (p: process name, l: listening sockets, n: numeric ports, t: TCP).
* **Example:**
  ```bash
  sudo ss -plnt
  ```
* **Expected Output:**
  ```text
  State   Recv-Q  Send-Q   Local Address:Port   Peer Address:Port   Process
  LISTEN  0       511          127.0.0.1:8080        0.0.0.0:*      users:(("node",pid=1202,fd=19))
  LISTEN  0       128            0.0.0.0:22          0.0.0.0:*      users:(("sshd",pid=812,fd=3))
  ```

### 7. `ip` & `ifconfig`
* **Definition:** Network interface configuration and display.
* **Example:** Show network interfaces and assigned IPs:
  ```bash
  ip a
  ```
* **Expected Output:**
  ```text
  2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
      inet 172.31.25.10/20 brd 172.31.31.255 scope global dynamic eth0
  ```

### 8. `arp`
* **Definition:** Displays Address Resolution Protocol table mapping IPs to physical MAC addresses.

---

## 5.7 Step-by-Step Troubleshooting Recipes

### Scenario A: Server Not Reachable
1. Check interface status: `ip a` (Ensure UP state and correct IP address).
2. Ping default gateway: `ping -c 3 172.31.16.1`.
3. If gateway pings but public internet doesn't, check default routing table: `ip route`.

### Scenario B: Website Down
1. Check DNS resolution: `nslookup domain.com`.
2. Check connectivity on HTTP port: `curl -Iv http://domain.com`.
3. Log in to the server hosting the app and run `ss -plnt` to see if a process is listening on Port 80/443.
4. Check application and reverse proxy logs: `tail -n 50 /var/log/nginx/error.log`.

### Scenario C: Port Closed
1. If testing remote connection `nc -zv host port` fails:
2. Log in to target host, verify process is listening: `sudo ss -plnt | grep <port>`.
3. If listening locally on `127.0.0.1:<port>`, external clients cannot connect. Edit daemon configuration to listen on `0.0.0.0:<port>`.
4. Check firewalls: `sudo ufw status` or `sudo iptables -L`.

---

## 5.8 Chapter 5 Summary
* Networking links devices. IP addresses identify locations (Private vs Public, IPv4 vs IPv6).
* CIDR notation (`/24`) defines network boundaries and subnet scopes.
* DNS converts human-friendly URLs to IP coordinates.
* Protocols dictate transmission formats: TCP guarantees reliable, connected state. UDP is speed-first.
* Troubleshooting relies on structured checks starting from layer 1 (cabling/interface `ip a`), layer 3 (IP connectivity `ping`), layer 4 (ports `nc`, `ss`), and layer 7 (HTTP responses `curl`).

---

## 5.9 Interview Questions
1. **Q: What is the 3-Way Handshake in TCP?**
   * *A:* It is the method TCP uses to negotiate and establish a connection:
     1. Client sends a **SYN** (Synchronize) packet.
     2. Server responds with a **SYN-ACK** (Synchronize-Acknowledge) packet.
     3. Client returns an **ACK** (Acknowledge) packet to establish the session.
2. **Q: What is the difference between a 502 Bad Gateway and a 504 Gateway Timeout?**
   * *A:* A `502 Bad Gateway` means the proxy (e.g. Nginx) received an invalid/immediate error response from the upstream server (e.g. Node.js backend crashed). A `504 Gateway Timeout` means the upstream server took too long to respond, causing the proxy connection to timeout.
3. **Q: How does DNS lookup work when you search a website?**
   * *A:* The OS checks its local cache -> requests the recursive resolver -> queries root server (`.`) -> queries TLD (`.com`) -> queries Authoritative Name Server -> returns IP mapping to the OS.

---

## 5.10 Hands-On Lab
**Objective:** Identify listening ports, test web routes, and inspect remote IPs.

1. Locate a site name to test (e.g., `example.com`).
2. Run `nslookup example.com` to get the host's IP address.
3. Attempt to download the main index file using `curl`:
   ```bash
   curl -o /tmp/example.html http://example.com
   ```
4. Verify the file contents downloaded correctly.
5. List all active listening TCP ports on your current server:
   ```bash
   sudo ss -plnt
   ```
6. Check if you can connect to local port 22 (SSH) using Netcat loopback test:
   ```bash
   nc -zv 127.0.0.1 22
   ```
7. Verify that the output shows `succeeded!`.
