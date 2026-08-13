# IT Infrastructure & System Administrator Interview Preparation Guide
**Role:** System Engineer (Fresher / 0-1 year experience)
**Candidate Profile:** CSE graduate with knowledge in Linux, Docker, Kubernetes, AWS, Terraform, Jenkins, GitHub Actions, Networking, Java, Web Development.

---

## MODULE 1: LINUX FUNDAMENTALS

### LEVEL 1 – WHAT IS?

**Question:** 1. What is Linux? What is an operating system?
**Short Answer (30-45 sec):** Linux is a free, open-source operating system kernel created by Linus Torvalds. An operating system is the system software that manages computer hardware, software resources, and provides common services for computer programs. In simple terms, it's the bridge between the user/applications and the physical hardware.
**Detailed Explanation:** An OS acts as a resource manager (CPU, memory, disk). The Linux kernel is the core of the OS that handles this. Distributions (like Ubuntu, RHEL, CentOS) package the kernel with system utilities, desktop environments, and package managers to make it usable. Unlike Windows, Linux is heavily file-oriented and heavily relies on the CLI (Command Line Interface).
**Practical Example:** When you run a Java application, the OS allocates RAM and CPU time to that Java process and ensures it doesn't crash other running applications.
**Commands/Tools:** `uname -a` (shows kernel info), `cat /etc/os-release` (shows OS distribution details).
**Common Mistake:** Freshers often confuse "Linux" (the kernel) with "Ubuntu" or "CentOS" (the distribution).
**Strong Interview Line:** "Linux is an open-source kernel that, when combined with GNU utilities, forms a highly stable and secure operating system that powers the vast majority of enterprise servers and cloud infrastructure today."
**Follow-ups:** 
- Q: What distribution are you most comfortable with? A: Ubuntu/CentOS.
- Q: Why is Linux preferred over Windows for servers? A: Stability, security, lower resource overhead, and it's free.

**Question:** 2. What is a process in Linux?
**Short Answer (30-45 sec):** A process is simply a program in execution. When you run a command or start an application, the OS creates a process, assigns it a unique Process ID (PID), and allocates memory and CPU time to it.
**Detailed Explanation:** Every time an executable is loaded into memory, it becomes a process. Processes have states (Running, Sleeping, Stopped, Zombie). The kernel scheduler decides which process gets CPU time. There are user processes (started by users) and daemon processes (background services).
**Practical Example:** When you start a Jenkins server, Java creates a process. If Jenkins stops responding, you would find its PID and troubleshoot or kill the process.
**Commands/Tools:** `ps aux`, `top`, `htop`, `kill <PID>`.
**Common Mistake:** Thinking a program on disk is a process. It's only a process when executed.
**Strong Interview Line:** "In Linux, everything is either a file or a process, making process management a fundamental skill for maintaining server health and application uptime."
**Follow-ups:** 
- Q: What is a zombie process? A: A process that has completed execution but still has an entry in the process table because its parent hasn't read its exit status.
- Q: How do you kill a process? A: Using `kill -9 <PID>` for a forceful termination.

**Question:** 3. What is a file system? What file systems does Linux support?
**Short Answer (30-45 sec):** A file system is the method and data structure the OS uses to control how data is stored, organized, and retrieved on a disk. Without it, data on a drive would just be one large chunk. Linux primarily supports ext4, XFS, and Btrfs.
**Detailed Explanation:** The file system manages metadata (permissions, creation dates, owners) and the actual data blocks. ext4 (Fourth Extended Filesystem) is the standard for Debian/Ubuntu, offering journaling (keeping track of uncommitted changes to prevent corruption). XFS is common in RHEL/CentOS for large scale data.
**Practical Example:** Formatting a new AWS EBS volume attached to an EC2 instance before you can store Docker volumes on it.
**Commands/Tools:** `df -T` (view file system types), `mkfs.ext4` (format), `mount` (attach).
**Common Mistake:** Forgetting that before mounting a disk, it must be formatted with a file system.
**Strong Interview Line:** "Understanding file systems like ext4 and XFS is crucial for ensuring data integrity and optimizing storage performance for databases or container volumes."
**Follow-ups:** 
- Q: What is journaling? A: Keeping a log of changes before they are committed to disk to recover from crashes.
- Q: How do you mount a filesystem? A: Using the `mount /dev/sda1 /mnt` command.

**Question:** 4. What is the Linux directory structure? Explain /etc, /var, /home, /bin, /usr, /tmp, /proc, /sys
**Short Answer (30-45 sec):** Linux uses a single hierarchical directory structure starting from the root directory (`/`). Everything branches from here. `/etc` is for configs, `/var` for variable data like logs, `/home` for user files, `/bin` for essential binaries, `/tmp` for temporary files, and `/proc` is a virtual filesystem for process and kernel info.
**Detailed Explanation:** 
- `/etc`: System-wide configuration files (e.g., `/etc/passwd`, `/etc/ssh/sshd_config`).
- `/var`: Variable data that grows over time, like logs (`/var/log`) and databases.
- `/home`: Personal directories for regular users.
- `/bin`: Essential user command binaries (like `ls`, `cat`).
- `/usr`: Secondary hierarchy for read-only user data and programs.
- `/tmp`: Temporary files cleared on reboot.
- `/proc`: Virtual filesystem providing a window into the running kernel and processes (e.g., `/proc/cpuinfo`).
- `/sys`: Virtual filesystem for interacting with hardware devices.
**Practical Example:** If an Nginx server isn't starting, you check `/var/log/nginx/error.log` for logs, and `/etc/nginx/nginx.conf` to fix the configuration.
**Commands/Tools:** `ls /`, `cd /var/log`, `tree -L 1 /`
**Common Mistake:** Confusing `/bin` (essential system binaries) with `/usr/bin` (user installed applications).
**Strong Interview Line:** "Navigating the Filesystem Hierarchy Standard natively allows me to quickly locate configuration files and logs during critical incident troubleshooting."
**Follow-ups:** 
- Q: Where do you find application logs? A: Typically in `/var/log`.
- Q: Is `/proc` a real folder on the hard drive? A: No, it's an in-memory virtual filesystem.

**Question:** 5. What is a shell? What is bash?
**Short Answer (30-45 sec):** A shell is a program that acts as the command-line interface between the user and the Linux kernel. It takes commands, interprets them, and executes them. BASH (Bourne Again SHell) is the most common and default shell on most Linux distributions.
**Detailed Explanation:** When you open a terminal, you are interacting with the shell. The shell parses your text, expands wildcards (like `*`), sets up input/output redirection (like `>`), and passes the command to the kernel. Bash scripting allows combining commands to automate administrative tasks. Other shells include Zsh, sh, and csh.
**Practical Example:** Writing a bash script to automate the backup of a database every midnight.
**Commands/Tools:** `echo $SHELL` (shows current shell), `bash` (starts bash).
**Common Mistake:** Confusing the terminal emulator (like PuTTY or GNOME Terminal) with the shell itself. The terminal displays the text; the shell interprets the commands.
**Strong Interview Line:** "Mastering Bash is essential for a SysAdmin or DevOps engineer, as it transforms repetitive manual tasks into automated, reliable scripts."
**Follow-ups:** 
- Q: What does `#!/bin/bash` mean at the top of a script? A: It's the shebang, telling the system which interpreter to use to execute the script.
- Q: Can you change your default shell? A: Yes, using the `chsh` command.

**Question:** 6. What is root user? What is sudo?
**Short Answer (30-45 sec):** The root user is the superuser in Linux with absolute administrative privileges, capable of doing anything on the system. `sudo` (SuperUser DO) is a command that allows authorized regular users to run specific commands with root privileges temporarily.
**Detailed Explanation:** Logging in directly as root is dangerous because a simple typo (like `rm -rf /`) can destroy the system. `sudo` mitigates this by logging all privileged commands (accountability) and requiring the user's own password, granting temporary elevated rights without sharing the actual root password.
**Practical Example:** Installing a package requires root. Instead of logging in as root, you run `sudo apt install nginx`.
**Commands/Tools:** `sudo su -` (switch to root), `visudo` (edit sudoers file safely).
**Common Mistake:** Using root directly for daily tasks or giving users root passwords instead of setting them up in the sudoers file.
**Strong Interview Line:** "Implementing the principle of least privilege using `sudo` rather than direct root access is the foundation of secure Linux server administration."
**Follow-ups:** 
- Q: Where are sudo permissions configured? A: In the `/etc/sudoers` file.
- Q: Why use `visudo` instead of editing `/etc/sudoers` directly? A: `visudo` checks for syntax errors before saving, preventing you from breaking `sudo` access.

**Question:** 7. What are Linux file permissions? What does rwxr-xr-- mean?
**Short Answer (30-45 sec):** Linux file permissions control who can Read (r), Write (w), or eXecute (x) a file. The permissions are grouped into three sets: User (owner), Group, and Others. `rwxr-xr--` means the Owner has full rights (rwx), the Group can read and execute (r-x), and Others can only read (r--).
**Detailed Explanation:** In Linux, permissions are essential for security. 
- Read (r) = 4
- Write (w) = 2
- Execute (x) = 1
So `rwxr-xr--` translates to 754 in octal format (7 = 4+2+1, 5 = 4+1, 4 = 4).
**Practical Example:** When you create a bash script, you must run `chmod +x script.sh` (or `chmod 755 script.sh`) to make it executable.
**Commands/Tools:** `ls -l` (view permissions), `chmod` (change permissions), `chown` (change owner).
**Common Mistake:** Setting files to `777` (rwxrwxrwx) to fix "Permission Denied" errors, which is a massive security risk.
**Strong Interview Line:** "Properly managing file permissions is my first line of defense in preventing unauthorized access to critical configuration and secret files on a server."
**Follow-ups:** 
- Q: What does `chmod 644` do? A: Sets read/write for owner, read-only for group and others. Common for text files.
- Q: How do you change the owner of a file? A: `chown user:group filename`

**Question:** 8. What is a Linux service/daemon?
**Short Answer (30-45 sec):** A service or daemon is a background process that runs continuously, waiting to handle requests or perform system tasks without user interaction. Daemons usually have names ending in 'd', like `sshd` or `httpd`.
**Detailed Explanation:** Unlike interactive commands you run in the shell, daemons start up during boot and keep running. They handle network requests (web servers, SSH), hardware (printing), or scheduling (cron). In modern Linux, they are managed by `systemd`.
**Practical Example:** The SSH daemon (`sshd`) runs in the background listening on port 22 so you can connect to the server remotely at any time.
**Commands/Tools:** `systemctl status sshd`, `systemctl restart nginx`.
**Common Mistake:** Confusing a foreground process (like running a python script manually) with a properly managed daemon.
**Strong Interview Line:** "Managing daemons effectively ensures that critical services like web servers and databases restart automatically upon server reboots, ensuring high availability."
**Follow-ups:** 
- Q: How do you make a service start on boot? A: `systemctl enable <servicename>`.
- Q: How do you view logs for a service? A: `journalctl -u <servicename>`.

**Question:** 9. What is a package manager? What is apt vs yum?
**Short Answer (30-45 sec):** A package manager is a tool that automates installing, upgrading, configuring, and removing software packages in Linux. It handles dependencies automatically. `apt` is used by Debian/Ubuntu-based systems, while `yum` (or `dnf`) is used by RedHat/CentOS-based systems.
**Detailed Explanation:** Before package managers, you had to compile software from source and manually find all required libraries (dependency hell). Package managers connect to remote repositories, download pre-compiled packages (.deb for apt, .rpm for yum), and install prerequisites automatically.
**Practical Example:** When setting up a new server for deployment, using `sudo apt install docker.io` pulls Docker and all its dependencies securely.
**Commands/Tools:** `apt update && apt upgrade`, `yum install httpd`.
**Common Mistake:** Running `apt install` without first running `apt update` to refresh the local package index.
**Strong Interview Line:** "Leveraging package managers is fundamental for reproducible server setups and keeping infrastructure secure with the latest security patches."
**Follow-ups:** 
- Q: What does `apt update` do? A: It fetches the latest list of available packages from repositories, but doesn't install them.
- Q: What is the RPM equivalent for local installation in Debian? A: `dpkg -i package.deb`.

**Question:** 10. What is a cron job?
**Short Answer (30-45 sec):** A cron job is a scheduled task in Linux executed by the `cron` daemon at specified intervals (times, dates, or days of the week). It's used for automating repetitive tasks.
**Detailed Explanation:** The scheduling is defined using a crontab (cron table) file. The syntax uses five asterisks `* * * * *` representing Minute, Hour, Day of Month, Month, and Day of Week.
**Practical Example:** Scheduling a daily database backup script to run at 2 AM when server load is low.
**Commands/Tools:** `crontab -e` (edit cron jobs), `crontab -l` (list cron jobs).
**Common Mistake:** Forgetting that cron jobs run in a limited environment and often fail because they lack the necessary PATH variables or absolute paths aren't used.
**Strong Interview Line:** "Cron is the workhorse of system administration for automating backups, log rotations, and health checks, ensuring routine maintenance happens without human intervention."
**Follow-ups:** 
- Q: How do you write a cron expression for every day at midnight? A: `0 0 * * *`.
- Q: Where do you redirect cron job output? A: To a log file or `/dev/null` using `> /path/to/log 2>&1`.

### LEVEL 2 – DIFFERENCE QUESTIONS (Linux)

**Question:** 11. Hard link vs soft link
**Short Answer (30-45 sec):** A hard link is a direct pointer to the underlying data (inode) on the disk, meaning if the original file is deleted, the data remains accessible via the hard link. A soft link (symlink) is like a Windows shortcut; it points to the file name. If the original file is deleted, the soft link breaks (becomes dangling).
**Detailed Explanation:** 
- Hard links cannot cross different file systems and cannot link to directories.
- Soft links can cross file systems and link to directories.
**Practical Example:** You install a new version of Java in `/opt/java-17`. You create a soft link `/usr/bin/java` pointing to it. If you upgrade, you just update the soft link.
**Commands/Tools:** `ln file1 file2` (hard link), `ln -s target linkname` (soft link).
**Common Mistake:** Creating a soft link with a relative path instead of an absolute path, causing it to break when moved.
**Strong Interview Line:** "I use soft links frequently to manage application versions and configuration files, ensuring zero-downtime path updates during deployments."
**Follow-ups:** 
- Q: Can you create a hard link to a directory? A: No, only soft links.

**Question:** 12. Process vs Thread
**Short Answer (30-45 sec):** A process is an independent program in execution with its own memory space. A thread is a smaller unit of execution within a process. Multiple threads within the same process share the same memory and resources.
**Detailed Explanation:** Processes are heavy; context switching between them takes time. If one process crashes, others survive. Threads are lightweight and communicate easily because they share memory, but if one thread crashes due to a memory error, it can crash the whole process.
**Practical Example:** The Nginx web server uses multiple worker processes. A Java application usually runs as a single process with hundreds of internal threads handling different user requests.
**Commands/Tools:** `ps aux` (processes), `ps -T -p <PID>` (threads of a process).
**Common Mistake:** Not realizing that in Linux, threads are often implemented as lightweight processes (LWP).
**Strong Interview Line:** "Understanding the difference helps me tune server performance; deciding whether to allocate more CPU cores to scale out processes or increase heap size for multithreaded apps."

**Question:** 13. foreground vs background process
**Short Answer (30-45 sec):** A foreground process ties up your terminal; you can't run other commands until it finishes. A background process runs independently, returning the prompt to you immediately.
**Detailed Explanation:** You can start a process in the background by appending `&` to the command. You can move a running foreground process to the background by pressing `Ctrl+Z` (suspending it) and typing `bg`. 
**Practical Example:** Running a long `tar` backup command in the background `tar -czf backup.tar.gz /var/www &` so you can continue working in the terminal.
**Commands/Tools:** `&` (start in background), `jobs` (list background jobs), `fg` (bring to foreground), `nohup` (keep running after logout).
**Common Mistake:** Starting a background process and then closing the SSH session without using `nohup` or `tmux/screen`, causing the process to die.
**Strong Interview Line:** "Effective background job management is crucial for running long-running operational scripts without blocking the session or risking termination upon disconnect."

**Question:** 14. /etc/passwd vs /etc/shadow
**Short Answer (30-45 sec):** `/etc/passwd` stores basic user account information (username, UID, GID, home directory, shell) and is readable by all users. `/etc/shadow` securely stores the actual encrypted user passwords and expiration rules, and is only readable by root.
**Detailed Explanation:** Historically, passwords were in `/etc/passwd`. For security, they were moved to `/etc/shadow`. If a hacker reads `/etc/passwd`, they know who exists, but they need `/etc/shadow` to try cracking the passwords.
**Practical Example:** When troubleshooting a user who can't log in, I check `/etc/passwd` to ensure their shell isn't `/sbin/nologin`.
**Commands/Tools:** `cat /etc/passwd`, `sudo cat /etc/shadow`.
**Common Mistake:** Thinking the plain text password is in the shadow file; it's a hash (SHA-512 usually).
**Strong Interview Line:** "Separating user metadata from hashed credentials is a fundamental Linux security design that prevents privilege escalation through password cracking."

**Question:** 15. grep vs find
**Short Answer (30-45 sec):** `find` searches for *files and directories* based on attributes like name, size, or modification date. `grep` searches for specific *text patterns* *inside* files or command outputs.
**Detailed Explanation:** You use `find` when you know what a file looks like from the outside (e.g., all `.log` files older than 7 days). You use `grep` when you know what is inside the file (e.g., the word "ERROR" inside a log file).
**Practical Example:** `find /var/log -name "*.log"` finds the log files. `grep "Failed password" /var/log/auth.log` finds SSH login failures. They are often combined.
**Commands/Tools:** `find /path -name "file"`, `grep "text" file`.
**Common Mistake:** Using `grep` to try to find a file by its name, or using `find` to look for text inside a file.
**Strong Interview Line:** "Mastering the combination of `find` to locate files and `xargs` with `grep` to parse them is my go-to technique for rapid incident response."

**Question:** 16. kill vs killall
**Short Answer (30-45 sec):** `kill` terminates a process using its specific Process ID (PID). `killall` terminates all processes that match a specific program name.
**Detailed Explanation:** To use `kill`, you must first find the PID using `ps` or `pgrep`. With `killall`, you just need the name. Both send signals, defaulting to SIGTERM (15) for graceful shutdown, or SIGKILL (9) for forceful immediate termination.
**Practical Example:** If you have 10 hung Apache processes, finding 10 PIDs for `kill` is slow. `killall apache2` cleanly kills them all at once.
**Commands/Tools:** `kill 1234`, `kill -9 1234`, `killall nginx`.
**Common Mistake:** Using `kill -9` immediately. It doesn't allow the application to save state or close database connections gracefully. Always try standard kill first.
**Strong Interview Line:** "I always prefer graceful termination signals to ensure data integrity, reserving SIGKILL strictly for completely unresponsive, zombie-like processes."

**Question:** 17. systemd vs init
**Short Answer (30-45 sec):** `init` (SysVinit) is the older, sequential initialization system where services start one by one using scripts. `systemd` is the modern replacement that starts services in parallel, manages dependencies better, and standardizes logging.
**Detailed Explanation:** `systemd` is much faster because it uses socket activation and parallel startup. It also introduces `journalctl` for centralized logging and unit files (`.service`) instead of complex bash scripts for managing services.
**Practical Example:** Writing a `systemd` service unit file for a custom Node.js application to ensure it automatically restarts if it crashes.
**Commands/Tools:** `systemctl`, `journalctl`.
**Common Mistake:** Trying to use old `service` or `chkconfig` commands on modern distributions instead of natively using `systemctl`.
**Strong Interview Line:** "While `init` was reliable, `systemd` provides the robust process supervision and dependency management necessary for modern, complex server architectures."

**Question:** 18. apt vs yum vs dnf
**Short Answer (30-45 sec):** They are all package managers. `apt` is for Debian/Ubuntu (uses .deb packages). `yum` is for older RedHat/CentOS (uses .rpm packages). `dnf` is the modern, faster, and more efficient replacement for `yum` in newer RedHat/Fedora/CentOS versions.
**Detailed Explanation:** `dnf` was introduced to fix performance issues, excessive memory usage, and poor dependency resolution in `yum`. 
**Practical Example:** When writing an Ansible playbook or Dockerfile, I ensure I use `apt` for Ubuntu images and `dnf`/`yum` for Amazon Linux or CentOS images.
**Commands/Tools:** `apt install`, `dnf install`.
**Common Mistake:** Trying to use `apt` on an Amazon EC2 instance running Amazon Linux (which requires `yum`/`dnf`).
**Strong Interview Line:** "Adapting to the specific package manager of the target OS is a fundamental skill, especially when automating multi-OS environments with tools like Terraform and Ansible."

**Question:** 19. vi vs nano
**Short Answer (30-45 sec):** `nano` is a simple, easy-to-use text editor perfect for beginners. `vi` (or `vim`) is a powerful, modal text editor that is installed on almost every Unix system by default but has a steep learning curve.
**Detailed Explanation:** `vi` operates in modes (Command mode, Insert mode). You can't just start typing. It is highly efficient once learned. `nano` works more like notepad; you just open it and type. 
**Practical Example:** Editing a config file quickly on a minimal Docker container where only `vi` is installed. 
**Commands/Tools:** `vi /etc/hosts` (Press 'i' to insert, 'Esc' then ':wq' to save and quit).
**Common Mistake:** Opening `vi` and getting stuck because they don't know how to enter insert mode or exit (the famous "how to exit vim" problem).
**Strong Interview Line:** "While `nano` is user-friendly, I strictly use `vim` because its ubiquity across all Unix environments guarantees I can edit configurations effectively anywhere."

**Question:** 20. cp vs mv vs rsync
**Short Answer (30-45 sec):** `cp` copies files, duplicating them. `mv` moves or renames files, deleting the original. `rsync` is an advanced tool that syncs files and directories, copying only the differences (delta transfer), making it highly efficient for backups.
**Detailed Explanation:** While `cp` copies everything blindly, `rsync` checks what's already at the destination. If transferring a 10GB file locally or over SSH and it fails halfway, `rsync` can resume where it left off.
**Practical Example:** Migrating 50GB of web files to a new server. `scp` or `cp` would take forever, but `rsync -avz` will securely and efficiently mirror the data.
**Commands/Tools:** `cp -r dir1 dir2`, `mv file1 newname`, `rsync -avz /source/ /dest/`.
**Common Mistake:** Forgetting the trailing slash in `rsync` source directories, which copies the directory itself instead of its contents.
**Strong Interview Line:** "For localized changes `cp` and `mv` are fine, but for any production data migration or backups, `rsync` is mandatory for its delta-transfer efficiency and network resilience."

### LEVEL 3 – HOW IT WORKS (Linux)

**Question:** 21. How does Linux boot? (BIOS → GRUB → Kernel → init/systemd → runlevel)
**Short Answer (30-45 sec):** The boot process has 4 main stages. 1) BIOS/UEFI performs hardware checks (POST) and finds the bootloader. 2) The bootloader (GRUB) loads the Linux Kernel into memory. 3) The Kernel initializes hardware and mounts the root filesystem. 4) The Kernel starts the first user-space process (`systemd` or `init`), which then starts all other services.
**Detailed Explanation:** 
- **BIOS/UEFI:** Basic Input/Output System. Checks RAM, CPU.
- **Bootloader (GRUB2):** Grand Unified Bootloader. Gives you the menu to select OS/Kernel version.
- **Kernel:** Extracts the initramfs (initial RAM filesystem) to get necessary drivers to mount the real hard drive.
- **systemd:** Takes over as PID 1, mounts file systems in `/etc/fstab`, and starts targets (like multi-user.target for CLI or graphical.target for GUI).
**Practical Example:** If a server is stuck in a boot loop, I access the console, edit the GRUB menu during boot to boot into single-user mode, and fix the broken `/etc/fstab` entry.
**Commands/Tools:** `dmesg` (kernel ring buffer logs), `journalctl -b` (current boot logs).
**Common Mistake:** Not realizing that `systemd` is PID 1 and is responsible for everything that happens after the kernel loads.
**Strong Interview Line:** "A deep understanding of the Linux boot sequence is critical for recovering crashed servers and fixing boot-level configuration errors."
**Follow-ups:** 
- Q: What is initramfs? A: A temporary root filesystem loaded into memory to provide drivers needed to mount the actual disk.

**Question:** 22. How do Linux file permissions work? Explain chmod numerically and symbolically
**Short Answer (30-45 sec):** Permissions apply to User, Group, and Others. Symbolically, you use letters (u, g, o) and operators (+, -, =) like `chmod u+x file`. Numerically, you use octal numbers (4=Read, 2=Write, 1=Execute) like `chmod 755 file`.
**Detailed Explanation:** 
Numeric is faster:
- 7 = 4+2+1 (rwx)
- 6 = 4+2 (rw-)
- 5 = 4+1 (r-x)
- 0 = ---
So `chmod 755` means Owner=rwx, Group=r-x, Other=r-x.
Symbolic is good for specific changes: `chmod o-w file` removes write permission for others without touching existing user/group permissions.
**Practical Example:** Generating an SSH keypair. The private key `id_rsa` MUST be strictly secured. You run `chmod 600 id_rsa` (rw-------) otherwise SSH will refuse to use it.
**Commands/Tools:** `chmod`, `stat <file>` (shows detailed permissions).
**Common Mistake:** Using `777` lazily. Also, not knowing that for a *directory*, Execute (x) permission means the ability to `cd` into it.
**Strong Interview Line:** "I heavily rely on numeric `chmod` for automation scripts, ensuring strict zero-trust permission models for sensitive files like certificates and keys."

**Question:** 23. How does the Linux process lifecycle work?
**Short Answer (30-45 sec):** A process is created via a `fork()` system call, which creates a child process from a parent. The child then uses `exec()` to replace itself with the new program. When finished, it calls `exit()`, and the parent must read its exit status using `wait()`.
**Detailed Explanation:** 
1. **Running/Runnable (R):** Using CPU or waiting in queue.
2. **Sleeping (S/D):** Waiting for an event or I/O.
3. **Stopped (T):** Suspended (e.g., via Ctrl+Z).
4. **Zombie (Z):** The child exited, but the parent hasn't read its status yet. The process table still holds the entry.
**Practical Example:** If I see a high number of 'Z' (Zombie) processes in `top`, I know the parent application (maybe a custom Java app) is poorly written and failing to clean up its children. I must kill the parent to clear them.
**Commands/Tools:** `top`, `ps -ef f` (shows process tree).
**Common Mistake:** Trying to `kill -9` a zombie process. You can't kill what's already dead; you must kill its parent process or wait for `init` to reap it.
**Strong Interview Line:** "Understanding the fork-exec model and process states is vital for diagnosing application deadlocks and identifying resource leaks in production environments."

**Question:** 24. How does systemd manage services?
**Short Answer (30-45 sec):** `systemd` manages services using unit files (usually `.service` files). It acts as a central manager (PID 1) that tracks service dependencies, handles parallel startup, and automatically restarts services if they crash.
**Detailed Explanation:** A unit file defines what command to run, what user to run it as, and dependencies (`After=network.target`). `systemd` monitors the cgroups (control groups) of the service. If the main process dies, `systemd` knows and can trigger an automatic restart based on the `Restart=always` directive.
**Practical Example:** I deployed a custom Python web scraper. I created `/etc/systemd/system/scraper.service` so that `systemctl start scraper` manages it, and logs go directly to `journalctl`.
**Commands/Tools:** `systemctl daemon-reload` (apply unit file changes), `systemctl restart <service>`.
**Common Mistake:** Editing a unit file and forgetting to run `systemctl daemon-reload` before restarting the service, causing the changes to be ignored.
**Strong Interview Line:** "Writing custom `systemd` unit files is a standard practice I use to bridge the gap between developer code and robust, production-grade service availability."

**Question:** 25. How does SSH work? (key exchange, authentication)
**Short Answer (30-45 sec):** SSH (Secure Shell) provides a secure, encrypted connection over an insecure network (port 22). It works in two phases: first, an asymmetric key exchange (like Diffie-Hellman) establishes a secure encrypted tunnel. Second, user authentication occurs inside that tunnel using passwords or public-key cryptography.
**Detailed Explanation:** 
1. **Key Exchange:** Client and server agree on encryption algorithms and generate a shared symmetric session key. The data is now encrypted.
2. **Authentication:** The server checks if the client is allowed. Best practice uses SSH keys. The client proves it holds the private key matching the public key stored in the server's `~/.ssh/authorized_keys` file.
**Practical Example:** Instead of using passwords, I generate a key pair on my laptop (`ssh-keygen`), copy the public key to the AWS EC2 instance, and disable password authentication entirely in `/etc/ssh/sshd_config`.
**Commands/Tools:** `ssh-keygen`, `ssh-copy-id`, `ssh -i key.pem user@host`.
**Common Mistake:** Setting incorrect permissions on the `~/.ssh` directory (must be 700) or `authorized_keys` file (must be 600) on the server, causing SSH to silently reject key logins.
**Strong Interview Line:** "Implementing key-based SSH authentication and disabling password logins is the absolute baseline security standard for any cloud infrastructure."

### LEVEL 4 – LINUX COMMANDS (COMPLETE WITH EXAMPLES)

**File & Navigation:**
- **ls (with -la, -lh flags)**
  - **Purpose:** List directory contents.
  - **Syntax:** `ls [options] [path]`
  - **Real Example:** `ls -lah /var/log`
  - **Expected Output:** Lists all files (including hidden `.`), with human-readable sizes (e.g., 10M, 2K), showing permissions and owners.
  - **When used:** Checking file sizes or if a specific configuration file exists and has the right permissions.
- **mkdir (-p flag)**
  - **Purpose:** Make directories.
  - **Syntax:** `mkdir -p /path/to/dir`
  - **Real Example:** `mkdir -p /app/data/mysql`
  - **Expected Output:** Creates the directory structure without errors even if parent directories don't exist.
  - **When used:** Setting up application directory structures in provisioning scripts.
- **rm (-rf, danger warning)**
  - **Purpose:** Remove files or directories.
  - **Syntax:** `rm -rf /path`
  - **Real Example:** `rm -rf /tmp/old_logs/`
  - **Expected Output:** Silently deletes the folder and everything inside it.
  - **When used:** Cleaning up old data. *Danger:* Never use `rm -rf /` or do this as root without triple-checking the path.
- **cat, less, head, tail (-f for live log)**
  - **Purpose:** View file contents.
  - **Syntax:** `tail -f /path/to/file`
  - **Real Example:** `tail -f /var/log/nginx/access.log`
  - **Expected Output:** Outputs the last 10 lines and waits, printing new lines in real-time as users hit the web server.
  - **When used:** Live troubleshooting during application deployments to watch for errors.

**Text & Search:**
- **grep (-r, -i, -n, -v flags)**
  - **Purpose:** Search text globally for regular expressions.
  - **Syntax:** `grep -irn "error" /var/log/`
  - **Real Example:** `grep -i "failed password" /var/log/auth.log`
  - **Expected Output:** `Failed password for root from 192.168.1.10 port 22 ssh2`
  - **When used:** Investigating security breaches or application errors.
- **find**
  - **Purpose:** Search for files in a directory hierarchy.
  - **Syntax:** `find /path -name "pattern" -type f`
  - **Real Example:** `find /var/log -type f -name "*.log" -mtime +30`
  - **Expected Output:** Lists all `.log` files older than 30 days.
  - **When used:** Finding old log files to delete or archive to free up disk space.
- **awk**
  - **Purpose:** Pattern scanning and text processing language.
  - **Syntax:** `awk '{print $N}' file`
  - **Real Example:** `ls -l | awk '{print $9}'`
  - **Expected Output:** Prints only the 9th column (the filenames).
  - **When used:** Extracting specific columns of data from command outputs for scripting.

**Permissions & Users:**
- **chmod**
  - **Purpose:** Change file mode bits (permissions).
  - **Syntax:** `chmod 755 filename`
  - **Real Example:** `chmod 600 ~/.ssh/id_rsa`
  - **Expected Output:** Restricts the private key so only the owner can read/write it.
- **chown**
  - **Purpose:** Change file owner and group.
  - **Syntax:** `chown user:group file`
  - **Real Example:** `sudo chown -R www-data:www-data /var/www/html`
  - **Expected Output:** Recursively gives the Nginx/Apache web user ownership of the web files.

**Processes:**
- **ps (aux flags)**
  - **Purpose:** Report a snapshot of current processes.
  - **Syntax:** `ps aux | grep process_name`
  - **Real Example:** `ps aux | grep java`
  - **Expected Output:** Lists the Java process, its PID, CPU/Memory usage, and exact launch command.
- **top, htop**
  - **Purpose:** Display Linux tasks dynamically.
  - **Syntax:** `htop`
  - **Real Example:** Running `htop` during an incident.
  - **Expected Output:** An interactive, color-coded live view of CPU, Memory, Swap, and processes.
  - **When used:** Identifying which process is spiking the CPU to 100%.

**Disk & Memory:**
- **df (-h flag)**
  - **Purpose:** Report file system disk space usage.
  - **Syntax:** `df -h`
  - **Real Example:** `df -h /`
  - **Expected Output:** `/dev/sda1  50G  45G  5G  90% /`
  - **When used:** Checking if the disk is full, which causes databases and applications to crash.
- **free (-h)**
  - **Purpose:** Display amount of free and used memory.
  - **Syntax:** `free -h`
  - **Real Example:** `free -h`
  - **Expected Output:** Shows Total, Used, Free, Shared, Buff/Cache, and Available RAM.
  - **When used:** Checking if the server is swapping (running out of physical RAM).

**Network:**
- **ip addr**
  - **Purpose:** Show / manipulate routing, network devices, interfaces.
  - **Syntax:** `ip addr show`
  - **Expected Output:** Shows the eth0 interface and its assigned IP address.
- **ss (-tulnp)**
  - **Purpose:** Investigate sockets (modern netstat).
  - **Syntax:** `ss -tulnp`
  - **Expected Output:** Shows which ports are open and listening (e.g., port 80 for Nginx) and their PIDs.
  - **When used:** Verifying if a web server actually started and is listening on the correct port.
- **curl (-I, -L, -o flags)**
  - **Purpose:** Transfer a URL.
  - **Syntax:** `curl -I https://google.com`
  - **Expected Output:** Returns the HTTP response headers (e.g., HTTP/2 200).
  - **When used:** Testing from the CLI if an API endpoint or website is up and reachable.

**System:**
- **systemctl**
  - **Purpose:** Control the systemd system and service manager.
  - **Syntax:** `systemctl status|start|stop|restart|enable nginx`
  - **Real Example:** `systemctl enable docker`
  - **Expected Output:** Creates a symlink ensuring Docker starts on the next server reboot.
- **journalctl**
  - **Purpose:** Query the systemd journal.
  - **Syntax:** `journalctl -u service_name -f`
  - **Real Example:** `journalctl -u sshd -f`
  - **Expected Output:** Live tail of SSH login attempts.

---

## MODULE 2: WINDOWS FUNDAMENTALS

### LEVEL 1 – WHAT IS?

**Question:** 26. What is Windows Server vs Windows Desktop?
**Short Answer (30-45 sec):** Windows Desktop (like Windows 10/11) is designed for individual users, focusing on UI and consumer apps. Windows Server is designed for enterprise infrastructure, focusing on reliability, networking, and hosting services like Active Directory, DNS, and file sharing for multiple users.
**Detailed Explanation:** Windows Server includes server-specific roles (IIS, DHCP, Hyper-V, Active Directory Domain Services) that are either absent or limited in desktop versions. It also supports significantly higher hardware limits (massive RAM and multi-processor support) and limits background tasks to prioritize server processes.
**Practical Example:** You install Windows 11 on an employee's laptop, but you install Windows Server 2022 on the data center rack server to run the company's SQL database.
**Commands/Tools:** `winver` or `systeminfo` to check the OS version.
**Common Mistake:** Thinking the only difference is the UI; the kernel tuning (foreground vs background task priority) is completely different.
**Strong Interview Line:** "Windows Server is fundamentally tuned for continuous background service availability and enterprise directory management, whereas Desktop is tuned for interactive user experience."

**Question:** 27. What are Windows Services?
**Short Answer (30-45 sec):** Windows Services are long-running executable applications that operate in their own Windows session, running in the background without user interaction. (Equivalent to Linux daemons).
**Detailed Explanation:** Services start when the computer boots (even before a user logs in). They handle core OS functions (like Windows Update, Print Spooler) and third-party software (like SQL Server, Apache). 
**Practical Example:** The "Print Spooler" service manages printing. If users can't print, restarting this service often fixes the queue without rebooting the server.
**Commands/Tools:** `services.msc` (GUI), `Get-Service` (PowerShell), `sc query` (CMD).
**Common Mistake:** Confusing a startup program (runs only when a user logs in) with a Service (runs regardless of user login).
**Strong Interview Line:** "Managing Windows Services effectively is critical because they dictate the availability of core infrastructure applications independent of active user sessions."

**Question:** 28. What is the Windows Registry?
**Short Answer (30-45 sec):** The Windows Registry is a hierarchical database that stores low-level settings for the Windows operating system and for applications that opt to use the registry.
**Detailed Explanation:** It contains settings for hardware, OS configuration, user profiles, and installed software. It replaces the old `.ini` files. Changes here take effect immediately or on reboot and can break the OS if done incorrectly. It consists of root keys like HKEY_LOCAL_MACHINE (system-wide) and HKEY_CURRENT_USER (user-specific).
**Practical Example:** Disabling USB storage devices across the company by modifying a specific registry key via a deployment script.
**Commands/Tools:** `regedit` (GUI), `reg query / reg add` (CMD).
**Common Mistake:** Making registry changes without backing up the specific key first, leading to unbootable systems.
**Strong Interview Line:** "The registry is the nervous system of Windows; modifying it allows powerful configurations but demands strict caution and backups."

**Question:** 29. What is Active Directory? (basic understanding)
**Short Answer (30-45 sec):** Active Directory (AD) is Microsoft's directory service used for centralized domain management. It stores information about users, computers, and groups, and authenticates users on a network.
**Detailed Explanation:** Without AD, every computer needs its own local user accounts (peer-to-peer). With AD, a Windows Server acts as a Domain Controller (DC). A user can log into any PC in the domain using one set of credentials. It uses LDAP for querying and Kerberos for secure authentication.
**Practical Example:** When a new employee joins, I create one AD user account. That single account grants them access to their laptop, the company WiFi, and the shared file servers.
**Commands/Tools:** Active Directory Users and Computers (ADUC) GUI, `Get-ADUser` (PowerShell).
**Common Mistake:** Confusing AD (the database/service) with a Domain Controller (the server running the service).
**Strong Interview Line:** "Active Directory is the cornerstone of enterprise identity and access management in a Windows environment, centralizing security and administration."

**Question:** 30. What is Group Policy?
**Short Answer (30-45 sec):** Group Policy (GPO) is a feature in Windows Server (via Active Directory) that allows administrators to centrally manage and enforce configurations, security settings, and software deployment for users and computers across the domain.
**Detailed Explanation:** Instead of going to 500 computers to set the desktop wallpaper, disable the Control Panel, or enforce a password complexity rule, you create one GPO on the Domain Controller. The computers download and apply this policy automatically.
**Practical Example:** Creating a GPO to map a shared network drive (Z: drive) for the HR department so it appears automatically when they log in.
**Commands/Tools:** Group Policy Management Console (GPMC), `gpupdate /force` (on the client).
**Common Mistake:** Applying a GPO to the wrong Organizational Unit (OU) and accidentally locking out administrators.
**Strong Interview Line:** "Group Policy is my primary tool for enforcing company-wide security compliance and standardizing the user experience at scale."

### LEVEL 2 – DIFFERENCE QUESTIONS (Windows)

**Question:** 36. FAT32 vs NTFS vs exFAT
**Short Answer (30-45 sec):** FAT32 is older, highly compatible, but limits file sizes to 4GB. NTFS is the modern Windows standard, supporting massive files, encryption, and strict file-level security permissions. exFAT is optimized for flash drives, removing the 4GB limit of FAT32 while maintaining cross-platform compatibility (Mac/PC).
**Detailed Explanation:** For an OS drive or server storage, NTFS is mandatory because it supports Access Control Lists (ACLs) and journaling. FAT32/exFAT do not have granular security permissions.
**Practical Example:** Formatting a 16GB USB drive to share a 5GB ISO file with a Mac user; I must use exFAT because FAT32 fails at 4GB and NTFS is read-only on Mac.
**Strong Interview Line:** "For Windows Servers, NTFS is absolute; its security features and journaling are non-negotiable for data protection."

**Question:** 37. Local Account vs Domain Account
**Short Answer (30-45 sec):** A local account only exists on that specific computer's Security Accounts Manager (SAM) database. A domain account exists on the Active Directory Domain Controller and allows the user to log into any computer joined to that domain.
**Detailed Explanation:** If a laptop dies, a local account's profile is trapped. With a domain account, the user just takes a new laptop, connects to the network, and logs in.
**Practical Example:** The "Administrator" account you use during initial setup is Local. `john.doe@company.local` is a Domain account.

**Question:** 40. CMD vs PowerShell
**Short Answer (30-45 sec):** CMD is the legacy command-line interpreter originating from MS-DOS, processing text strings. PowerShell is a modern, object-oriented automation framework built on .NET, dealing with objects rather than just text.
**Detailed Explanation:** In CMD, if you get a list of services, it's just text. In PowerShell, `Get-Service` returns .NET objects. You can easily pipe these objects to filter them (e.g., `Get-Service | Where-Object Status -eq 'Running'`).
**Practical Example:** Stopping all processes named "notepad". In CMD it requires complex text parsing or specific tools. In PS: `Get-Process notepad | Stop-Process`.
**Strong Interview Line:** "While I use CMD for quick network pings, PowerShell is my primary tool for Windows automation due to its powerful object-oriented pipeline and cloud-module integration."

### LEVEL 4 – WINDOWS COMMANDS (COMPLETE WITH EXAMPLES)

**Network:**
- **ipconfig (basic + /all + /release + /renew + /flushdns)**
  - **Purpose:** Display or manage IP configuration.
  - **Real Example:** `ipconfig /flushdns`
  - **Expected Output:** Clears the DNS resolver cache.
  - **When used:** A user can't access an internal website after the server's IP changed. Flushing forces the PC to fetch the new IP.
- **ping (with -t flag)**
  - **Purpose:** Test network connectivity continuously.
  - **Syntax:** `ping google.com -t`
  - **When used:** Running a continuous ping while rebooting a remote router to see exactly when it comes back online. (Ctrl+C to stop).
- **netstat (-an)**
  - **Purpose:** Display active TCP connections and listening ports.
  - **Real Example:** `netstat -ano | findstr :80`
  - **Expected Output:** Shows the PID of the process binding port 80.
  - **When used:** Figuring out what application is hogging a port when IIS fails to start.

**System:**
- **taskkill (/f /im /pid)**
  - **Purpose:** Terminate tasks by process ID (PID) or image name.
  - **Real Example:** `taskkill /F /IM excel.exe`
  - **Expected Output:** Forcefully closes Excel.
  - **When used:** When a program completely freezes and Task Manager won't open.
- **sfc /scannow**
  - **Purpose:** System File Checker; scans and repairs corrupt Windows system files.
  - **Real Example:** `sfc /scannow`
  - **When used:** When Windows is behaving erratically or throwing random DLL errors.
- **gpupdate /force**
  - **Purpose:** Force an immediate update of Group Policy.
  - **Real Example:** `gpupdate /force`
  - **When used:** After an admin changes a policy on the server, you run this on the client to apply it immediately instead of waiting 90 minutes.

**PowerShell Essentials:**
- **Get-Service**
  - **Purpose:** Get status of services on a local or remote computer.
  - **Real Example:** `Get-Service -Name wuauserv` (Windows Update service).
- **Test-Connection**
  - **Purpose:** PowerShell equivalent of ping, returning an object.
  - **Real Example:** `Test-Connection -ComputerName server01 -Count 2`

---

## MODULE 3: NETWORKING FUNDAMENTALS

### LEVEL 1 – WHAT IS?

**Question:** 45. What is an IP address? What is IPv4 vs IPv6?
**Short Answer (30-45 sec):** An IP address is a unique numerical identifier assigned to every device on a network to locate and communicate with it. IPv4 uses 32-bit addresses (e.g., 192.168.1.1), allowing ~4.3 billion addresses. IPv6 uses 128-bit addresses (alphanumeric) to solve IPv4 exhaustion, offering virtually infinite addresses.
**Detailed Explanation:** IPs operate at Layer 3 (Network Layer) of the OSI model. IPv4 is still dominant, sustained by NAT (Network Address Translation). IPv6 removes the need for NAT and has built-in IPsec security.
**Practical Example:** Setting up a web server requires assigning it a static IPv4 address so DNS can reliably point users to it.
**Common Mistake:** Confusing IP addresses (logical, can change) with MAC addresses (physical, hardcoded on the hardware).
**Strong Interview Line:** "Understanding IP addressing is the foundation of network engineering; without it, routing traffic to servers or troubleshooting connectivity is impossible."

**Question:** 46. What is a subnet mask? What is subnetting?
**Short Answer (30-45 sec):** A subnet mask separates an IP address into two parts: the Network ID and the Host ID. Subnetting is the process of dividing a large network into smaller, more efficient, and secure sub-networks.
**Detailed Explanation:** For IP `192.168.1.50` with subnet mask `255.255.255.0` (or /24), the first three octets (`192.168.1`) identify the network, and `.50` identifies the specific computer. 
**Practical Example:** In AWS VPC, you create a public subnet for Web servers and a private subnet for Databases to isolate them for security and broadcast control.
**Strong Interview Line:** "Subnetting allows me to logically isolate network traffic, improving both security and network performance by containing broadcast domains."

**Question:** 47. What is a gateway? What is a default gateway?
**Short Answer (30-45 sec):** A gateway is a router or device that connects two different networks. A default gateway is the IP address a computer sends its traffic to when it wants to reach a device outside its own local subnet (usually the Internet).
**Detailed Explanation:** If PC-A wants to talk to PC-B on the same switch, it uses MAC addresses. If PC-A wants to reach google.com, it realizes the IP is outside its subnet and forwards the packet to its Default Gateway (the local router).
**Practical Example:** Your home WiFi router acts as the default gateway (usually `192.168.1.1`) for your laptop to reach the internet.
**Common Mistake:** Forgetting to configure the default gateway on a static IP server, resulting in it being able to ping local servers but failing to reach the internet.

**Question:** 48. What is DNS? What is DHCP?
**Short Answer (30-45 sec):** DNS (Domain Name System) translates human-readable domain names (google.com) into IP addresses (142.250.190.46). DHCP (Dynamic Host Configuration Protocol) automatically assigns IP addresses and network configurations (like gateway and DNS servers) to devices when they join a network.
**Detailed Explanation:** DNS is the phonebook of the internet. DHCP is the receptionist handing out badges. Without DHCP, you'd have to manually type an IP address, subnet mask, and gateway into every single device.
**Practical Example:** Setting up a corporate WiFi network relies on a DHCP server to lease IPs to employee phones, while internal DNS resolves internal names like `intranet.company.local`.
**Commands/Tools:** `nslookup`, `dig` (for DNS). `ipconfig /release & /renew` (for DHCP).
**Strong Interview Line:** "DNS and DHCP are the invisible pillars of network usability; when either fails, the network effectively appears 'down' to end users."

**Question:** 50. What is a port?
**Short Answer (30-45 sec):** A port is a logical endpoint for communication in an operating system. While an IP address gets data to the correct computer, the port number ensures the data goes to the correct application on that computer.
**Detailed Explanation:** Ports range from 0 to 65535. Ports 0-1023 are well-known (reserved for system services). When a packet arrives, the OS checks the destination port to route it (e.g., port 80 traffic goes to Apache, port 22 traffic goes to the SSH daemon).
**Practical Example:** Running multiple websites on one server using Docker by mapping host port 8080 to container A and port 8081 to container B.
**Common Mistake:** Confusing physical switch ports with logical TCP/UDP ports.
**Strong Interview Line:** "Understanding port mapping and firewall rules is critical when deploying microservices or configuring load balancers in a cloud environment."

### LEVEL 2 – DIFFERENCE QUESTIONS (Networking)

**Question:** 61. TCP vs UDP
**Short Answer (30-45 sec):** TCP (Transmission Control Protocol) is connection-oriented, ensuring reliable, ordered, and error-checked delivery of data. UDP (User Datagram Protocol) is connectionless, sending data quickly without guaranteeing delivery or order.
**Detailed Explanation:** TCP uses a 3-way handshake (SYN, SYN-ACK, ACK) to establish a connection. If a packet drops, TCP retransmits it. UDP just fires packets (fire-and-forget). 
**Practical Example:** Browsing a website (HTTP) or downloading a file uses TCP because losing a byte corrupts the file. Live video streaming (Zoom) or gaming uses UDP because speed is prioritized; dropping a single frame is better than buffering.
**Strong Interview Line:** "Choosing between TCP and UDP depends entirely on the application's tolerance for data loss versus its need for speed."

**Question:** 62. Switch vs Router vs Hub
**Short Answer (30-45 sec):** A Hub broadcasts data to all connected ports (dumb, causes collisions). A Switch is smart; it learns MAC addresses and sends data only to the specific port it's meant for (Layer 2). A Router connects different networks together and routes traffic based on IP addresses (Layer 3).
**Detailed Explanation:** Hubs are obsolete. Switches handle local traffic within a LAN (Local Area Network). Routers handle traffic moving from one LAN to another (like your home network to the ISP).
**Practical Example:** Computers in an office connect to a Switch to share local files. The Switch connects to a Router, which connects the office to the internet.

### LEVEL 3 – HOW IT WORKS (Networking)

**Question:** 71. What happens step by step when you type google.com in a browser?
**Short Answer (30-45 sec):** 
1. **DNS Resolution:** The browser checks cache, then asks the DNS server to translate google.com to an IP address.
2. **TCP Handshake:** The browser initiates a 3-way TCP handshake (SYN, SYN-ACK, ACK) with that IP on port 443.
3. **TLS Handshake:** Secure encryption keys are exchanged for HTTPS.
4. **HTTP Request:** An HTTP GET request is sent.
5. **Response & Render:** The server sends back the HTML/CSS/JS, and the browser renders the page.
**Detailed Explanation:** This is the ultimate full-stack question. It proves understanding of Layer 7 (HTTP/DNS), Layer 4 (TCP), and Layer 3 (IP). 
**Strong Interview Line:** "This process highlights the entire OSI model in action, from the application layer parsing the URL down to the physical layer transmitting the bits."

**Question:** 78. What are common port numbers?
**Detailed Explanation:** Must memorize:
- 20/21: FTP (File Transfer)
- 22: SSH (Secure Shell)
- 23: Telnet (Insecure, deprecated)
- 25: SMTP (Email routing)
- 53: DNS (Domain Name System)
- 80: HTTP (Web unencrypted)
- 443: HTTPS (Web encrypted)
- 3389: RDP (Remote Desktop Protocol)
- 3306: MySQL Database

### LEVEL 4 – NETWORKING COMMANDS

**Linux Networking Commands:**
- **ping -c 4 google.com**
  - **Purpose:** Test reachability. `-c 4` limits to 4 pings.
- **traceroute google.com**
  - **Purpose:** Shows the path (routers/hops) a packet takes to reach the destination. Used to find where the network is breaking.
- **netstat -rn (or ip route)**
  - **Purpose:** Displays the routing table, showing the default gateway.

---

## MODULE 4: HARDWARE & VIRTUALIZATION

**Question:** 79. What is CPU? What are cores and threads?
**Short Answer (30-45 sec):** The CPU (Central Processing Unit) is the brain of the server. Cores are independent physical processing units within the CPU. Threads are virtual cores created by technologies like Hyper-Threading, allowing a single physical core to handle two tasks concurrently.
**Practical Example:** When provisioning an AWS EC2 `t3.medium`, it offers 2 vCPUs (threads), allowing it to handle concurrent web server requests more efficiently than a single thread.

**Question:** 87. What is RAID? Types of RAID (0, 1, 5, 10)
**Short Answer (30-45 sec):** RAID (Redundant Array of Independent Disks) combines multiple hard drives for performance, redundancy, or both.
**Detailed Explanation:** 
- **RAID 0 (Striping):** Speed. Data split across drives. No redundancy (1 drive dies, all data lost).
- **RAID 1 (Mirroring):** Redundancy. Data is duplicated across 2 drives. 
- **RAID 5 (Striping with Parity):** Good balance. Requires min 3 drives. Survives 1 drive failure.
- **RAID 10 (1+0):** Stripe of mirrors. Excellent speed and redundancy. Expensive.
**Practical Example:** Database servers usually use RAID 10 for the high write speed and fault tolerance.

**Question:** 94. What is virtualization?
**Short Answer (30-45 sec):** Virtualization uses software to create an abstraction layer over computer hardware, allowing the hardware elements (CPU, memory, storage) to be divided into multiple virtual computers, called Virtual Machines (VMs).
**Detailed Explanation:** It allows you to run multiple different operating systems on a single physical server simultaneously, maximizing hardware utilization and isolating applications.

**Question:** 95. What is a hypervisor? Type 1 vs Type 2
**Short Answer (30-45 sec):** A hypervisor is the software that creates and runs VMs. 
- **Type 1 (Bare-metal):** Installs directly on the server hardware (e.g., VMware ESXi, Proxmox, Hyper-V). Used in enterprise data centers.
- **Type 2 (Hosted):** Installs on top of an existing OS like an application (e.g., VirtualBox, VMware Workstation). Used on personal laptops.

---

## MODULE 6: SECURITY BASICS

**Question:** 100. What is a firewall?
**Short Answer (30-45 sec):** A firewall is a network security device (hardware or software) that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies.
**Practical Example:** Configuring AWS Security Groups (a virtual firewall) to only allow inbound port 443 (HTTPS) from the internet, and only allow port 22 (SSH) from the office IP address.

**Question:** 104. What is least privilege principle?
**Short Answer (30-45 sec):** The Principle of Least Privilege (PoLP) dictates that a user, program, or process should have only the bare minimum privileges necessary to perform its intended function.
**Practical Example:** Instead of giving a developer "Domain Admin" rights, you give them read/write access only to their specific project folder. If their account is compromised, the blast radius is contained.

**Question:** 109. How would you secure a Linux server?
**Short Answer (30-45 sec):** 
1. Disable root login in SSH.
2. Disable password authentication; use SSH keys only.
3. Configure a firewall (UFW or iptables) to allow only necessary ports.
4. Keep the system updated (`apt update && apt upgrade`).
5. Run services using non-root users.
**Strong Interview Line:** "Security is about defense in depth; by locking down SSH, enforcing firewall rules, and strictly applying the principle of least privilege, we drastically reduce the server's attack surface."

---
*End of Document. Good luck with the interview!*
