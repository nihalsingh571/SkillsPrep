# Chapter 1: Linux Fundamentals

## 1.1 What is Linux?
At its core, **Linux** is a family of open-source, Unix-like operating systems based on the Linux kernel, first released by **Linus Torvalds** on September 17, 1991. 

To understand Linux, let's start with a simple real-world analogy:
> **Analogy:** Think of a computer as a busy restaurant. 
> * The **Hardware** (CPU, RAM, Disk) is the kitchen, cooking equipment, and physical tables.
> * The **User Space** (applications you run) is the customers placing orders.
> * The **Kernel** (Linux) is the Head Chef/Manager. It decides which cook uses the oven (scheduling CPU), where ingredients are stored (allocating Memory), and makes sure the customers get their orders safely and efficiently without crashing into each other.

### History of Linux
Before Linux, there was **Unix**, a powerful operating system developed in the late 1960s at AT&T Bell Labs. Unix was proprietary and expensive. In 1983, Richard Stallman started the **GNU Project** with the goal of creating a completely free, Unix-compatible operating system. By the early 1990s, GNU had built almost all the necessary parts (compiler, shell, text editors) except for the core engine: the kernel. 
In 1991, Linus Torvalds, a student at the University of Helsinki, developed a hobby kernel that eventually filled this gap. By combining Torvalds' kernel with GNU's software tools, the **GNU/Linux** operating system was born.

### Why Linux Dominates DevOps
In modern cloud architecture, Linux is the undisputed king. Over **90%** of the world's cloud infrastructure runs on Linux. Here is why:

1. **Open-Source and Zero Licensing Cost:** Unlike Windows Server, which requires expensive licenses per core, Linux is free to use, modify, and distribute. This allows startups and tech giants alike to spin up millions of server instances without licensing bottlenecks.
2. **Lightweight & Efficient:** Linux servers can run without a Graphical User Interface (GUI), operating entirely in command-line mode (CLI). This saves massive amounts of RAM and CPU cycles for application workloads.
3. **Stability & Reliability:** Linux handles high network traffic, multiple users, and system resources exceptionally well. It rarely needs to be rebooted after updates or configuration changes, guaranteeing high availability.
4. **Security:** The Linux permission model is strict by design. Furthermore, because it is open-source, global developers continuously audit it to patch vulnerabilities immediately.

### Linux in Cloud, Containers, and Kubernetes
DevOps technologies are built on top of Linux primitives:
* **Cloud Computing:** Infrastructure-as-a-Service (IaaS) providers (AWS, Google Cloud, Azure) default their virtual machines (like EC2) to Linux distributions because they are highly scriptable and fast to boot.
* **Containers (Docker):** Docker is not a virtualization platform; it runs containers by sharing the host Linux kernel. It utilizes Linux-specific kernel features called **Namespaces** (to isolate what a process sees) and **Cgroups (Control Groups)** (to limit how much resource a process uses).
* **Kubernetes (K8s):** Kubernetes orchestrates containers across a cluster of servers, managing container storage, networking, and CPU/RAM allocation. Since containers are built on Linux features, Kubernetes is natively designed to control Linux infrastructure.

---

## 1.2 Linux Architecture
Linux is structured in layers, separating raw hardware from human users.

```
+-------------------------------------------------------------+
|                         USER SPACE                          |
|  +------------------+  +-------------------+  +----------+  |
|  | Web Browser      |  | Text Editors (vim)|  | Utilities|  |
|  +------------------+  +-------------------+  +----------+  |
|          |                      |                   |       |
+----------v----------------------v-------------------v-------+
|  +-------------------------------------------------------+  |
|  |                         SHELL                         |  |
|  |              (Bash, Zsh, Sh Command Line)             |  |
|  +-------------------------------------------------------+  |
+-----------------------------|-------------------------------+
|                             | System Calls                  |
+-----------------------------v-------------------------------+
|                         KERNEL SPACE                        |
|  +-------------------------------------------------------+  |
|  |                     LINUX KERNEL                      |  |
|  |  [Process Mgr]   [Memory Mgr]   [Filesystem]   [Net]  |  |
|  +-------------------------------------------------------+  |
+-----------------------------|-------------------------------+
|                             | Drivers                       |
+-----------------------------v-------------------------------+
|                       PHYSICAL HARDWARE                     |
|         [CPU]             [RAM]          [SSD/Disk]   [NIC] |
+-------------------------------------------------------------+
```

1. **Hardware:** The physical components of the system (CPU, RAM, Hard Disk/SSD, Network Interface Card).
2. **Kernel:** The core of the operating system. It communicates directly with hardware and manages processes, memory, files, and device drivers.
3. **Shell:** The command-line interface that interprets user commands and sends them to the kernel. Examples include `bash`, `sh`, and `zsh`.
4. **User Space:** The layer where user programs and system daemons run (e.g., Nginx, Python, Docker, systemd, or custom scripts).

---

## 1.3 Linux Distributions (Distros)
A **Linux Distribution** is an operating system made from a Linux kernel, GNU tools, additional software packages, a package manager, and configuration files.

| Distribution | Derived From | Package Manager | Default Target | DevOps Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Debian** | Independent | `apt` (dpkg) | Servers / Desktop | Ultra-stable base for minimal Docker images. |
| **Ubuntu** | Debian | `apt` (dpkg) | Server, Desktop, IoT | Most popular distro for local testing and cloud instances. |
| **CentOS** | Red Hat (RHEL) | `yum` / `dnf` | Server (Historical) | Traditional enterprise server (being replaced by Rocky/Alma Linux). |
| **RHEL** | Enterprise | `yum` / `dnf` | Enterprise Server | Highly secure, paid support environment for enterprise apps. |
| **Fedora** | Red Hat | `dnf` | Desktop / Dev | Cutting-edge features; testing ground for future RHEL code. |
| **Amazon Linux**| RHEL/Fedora | `yum` / `dnf` | AWS EC2 Cloud | Tuned for maximum performance and security on AWS. |

---

## 1.4 Linux File System Hierarchy
In Linux, **everything is a file**. Directories are simply files containing lists of other files. The filesystem follows a tree-like structure starting from the root directory `/`.

```
/ (Root)
├── bin -> usr/bin (User Binaries)
├── boot (Static Boot Loader Files)
├── dev (Device Files)
├── etc (System Configuration)
├── home (User Home Directories)
├── lib (Shared Libraries)
├── media (Mount point for removable media)
├── opt (Optional/Add-on Applications)
├── proc (Kernel & Process Info virtual files)
├── root (Superuser Home Directory)
├── run (Runtime volatile data)
├── sbin -> usr/sbin (System Binaries)
├── srv (Service Data)
├── sys (Kernel Device & Subsystem files)
├── tmp (Temporary Files)
├── usr (User Programs & Shareable data)
└── var (Variable data, Logs, Mail spools)
```

### File System Details & DevOps Use Cases

* **`/` (Root):** The top-level directory of the filesystem. All directories branch off here.
* **`/bin`:** Contains essential command binaries needed for system booting and single-user mode (e.g., `ls`, `cp`, `pwd`).
* **`/boot`:** Contains files required to boot the system, including the Linux kernel (`vmlinuz`) and bootloader files (GRUB).
* **`/dev`:** Contains device nodes representing hardware. For example, `/dev/sda` represents the first hard drive, and `/dev/urandom` provides random numbers.
* **`/etc`:** The config capital. Contains system-wide configuration files (e.g., network settings `/etc/netplan/`, user credentials `/etc/passwd`, database configs). *DevOps Use Case:* You will spend 40% of your time editing files here.
* **`/home`:** Users' personal directories. For user `john`, his home is `/home/john`.
* **`/lib`:** System libraries required by binaries in `/bin` and `/sbin`.
* **`/media` & `/mnt`:** Mount points for temporary external media (like USB drives) or permanent external file systems (like NFS shares).
* **`/opt`:** Standard directory for manual software installations that don't come from package managers (e.g., `/opt/jenkins`).
* **`/proc`:** A virtual filesystem mapping kernel and process states. For example, `/proc/cpuinfo` displays CPU specifications.
* **`/root`:** The home directory of the system administrator (`root`).
* **`/run`:** Temporary runtime data since the last boot (e.g., PID files for active processes).
* **`/sbin`:** System administrator binaries. Commands that change system configurations (e.g., `fdisk`, `iptables`, `ip`).
* **`/sys`:** A virtual filesystem similar to `/proc` that exposes devices and drivers to user space.
* **`/tmp`:** Temporary files. Any user can read/write here. Files here are usually wiped on reboot.
* **`/usr`:** User applications and read-only data. Contains its own `/usr/bin`, `/usr/sbin`, `/usr/lib`.
* **`/var`:** Variable data. Includes log files (`/var/log`), mail systems, spool files, and printer queues. *DevOps Use Case:* `/var/log` is critical for application debugging.

---

## 1.5 Linux Commands Mastery
Here is a comprehensive breakdown of the 23 commands you must master.

### 1. `pwd` (Print Working Directory)
* **Definition:** Prints the absolute path of the directory you are currently in.
* **Syntax:** `pwd [options]`
* **Options:** `-P` (Avoids symbolic links and prints physical directory path).
* **Example:**
  ```bash
  pwd
  ```
* **Expected Output:**
  ```text
  /home/ubuntu/app
  ```
* **Real DevOps Use Case:** Crucial in deployment scripts to determine the active script directory and verify relative paths.

### 2. `ls` (List)
* **Definition:** Lists files and directories in the target path.
* **Syntax:** `ls [options] [path]`
* **Options:**
  * `-l` (Long listing format: permissions, size, owner, timestamps).
  * `-a` (Show hidden files starting with `.`).
  * `-h` (Human-readable file sizes, e.g., 2K, 5M).
* **Example:**
  ```bash
  ls -lah /var/log
  ```
* **Expected Output:**
  ```text
  drwxr-xr-x  12 root root 4.0K Jun  1 08:30 .
  drwxr-xr-x  20 root root 4.0K May 15 12:00 ..
  -rw-r--r--   1 root root 1.2M Jun  1 08:45 syslog
  -rw-r-----   1 root adm  452K Jun  1 08:12 auth.log
  ```
* **Real DevOps Use Case:** Inspecting directory contents to check if application config files or logs are present.

### 3. `cd` (Change Directory)
* **Definition:** Changes the current shell directory.
* **Syntax:** `cd [directory]`
* **Common Targets:**
  * `cd ~` or `cd` (Navigate to home directory).
  * `cd ..` (Move up one directory level).
  * `cd -` (Toggle back to the previous directory).
* **Example:**
  ```bash
  cd /var/log && pwd
  ```
* **Expected Output:**
  ```text
  /var/log
  ```
* **Real DevOps Use Case:** Navigating system folders during interactive troubleshooting sessions.

### 4. `mkdir` (Make Directory)
* **Definition:** Creates one or more directories.
* **Syntax:** `mkdir [options] <directory_name>`
* **Options:** `-p` (Parent flag: creates nested directories and doesn't fail if the directory exists).
* **Example:**
  ```bash
  mkdir -p /tmp/production/v1/app
  ```
* **Expected Output:** No output (creates `/tmp/production/`, `/tmp/production/v1/`, and `/tmp/production/v1/app` recursively).
* **Real DevOps Use Case:** Creating structured storage mounts and artifact storage folders in CI/CD pipeline runs.

### 5. `rmdir` (Remove Directory)
* **Definition:** Removes **empty** directories.
* **Syntax:** `rmdir [options] <directory_name>`
* **Example:**
  ```bash
  rmdir /tmp/production/v1/app
  ```
* **Expected Output:** No output if successful; error output if directory contains files.
* **Real DevOps Use Case:** Safely removing empty temporary folder structures.

### 6. `touch` (Create/Update File)
* **Definition:** Creates an empty file if it doesn't exist; updates the file's modification timestamp if it does.
* **Syntax:** `touch <filename>`
* **Example:**
  ```bash
  touch /tmp/health_check.txt
  ```
* **Expected Output:** No output.
* **Real DevOps Use Case:** Creating a mock file or flag file (e.g., `.maintenance_mode`) to signal configuration states.

### 7. `cp` (Copy)
* **Definition:** Copies files or directories from source to destination.
* **Syntax:** `cp [options] <source> <destination>`
* **Options:**
  * `-r` (Recursive copy for directories).
  * `-p` (Preserves file attributes like owner, group, and timestamp).
  * `-v` (Verbose mode: prints details of files being copied).
* **Example:**
  ```bash
  cp -rp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
  ```
* **Expected Output:** No output (silently copies).
* **Real DevOps Use Case:** Backing up configuration files before making edits.

### 8. `mv` (Move/Rename)
* **Definition:** Moves or renames files or directories.
* **Syntax:** `mv <source> <destination>`
* **Example:**
  ```bash
  mv /tmp/health_check.txt /tmp/ready.txt
  ```
* **Expected Output:** No output.
* **Real DevOps Use Case:** Renaming application logs during rotation or staging deployment builds.

### 9. `rm` (Remove)
* **Definition:** Deletes files or directories.
* **Syntax:** `rm [options] <target>`
* **Options:**
  * `-f` (Force: ignore non-existent files and never prompt).
  * `-r` (Recursive: delete directories and their contents).
* **Example:**
  ```bash
  rm -rf /tmp/production
  ```
* **Expected Output:** No output.
* **Real DevOps Use Case:** Cleaning up old builds or build artifacts in a CI/CD build stage.
* **Warning:** `rm -rf /` is dangerous and will destroy the entire OS. Never run this with root permissions.

### 10. `cat` (Concatenate)
* **Definition:** Reads and prints the content of files to the terminal.
* **Syntax:** `cat [options] [file]`
* **Options:** `-n` (Prepend line numbers to output).
* **Example:**
  ```bash
  cat -n /etc/hostname
  ```
* **Expected Output:**
  ```text
       1  web-prod-srv-01
  ```
* **Real DevOps Use Case:** Inspecting small static configurations like SSH public keys or environment variables.

### 11. `less` (Paginate)
* **Definition:** Opens files in a scrollable, read-only interface. Does not load the entire file into memory (highly efficient for large files).
* **Syntax:** `less <filename>`
* **Navigation:** `Space` (page down), `b` (page up), `/pattern` (search), `q` (quit).
* **Example:**
  ```bash
  less /var/log/syslog
  ```
* **Expected Output:** An interactive screen presenting system log lines.
* **Real DevOps Use Case:** Browsing through large server log files without overloading system memory.

### 12. `more` (Paginate Basic)
* **Definition:** Primitive version of `less`. Scrollable downwards only.
* **Syntax:** `more <filename>`
* **Real DevOps Use Case:** Largely superseded by `less`, but sometimes default on minimal containers.

### 13. `head` (View Beginning)
* **Definition:** Output the first N lines of a file.
* **Syntax:** `head [options] <filename>`
* **Options:** `-n <number>` (Specify number of lines; default is 10).
* **Example:**
  ```bash
  head -n 5 /etc/passwd
  ```
* **Expected Output:**
  ```text
  root:x:0:0:root:/root:/bin/bash
  daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
  bin:x:2:2:bin:/bin:/usr/sbin/nologin
  sys:x:3:3:sys:/dev:/usr/sbin/nologin
  sync:x:4:65534:sync:/bin:/bin/sync
  ```
* **Real DevOps Use Case:** Checking file headers or the beginning of CSV databases.

### 14. `tail` (View End)
* **Definition:** Output the last N lines of a file.
* **Syntax:** `tail [options] <filename>`
* **Options:**
  * `-n <number>` (Specify number of lines; default is 10).
  * `-f` (Follow mode: keeps the file open and appends new incoming lines in real-time).
* **Example:**
  ```bash
  tail -f -n 3 /var/log/auth.log
  ```
* **Expected Output:**
  ```text
  Jun  1 08:45:01 web-prod sshd[12345]: Accepted publickey for ubuntu from 192.168.1.100
  Jun  1 08:45:02 web-prod systemd-logind[452]: New session 12 of user ubuntu.
  Jun  1 08:46:12 web-prod sshd[12360]: Connection closed by authenticating user root
  ```
* **Real DevOps Use Case:** Monitoring real-time system logs during application debugging.

### 15. `echo` (Print Text)
* **Definition:** Displays a line of text or variable value.
* **Syntax:** `echo [options] [string]`
* **Options:** `-e` (Enable interpretation of backslash escapes like `\n` or `\t`).
* **Example:**
  ```bash
  echo -e "DB_HOST=12.0.0.1\nDB_PORT=3306" >> /tmp/db.env
  ```
* **Expected Output:** Appends two lines containing environment parameters to `/tmp/db.env`.
* **Real DevOps Use Case:** Writing environment configs and values to files inside containers or deployment scripts.

### 16. `find` (Search files)
* **Definition:** Searches the directory tree for files matching criteria.
* **Syntax:** `find <path> [expression]`
* **Common Flags:**
  * `-name <pattern>` (Search by file name).
  * `-type <f/d>` (f for file, d for directory).
  * `-mtime -<days>` (Modified less than N days ago).
  * `-exec <cmd> {} \;` (Execute a command on found files).
* **Example:**
  ```bash
  find /var/log -type f -name "*.log" -mtime -7
  ```
* **Expected Output:**
  ```text
  /var/log/nginx/access.log
  /var/log/nginx/error.log
  /var/log/syslog
  ```
* **Real DevOps Use Case:** Finding files modified recently or batch-deleting logs older than 30 days (`-exec rm {} \;`).

### 17. `locate` (Search via database)
* **Definition:** Finds files quickly using a pre-indexed database (`mlocate`). Much faster than `find` but requires database update.
* **Syntax:** `locate <filename>`
* **Real DevOps Use Case:** Fast searches on persistent servers. Note: Run `sudo updatedb` to refresh the file system index.

### 18. `which` (Locate command binary)
* **Definition:** Returns the path of the executable file that would run in the current shell.
* **Syntax:** `which <command>`
* **Example:**
  ```bash
  which python3
  ```
* **Expected Output:**
  ```text
  /usr/bin/python3
  ```
* **Real DevOps Use Case:** Confirming if dependency binaries are installed and accessible in the system path.

### 19. `whereis` (Locate binary, source, and manual files)
* **Definition:** Locates the binary, source, and manual page files for a command.
* **Syntax:** `whereis <command>`
* **Example:**
  ```bash
  whereis nginx
  ```
* **Expected Output:**
  ```text
  nginx: /usr/sbin/nginx /etc/nginx /usr/share/nginx /usr/share/man/man8/nginx.8.gz
  ```
* **Real DevOps Use Case:** Troubleshooting package installations and checking config paths.

### 20. `history` (Command history)
* **Definition:** Lists commands entered in the current shell history.
* **Syntax:** `history [number]`
* **Example:**
  ```bash
  history 4
  ```
* **Expected Output:**
  ```text
   2001  cd /var/log
   2002  tail -f syslog
   2003  which nginx
   2004  history 4
  ```
* **Real DevOps Use Case:** Auditing previous interactive troubleshooting commands or repeating a complex terminal pipe command.

### 21. `clear` (Clear screen)
* **Definition:** Wipes all text from the terminal view window.
* **Syntax:** `clear`
* **Real DevOps Use Case:** Clearing cluttered console logs during terminal operations.

### 22. `man` (Manual page)
* **Definition:** Displays reference manuals for commands and utilities.
* **Syntax:** `man <command>`
* **Example:**
  ```bash
  man find
  ```
* **Expected Output:** Opens scrollable help instructions for the `find` command.
* **Real DevOps Use Case:** Checking command parameters and options without internet access.

---

## 1.6 Command Reference Table

| Command | Primary Option | Syntax | Purpose |
| :--- | :--- | :--- | :--- |
| `pwd` | None | `pwd` | Print current directory path. |
| `ls` | `-lah` | `ls -lah [path]` | Detailed long list including hidden files. |
| `cd` | `-` | `cd [dir]` | Switch directory. |
| `mkdir` | `-p` | `mkdir -p [dir]` | Create nested directory structure. |
| `rmdir` | None | `rmdir [dir]` | Remove empty directory. |
| `touch` | None | `touch [file]` | Create empty file or update timestamp. |
| `cp` | `-rp` | `cp -rp [src] [dest]` | Copy recursively, preserving permissions. |
| `mv` | None | `mv [src] [dest]` | Move or rename file/directory. |
| `rm` | `-rf` | `rm -rf [path]` | Force recursive delete (highly destructive). |
| `cat` | `-n` | `cat -n [file]` | View file with line numbers. |
| `less` | None | `less [file]` | Memory-efficient scrollable file viewer. |
| `more` | None | `more [file]` | Scroll down only file viewer. |
| `head` | `-n` | `head -n X [file]` | Print first X lines of a file. |
| `tail` | `-f` | `tail -f [file]` | View files live (follow updates). |
| `echo` | `-e` | `echo -e "text"` | Output text, processing escape sequences. |
| `find` | `-type`, `-name` | `find [path] -name "*.ext"` | Search files matching criteria recursively. |
| `locate` | None | `locate [name]` | Quick file lookup using index database. |
| `which` | None | `which [cmd]` | Identify executable binary location. |
| `whereis` | None | `whereis [cmd]` | Find binary, config, and manual pages. |
| `history` | None | `history` | List previous commands run in shell. |
| `clear` | None | `clear` | Clear terminal output screen. |
| `man` | None | `man [cmd]` | Open system manual for a command. |

---

## 1.7 Chapter 1 Summary
* Linux was created in 1991 by Linus Torvalds and GNU. It dominates DevOps due to efficiency, stability, and zero licensing fees.
* Linux architecture contains layers: Hardware -> Kernel -> Shell -> User Space.
* System files are strictly organized inside the Root file system `/` in locations like `/etc` (configs), `/var/log` (logs), and `/bin` (binaries).
* Essential CLI commands allow users to navigate directories (`cd`), create structures (`mkdir -p`), copy configs (`cp -rp`), trace logs (`tail -f`), and locate binaries (`which`/`whereis`).

---

## 1.8 Interview Questions
1. **Q: Why does a DevOps Engineer need to learn Linux?**
   * *A:* DevOps tools (like Docker, Kubernetes, Ansible, and Terraform agents) run natively on Linux servers. Understanding Linux internals (such as namespaces, filesystems, processes, and permissions) is essential to host, deploy, and debug applications.
2. **Q: What is the difference between `less` and `cat`?**
   * *A:* `cat` reads the entire file and prints it to the standard output at once, which can freeze your shell if the file is multiple gigabytes in size. `less` reads files line-by-line on demand, allowing you to scroll through extremely large files without high memory utilization.
3. **Q: How does `find` differ from `locate`?**
   * *A:* `find` actively walks the file system live, checking parameters in real-time (slower, but always up-to-date). `locate` reads a pre-built indexed database (`mlocate.db`) to quickly retrieve paths (fast, but requires `updatedb` to capture new files).

---

## 1.9 Practice Questions
1. How do you print the path of the current directory?
2. Write a command to create nested directories `/opt/app/src/main/` in one run.
3. How do you copy a folder `deploy/` to a backup location `deploy_backup/` while preserving the directory's owner permissions and creation timestamps?
4. How do you list all files in a folder, including hidden files, ordered by modification time?

---

## 1.10 Hands-On Lab
**Objective:** Set up a workspace directory, create mock logs, and practice real-time log monitoring.
1. Spin up a Linux environment (WSL, EC2 instance, or VirtualBox VM).
2. Open your terminal and create a folder `/tmp/lab1` and switch to it.
3. Create an empty file named `app.log`.
4. Run `tail -f app.log` in your terminal.
5. Open a second terminal window or SSH session, navigate to the same folder, and execute:
   ```bash
   echo "INFO: System started successfully" >> app.log
   echo "WARNING: Connection speed slow" >> app.log
   ```
6. Watch the first terminal screen output change immediately.
7. Use the `history` command to review the steps you took, and clean up the `/tmp/lab1` folder.
