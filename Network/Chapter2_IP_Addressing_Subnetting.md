# Chapter 2: IP Addressing & Subnetting

Welcome to Chapter 2 of the Networking Interview Handbook! Whether you are preparing for TCS, Infosys, Accenture, Capgemini, Cognizant, Deloitte, Oracle, IBM, HCL, Amazon, or Microsoft, this chapter is **crucial**. IP addressing and subnetting are heavily tested in almost every network engineering or IT support interview. 

This chapter is designed with a 30% theory and 70% practical approach. We will dive deep into solved numericals, providing step-by-step solutions, ASCII diagrams, tables, and powerful shortcuts to save you time during technical interviews.

---

## 1. IPv4 Basics

An Internet Protocol version 4 (IPv4) address is a numerical label assigned to each device connected to a computer network that uses the IP for communication.

### Key Characteristics
- **Size**: 32 bits long.
- **Format**: Written as 4 octets (an octet is 8 bits) separated by periods (dots) in decimal format.
- **Range**: 0.0.0.0 to 255.255.255.255.

### What Each Octet Represents
Each of the 4 octets can represent a decimal number from 0 to 255 (since 2^8 = 256 possibilities).
The combination of the octets defines both the **Network ID** (which network the device belongs to) and the **Host ID** (the specific device on that network).

### Binary Representation
An IP address is fundamentally a 32-bit binary number. Let's look at a common IP address: `192.168.1.1`

```text
Decimal:     192    .    168    .     1     .     1
Binary:   11000000  .  10101000 . 00000001  . 00000001
```

Each block of 8 binary digits (bits) is one octet.
11000000 = 128 + 64 = 192
10101000 = 128 + 32 + 8 = 168
00000001 = 1
00000001 = 1

---

## 2. IPv4 Classes

To accommodate networks of varying sizes, the original IPv4 architecture defined five classes of IP addresses: A, B, C, D, and E.

### Class Details

**Class A**
- **Range**: 1.0.0.0 – 126.255.255.255
- **Default Subnet Mask**: 255.0.0.0 (/8)
- **Networks**: 126 networks
- **Hosts per Network**: 16,777,214 (approx 16M)
- **Use Case**: Massive organizations (e.g., ISPs, tech giants).
- **Format**: N.H.H.H (N = Network, H = Host)

**Class B**
- **Range**: 128.0.0.0 – 191.255.255.255
- **Default Subnet Mask**: 255.255.0.0 (/16)
- **Networks**: 16,384 networks
- **Hosts per Network**: 65,534
- **Use Case**: Medium to large organizations (e.g., Universities).
- **Format**: N.N.H.H

**Class C**
- **Range**: 192.0.0.0 – 223.255.255.255
- **Default Subnet Mask**: 255.255.255.0 (/24)
- **Networks**: 2,097,152 networks (approx 2M)
- **Hosts per Network**: 254
- **Use Case**: Small organizations, home networks.
- **Format**: N.N.N.H

**Class D**
- **Range**: 224.0.0.0 – 239.255.255.255
- **Use Case**: Multicast (sending data to a group of devices). No subnet mask is used.

**Class E**
- **Range**: 240.0.0.0 – 255.255.255.255
- **Use Case**: Experimental / Reserved for future use.

### Comparison Table

| Class | 1st Octet Range | Default Mask  | Subnet (CIDR) | Max Hosts | Format |
|-------|-----------------|---------------|---------------|-----------|--------|
| A     | 1 - 126         | 255.0.0.0     | /8            | 16.7 M    | N.H.H.H|
| B     | 128 - 191       | 255.255.0.0   | /16           | 65,534    | N.N.H.H|
| C     | 192 - 223       | 255.255.255.0 | /24           | 254       | N.N.N.H|
| D     | 224 - 239       | N/A           | N/A           | Multicast | N/A    |
| E     | 240 - 255       | N/A           | N/A           | Reserved  | N/A    |

> **Memory Trick:** To remember the first octet boundaries, remember the high-order bits:
> Class A starts with `0` (0-127)
> Class B starts with `10` (128-191)
> Class C starts with `110` (192-223)
> Class D starts with `1110` (224-239)
> Class E starts with `1111` (240-255)

> **💡 Interview Trap:** "Why is 127.x.x.x not in Class A?"
> **Answer:** 127.0.0.0 to 127.255.255.255 is officially reserved for loopback testing and inter-process communication on the local host. While it mathematically falls in the 0-127 binary range of Class A, it cannot be assigned to a physical network interface.

---

## 3. Private vs Public IP

With only ~4.3 billion IPv4 addresses available, the internet would have run out of addresses in the 1990s. The solution was Private IPs and NAT.

### Private Ranges (RFC 1918)
These addresses cannot be routed over the public internet. They are strictly for local area networks (LANs).

- **Class A Private**: `10.0.0.0` to `10.255.255.255` (Prefix: `10.0.0.0/8`)
- **Class B Private**: `172.16.0.0` to `172.31.255.255` (Prefix: `172.16.0.0/12`)
- **Class C Private**: `192.168.0.0` to `192.168.255.255` (Prefix: `192.168.0.0/16`)

### Public IP
Everything that is NOT private (and not reserved) is a Public IP. Public IPs are globally unique and routable on the internet.

### Why Private IPs? Network Address Translation (NAT) Explanation
Because private IPs aren't routable on the internet, multiple different organizations can use the EXACT same private IPs (e.g., almost every home network uses `192.168.1.0/24`).
When a device with a private IP wants to talk to the internet, the router uses **NAT (Network Address Translation)** to translate the private IP into the router's single Public IP address.

> **💡 Interview Q:** "Can two devices have the same private IP?"
> **Answer:** Yes, as long as they are on completely different, disconnected local networks. (e.g., My laptop at home and your laptop at your home can both be 192.168.1.5). However, two devices on the *same* network cannot have the same IP, as it would cause an IP conflict.

---

## 4. Special/Reserved IP Ranges

You must memorize these for interviews:
- **`0.0.0.0/8`**: Used for default routes or to specify "this network" / "any IPv4 address" (e.g., binding a server to 0.0.0.0 means it listens on all interfaces).
- **`127.0.0.0/8`**: Loopback. The standard IP is `127.0.0.1` (localhost). Used to test the local TCP/IP stack.
- **`169.254.0.0/16`**: APIPA (Automatic Private IP Addressing).
- **`255.255.255.255`**: Limited Broadcast. Sends a packet to every host on the local physical network.
- **`224.0.0.0/4`**: Multicast routing.

---

## 5. APIPA

### What is APIPA? When does it trigger?
APIPA stands for Automatic Private IP Addressing. 
It triggers when a device is configured to get an IP dynamically (via DHCP), but it cannot reach the DHCP server (server is down, cable is unplugged, etc.).
Windows (and other OSs) will self-assign an IP from the APIPA range so devices on the same switch can still talk to each other locally.

### Range
**169.254.0.0** to **169.254.255.255** (Subnet Mask: 255.255.0.0)

> **💡 Interview Q:** "You see 169.254.x.x on a device — what does that mean?"
> **Answer:** It means the device failed to obtain an IP address from a DHCP server. Troubleshooting steps would include checking the physical connection, verifying the DHCP server is up, and ensuring the DHCP pool isn't exhausted.

---

## 6. Binary Conversion — Complete Guide

To master subnetting, you MUST be comfortable with 8-bit binary conversions.
The positional weights for an 8-bit number are powers of 2:
**128 | 64 | 32 | 16 | 8 | 4 | 2 | 1**

### Decimal to Binary (Positional Weight Method / Subtraction Method)
Convert `192` to binary:
1. Does 128 fit in 192? Yes (1). 192 - 128 = 64
2. Does 64 fit in 64? Yes (1). 64 - 64 = 0
3. The rest are 0.
Result: `11000000`

Convert `168`:
1. Fits 128? Yes (1). 168 - 128 = 40
2. Fits 64? No (0).
3. Fits 32? Yes (1). 40 - 32 = 8
4. Fits 16? No (0).
5. Fits 8? Yes (1). 8 - 8 = 0
6. Rest are 0.
Result: `10101000`

### Binary to Decimal
Convert `00110101`:
Positions: 128 (0), 64 (0), 32 (1), 16 (1), 8 (0), 4 (1), 2 (0), 1 (1)
Math: 32 + 16 + 4 + 1 = `53`

### Quick Conversion Table (Common Subnet Mask Octets)
You must memorize this table for fast CIDR conversions:
| Binary | Decimal |
|--------|---------|
| 10000000 | 128 |
| 11000000 | 192 |
| 11100000 | 224 |
| 11110000 | 240 |
| 11111000 | 248 |
| 11111100 | 252 |
| 11111110 | 254 |
| 11111111 | 255 |

### 10 Practice Problems with Solutions
1. **10** → 00001010 (8+2)
2. **55** → 00110111 (32+16+4+2+1)
3. **100** → 01100100 (64+32+4)
4. **172** → 10101100 (128+32+8+4)
5. **200** → 11001000 (128+64+8)
6. **01010101** → 85 (64+16+4+1)
7. **11101110** → 238 (128+64+32+8+4+2)
8. **10000001** → 129 (128+1)
9. **00011111** → 31 (16+8+4+2+1)
10. **11111111** → 255 (Sum of all)

> **💡 Interview Shortcut:** "How to convert 192.168.1.100 to binary in 30 seconds?"
> Think weights instantly. 192 = 128+64 -> `11000000`. 168 = 128+32+8 -> `10101000`. 1 -> `00000001`. 100 = 64+32+4 -> `01100100`. Total: `11000000.10101000.00000001.01100100`. Done.

---

## 7. Subnet Mask

### What is a subnet mask?
A 32-bit number that masks an IP address, and divides the IP address into a network address and a host address.
Where the mask has a `1`, it represents the network portion. Where it has a `0`, it represents the host portion.

### CIDR Notation (Classless Inter-Domain Routing)
CIDR notation simplifies masks. Instead of writing `255.255.255.0`, you write `/24`.
`/24` means the first 24 bits of the subnet mask are `1`s.
`11111111.11111111.11111111.00000000` = `255.255.255.0`

### CIDR to Subnet Mask Full Table (/8 to /30)

| CIDR | Subnet Mask | CIDR | Subnet Mask | CIDR | Subnet Mask |
|------|-------------|------|-------------|------|-------------|
| /8 | 255.0.0.0 | /16 | 255.255.0.0 | /24 | 255.255.255.0 |
| /9 | 255.128.0.0 | /17 | 255.255.128.0 | /25 | 255.255.255.128 |
| /10 | 255.192.0.0 | /18 | 255.255.192.0 | /26 | 255.255.255.192 |
| /11 | 255.224.0.0 | /19 | 255.255.224.0 | /27 | 255.255.255.224 |
| /12 | 255.240.0.0 | /20 | 255.255.240.0 | /28 | 255.255.255.240 |
| /13 | 255.248.0.0 | /21 | 255.255.248.0 | /29 | 255.255.255.248 |
| /14 | 255.252.0.0 | /22 | 255.255.252.0 | /30 | 255.255.255.252 |
| /15 | 255.254.0.0 | /23 | 255.255.254.0 | /31 | 255.255.255.254 |

---

## 8. Network Address, Broadcast Address, Host Range Calculation

When given an IP and a Subnet Mask, you need to calculate 4 things:
1. **Network Address**: The first IP in the subnet. Identifies the network itself.
2. **First Usable Host**: Network Address + 1
3. **Last Usable Host**: Broadcast Address - 1
4. **Broadcast Address**: The last IP in the subnet. Used to send packets to ALL hosts in this subnet.

### Formulas
- **Network Address** = IP `AND` Subnet Mask (Binary AND operation)
- **Host Bits (h)** = 32 - CIDR Prefix
- **Block Size** (Total IPs in subnet) = 2^h
- **Number of Usable Hosts** = (2^h) - 2
- **Broadcast Address** = Network Address + (Block Size - 1)

### Solved Example
**Given:** IP `192.168.10.50/26`
**Goal:** Find Network, Broadcast, and Host Range.

**Step 1: Find host bits (h)**
32 - 26 = **6 bits**

**Step 2: Find Block Size**
2^6 = **64 IPs**

**Step 3: Find Subnet Mask**
/26 = `11111111.11111111.11111111.11000000` = `255.255.255.192`
The "interesting octet" (the one where the network and host bits mix) is the 4th octet.

**Step 4: Find Network Address**
We are incrementing in blocks of 64 in the 4th octet.
Networks: .0, .64, .128, .192
Our IP is 192.168.10.50. The number 50 falls in the block between 0 and 64.
So, the **Network Address** is `192.168.10.0`

**Step 5: Find Broadcast Address**
The next network is .64, so the broadcast for our network is one less.
**Broadcast Address** = `192.168.10.63`

**Step 6: Find Host Range**
First Host = 192.168.10.1
Last Host = 192.168.10.62
**Range**: `192.168.10.1` to `192.168.10.62`

---

## 9. CIDR — Complete Guide

### What is CIDR? Why was it introduced?
CIDR (Classless Inter-Domain Routing) was introduced in 1993 to replace the rigid Class A/B/C system. In the classful system, if you needed 300 IPs, a Class C (/24, 254 hosts) was too small, so you were forced to buy a Class B (/16, 65,534 hosts), wasting over 65,000 IPs!
CIDR allows VLSM (Variable Length Subnet Masking), letting network admins allocate exactly the amount of IPs needed (e.g., a /23 gives 510 hosts).

### Supernetting with CIDR
CIDR is also used for route summarization (supernetting).
Instead of a router advertising four separate /24 routes:
192.168.0.0/24, 192.168.1.0/24, 192.168.2.0/24, 192.168.3.0/24
It can advertise a single summarized route: **192.168.0.0/22**. This shrinks routing tables, making routers faster and more efficient.

---

## 10. Complete Subnetting — FLSM (Fixed Length Subnet Masking)

### What is FLSM?
FLSM is when all subnets created from a larger network are precisely the same size, using the exact same subnet mask.

### When to use FLSM
Use it when all departments/networks need approximately the same number of hosts, or in introductory learning scenarios. (In the real world, VLSM is preferred).

### Formulas
- Subnet Bits Borrowed (n) = New CIDR - Old CIDR
- Number of Subnets created = 2^n
- Host bits left (h) = 32 - New CIDR
- Hosts per Subnet = (2^h) - 2

### SOLVED NUMERICAL 1 (Beginner)
**Problem:** Divide `192.168.1.0/24` into 4 equal subnets.
**Solution:**
1. We need 4 subnets. 2^n = 4. Therefore, n = 2. (Borrow 2 bits from host portion).
2. Old CIDR = /24. New CIDR = /24 + 2 = **/26**
3. New Mask: /26 = `255.255.255.192`
4. Host bits left (h) = 32 - 26 = 6.
5. Block Size = 2^6 = **64**
6. Subnets:
   - **Subnet 1:**
     Network: 192.168.1.0
     First Host: 192.168.1.1
     Last Host: 192.168.1.62
     Broadcast: 192.168.1.63
   - **Subnet 2:**
     Network: 192.168.1.64
     First Host: 192.168.1.65
     Last Host: 192.168.1.126
     Broadcast: 192.168.1.127
   - **Subnet 3:**
     Network: 192.168.1.128
     First Host: 192.168.1.129
     Last Host: 192.168.1.190
     Broadcast: 192.168.1.191
   - **Subnet 4:**
     Network: 192.168.1.192
     First Host: 192.168.1.193
     Last Host: 192.168.1.254
     Broadcast: 192.168.1.255

### SOLVED NUMERICAL 2 (Intermediate)
**Problem:** Divide `172.16.0.0/16` into 16 subnets.
**Solution:**
1. Need 16 subnets. 2^n = 16. n = 4.
2. New CIDR = /16 + 4 = **/20**
3. New Mask: /20 = `255.255.240.0`
4. Host bits (h) = 32 - 20 = 12.
5. Block size = 2^12 = 4096. However, it's easier to look at the "interesting octet". The 3rd octet changed. Block size in 3rd octet = 256 - 240 = 16.
6. The subnets count up by 16 in the 3rd octet:
   - S1: 172.16.0.0 to 172.16.15.255
   - S2: 172.16.16.0 to 172.16.31.255
   - S3: 172.16.32.0 to 172.16.47.255
   ...
   - S16: 172.16.240.0 to 172.16.255.255

### SOLVED NUMERICAL 3 (Advanced)
**Problem:** A company needs 6 subnets from `10.0.0.0/24`, each with at least 25 hosts.
**Solution:**
1. To get 6 subnets, we need to borrow bits. 2^2 = 4 (not enough). 2^3 = 8 (enough). So we need 3 network bits.
2. This leaves 8 - 3 = 5 host bits per subnet.
3. Check host requirement: 2^5 = 32. Usable = 30. (30 > 25, so this works!)
4. New CIDR = /24 + 3 = **/27**
5. Mask: `255.255.255.224`. Block size = 32.
6. Subnets:
   - 10.0.0.0/27 (Hosts: .1 to .30, BC: .31)
   - 10.0.0.32/27 (Hosts: .33 to .62, BC: .63)
   - 10.0.0.64/27 (Hosts: .65 to .94, BC: .95)
   - 10.0.0.96/27
   - 10.0.0.128/27
   - 10.0.0.160/27
   (And two spare subnets at .192 and .224).

---

## 11. Complete VLSM (Variable Length Subnet Masking)

### What is VLSM? Why is it more efficient?
VLSM allows a network administrator to divide an IP address space into a hierarchy of subnets of varying sizes. Instead of wasting IPs using FLSM, VLSM custom-fits the subnet size to the exact number of hosts required by a department.

### The VLSM Golden Rule
**ALWAYS sort the requirements from largest to smallest before subnetting.**

### SOLVED NUMERICAL 1 (Standard)
**Problem:**
Network: `192.168.1.0/24`
Requirements: Dept A: 60 hosts, Dept B: 30 hosts, Dept C: 14 hosts, Dept D: 6 hosts.

**Solution:**
Requirements are already sorted (60, 30, 14, 6).

**Dept A (Need 60):**
1. Find power of 2: 2^6 = 64. Usable = 62. (Fits 60).
2. Host bits (h) = 6. CIDR = 32 - 6 = **/26**
3. Block size = 64.
4. **Network:** `192.168.1.0/26`
   **Range:** 192.168.1.1 - 192.168.1.62
   **Broadcast:** 192.168.1.63
   *(Next available IP to start Dept B is 192.168.1.64)*

**Dept B (Need 30):**
1. 2^5 = 32. Usable = 30. (Fits exactly 30).
2. Host bits (h) = 5. CIDR = 32 - 5 = **/27**
3. Block size = 32.
4. **Network:** `192.168.1.64/27`
   **Range:** 192.168.1.65 - 192.168.1.94
   **Broadcast:** 192.168.1.95
   *(Next available IP to start Dept C is 192.168.1.96)*

**Dept C (Need 14):**
1. 2^4 = 16. Usable = 14.
2. Host bits (h) = 4. CIDR = 32 - 4 = **/28**
3. Block size = 16.
4. **Network:** `192.168.1.96/28`
   **Range:** 192.168.1.97 - 192.168.1.110
   **Broadcast:** 192.168.1.111
   *(Next available IP is 192.168.1.112)*

**Dept D (Need 6):**
1. 2^3 = 8. Usable = 6.
2. Host bits (h) = 3. CIDR = 32 - 3 = **/29**
3. Block size = 8.
4. **Network:** `192.168.1.112/29`
   **Range:** 192.168.1.113 - 192.168.1.118
   **Broadcast:** 192.168.1.119

*(Waste is minimized! We still have IPs from .120 to .255 for future use).*

### SOLVED NUMERICAL 2 (Advanced)
**Problem:**
Network: `10.0.0.0/8` (Wait, this is a massive network, but we only need a few hosts!). Let's assume we are given `10.1.0.0/16` for our site.
Requirements: 5 departments: 500, 200, 100, 50, 10 hosts.

**Solution:**
**Dept 1 (500 hosts):**
2^9 = 512. h=9. CIDR = 32 - 9 = /23. Mask: 255.255.254.0. Block in 3rd octet = 2.
Net: `10.1.0.0/23`. Range: 10.1.0.1 - 10.1.1.254. BC: 10.1.1.255. (Next IP: 10.1.2.0)

**Dept 2 (200 hosts):**
2^8 = 256. h=8. CIDR = /24. Mask: 255.255.255.0. Block = 1 (in 3rd octet) or 256 in 4th.
Net: `10.1.2.0/24`. Range: 10.1.2.1 - 10.1.2.254. BC: 10.1.2.255. (Next IP: 10.1.3.0)

**Dept 3 (100 hosts):**
2^7 = 128. h=7. CIDR = /25. Block = 128 (4th octet).
Net: `10.1.3.0/25`. Range: 10.1.3.1 - 10.1.3.126. BC: 10.1.3.127. (Next IP: 10.1.3.128)

**Dept 4 (50 hosts):**
2^6 = 64. h=6. CIDR = /26. Block = 64.
Net: `10.1.3.128/26`. Range: 10.1.3.129 - 10.1.3.190. BC: 10.1.3.191. (Next: 10.1.3.192)

**Dept 5 (10 hosts):**
2^4 = 16. h=4. CIDR = /28. Block = 16.
Net: `10.1.3.192/28`. Range: 10.1.3.193 - 10.1.3.206. BC: 10.1.3.207.

### SOLVED NUMERICAL 3 (Interview level)
**Problem:** A router has 4 interfaces. Design VLSM for: 100 hosts, 50 hosts, 25 hosts, 2 hosts (point-to-point link). Starting IP: `192.168.100.0/24`.

**Solution:**
1. **100 hosts**: Need 128 block. CIDR = /25.
   Net: 192.168.100.0/25. Range: .1 - .126. Next: .128
2. **50 hosts**: Need 64 block. CIDR = /26.
   Net: 192.168.100.128/26. Range: .129 - .190. Next: .192
3. **25 hosts**: Need 32 block. CIDR = /27.
   Net: 192.168.100.192/27. Range: .193 - .222. Next: .224
4. **2 hosts (Point-to-Point)**: Need 4 block. CIDR = /30.
   Net: 192.168.100.224/30. Range: .225 - .226. BC: .227.
   *Note: /30 is the standard for P2P router links! (2 usable IPs).*

---

## 12. Subnetting Shortcuts for Interviews

### The Magic Number Method (Block Size)
The "Magic Number" is just `256 - Interesting Subnet Mask Octet`.
Example: Mask is 255.255.255.224. 
Magic number = 256 - 224 = 32.
This means networks count by 32! (0, 32, 64, 96...). Easiest way to find the next subnet.

### Quick CIDR-to-Hosts Table (Memorize this for /24 and above!)
| CIDR | Mask End | Block Size | Usable Hosts |
|------|----------|------------|--------------|
| /24  | .0       | 256        | 254          |
| /25  | .128     | 128        | 126          |
| /26  | .192     | 64         | 62           |
| /27  | .224     | 32         | 30           |
| /28  | .240     | 16         | 14           |
| /29  | .248     | 8          | 6            |
| /30  | .252     | 4          | 2            |
| /31  | .254     | 2          | 0 (Used in P2P sometimes, but rarely tested) |
| /32  | .255     | 1          | 1 (Host Route)|

### How to find which subnet an IP belongs to in 30 seconds
**Question:** Which subnet does `192.168.1.115/27` belong to?
1. /27 -> Block size is 32.
2. Subnets are multiples of 32: 0, 32, 64, 96, 128.
3. 115 falls between 96 and 128.
4. **Answer:** Network is `192.168.1.96`.

### How to verify your answer
1. Network Address must always be an EVEN number.
2. Broadcast Address must always be an ODD number.
3. (Network + 1) = First Host. (Broadcast - 1) = Last Host.

---

## Chapter Summary
- IPv4 is 32 bits, 4 octets.
- Classes: A (1-126), B (128-191), C (192-223), D (224-239), E (240-255).
- Private IPs (RFC1918) are for LANs; translated by NAT to access the internet.
- 127.0.0.1 = Loopback, 169.254.x.x = APIPA, 255.255.255.255 = Broadcast.
- Subnet mask delineates network vs host bits.
- FLSM uses same mask for all subnets; VLSM uses different masks to save IPs.
- Golden rule of VLSM: Sort requirements highest to lowest.

---

## All Formulas in One Place
- **Host Bits (h)** = 32 - CIDR
- **Subnet Bits (n)** = New CIDR - Old CIDR
- **Block Size** = 2^h
- **Usable Hosts** = 2^h - 2
- **Number of Subnets** = 2^n
- **Network Address** = IP AND Subnet Mask
- **Broadcast Address** = Next Network Address - 1

---

## Top 15 Interview Questions for IP & Subnetting

1. **What is the difference between an IP address and a MAC address?**
   *IP is logical and routable (Layer 3). MAC is physical, burned into the NIC, and non-routable (Layer 2).*
2. **What is a subnet mask and why is it necessary?**
   *It determines which part of the IP is the network and which is the host.*
3. **What is default gateway?**
   *The IP address of the router interface that connects your local network to other networks (the internet).*
4. **Why is 127.0.0.1 important?**
   *It is the loopback address used to test the local TCP/IP stack.*
5. **What happens if a device receives an IP of 169.254.x.x?**
   *It means the DHCP request failed (APIPA took over).*
6. **How does NAT work?**
   *It translates many private, non-routable IP addresses into a single (or pool of) public, routable IP addresses to access the internet.*
7. **What is the difference between FLSM and VLSM?**
   *FLSM allocates equal-sized subnets. VLSM allows variable-sized subnets, minimizing IP wastage.*
8. **What is the purpose of CIDR?**
   *To replace classful addressing, allow VLSM, and enable route summarization (supernetting).*
9. **How many usable hosts are in a /28 network?**
   *32 - 28 = 4 host bits. 2^4 = 16. 16 - 2 = 14 usable hosts.*
10. **Can a network address be assigned to a computer?**
    *No, the network address represents the wire itself.*
11. **Can a broadcast address be assigned to a computer?**
    *No, it is used to send traffic to all computers in that subnet.*
12. **Which CIDR notation is used for a point-to-point serial WAN link?**
    */30, because it provides exactly 2 usable IPs.*
13. **You have IP 10.0.0.5/24 and 10.0.1.5/24. Can they ping each other without a router?**
    *No, they have different network IDs (10.0.0.0 vs 10.0.1.0).*
14. **What is a MAC Broadcast address?**
    *FF:FF:FF:FF:FF:FF.*
15. **Convert 192.168.0.1 to binary.**
    *11000000.10101000.00000000.00000001*

---

## 5 Self-Practice Problems

1. **Beginner:** Find the Network, Broadcast, and Host range for `192.168.5.80 /28`.
   *(Hint: Block size is 16. Multiples of 16 are 0, 16, 32, 48, 64, 80...)*
2. **Intermediate:** You are given `172.16.0.0 /22`. How many usable hosts are in this single subnet?
   *(Hint: Host bits = 32 - 22 = 10).*
3. **Advanced:** Subnet `192.168.1.0/24` for 3 departments needing 50, 20, and 12 hosts using VLSM. Provide the Network IPs for all 3.
4. **Expert:** What is the subnet mask, in decimal format, for a /19?
5. **Interview Test:** An employee claims their computer cannot reach the internet. Their IP config shows: IP = 192.168.10.150, Mask = 255.255.255.128, Gateway = 192.168.10.1. Why is it failing?
   *(Hint: Calculate the subnet range for 192.168.10.150/25. Is the gateway in the same subnet?)*

---
*End of Chapter 2. Next up: Chapter 3 - OSI Model & TCP/IP Suite.*
