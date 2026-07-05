# Chapter 4: SSH (Secure Shell)

## 4.1 What is SSH?
**SSH (Secure Shell)** is a cryptographic network protocol used for secure execution of command-line operations, file transfers, and remote administration over an unsecured network.

Let's use a real-world analogy:
> **Analogy:** Imagine sending letters containing secret project plans. 
> * **Unencrypted connection (HTTP/Telnet):** Writing the plans on the back of a postcard. Anyone at the post office (routers, ISPs) can read it as it travels.
> * **SSH Connection:** Locking the plans inside a titanium safe, sending it, and opening it with a secret key known only to you and the recipient. Even if someone steals the safe in transit, they cannot see what's inside.

### Why SSH is Crucial in DevOps
In DevOps, automation is remote-first:
1. **Server Management:** Operating virtual machines in the cloud (AWS EC2, GCP Compute Engine) is done entirely via SSH terminal connections.
2. **Configuration Management:** Tools like **Ansible** use agentless SSH connections to push configuration files and execute setup steps across hundreds of target servers.
3. **CI/CD Pipelines:** Jenkins, GitHub Actions, or GitLab CI/CD runners connect to target servers using SSH keys to deploy built software containers and code artifacts.

---

## 4.2 SSH Architecture
SSH follows a standard **Client-Server** architecture. The client starts the connection, and the server listens for incoming connections.

```
       [SSH CLIENT]                                       [SSH SERVER]
   (e.g., Local Laptop)                                (e.g., Remote VM)
    ┌────────────────┐                                ┌────────────────┐
    │  Executes:     │                                │  Runs Daemon:  │
    │  ssh user@host │                                │  sshd (Port 22)│
    └───────┬────────┘                                └────────┬───────┘
            │                                                  │
            │ 1. Establish TCP Connection (Port 22)            │
            ├─────────────────────────────────────────────────>│
            │                                                  │
            │ 2. Key Exchange (Agree on Session Encryption)    │
            │<================================================>│
            │                                                  │
            │ 3. Client Authenticates (Password or Key)        │
            ├─────────────────────────────────────────────────>│
            │                                                  │
            │ 4. Establish Secure Encrypted Shell Session      │
            │<────────────────────────────────────────────────>│
```

---

## 4.3 SSH Authentication Methods

### Method 1: Password Authentication
The client inputs a username and password, which travels encrypted inside the SSH session to the server. 
* **The Risk:** Vulnerable to brute-force attacks. Attackers run automated scripts trying millions of password combinations against public IPs.

### Method 2: Key-Based Authentication (Recommended)
Uses asymmetric cryptography with a key pair consisting of a **Public Key** and a **Private Key**:
* **Private Key (`id_rsa` / `id_ed25519`):** Stored securely on the client machine. **Never share this key.**
* **Public Key (`id_rsa.pub` / `id_ed25519.pub`):** Placed on the remote server inside the user's `~/.ssh/authorized_keys` file.

#### The Key Handshake
1. The client sends a connection request showing its public key ID.
2. The server encrypts a random challenge string using that public key and sends it to the client.
3. Only the client holding the corresponding private key can decrypt the challenge.
4. The client decrypts the challenge, combines it with the session ID, hashes it, and sends it back.
5. The server computes the same hash. If they match, access is granted. The private key never travels across the network.

---

## 4.4 SSH Commands Mastery

### 1. `ssh` (Secure Shell Connect)
* **Definition:** Establishes a remote terminal connection.
* **Syntax:** `ssh [options] <username>@<hostname_or_ip>`
* **Options:**
  * `-i <key_file>` (Specify private key file identity path).
  * `-p <port>` (Specify remote SSH port; default is 22).
* **Example:**
  ```bash
  ssh -i ~/.ssh/my_aws_key.pem ubuntu@54.210.12.5
  ```

---

### 2. `ssh-keygen` (Generate Key Pair)
* **Definition:** Generates a new cryptographic key pair.
* **Syntax:** `ssh-keygen -t <algorithm> -b <bits> -C "<comment>"`
* **Recommended Algorithm:** `ed25519` (more secure and faster than RSA).
* **Example:**
  ```bash
  ssh-keygen -t ed25519 -C "admin@production-server"
  ```
* **Expected Output:**
  ```text
  Generating public/private ed25519 key pair.
  Enter file in which to save the key (/home/ubuntu/.ssh/id_ed25519): 
  Enter passphrase (empty for no passphrase): 
  Enter same passphrase again: 
  Your identification has been saved in /home/ubuntu/.ssh/id_ed25519
  Your public key has been saved in /home/ubuntu/.ssh/id_ed25519.pub
  ```

---

### 3. `ssh-copy-id` (Install Public Key)
* **Definition:** Automates copying your local public key to the remote server's `authorized_keys` file.
* **Syntax:** `ssh-copy-id -i <public_key_file> <user>@<host>`
* **Example:**
  ```bash
  ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@192.168.1.50
  ```
* **Expected Output:**
  ```text
  /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
  /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
  Number of key(s) added: 1
  ```

---

### 4. `scp` (Secure Copy Protocol)
* **Definition:** Copies files between local and remote hosts over SSH.
* **Syntax:** `scp [options] <source> <destination>`
* **Options:** `-r` (Recursive copy for folders), `-P` (Custom port).
* **Examples:**
  * **Local to Remote:**
    ```bash
    scp -i ~/.ssh/key.pem app.tar.gz ubuntu@192.168.1.50:/var/www/
    ```
  * **Remote to Local:**
    ```bash
    scp -i ~/.ssh/key.pem ubuntu@192.168.1.50:/var/log/nginx/error.log ./local_logs/
    ```

---

### 5. `sftp` (Secure File Transfer Protocol)
* **Definition:** Interactive shell interface to navigate and transfer files over SSH.
* **Syntax:** `sftp -i <key> <user>@<host>`
* **Navigation Commands:** `get <file>` (Download), `put <file>` (Upload), `ls`, `cd`, `pwd` (Remote filesystem), `lls`, `lcd` (Local filesystem).
* **Example:**
  ```bash
  sftp ubuntu@192.168.1.50
  ```

---

## 4.5 The SSH Configuration File
Instead of remembering complex flags, IP addresses, and key files, configure them inside the client-side file `~/.ssh/config`.

### Configuration Structure
Create/edit `~/.ssh/config` on your local machine:
```text
# Default parameters for all connections
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 3

# Specific server configuration
Host prod-web
  HostName 54.210.12.5
  User ubuntu
  Port 2222
  IdentityFile ~/.ssh/production_key.pem

Host staging-db
  HostName 10.0.1.15
  User postgres
  IdentityFile ~/.ssh/staging_key.pem
  ProxyJump prod-web
```

### Explanation of Directives:
* **Host:** Nickname you use to connect (e.g., `ssh prod-web`).
* **HostName:** The actual target public IP or DNS domain name.
* **IdentityFile:** Path to the private key used for this host.
* **Port:** Target SSH server port (if non-standard).
* **ProxyJump:** Routes connection through a bastion server (`prod-web`) to reach an isolated internal database server (`staging-db`).

---

## 4.6 SSH Hardening (Best Practices)
Protect your production servers by configuration settings inside `/etc/ssh/sshd_config` on the server:

1. **Disable Password Authentication:** Force key-based authorization.
   ```text
   PasswordAuthentication no
   ```
2. **Disable Root Login:** Force users to connect as a standard user first and use `sudo`.
   ```text
   PermitRootLogin no
   ```
3. **Change Default Port:** Move SSH from port 22 to a random high port (e.g., `2222`) to filter out automated scanning scripts.
   ```text
   Port 2222
   ```
4. **Restrict Access by IP:** Use firewalls (Security Groups, `ufw`, or `iptables`) to restrict SSH incoming connections to trusted IP addresses or VPN subnets.

---

## 4.7 Common Security Mistakes
* **❌ Keeping Private Keys Open:** If your key has too broad permissions, SSH client will reject it. Fix with `chmod 600 key.pem`.
* **❌ Committing Keys to GitHub:** Accidentally pushing private key files to git repositories. **The Fix:** Add key files to `.gitignore` and revoke any leaked credentials immediately.
* **❌ Using weak keys:** Generating low-bit keys. Avoid RSA keys under 2048 bits; prefer Ed25519 keys.

---

## 4.8 Interview Questions
1. **Q: How does `ProxyJump` work in SSH?**
   * *A:* It allows an SSH connection to a private database server in an isolated subnet by routing traffic through an intermediary public-facing host (called a Bastion or Jump host). The client establishes an encrypted session with the Jump host, which forwards the traffic to the destination server.
2. **Q: Why does SSH fail with "Host key verification failed"?**
   * *A:* This warning occurs when the remote host's identification key does not match the key stored in the client's `~/.ssh/known_hosts` file. This can indicate a Man-in-the-Middle attack or a simple rebuild/reinstallation of the remote server.
3. **Q: How do you fix a "Permissions are too open" error for a private key?**
   * *A:* Run `chmod 600 <keyfile>` to ensure only the owner can read and write to the file.

---

## 4.9 Hands-On Lab
**Objective:** Generate an SSH keypair, set up a local user ssh configuration, and simulate key authorization.

1. Open your terminal and create a directory `/tmp/ssh_lab/`:
   ```bash
   mkdir -p /tmp/ssh_lab/
   cd /tmp/ssh_lab/
   ```
2. Generate an Ed25519 keypair without a passphrase (for automation testing):
   ```bash
   ssh-keygen -t ed25519 -f ./lab_key -N ""
   ```
3. Inspect the files created:
   ```bash
   ls -la
   ```
   *Expected Output:*
   ```text
   -rw------- 1 ubuntu ubuntu 411 Jun  1 09:10 lab_key
   -rw-r--r-- 1 ubuntu ubuntu  98 Jun  1 09:10 lab_key.pub
   ```
4. Emulate setting up authorization on a remote target:
   Create a mock `authorized_keys` file containing your public key contents:
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   cat ./lab_key.pub >> ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   ```
5. Test key authentication locally by connecting to your own local loopback address:
   ```bash
   ssh -i ./lab_key ubuntu@127.0.0.1
   ```
6. Clean up the generated keys from `/tmp/ssh_lab/` and `~/.ssh/authorized_keys`.
