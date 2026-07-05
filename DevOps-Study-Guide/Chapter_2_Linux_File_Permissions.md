# Chapter 2: Linux File Permissions

## 2.1 Why Permissions Matter
In a multi-user environment like Linux, security is based on isolation. 

Let's use a real-world analogy:
> **Analogy:** Think of an office building.
> * **Owner (User):** The employee who owns the desk. They have full access to files inside their desk drawer.
> * **Group:** The Finance department. Only members of Finance can read the company financial spreadsheets.
> * **Others (Public):** The delivery person or visitors. They should only be allowed in the reception area and cannot look at desks or spreadsheets.

Without permissions, a malicious process or standard user could modify critical configuration files (like `/etc/passwd`), delete system binaries, or access sensitive application environment variables containing API keys and passwords.

---

## 2.2 The Linux Ownership Model
In Linux, every file and directory is owned by exactly **one User** and **one Group**. The access rights are separated into three classes:

1. **User (u):** The owner of the file (typically the user who created it).
2. **Group (g):** A collection of users who share access to the file.
3. **Others (o):** Everyone else who is not the owner and is not a member of the group. (Also referred to as *world* or *public*).

---

## 2.3 The Permission Model: Read, Write, Execute
For each owner class, there are three types of access permissions:

* **Read (r):**
  * *For Files:* Allows viewing the contents of the file (e.g., using `cat`, `less`).
  * *For Directories:* Allows listing the contents of the directory (using `ls`).
* **Write (w):**
  * *For Files:* Allows modifying or deleting file contents.
  * *For Directories:* Allows creating, deleting, or renaming files inside the directory (even if you don't have write permissions on the individual files themselves!).
* **Execute (x):**
  * *For Files:* Allows running the file as a program or script.
  * *For Directories:* Allows entering the directory (using `cd`) and accessing files inside it.

### How Permissions Appear in `ls -l`
When running `ls -l`, you see a 10-character string representing permissions:

```
 -  rwx  r-x  r--
 |   |    |    |
 |   |    |    +-- Others (o) permissions
 |   |    +------- Group (g) permissions
 |   +------------ User/Owner (u) permissions
 +---------------- File Type: (-) for file, (d) for directory, (l) for symbolic link
```

---

## 2.4 Numeric Representation
Permissions are represented mathematically using octal numbers (base-8). Each permission type has a designated value:

* **Read (r)** = 4
* **Write (w)** = 2
* **Execute (x)** = 1
* **No Permission (-)** = 0

To calculate the permission number for a class (User, Group, or Others), add the values of its permissions:

$$\text{Permission Total} = \text{Read} + \text{Write} + \text{Execute}$$

| Octal Value | Active Permissions | Text Equivalent | Explanation |
| :--- | :--- | :--- | :--- |
| **7** | $4 + 2 + 1$ | `rwx` | Full permissions (Read, Write, and Execute). |
| **6** | $4 + 2 + 0$ | `rw-` | Read and Write access. |
| **5** | $4 + 0 + 1$ | `r-x` | Read and Execute access. |
| **4** | $4 + 0 + 0$ | `r--` | Read-only access. |
| **0** | $0 + 0 + 0$ | `---` | No permissions at all. |

### Common Permission Combinations

* **`777` (rwxrwxrwx):** Everyone can read, write, and execute. **Dangerous in production.**
* **`755` (rwxr-xr-x):** Owner can read, write, and execute. Group and others can only read and execute. Standard for executable scripts and directories.
* **`644` (rw-r--r--):** Owner can read and write. Group and others can only read. Standard for configurations and documents.
* **`600` (rw-------):** Owner can read and write. No one else has any access. Standard for private SSH keys (`id_rsa`) and credentials.
* **`700` (rwx------):** Owner can read, write, and execute. No access for anyone else. Standard for private user scripts or home folders.

---

## 2.5 Linux Permission Commands

### 1. `chmod` (Change Mode)
* **Definition:** Modifies the file or directory permissions.
* **Syntax:** `chmod [options] <mode> <filename>`
* **Modes:**
  * **Numeric Mode:** Using octal numbers (e.g., `chmod 600 config.env`).
  * **Symbolic Mode:** Using letters to add (`+`), remove (`-`), or set (`=`) permissions (e.g., `chmod u+x script.sh`).
* **Options:** `-R` (Recursive: applies permissions to all nested files and directories).

#### Numeric Examples
* **Example 1:** Restrict a database credential file so only the owner can read/write:
  ```bash
  touch /tmp/db.creds
  chmod 600 /tmp/db.creds
  ls -l /tmp/db.creds
  ```
  *Expected Output:*
  ```text
  -rw------- 1 ubuntu ubuntu 0 Jun  1 08:50 /tmp/db.creds
  ```

#### Symbolic Examples
* **Example 2:** Grant execution rights to a custom deployment script for user and group:
  ```bash
  touch /tmp/deploy.sh
  chmod ug+x /tmp/deploy.sh
  ls -l /tmp/deploy.sh
  ```
  *Expected Output:*
  ```text
  -rwxr-xr-- 1 ubuntu ubuntu 0 Jun  1 08:52 /tmp/deploy.sh
  ```

---

### 2. `chown` (Change Owner)
* **Definition:** Changes the user and/or group ownership of a file or directory.
* **Syntax:** `chown [options] [owner][:[group]] <file>`
* **Options:** `-R` (Recursive: changes ownership for all nested files).
* **Examples:**
  * **Example 1:** Change owner of website root files to the `nginx` system user:
    ```bash
    sudo touch /var/www/index.html
    sudo chown nginx /var/www/index.html
    ls -l /var/www/index.html
    ```
    *Expected Output:*
    ```text
    -rw-r--r-- 1 nginx root 0 Jun  1 08:55 /var/www/index.html
    ```
  * **Example 2:** Change both owner and group recursively:
    ```bash
    sudo chown -R ubuntu:www-data /var/www
    ```

---

### 3. `chgrp` (Change Group)
* **Definition:** Changes only the group ownership of a file or directory.
* **Syntax:** `chgrp [options] <group> <file>`
* **Example:**
  ```bash
  sudo chgrp devops /opt/app
  ```
* **Real DevOps Use Case:** Granting a DevOps user group access to application directories without altering individual file owners.

---

### 4. `umask` (User Mask)
* **Definition:** Sets the default permission mask for newly created files and directories. It defines what permissions are **subtracted** from the maximum possible permissions.
  * Maximum file permissions: `666` (rw-rw-rw-)
  * Maximum directory permissions: `777` (rwxrwxrwx)
* **Syntax:** `umask [octal_mask]`
* **How to Calculate Permissions with Umask:**
  * File Permissions = `666` minus `umask`
  * Directory Permissions = `777` minus `umask`
* **Example:**
  ```bash
  umask 022
  touch /tmp/file_022.txt
  mkdir /tmp/dir_022
  ls -ld /tmp/file_022.txt /tmp/dir_022
  ```
  *Calculations:*
  * File: $666 - 022 = 644$ (rw-r--r--)
  * Directory: $777 - 022 = 755$ (rwxr-xr-x)
  *Expected Output:*
  ```text
  drwxr-xr-x 2 ubuntu ubuntu 4096 Jun  1 08:58 /tmp/dir_022
  -rw-r--r-- 1 ubuntu ubuntu    0 Jun  1 08:58 /tmp/file_022.txt
  ```
* **Real DevOps Use Case:** Ensuring created log files do not have write access for non-privileged users by configuring `umask 027` in system startup scripts.

---

## 2.6 Security Implications & Common Mistakes

### ❌ Mistake 1: Running `chmod 777` to Fix Errors
When an application encounters a "Permission Denied" error, developers often run `chmod -R 777 /app`.
* **The Risk:** This opens the directory to any user on the system. If an attacker gains access to a low-privileged system user (like `nobody` or `www-data`), they can instantly overwrite execution scripts, plant backdoors, or read database credentials.
* **Best Practice:** Identify the user executing the process and grant ownership or group memberships explicitly. Keep permissions as restrictive as possible (Principle of Least Privilege).

### ❌ Mistake 2: Leaking SSH Keys (Permissions Too Open)
If your private key (`id_rsa`) is readable by group or others, SSH will block the connection.
* **The Fix:** Private keys must have `600` permissions:
  ```bash
  chmod 600 ~/.ssh/id_rsa
  ```

---

## 2.7 Practice Scenarios
* **Scenario A:** A backup script `/opt/backup.sh` must be run by a cron job under the `backup` user. It needs to read data, but other developers shouldn't edit it.
  * *Solution:* Owner should be `backup`. Permissions should be `755` or `700`.
* **Scenario B:** An environment variable file `.env` contains AWS credentials. The web server process (user `www-data`) needs to read it.
  * *Solution:* Run `chown web-admin:www-data .env` and `chmod 640 .env`. Owner can write/read, web server can read-only, others have no access (`---`).

---

## 2.8 Chapter 2 Summary
* Permissions are split into Owner, Group, and Others.
* Actions are Read (4), Write (2), and Execute (1).
* Calculate permission octal codes by summing up values (e.g., $r(4) + w(2) + x(0) = 6$).
* `chmod` updates permissions; `chown` changes user and group ownership.
* `umask` acts as a filter subtracted from default permissions for new items.

---

## 2.9 Interview Questions
1. **Q: Explain what permission code `750` means on a directory.**
   * *A:*
     * Owner (`7` = $4+2+1$): `rwx` (Can list files, create/delete files, and enter directory).
     * Group (`5` = $4+0+1$): `r-x` (Can list files and enter directory, but cannot edit files or create/delete directories).
     * Others (`0`): `---` (Has no access; cannot list files, enter the directory, or read files).
2. **Q: If a file has permission `000` (no permissions), can root still read it?**
   * *A:* Yes. The `root` superuser bypasses all standard permission checks and can read, write, and execute any file on the system.
3. **Q: What is the default permission for a directory if the umask is set to `007`?**
   * *A:* Standard directory maximum is `777`. With umask `007`, the permissions become $777 - 007 = 770$ (`rwxrwx---`).

---

## 2.10 Hands-On Lab
**Objective:** Correct permission errors on sensitive security keys and simulate standard user boundaries.

1. Create a simulated private key file:
   ```bash
   touch /tmp/my_ssh_key
   chmod 644 /tmp/my_ssh_key
   ```
2. Verify its current permissions:
   ```bash
   ls -l /tmp/my_ssh_key
   ```
3. Secure it using the correct numeric permission code for private keys:
   ```bash
   chmod 600 /tmp/my_ssh_key
   ```
4. Confirm permissions changed to `-rw-------`:
   ```bash
   ls -l /tmp/my_ssh_key
   ```
5. Switch to a non-root user (or run `sudo -u nobody cat /tmp/my_ssh_key`) to check if access is successfully blocked.
