# Chapter 4: Routing, Switching, and Network Security

Welcome to Chapter 4 of the Networking Interview Handbook. This chapter covers the most heavily tested topics in networking interviews at major IT companies (TCS, Infosys, Accenture, Amazon, Microsoft, etc.). We will focus on 30% theory and 70% practical knowledge, emphasizing configuration, troubleshooting, and interview scenarios.

---

## 1. VLAN (Virtual Local Area Network)

### What is a VLAN? Why use it?
A VLAN (Virtual Local Area Network) is a logical grouping of devices in the same broadcast domain, regardless of their physical location on the network. 

**Why use VLANs?**
1. **Segmentation**: Reduces the size of broadcast domains.
2. **Security**: Isolates sensitive traffic (e.g., HR vs. Guest networks).
3. **Flexibility**: Group users by function, not physical location.
4. **Performance**: Reduces broadcast traffic, freeing up bandwidth.

### VLAN Without Physical Separation
Traditionally, to separate networks, you needed separate physical switches. With VLANs, you can create multiple isolated networks on a single physical switch. 

### How VLANs Segment Broadcast Domains
By default, all ports on a switch belong to VLAN 1 (the default VLAN), making the entire switch one large broadcast domain. When you assign ports to different VLANs, a broadcast sent by a device in VLAN 10 will only be forwarded to other ports in VLAN 10.

### Access Port vs. Trunk Port
- **Access Port**: Belongs to a single VLAN. Used to connect end devices (PCs, printers).
- **Trunk Port**: Carries traffic for multiple VLANs across a single physical link. Used to connect switches to other switches or routers.

### 802.1Q VLAN Tagging
When traffic from multiple VLANs crosses a trunk link, the receiving switch needs to know which VLAN the frame belongs to. The IEEE 802.1Q standard adds a 4-byte VLAN tag into the Ethernet frame header (inserting it after the Source MAC address). 

### Inter-VLAN Routing: Router-on-a-Stick
Devices in different VLANs cannot communicate natively at Layer 2. They require a Layer 3 device (router or multilayer switch) to route traffic between them. 
**Router-on-a-Stick (ROAS)** uses a single physical router interface connected to a switch trunk port. The router interface is divided into sub-interfaces, one for each VLAN, acting as the default gateway for that VLAN.

### Native VLAN
The Native VLAN (default is VLAN 1) is the only VLAN that sends untagged frames across a trunk link. It is primarily used for backward compatibility with legacy devices that do not understand 802.1Q tags. For security, it is best practice to change the Native VLAN to an unused VLAN (e.g., VLAN 99).

### ASCII Diagram: 3 VLANs on one switch

```text
       [ Router ]
           | (G0/0 - Trunk, ROAS)
           |
   +-------------------+
   |  Layer 2 Switch   |
   |                   |
   |  Fa0/1   VLAN 10  | ---- PC 1 (192.168.10.10) [HR]
   |  Fa0/2   VLAN 20  | ---- PC 2 (192.168.20.10) [IT]
   |  Fa0/3   VLAN 30  | ---- PC 3 (192.168.30.10) [Sales]
   +-------------------+
```

### Practical Configuration (Cisco IOS)

**Creating VLANs and assigning access ports:**
```cisco
Switch(config)# vlan 10
Switch(config-vlan)# name HR
Switch(config-vlan)# exit

Switch(config)# interface FastEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport access vlan 10
```

**Configuring a Trunk Port:**
```cisco
Switch(config)# interface GigabitEthernet 0/1
Switch(config-if)# switchport trunk encapsulation dot1q
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk native vlan 99
```

**Configuring Router-on-a-Stick:**
```cisco
Router(config)# interface GigabitEthernet 0/0
Router(config-if)# no shutdown

Router(config)# interface GigabitEthernet 0/0.10
Router(config-subif)# encapsulation dot1Q 10
Router(config-subif)# ip address 192.168.10.1 255.255.255.0
```

> **Interview Q:** "How do devices in different VLANs communicate?"
> **Answer:** Devices in different VLANs are in different broadcast domains and logical subnets. To communicate, they require Layer 3 routing. This can be achieved using a Router-on-a-Stick setup or a Layer 3 (multilayer) switch using Switch Virtual Interfaces (SVIs).

> **Common Trap / Mistake:** Forgetting to configure the link between two switches as a trunk port. If left as an access port, only traffic for that specific VLAN will pass, causing a loss of connectivity for other VLANs.

---

## 2. Routing Fundamentals

### What is Routing?
Routing is the process of determining the best path for forwarding data packets across networks from a source to a destination. Routers operate at Layer 3 (Network Layer) of the OSI model.

### The Routing Table
A router uses a routing table to make forwarding decisions. Key components include:
- **Destination Network**: The target IP network and subnet mask.
- **Next-Hop Address**: The IP address of the next router in the path.
- **Metric**: The cost to reach the destination (used to choose between multiple paths from the *same* routing protocol).
- **Exit Interface**: The local interface the router will use to forward the packet.

### How a Router Decides Where to Send a Packet
1. Examines the destination IP address of the incoming packet.
2. Checks the routing table for a matching network.
3. If a match is found, forwards the packet to the next-hop or exit interface.
4. If no match is found, it uses the default route. If there is no default route, the packet is dropped.

### Administrative Distance (AD)
AD is the "trustworthiness" or reliability of a route source. When a router learns about the *same destination network* from multiple different routing protocols, it chooses the route with the lowest AD.

**Common AD Values:**
- Connected Interface: 0
- Static Route: 1
- External BGP (eBGP): 20
- EIGRP: 90
- OSPF: 110
- RIP: 120

### Routing Table Lookup: Longest Prefix Match
If a router has multiple matching routes in its table for a destination IP, it will always choose the **Longest Prefix Match** (the most specific route).
*Example*: Destination IP is 192.168.1.50.
Route 1: 192.168.1.0/24
Route 2: 192.168.1.0/26
The router will choose Route 2 because /26 is a longer match (more specific) than /24.

### Default Route
A default route is a special type of static route used when there is no specific entry in the routing table for a destination network. It is represented as `0.0.0.0/0` (or `0.0.0.0 0.0.0.0`). It acts as the "Gateway of Last Resort."

```text
Routing Table Example:
C   192.168.1.0/24 is directly connected, GigabitEthernet0/0
O   10.0.0.0/8 [110/65] via 192.168.1.2, 00:12:34, GigabitEthernet0/0
S*  0.0.0.0/0 [1/0] via 203.0.113.1
```

---

## 3. Static Routing

### What is Static Routing?
Static routing involves a network administrator manually configuring network paths into the routing table. 

### When to Use Static Routing
- **Small Networks**: Where the topology is simple and rarely changes.
- **Stub Networks**: Networks with only one exit point.
- **Specific Routes**: To override dynamic routing for a specific path (e.g., forcing traffic through a security appliance).

### Configuration
Command syntax: `ip route <destination_network> <subnet_mask> <next-hop_IP_or_exit_interface>`

```cisco
Router(config)# ip route 10.1.1.0 255.255.255.0 192.168.1.2
```

### Floating Static Routes
A floating static route is a backup route. It is configured with an Administrative Distance (AD) higher than the primary route (which could be learned dynamically or statically). It remains hidden in the routing table until the primary route fails.

```cisco
! Primary route via OSPF (AD 110)
! Backup static route with AD 115
Router(config)# ip route 10.1.1.0 255.255.255.0 192.168.2.2 115
```

### Pros and Cons
**Pros:**
- Simple to configure in small networks.
- Highly secure (no routing updates are advertised).
- Predictable routing.
- Uses zero CPU/RAM overhead for protocol processing.

**Cons:**
- Does not scale well in large networks.
- Manual intervention required when topology changes (no automatic failover unless floating).
- High administrative burden.

> **Interview Q:** "When would you prefer static routing over OSPF?"
> **Answer:** I would prefer static routing in a very small network where the topology doesn't change, or for a stub network that has only a single connection to the ISP. It is also useful for creating floating static routes as backups, or when security requirements dictate that no routing updates should be sent over the wire.

---

## 4. Dynamic Routing Overview

### Why Dynamic Routing?
Dynamic routing protocols allow routers to automatically share information about the networks they know and learn about networks from other routers. They automatically adapt to topology changes (e.g., link failures).

### Routing Protocols Classification

1. **Interior Gateway Protocols (IGP)**: Used *within* a single Autonomous System (AS) - e.g., an enterprise network.
   - RIP, OSPF, EIGRP, IS-IS
2. **Exterior Gateway Protocols (EGP)**: Used to route *between* different Autonomous Systems.
   - BGP

**IGP Sub-classifications:**
- **Distance Vector**: Routers share their entire routing table with neighbors. They view the network from their neighbor's perspective. (Based on Bellman-Ford algorithm).
  - Examples: RIP, EIGRP (Advanced Distance Vector)
- **Link State**: Routers map the entire network topology and calculate the best path independently. (Based on Dijkstra's Shortest Path algorithm).
  - Examples: OSPF, IS-IS

### Convergence Time
Convergence is the time it takes for all routers in the network to update their routing tables and agree on the new topology after a change occurs.
- OSPF/EIGRP: Fast convergence.
- RIP: Very slow convergence.

---

## 5. RIP (Routing Information Protocol)

### Overview
RIP is a legacy Distance Vector routing protocol. It is rarely used in modern production networks due to its limitations but is heavily tested in interviews to check your understanding of routing loops.

### Characteristics
- **Metric**: Hop count. Maximum valid hops = 15. A hop count of 16 is considered "Infinite" (unreachable).
- **Updates**: Broadcasts its entire routing table every 30 seconds.

### RIP v1 vs RIP v2
- **RIP v1**: Classful (does not send subnet masks in updates), broadcasts to 255.255.255.255, does not support VLSM (Variable Length Subnet Masking).
- **RIP v2**: Classless (sends subnet masks), multicasts to 224.0.0.9, supports VLSM and authentication.

### Problems: Routing Loops and Slow Convergence
Because RIP routers only know what their neighbors tell them, a failed link can cause routers to continuously pass incorrect routing information back and forth, endlessly incrementing the hop count.

### Count to Infinity Problem & Solutions
To prevent routing loops in RIP:
1. **Maximum Hop Count**: Defines 16 as unreachable.
2. **Split Horizon**: A router will not advertise a route back out the same interface it learned it from.
3. **Route Poisoning**: When a network fails, the router explicitly advertises it with a metric of 16 to immediately inform neighbors it is dead.
4. **Holddown Timers**: If a route fails, the router enters a holddown state and will not accept new updates for that route for a specific period, preventing it from accepting false information while the network converges.

> **Interview Q:** "Why is RIP not suitable for large networks?"
> **Answer:** RIP has a maximum hop count limit of 15, meaning it cannot route packets across networks larger than 15 routers wide. Furthermore, it sends full routing table updates every 30 seconds, which consumes excessive bandwidth on large networks, and it suffers from very slow convergence times.

---

## 6. OSPF (Open Shortest Path First)

### Overview
OSPF is a Link-State routing protocol. It is the most widely used IGP in large enterprise networks.

### Characteristics
- **Metric**: Cost. Calculated based on bandwidth (Reference Bandwidth / Interface Bandwidth). Lower cost is better. (e.g., 100Mbps link has cost 1, 10Mbps link has cost 10).
- **Algorithm**: Dijkstra's Shortest Path First (SPF) algorithm.

### OSPF Areas
To scale efficiently, OSPF uses a hierarchical design divided into **Areas**.
- **Area 0 (Backbone Area)**: The core of the OSPF network. All other areas must connect to Area 0.
- **Non-backbone Areas**: (e.g., Area 1, Area 2).

**Why Areas?**
In a single area, every router must hold a full map of the network (LSDB - Link State Database). A topology change causes every router to run the SPF algorithm, consuming CPU. Splitting into areas restricts LSA (Link State Advertisement) flooding; topology changes in Area 1 do not force routers in Area 2 to recalculate their SPF tree.

### OSPF Router Types
- **Internal Router**: All interfaces in the same area.
- **Backbone Router**: Has at least one interface in Area 0.
- **ABR (Area Border Router)**: Connects a non-backbone area to Area 0.
- **ASBR (Autonomous System Boundary Router)**: Connects the OSPF network to an external network (e.g., another AS running BGP, or redistributing static routes).

### DR and BDR Election
On broadcast multi-access networks (like Ethernet switches), having every router form adjacencies with every other router creates excessive LSA traffic ($n(n-1)/2$ adjacencies). 
OSPF elects a **Designated Router (DR)** and a **Backup Designated Router (BDR)**.
- All other routers (DROTHERs) only form full adjacencies with the DR and BDR.
- Election is based on: 1) Highest OSPF Priority (default is 1), 2) Highest Router ID.

### OSPF Neighbor States
When two OSPF routers connect, they transition through several states:
1. **Down**: No Hello packets received.
2. **Init**: Received a Hello, but own Router ID is not in it.
3. **2-Way**: Bi-directional communication established (Router ID seen in neighbor's Hello). DR/BDR election happens here.
4. **ExStart**: Establish master/slave relationship for database exchange.
5. **Exchange**: Trade Database Description (DBD) packets (summaries of LSDB).
6. **Loading**: Send Link State Requests (LSR) for detailed info; receive Link State Updates (LSU).
7. **Full**: Fully adjacent; LSDBs are completely synchronized.

### Hello and Dead Timers
OSPF sends Hello packets to discover neighbors and maintain adjacencies.
- **Hello Timer**: Typically 10 seconds (on broadcast networks).
- **Dead Timer**: Typically 4x Hello interval (40 seconds). If a Hello isn't received in this time, the neighbor is declared dead.

> **Interview Q:** "What is the difference between OSPF and RIP?"
> **Answer:** 
> 1) Type: OSPF is Link-State, RIP is Distance-Vector. 
> 2) Metric: OSPF uses Cost (bandwidth), RIP uses Hop Count. 
> 3) Scalability: OSPF is highly scalable using areas; RIP is limited to 15 hops. 
> 4) Convergence: OSPF converges very fast; RIP converges slowly and is prone to routing loops. 
> 5) Updates: OSPF sends partial, triggered updates; RIP sends full routing table broadcasts every 30 seconds.

---

## 7. BGP (Border Gateway Protocol)

### Overview
BGP is an Exterior Gateway Protocol (EGP). It is the routing protocol of the Internet, used to route traffic between different Autonomous Systems (AS).

### Characteristics
- **Protocol Type**: Path Vector (a specialized distance vector protocol that tracks the exact path of ASes a route has traversed).
- **Metric**: BGP doesn't have a single metric. It uses a complex set of **Path Attributes** (Weight, Local Preference, AS-PATH, MED, etc.) to determine the best path.

### iBGP vs eBGP
- **eBGP (External BGP)**: Formed between routers in *different* Autonomous Systems. (AD = 20)
- **iBGP (Internal BGP)**: Formed between routers within the *same* Autonomous System. Used to transit internet routes across an enterprise core. (AD = 200)

### Why BGP for the Internet?
OSPF cannot hold the hundreds of thousands of routes required for the Internet; its SPF algorithm would crash the router's CPU. BGP is designed for massive scalability, stability, and granular policy control (allowing ISPs to control traffic flow based on business agreements rather than just link speed).

> **Interview Q:** "What is an Autonomous System (AS)?"
> **Answer:** An Autonomous System is a large network or group of networks managed by a single organization (like an ISP, a large enterprise, or a university) that shares a common routing policy to the internet. They are identified by unique AS Numbers (ASNs) assigned by IANA.

---

## 8. Switching Concepts

### How a Layer 2 Switch Works
A Layer 2 switch forwards frames based on MAC addresses.
1. **Learning**: When a frame enters, the switch reads the Source MAC and records it in its MAC Address Table (CAM table) along with the incoming port.
2. **Forwarding**: The switch reads the Destination MAC, looks it up in the CAM table, and forwards the frame out the specific port.
3. **Flooding**: If the Destination MAC is unknown (or is a broadcast/multicast), the switch floods the frame out all ports EXCEPT the incoming port.
4. **Filtering**: If the Destination MAC is known to be on the same port the frame arrived on, the switch drops (filters) the frame.

### STP (Spanning Tree Protocol)
Redundant links in a switched network cause **Layer 2 Broadcast Loops**, broadcast storms, and MAC table instability. Since Layer 2 frames lack a TTL (Time-To-Live) field, loops will continue endlessly. 
STP (IEEE 802.1D) prevents loops by logically blocking redundant paths.

**Root Bridge Election:**
1. The switch with the lowest Bridge ID (Priority + MAC Address) becomes the Root Bridge.
2. Default priority is 32768.

**Port States:**
1. **Blocking**: Prevents loops, only receives BPDU packets.
2. **Listening**: Prepares to forward, listens to BPDUs, no MAC learning.
3. **Learning**: Learns MAC addresses, does not forward data.
4. **Forwarding**: Normal operation, forwards data.
5. **Disabled**: Administratively shut down.

**RSTP (Rapid STP - 802.1w):**
Legacy STP takes 30-50 seconds to converge. RSTP converges in milliseconds by introducing new port roles (Alternate, Backup) and states (Discarding, Learning, Forwarding).

### EtherChannel / Link Aggregation
Combines multiple physical links into one logical link to increase bandwidth and provide redundancy.
- Protocols: PAgP (Cisco proprietary) or LACP (IEEE 802.3ad standard).
- If one link fails, traffic seamlessly shifts to the remaining links. STP treats the EtherChannel as a single port.

> **Interview Q:** "What happens if STP is not running and you have a loop?"
> **Answer:** A broadcast storm will occur. A broadcast frame will circulate infinitely between the switches because Layer 2 headers do not have a Time-To-Live (TTL) field. This will rapidly consume all CPU and bandwidth resources, effectively bringing down the network.

---

## 9. CSMA/CD (Carrier Sense Multiple Access with Collision Detection)

### Overview
CSMA/CD is the access method used in early wired Ethernet (hub-based, half-duplex environments).

### Process
1. **Sense (Carrier Sense)**: Device listens to the wire. Is anyone talking?
2. **Transmit**: If the wire is clear, it transmits data.
3. **Detect (Collision Detection)**: While transmitting, it listens. If it detects a voltage spike, a collision has occurred.
4. **Jam**: It sends a jam signal to ensure all devices know a collision happened.
5. **Backoff**: All devices wait a random amount of time (backoff timer).
6. **Retry**: Devices attempt to transmit again.

### Collision Domain
A network segment where data packets can collide. A hub represents one large collision domain. Every port on a switch is its own separate collision domain.

### Why CSMA/CD is less relevant now
Modern networks use switches operating in **Full-Duplex** mode, which uses separate transmit (TX) and receive (RX) wires. Because devices can transmit and receive simultaneously without interference, collisions cannot physically occur, rendering CSMA/CD obsolete in modern switched networks.

> **Interview Q:** "Does CSMA/CD work with switches?"
> **Answer:** Technically, yes, if the switch port is operating in half-duplex mode. However, in modern networks, switches operate in full-duplex mode, which completely eliminates collisions, so CSMA/CD is effectively disabled or inactive.

---

## 10. CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)

### Overview
CSMA/CA is used in Wireless LANs (802.11 WiFi).

### Why Avoidance instead of Detection?
Wireless radios are half-duplex (they cannot transmit and receive on the same frequency at the same time). Therefore, a wireless device cannot "listen" for a collision while it is transmitting. Furthermore, the "Hidden Node Problem" means device A might not be able to hear device B, but both try to talk to the Access Point simultaneously.

### RTS/CTS Mechanism
To *avoid* collisions, CSMA/CA uses Request To Send / Clear To Send:
1. Device wants to transmit. It sends an **RTS** frame to the Access Point.
2. The AP responds with a **CTS** frame, effectively telling all other devices to be quiet.
3. The device transmits its data.
4. The AP sends an ACK (Acknowledgment).

### Comparison Table

| Feature | CSMA/CD (Ethernet) | CSMA/CA (WiFi) |
| :--- | :--- | :--- |
| **Media** | Wired (Half-Duplex) | Wireless |
| **Strategy** | Detects and recovers from collisions | Attempts to prevent collisions entirely |
| **Mechanism** | Jam signal and backoff timer | RTS/CTS and Acknowledgments |

---

## 11. Network Security Basics

### CIA Triad
The foundation of all security policies:
- **Confidentiality**: Ensuring data is only accessed by authorized people (Encryption).
- **Integrity**: Ensuring data is not altered in transit (Hashing).
- **Availability**: Ensuring systems and data are available to users when needed (Redundancy, DDoS mitigation).

### AAA (Authentication, Authorization, Accounting)
- **Authentication**: "Who are you?" (Passwords, Biometrics).
- **Authorization**: "What are you allowed to do?" (Permissions, ACLs).
- **Accounting**: "What did you do?" (Logs, Audits). Protocols: RADIUS, TACACS+.

### Common Network Attacks
- **Man-in-the-Middle (MITM)**: Attacker intercepts and relays communication between two parties.
- **DoS/DDoS**: Overwhelming a system with traffic to make it unavailable.
- **ARP Spoofing/Poisoning**: Attacker sends forged ARP messages to associate their MAC address with the IP address of the default gateway, intercepting traffic.
- **VLAN Hopping**: Attacker exploits DTP (Dynamic Trunking Protocol) to negotiate a trunk link and gain access to other VLANs. (Prevention: disable DTP, statically set access ports).
- **DNS Poisoning**: Corrupting DNS cache so a legitimate domain name redirects to a malicious IP.
- **Phishing**: Social engineering to trick users into providing credentials.
- **SQL Injection**: Inserting malicious SQL statements into entry fields for execution (Layer 7 attack).
- **Brute Force**: Repeatedly guessing passwords.

---

## 12. Firewalls

### What is a Firewall?
A firewall is a network security device that monitors and controls incoming and outgoing network traffic based on predetermined security rules. It establishes a barrier between a trusted internal network and untrusted external networks (the Internet).

### Types of Firewalls
1. **Packet Filtering (Stateless)**: Operates at Layer 3/4. Inspects each packet individually against a set of rules (IPs, Ports). It does not remember the state of the connection. Fast but insecure.
2. **Stateful Inspection**: Operates at Layer 3/4. Keeps track of the state of active connections (e.g., TCP 3-way handshake). If internal PC initiates a connection to a web server, the firewall dynamically opens a port for the returning traffic.
3. **Application Layer (Proxy)**: Operates at Layer 7. Understands application protocols (HTTP, FTP). Can perform deep packet inspection to block specific commands (e.g., allow HTTP GET, deny HTTP POST).
4. **Next-Generation Firewall (NGFW)**: Combines stateful inspection with deep packet inspection, Intrusion Prevention Systems (IPS), malware filtering, and application awareness (e.g., blocking Facebook games but allowing Facebook chat).

### Firewall Placement
Usually placed at the network perimeter (between the WAN router and the LAN switch). In larger architectures, they are also placed internally to segment data centers or sensitive VLANs.

> **Interview Q:** "What is the difference between a stateless and stateful firewall?"
> **Answer:** A stateless firewall inspects every packet in isolation based on static rules (ACLs); it requires rules for both outbound requests and inbound replies. A stateful firewall tracks the state of connections; if an internal user establishes an outbound connection, the firewall dynamically allows the corresponding inbound return traffic without needing a specific inbound rule.

---

## 13. ACL (Access Control List)

### What is an ACL?
An ACL is a sequential list of permit or deny statements (rules) applied to an interface to filter network traffic.

### Standard vs. Extended ACL

**Standard ACL (Number 1-99, 1300-1999):**
- Filters based **ONLY on Source IP Address**.
- **Placement Rule**: Place as CLOSE to the DESTINATION as possible. (If placed near the source, it would block the source from reaching *anything*).

**Extended ACL (Number 100-199, 2000-2699):**
- Filters based on Source IP, Destination IP, Protocol (TCP/UDP/ICMP), and Port Number.
- **Placement Rule**: Place as CLOSE to the SOURCE as possible. (Conserves bandwidth by dropping unwanted traffic immediately).

### Wildcard Masks
Used in ACLs (and OSPF) to specify IP ranges. It is the inverse of a subnet mask (0 = must match, 255 = ignore).
- /24 Subnet mask: 255.255.255.0 -> Wildcard: 0.0.0.255
- Host route (specific IP) -> Wildcard: 0.0.0.0

### Processing Rules
1. **Top-to-Bottom**: Rules are processed sequentially.
2. **First Match Wins**: Once a packet matches a rule, the action (permit/deny) is taken, and processing stops.
3. **Implicit Deny**: Every ACL has an invisible `deny any` at the very end. If a packet matches none of the rules, it is dropped.

### Practical Configuration Example
Allow host 192.168.10.5 to access Web Server 10.0.0.1 on port 80, but deny all other web traffic. Allow all other types of traffic.
```cisco
Router(config)# access-list 100 permit tcp host 192.168.10.5 host 10.0.0.1 eq 80
Router(config)# access-list 100 deny tcp any any eq 80
Router(config)# access-list 100 permit ip any any
Router(config)# interface GigabitEthernet 0/0
Router(config-if)# ip access-group 100 in
```

> **Interview Q:** "Where do you place a standard ACL vs an extended ACL, and why?"
> **Answer:** Standard ACLs filter only on source IP, so they must be placed as close to the destination as possible to avoid accidentally blocking traffic to legitimate destinations. Extended ACLs are very specific, so they should be placed as close to the source as possible to drop unauthorized traffic before it wastes bandwidth traversing the network.

---

## 14. VPN (Virtual Private Network)

### What is a VPN?
A VPN creates a secure, encrypted tunnel over an untrusted public network (like the Internet), ensuring confidentiality, integrity, and authentication.

### Types of VPNs
1. **Site-to-Site VPN**: Connects two fixed locations (e.g., Headquarters and Branch Office). The routers at each end handle the encryption/decryption transparently; end users don't know they are using a VPN.
2. **Remote Access VPN**: Connects individual users (e.g., a work-from-home employee) to the corporate network via VPN client software.

### VPN Protocols
- **IPSec (Internet Protocol Security)**: The industry standard for Site-to-Site VPNs. Operates at Layer 3.
- **SSL/TLS**: Used heavily for Remote Access VPNs (e.g., AnyConnect, browser-based VPNs). Operates at the Application Layer.
- **L2TP**: Often paired with IPSec since L2TP provides no encryption on its own.

### IPSec Deep Dive
IPSec uses two primary protocols:
- **AH (Authentication Header)**: Provides data integrity and origin authentication, but NO encryption. (Rarely used alone today).
- **ESP (Encapsulating Security Payload)**: Provides encryption, integrity, and authentication.

**Modes:**
- **Tunnel Mode**: Encrypts the entire original IP packet and adds a new IP header. Used in Site-to-Site VPNs.
- **Transport Mode**: Encrypts only the payload (data), keeping the original IP header intact. Used for host-to-host communications.

> **Interview Q:** "How does a VPN work?"
> **Answer:** A VPN works by establishing a secure tunnel over the internet. It uses tunneling protocols to encapsulate data, encryption (like AES) to ensure confidentiality so hackers cannot read the data, hashing algorithms (like SHA) for data integrity to ensure it wasn't modified, and authentication mechanisms to verify the identity of the parties communicating.

---

## 15. IDS and IPS

### Overview
- **IDS (Intrusion Detection System)**: A passive system. It monitors network traffic for suspicious activity and sends an ALERT if it finds a match. It acts like a security camera; it records the crime but doesn't stop it.
- **IPS (Intrusion Prevention System)**: An active system. It is placed inline in the network traffic path. It monitors traffic, and if a threat is detected, it actively BLOCKS the traffic by dropping packets or resetting connections.

### Detection Methods
1. **Signature-based**: Compares traffic against a database of known malicious patterns (signatures). Very fast, but cannot detect zero-day (brand new) attacks.
2. **Anomaly-based (Heuristic)**: Learns what "normal" network traffic looks like (establishing a baseline). If traffic deviates significantly from the baseline, it flags it. Slower, prone to false positives, but can detect zero-day attacks.

### Placement
- **IDS**: Placed off to the side, receiving a copy of traffic via a SPAN port (port mirroring) on a switch.
- **IPS**: Placed inline, directly behind the firewall, so all traffic must flow *through* it.

> **Interview Q:** "What is the difference between IDS and IPS?"
> **Answer:** An IDS is passive; it monitors traffic via a mirrored port and generates alerts without taking action to stop the threat. An IPS is active and inline; it analyzes traffic as it flows through it and can dynamically drop malicious packets and block the attacker, preventing the attack from reaching the internal network.

---

## 16. Practical Troubleshooting Scenarios

### Scenario 1: User cannot access the internet.
**Step-by-step methodology:**
1. Check physical layer (Is the cable plugged in? Link light on?).
2. `ipconfig /all` - Does the PC have a valid IP address, Subnet Mask, Default Gateway, and DNS server? (If APIPA 169.254.x.x, DHCP has failed).
3. `ping 127.0.0.1` - Tests the local TCP/IP stack.
4. `ping <Default Gateway>` - If fails, issue is on the local LAN (switch, cabling, VLAN).
5. `ping 8.8.8.8` (Google Public IP) - If passes, routing/internet is fine.
6. `ping google.com` - If step 5 passes but step 6 fails, it is a DNS issue.
7. Use `tracert 8.8.8.8` to see where the packets are dropping on the path.

### Scenario 2: Two devices in the same office cannot ping each other.
- Are they in the same VLAN?
- Check the switch MAC address table. Are their MAC addresses being learned?
- Is there an access list (ACL) applied to the VLAN interface (SVI)?
- Does the target device have Windows Firewall enabled? (Windows Firewall blocks ICMP Echo Requests by default).

### Scenario 3: Website loads but HTTPS doesn't work.
- The web server might have port 443 blocked on its local firewall, or the network firewall is blocking port 443 outbound.
- The SSL certificate on the server may have expired or is invalid.

### Scenario 4: VLAN 10 can access the internet but VLAN 20 cannot.
- Check the Router-on-a-Stick configuration. Is the sub-interface for VLAN 20 configured with the correct IP and `encapsulation dot1q 20`?
- Is the switch trunk port allowing VLAN 20? (`switchport trunk allowed vlan...`)
- Is there a NAT overload (PAT) statement on the router allowing the subnet of VLAN 20 to be translated?

### Scenario 5: After adding a new route, the routing table shows the wrong path.
- Check the Administrative Distance (AD). If a dynamic protocol (like OSPF, AD 110) knows a route, and you add a static route with AD 150, the static route will not appear.
- Check for Longest Prefix Match. Is there another route that has a more specific subnet mask (/28 vs /24)?

---

## Chapter Summary

- **VLANs** logically segment networks at Layer 2. **Trunks** carry multiple VLANs; **ROAS** routes between them.
- Routers use **Administrative Distance** (trustworthiness of source) and **Longest Prefix Match** (specificity of subnet) to make forwarding decisions.
- **OSPF** (Link-State, Cost/Bandwidth) is the enterprise standard IGP. **BGP** (Path Vector) runs the internet.
- **STP** stops catastrophic Layer 2 loops.
- **Firewalls** dictate what traffic can cross trust boundaries. **Stateful** firewalls track connections dynamically.
- **ACLs**: Standard (source only, near destination), Extended (source/dest/port, near source).
- Troubleshooting always follows the OSI model, starting at Layer 1 and working up (Ping, Tracert, DNS checks).

---

## Routing Protocol Comparison Table

| Feature | RIPv2 | OSPF | EIGRP | BGP |
| :--- | :--- | :--- | :--- | :--- |
| **Type** | Distance Vector | Link-State | Adv. Distance Vector | Path Vector |
| **Use Case** | Small/Legacy LAN | Large Enterprise Core | Cisco-heavy Enterprise | Internet / ISP |
| **Metric** | Hop Count (Max 15)| Cost (Bandwidth) | Bandwidth & Delay | Path Attributes |
| **Updates** | Full table / 30s | Partial / Triggered | Partial / Triggered | Partial / Triggered |
| **Convergence**| Very Slow | Fast | Very Fast | Slow |
| **Algorithm** | Bellman-Ford | Dijkstra (SPF) | DUAL | Best Path |
| **Admin Dist.**| 120 | 110 | 90 (Internal) | 20 (eBGP) |

---

## Top 15 Interview Questions

1. **What is the difference between a Hub and a Switch?** (Hub is Layer 1, 1 collision domain. Switch is Layer 2, creates separate collision domains per port).
2. **Explain the OSI Model.** (Please Please Do Not Throw Sausage Pizza Away - Physical, Data Link, Network, Transport, Session, Presentation, Application).
3. **TCP vs UDP?** (TCP is reliable, connection-oriented, uses 3-way handshake. UDP is fast, unreliable, connectionless).
4. **What is ARP?** (Address Resolution Protocol - maps known IP addresses to unknown MAC addresses).
5. **How does DHCP work?** (DORA process - Discover, Offer, Request, Acknowledge).
6. **What is DNS?** (Domain Name System - resolves human-readable domain names to IP addresses).
7. **What is NAT?** (Network Address Translation - translates private IP addresses to public routable IP addresses).
8. **What is a Default Gateway?** (The router interface IP that devices send traffic to when the destination is outside their local subnet).
9. **Difference between Public and Private IPs?** (Private IPs are non-routable on the internet - 10.x, 172.16-31.x, 192.168.x).
10. **What is a MAC Address?** (48-bit physical address burned into the NIC, represented in Hexadecimal).
11. **Explain the 3-Way Handshake.** (SYN -> SYN-ACK -> ACK).
12. **What is the difference between Half Duplex and Full Duplex?** (Half: send OR receive. Full: send AND receive simultaneously).
13. **What is Ping used for?** (Testing reachability using ICMP Echo Request/Reply).
14. **What is Tracert/Traceroute?** (Maps the path packets take to a destination using ICMP and manipulating the TTL field).
15. **What is Port Security?** (A switch feature that restricts input to an interface by limiting and identifying MAC addresses of the stations allowed to access the port).

---

## Security Checklist for Networks
- [ ] Change all default passwords (use strong, complex passwords).
- [ ] Disable unused switch ports and place them in an unused VLAN.
- [ ] Disable DTP (Dynamic Trunking Protocol) to prevent VLAN hopping; manually configure trunks.
- [ ] Configure Port Security to prevent CAM table flooding attacks.
- [ ] Implement SSH instead of Telnet for device management.
- [ ] Enable BPDU Guard on all access ports to prevent rogue switches from disrupting STP.
- [ ] Use Access Control Lists (ACLs) on boundary routers to drop spoofed IP ranges.
- [ ] Enforce 802.1x Authentication for wired and wireless access.
- [ ] Keep firmware and OS patches up to date on all network devices.
- [ ] Configure AAA (TACACS+ or RADIUS) for centralized admin tracking.
