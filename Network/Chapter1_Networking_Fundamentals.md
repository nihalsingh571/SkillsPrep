# Chapter 1: Networking Fundamentals

Welcome to Chapter 1 of the Networking Interview Handbook. This chapter lays the foundation for everything you need to know about computer networks to crack placement interviews at companies like TCS, Infosys, Accenture, Capgemini, Cognizant, Deloitte, Oracle, IBM, HCL, Amazon, and Microsoft.

Our focus is 30% theory and 70% practical understanding, prioritizing what interviewers actually ask and how things work in the real world.

---

## 1. Introduction to Computer Networks

### What is a network? Why do we need it?
A **computer network** is a group of interconnected computers or devices that can communicate, share resources (like printers or files), and exchange data with each other. 

**Why do we need it?**
- **Resource Sharing**: Sharing printers, scanners, or storage devices.
- **Information Sharing**: Accessing websites, sending emails, or file sharing.
- **Communication**: Video calls, VoIP, instant messaging.
- **Centralized Management**: Centralized databases and user authentication.

### Client-Server vs Peer-to-Peer

| Feature | Client-Server Model | Peer-to-Peer (P2P) Model |
| :--- | :--- | :--- |
| **Concept** | Centralized server provides resources to clients. | Decentralized; all nodes can act as both client and server. |
| **Security** | High (managed centrally by server). | Low (each node manages its own security). |
| **Scalability** | Highly scalable. | Less scalable (hard to manage many nodes). |
| **Cost** | Expensive (dedicated servers). | Cheaper (uses existing computers). |
| **Example** | Browsing a website (Web Server -> Your Browser). | Torrenting, Bluetooth file sharing. |

### Real-world Analogy
Think of a **Client-Server** model like a restaurant. You (the client) order food from the waiter, who fetches it from the kitchen (the server).
Think of a **Peer-to-Peer** model like a potluck dinner. Everyone brings food and shares it directly with everyone else.

### Interview Q&A for this topic
**Q: "Can a machine be both a client and a server?"**
**A:** Yes. In a P2P network, a machine downloads a file (acting as a client) while simultaneously uploading parts of that file to others (acting as a server). Even in a client-server setup, a web server might act as a client when it requests data from a separate database server.

---

## 2. Types of Networks

Networks are generally categorized by their geographical scope.

### LAN (Local Area Network)
- **Scope**: Covers a small geographic area like a home, office, or school building.
- **Speed**: Very fast (100 Mbps to 10 Gbps+).
- **Examples**: Your home WiFi, a college computer lab.

### MAN (Metropolitan Area Network)
- **Scope**: Covers a city or a large campus.
- **Speed**: Moderate to fast.
- **Examples**: Cable TV networks, city-wide public Wi-Fi.

### WAN (Wide Area Network)
- **Scope**: Covers a large geographic area (country, continent, or the globe).
- **Speed**: Slower than LAN due to distance and infrastructure.
- **Examples**: The Internet, a bank's global network of ATMs.

### PAN (Personal Area Network)
- **Scope**: Covers a very small area, usually within 10 meters around a person.
- **Speed**: Relatively slow.
- **Examples**: Bluetooth headphones connected to a phone.

### Comparison Table

| Feature | PAN | LAN | MAN | WAN |
| :--- | :--- | :--- | :--- | :--- |
| **Range** | < 10 meters | Up to a few kilometers | Up to 50 kilometers | Global / Country-wide |
| **Speed** | Low | High | Moderate | Low (comparatively) |
| **Cost** | Negligible | Low | High | Very High |
| **Ownership** | Private (single person) | Private (organization) | Private or Public | Public or Private |

### Interview Traps
**Trap: "Is WiFi a LAN?"**
**Answer:** Yes, it is specifically a WLAN (Wireless Local Area Network). It provides the same functionality as a wired LAN but over radio waves.

**Trap: "Is the Internet a WAN?"**
**Answer:** Yes, the Internet is the largest WAN in the world. It connects millions of smaller LANs and WANs globally.

---

## 3. OSI Model — Deep Dive

### Why OSI model exists
The Open Systems Interconnection (OSI) model was created by ISO to standardize how different computer systems communicate. Before OSI, an IBM computer couldn't easily talk to an Apple computer. OSI provides a universal language/framework.

### All 7 Layers

| # | Layer Name | Function | PDU (Protocol Data Unit) | Protocols | Devices |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 7 | **Application** | Network process to application (User interface) | Data | HTTP, FTP, SMTP | Gateway |
| 6 | **Presentation** | Data formatting, encryption, compression | Data | SSL/TLS, JPEG | Gateway |
| 5 | **Session** | Establishes, manages, terminates sessions | Data | NetBIOS, RPC | Gateway |
| 4 | **Transport** | End-to-end connections, reliability (TCP/UDP) | Segment | TCP, UDP | Load Balancer, Firewall |
| 3 | **Network** | Routing, IP addressing, path determination | Packet | IP, ICMP, OSPF | Router, L3 Switch |
| 2 | **Data Link** | MAC addressing, error detection, framing | Frame | Ethernet, MAC, ARP | Switch, Bridge |
| 1 | **Physical** | Physical medium, transmission of raw bits | Bits | 100Base-T, 802.11 | Hub, Repeater, Cables |

### Real-world Analogy (Sending a Letter)
7. **Application**: Writing the letter.
6. **Presentation**: Translating it to the recipient's language.
5. **Session**: Setting up the mailbox and verifying the address format.
4. **Transport**: Choosing registered mail (TCP - guaranteed) vs regular mail (UDP).
3. **Network**: The postal system mapping the route to the destination city.
2. **Data Link**: The local mail carrier delivering it to the specific street address.
1. **Physical**: The mail truck driving on the road.

### ASCII Diagram of OSI Layers

```text
+---------------------+
| 7. Application      | <-- User Interface / App
+---------------------+
| 6. Presentation     | <-- Format, Encrypt
+---------------------+
| 5. Session          | <-- Start/Stop Sessions
+---------------------+
| 4. Transport        | <-- TCP/UDP, Port Numbers
+---------------------+
| 3. Network          | <-- IP Addresses, Routing
+---------------------+
| 2. Data Link        | <-- MAC Addresses, Switches
+---------------------+
| 1. Physical         | <-- Cables, Hubs, 1s and 0s
+---------------------+
```

### Memory Trick for OSI Layers
- **Top-Down** (7 to 1): **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing.
- **Bottom-Up** (1 to 7): **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way.

### What happens when you send an email
1. **App**: Email client uses SMTP.
2. **Pres**: Formats the email text and encrypts it (TLS).
3. **Session**: Establishes session with the email server.
4. **Transport**: Chops data into segments, adds TCP port 25 or 587.
5. **Network**: Adds source/destination IP to create a packet.
6. **Data Link**: Adds MAC addresses to create a frame.
7. **Physical**: Converts frame to electrical/light signals (bits) over the wire.

### Interview Traps
**Trap: "At which layer does encryption happen?"**
**Answer:** Primarily at Layer 6 (Presentation) for things like SSL/TLS, though IPsec encrypts at Layer 3, and WPA encrypts at Layer 2. If forced to pick one in a multiple-choice, it's Layer 6.

**Trap: "Which layer does a switch operate at?"**
**Answer:** Layer 2 (Data Link). (Note: Multilayer/L3 switches exist and operate at Layer 3, but standard switches are Layer 2).

---

## 4. TCP/IP Model

The TCP/IP model is the practical implementation that actually runs the Internet.

### 4 Layers of TCP/IP
1. **Application Layer**: Combines OSI layers 5, 6, and 7. Handles high-level protocols.
2. **Transport Layer**: Corresponds to OSI layer 4. Handles TCP/UDP.
3. **Internet Layer**: Corresponds to OSI layer 3. Handles IP addressing and routing.
4. **Network Access (Link) Layer**: Combines OSI layers 1 and 2. Handles MAC addressing and physical medium.

### Protocols at each layer
- **Application**: HTTP, HTTPS, FTP, DNS, SMTP
- **Transport**: TCP, UDP
- **Internet**: IPv4, IPv6, ICMP, ARP
- **Network Access**: Ethernet, Wi-Fi (802.11)

### ASCII Diagram

```text
     TCP/IP Model
+---------------------+
|    Application      |
+---------------------+
|     Transport       |
+---------------------+
|      Internet       |
+---------------------+
|   Network Access    |
+---------------------+
```

---

## 5. OSI vs TCP/IP — Complete Comparison

### Comparison Table

| Feature | OSI Model | TCP/IP Model |
| :--- | :--- | :--- |
| **Nature** | Theoretical framework. | Practical, implemented model. |
| **Layers** | 7 Layers. | 4 Layers. |
| **Approach** | Top-down (Model defined first, then protocols). | Bottom-up (Protocols defined first, then model). |
| **Strictness** | Very strict layer boundaries. | Looser layer boundaries. |
| **Usage** | Used for teaching and referencing. | Used in real-world networking (The Internet). |

### Layer Mapping

```text
    OSI MODEL                 TCP/IP MODEL
+---------------+          +---------------+
| Application   | \        |               |
+---------------+  \       |               |
| Presentation  | --->     | Application   |
+---------------+  /       |               |
| Session       | /        |               |
+---------------+          +---------------+
| Transport     | -------> | Transport     |
+---------------+          +---------------+
| Network       | -------> | Internet      |
+---------------+          +---------------+
| Data Link     | \        |               |
+---------------+  ------> | Network Access|
| Physical      | /        |               |
+---------------+          +---------------+
```

### Interview Question
**Q: "Why do we study OSI if TCP/IP is used in practice?"**
**Answer:** The OSI model provides a universally understood, granular framework for troubleshooting and developing network technologies. When a network engineer says "We have a Layer 3 issue," everyone worldwide knows it's a routing/IP problem, not a cable problem.

---

## 6. Encapsulation & Decapsulation

### What is Encapsulation?
Encapsulation is the process of adding headers (and sometimes trailers) to data as it moves down the OSI layers from the sender.

### Step-by-Step
1. **Application Layer**: User creates **Data**.
2. **Transport Layer**: Adds Transport Header (Source/Dest Ports) -> Becomes a **Segment**.
3. **Network Layer**: Adds Network Header (Source/Dest IPs) -> Becomes a **Packet**.
4. **Data Link Layer**: Adds Frame Header (Source/Dest MACs) & FCS Trailer -> Becomes a **Frame**.
5. **Physical Layer**: Converts Frame to **Bits** (1s and 0s) for transmission.

### ASCII Diagram of Encapsulation

```text
Data            [        DATA        ]
                 |                  |
Segment         [TH][    DATA        ]  <-- Transport Header (Ports) added
                 |                  |
Packet      [NH][TH][    DATA        ]  <-- Network Header (IPs) added
                 |                  |
Frame   [FH][NH][TH][    DATA        ][FT] <-- Frame Header (MACs) & Trailer added
```

### Decapsulation
The reverse process happens at the receiver. As data moves UP the layers, each layer strips off its corresponding header, reads the instructions, and passes the remaining payload to the layer above.

### Interview Q
**Q: "What is a PDU?"**
**Answer:** Protocol Data Unit. It is the specific name for the data at a specific layer.
Layer 4 PDU = Segment
Layer 3 PDU = Packet
Layer 2 PDU = Frame
Layer 1 PDU = Bits

---

## 7. Data Transmission Modes

Defines the direction of communication between two devices.

### 1. Simplex
- **Concept**: One-way communication ONLY.
- **Example**: Keyboard to CPU, Radio broadcasting, Television broadcasting.
- **Analogy**: A one-way street.

### 2. Half-Duplex
- **Concept**: Two-way communication, but NOT simultaneously. One device transmits, the other receives, then they switch.
- **Example**: Walkie-talkie ("Over!").
- **Analogy**: A single-lane bridge where cars can go both ways, but only one direction at a time.

### 3. Full-Duplex
- **Concept**: Two-way communication SIMULTANEOUSLY.
- **Example**: Phone call, modern Ethernet switches.
- **Analogy**: A two-lane highway.

### Comparison Table

| Mode | Direction | Simultaneous? | Example | Performance |
| :--- | :--- | :--- | :--- | :--- |
| **Simplex** | Unidirectional | No | Keyboard, Monitor | Lowest |
| **Half-Duplex**| Bidirectional | No (One at a time)| Walkie-talkie | Medium |
| **Full-Duplex**| Bidirectional | Yes | Telephone, Switch | Highest |

### Interview Trick
**Trick to remember**: 
- **Simplex** = Simple (One way).
- **Half** = Half the time (Wait your turn).
- **Full** = Full power (Both talk at once).

---

## 8. Network Topologies

Topology is the physical or logical layout of a network.

### 1. Bus Topology
- All devices share a single communication cable (the backbone).
- **Pros**: Cheap, easy to install for small networks.
- **Cons**: If the main cable breaks, entire network goes down. High collision rate.
- **Use**: Rarely used today (old coax Ethernet).

```text
Device --+-- Device
         |
    [Backbone Cable]
         |
Device --+-- Device
```

### 2. Star Topology (Most Common)
- All devices connect to a central hub or switch.
- **Pros**: If one cable breaks, only that device goes down. Easy to troubleshoot.
- **Cons**: If the central hub/switch fails, the whole network goes down.
- **Use**: Almost all modern LANs (home WiFi, office ethernet).

```text
       Device
         |
Device - Switch - Device
         |
       Device
```

### 3. Ring Topology
- Devices are connected in a closed-loop circle. Data travels in one direction.
- **Pros**: Predictable performance.
- **Cons**: If one device or cable fails, the ring breaks.
- **Use**: Token Ring networks (obsolete), FDDI.

```text
    Device - Device
   /               \
Device           Device
   \               /
    Device - Device
```

### 4. Mesh Topology
- Devices are interconnected with many redundant links.
- **Full Mesh**: Every device connects to every other device. Formula for links: `n(n-1)/2`.
- **Partial Mesh**: Only some critical devices are fully connected.
- **Pros**: Extremely reliable. No single point of failure.
- **Cons**: Very expensive and complex to cable.
- **Use**: The Internet backbone, critical data centers.

```text
Device ----- Device
  | \       / |
  |   \   /   |
  |   /   \   |
  | /       \ |
Device ----- Device
```

### 5. Tree / Hybrid Topology
- A combination of two or more topologies (usually Star networks connected via a Bus).
- **Pros**: Scalable, flexible.
- **Cons**: Complex to manage.

### Comparison Table

| Topology | Cost | Reliability | Scalability | Impact of Single Link Failure |
| :--- | :--- | :--- | :--- | :--- |
| **Bus** | Low | Low | Low | Network crashes |
| **Star** | Medium | High | High | Only one node drops |
| **Ring** | Medium | Low | Low | Network crashes |
| **Mesh** | Very High| Very High | Low | No impact |

### Interview Questions
**Q: "Which topology is used in the Internet?"**
**Answer:** A Mesh (specifically, Partial Mesh) topology, ensuring multiple redundant paths between autonomous systems.

**Q: "What happens if the hub fails in a star topology?"**
**Answer:** The entire network goes down because it acts as the central point of failure.

---

## 9. Network Devices — Deep Dive

### Hub (Layer 1)
- **What it is**: A basic device that connects multiple computers.
- **What it does**: When it receives data on one port, it blindly broadcasts (repeats) it to ALL other ports.
- **Limitations**: Creates unnecessary traffic, low security, high collisions.

### Switch (Layer 2)
- **What it is**: An intelligent hub.
- **What it does**: Learns which MAC address is on which port (builds a MAC table). When data arrives, it forwards it ONLY to the specific destination port.
- **Limitations**: Only works within a single LAN. Cannot route traffic to the Internet.

### Router (Layer 3)
- **What it is**: Connects different networks together (e.g., your home LAN to the ISP's WAN).
- **What it does**: Reads IP addresses and determines the best path (routing) to send packets.
- **Limitations**: Slower than a switch (historically) because it has to inspect IP packets deeply.

### Bridge (Layer 2)
- **What it is**: Connects two LAN segments to make them act as one.
- **What it does**: Filters traffic based on MAC addresses to reduce collisions. (Mostly replaced by switches today).

### Gateway (Layer 7)
- **What it is**: A node that translates between completely different protocols or network architectures.
- **Example**: An API Gateway, or a proxy server.

### Repeater (Layer 1)
- **What it is**: Regenerates weakened signals over long distances.
- **Example**: WiFi Range Extender.

### Firewall (Layer 3/4/7)
- **What it is**: Inspects incoming/outgoing traffic and blocks/allows it based on rules.
- **Example**: Blocking all traffic on Port 23 (Telnet).

### Load Balancer (Layer 4/7)
- **What it is**: Distributes incoming network traffic across multiple servers to prevent overload.

### Comparison Table

| Device | OSI Layer | Addresses Used | Separates Collision Domains? | Separates Broadcast Domains? |
| :--- | :--- | :--- | :--- | :--- |
| **Hub** | 1 (Physical) | None | No | No |
| **Switch**| 2 (Data Link) | MAC Address | Yes | No |
| **Router**| 3 (Network) | IP Address | Yes | Yes |

### Interview Traps
**Trap: "What is the difference between a hub and a switch?"**
**Answer:** A hub broadcasts everything out all ports (Layer 1). A switch learns MAC addresses and sends data only out the necessary port (Layer 2), preventing collisions.

**Trap: "Can a router act as a firewall?"**
**Answer:** Yes. Modern routers have built-in ACLs (Access Control Lists) to filter traffic based on IP/Ports, effectively acting as a basic firewall.

---

## 10. Collision Domain vs Broadcast Domain

### What is a Collision Domain?
A network segment where if two devices talk at the exact same time, their signals will crash into each other (collide) and corrupt the data.
- **Hubs**: 1 Hub = 1 large collision domain (bad).
- **Switches**: 1 Switch Port = 1 isolated collision domain (good).

### What is a Broadcast Domain?
A logical division of a network where all nodes can reach each other via a broadcast at Layer 2 (e.g., an ARP request).
- **Switches**: Forward broadcasts. So an entire 24-port switch is ONE broadcast domain.
- **Routers**: Do NOT forward broadcasts. Therefore, a router stops broadcasts.

### The Rule
- **Hubs**: 1 Collision Domain, 1 Broadcast Domain.
- **Switches**: *N* Collision Domains (one per port), 1 Broadcast Domain.
- **Routers**: *N* Collision Domains, *N* Broadcast Domains (one per interface).

### ASCII Diagram

```text
[PC1]      [PC2]
  \        /
   [ HUB ]   <-- 1 Collision Domain, 1 Broadcast Domain
  /        \
[PC3]      [PC4]


[PC1]      [PC2]
  \        /
   [SWITCH]  <-- 4 Collision Domains, 1 Broadcast Domain
  /        \
[PC3]      [PC4]


   [LAN A]
      |
  [ROUTER]   <-- 2 Collision Domains, 2 Broadcast Domains
      |
   [LAN B]
```

### Interview Trick
**Remember this sentence:** *"Switches break up collision domains, Routers break up broadcast domains."*

---

## 11. MAC Address vs IP Address

### MAC Address (Media Access Control)
- **What is it**: The physical, burned-in address of a Network Interface Card (NIC).
- **Format**: 48-bit length, written in hexadecimal. (e.g., `00:1A:2B:3C:4D:5E`).
- **OUI**: The first 24 bits (3 octets) are the Organizationally Unique Identifier (tells you the manufacturer, e.g., Cisco or Dell).
- **Scope**: Used for local delivery (within the same LAN) at Layer 2.

### IP Address (Internet Protocol)
- **What is it**: The logical address assigned to a device on a network.
- **Format**: 32-bit (IPv4, e.g., `192.168.1.5`) or 128-bit (IPv6).
- **Assignment**: Usually assigned dynamically by a DHCP server, or configured manually.
- **Scope**: Used for global delivery (routing across the Internet) at Layer 3.

### Why do we need both?
- **Analogy**: MAC address is like your social security number (permanent, unique to you). IP address is like your home mailing address (changes if you move).
- The router uses your IP address to get the packet to your local network. Once the packet is on your local network, the switch uses your MAC address to get the frame to your specific computer.

### ARP (Address Resolution Protocol)
How do IP and MAC work together? If a PC knows the destination IP but not the MAC, it shouts (broadcasts): *"Hey, who has IP 192.168.1.10?"* The device with that IP replies: *"That's me, here is my MAC address."* This is ARP.

### Interview Q
**Q: "Can you change a MAC address?"**
**Answer:** Physically, no, it is burned into the NIC. However, you can use software to "spoof" or mask the MAC address to the operating system.

**Q: "Which layer uses MAC vs IP?"**
**Answer:** MAC is Layer 2 (Data Link). IP is Layer 3 (Network).

---

## Chapter Summary Table

| Concept | Key Takeaway |
| :--- | :--- |
| **Network** | Connecting devices to share resources. |
| **LAN/WAN** | LAN = Local (Fast/Cheap), WAN = Global (Slower/Expensive). |
| **OSI Model** | 7 Layers: APSTNDP. Theoretical framework. |
| **TCP/IP** | 4 Layers. Practical model running the Internet. |
| **Encapsulation** | Adding headers. Data -> Segment -> Packet -> Frame -> Bits. |
| **Simplex/Duplex**| Simplex (1-way), Half-Duplex (1 at a time), Full-Duplex (both same time). |
| **Topologies** | Star is most common. Mesh is most reliable (Internet). |
| **Hub/Switch** | Hub = Layer 1, Broadcasts. Switch = Layer 2, uses MAC table. |
| **Router** | Layer 3, uses IP, connects different networks, blocks broadcasts. |
| **Domains** | Switches break collision domains; Routers break broadcast domains. |
| **MAC vs IP** | MAC = Physical (Local). IP = Logical (Global). |

---

## Top 15 Interview Questions

1. **What is the OSI Model and why is it important?**
   *A conceptual 7-layer framework that standardizes network communication and aids in troubleshooting by dividing functions into distinct layers.*
2. **Differentiate between TCP and UDP.**
   *TCP is connection-oriented, reliable, and slow (e.g., Web, Email). UDP is connectionless, unreliable, but very fast (e.g., Video streaming, Gaming).*
3. **What is a MAC address? How is it different from an IP address?**
   *MAC is a 48-bit physical address used on a local network (L2). IP is a 32/128-bit logical address used for routing across networks (L3).*
4. **Explain ARP.**
   *Address Resolution Protocol resolves a known IP address to an unknown MAC address on a local network.*
5. **What is the difference between a Hub, Switch, and Router?**
   *(See section 9 comparison table).*
6. **What is a collision domain vs a broadcast domain?**
   *(See section 10).*
7. **What is Encapsulation? Name the PDUs.**
   *Adding headers to data. Data -> Segment -> Packet -> Frame -> Bits.*
8. **Is the Internet a LAN or WAN?**
   *The largest WAN.*
9. **At which OSI layer does a router operate? A switch?**
   *Router = Layer 3. Switch = Layer 2.*
10. **What topology is the most fault-tolerant?**
    *Mesh topology, as it provides redundant paths.*
11. **What is a Firewall?**
    *A network security device that monitors and filters incoming and outgoing network traffic based on security policies.*
12. **Can a device have an IP address without a MAC address?**
    *No, standard network communication requires a physical NIC, which inherently has a MAC address.*
13. **What is the difference between Half-Duplex and Full-Duplex?**
    *Half is two-way but one at a time (walkie-talkie). Full is two-way simultaneously (telephone).*
14. **Why don't routers forward broadcast traffic?**
    *To prevent broadcast storms from overwhelming WAN links and crashing the internet.*
15. **What is a Subnet Mask? (Preview for Ch 2)**
    *A number that divides an IP address into a Network portion and a Host portion.*

---

## Common Interview Mistakes to Avoid

1. **Saying "A switch routes traffic."** 
   *Mistake!* Switches **forward** frames based on MAC addresses. Routers **route** packets based on IP addresses. Terminology matters.
2. **Confusing TCP/IP layers with OSI layers.** 
   If asked "What layer is IP?", clarify: "It is Layer 3 in the OSI model, which corresponds to the Internet layer in the TCP/IP model."
3. **Assuming MAC addresses change.** 
   A MAC address is permanent hardware. Your IP address changes when you move to a new coffee shop, but your laptop's MAC stays exactly the same.
4. **Forgetting what PDU means.**
   Don't just say "data" for everything. Use Segment (L4), Packet (L3), and Frame (L2). It shows deep understanding.
5. **Blanking on OSI layer order.**
   Always memorize the mnemonic (All People Seem To Need Data Processing) before the interview begins. Write it down on your scratchpad immediately.
