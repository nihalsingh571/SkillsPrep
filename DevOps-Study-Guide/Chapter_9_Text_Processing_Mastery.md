# Chapter 9: Text Processing Mastery

## 9.1 Introduction
In DevOps, server output is text stream output. Whether you are parsing system statuses, checking configurations, analyzing access logs, or validating CI/CD build outputs, you must master three core tools: **grep**, **sed**, and **awk**.

Let's use a real-world analogy:
> **Analogy:** Imagine a huge pile of physical employee directories.
> * **`grep`** is a high-speed scanner. It searches the pile and pulls out every page containing the word "Engineer". (Filter lines).
> * **`sed`** is an editor with a red pen. It goes through the pages and replaces "NY" with "New York", or deletes empty lines. (Stream Editor / Substitutions).
> * **`awk`** is a data analyst with a calculator. It reads columns of data (like salary and department), sums them up, checks if an employee is in "Finance", and prints a formatted monthly budget report. (Column and Report Generator).

---

## 9.2 `grep` (Global Regular Expression Print)
* **Definition:** Searches files or input streams for lines matching a pattern.
* **Syntax:** `grep [options] <pattern> [file]`
* **Options:**
  * `-i` (Case insensitive).
  * `-v` (Invert match: show lines that do NOT match).
  * `-E` (Extended Regular Expression: enables advanced patterns like `(this|that)`).
  * `-o` (Output ONLY the matching text, not the entire line).
  * `-c` (Count matching lines).
  * `-r` (Recursive search in directories).

### Basic & Regex Examples
* **Example 1:** Find any occurrences of IP addresses in a log file:
  ```bash
  echo "Access from 192.168.1.10" > /tmp/access.log
  grep -E -o "([0-9]{1,3}\.){3}[0-9]{1,3}" /tmp/access.log
  ```
  *Expected Output:*
  ```text
  192.168.1.10
  ```
* **Example 2:** Exclude comments and empty lines when viewing a configuration file:
  ```bash
  echo -e "# Port config\nPORT=80\n\n# Timeout\nTIMEOUT=30" > /tmp/app.conf
  grep -E -v "^(#|$)" /tmp/app.conf
  ```
  *Expected Output:*
  ```text
  PORT=80
  TIMEOUT=30
  ```

---

## 9.3 `sed` (Stream Editor)
* **Definition:** Parses and transforms text streams line-by-line. Used for search, replace, deletion, and insertion.
* **Syntax:** `sed [options] 'command' [file]`
* **Commands:**
  * `s/search/replace/g` (Substitute search with replace globally).
  * `/pattern/d` (Delete lines containing pattern).
* **Options:** `-i` (In-place edit: modifies the source file directly. **Use with caution**).

### Real-world DevOps Examples
* **Example 1:** Change application environment setting from `dev` to `prod` in-place:
  ```bash
  echo "ENV=dev" > /tmp/env.conf
  sed -i 's/ENV=dev/ENV=prod/g' /tmp/env.conf
  cat /tmp/env.conf
  ```
  *Expected Output:*
  ```text
  ENV=prod
  ```
* **Example 2:** Delete lines containing the pattern `DEBUG` from log outputs:
  ```bash
  echo -e "INFO: Boot\nDEBUG: Loading module\nERROR: Failed connection" > /tmp/debug.log
  sed '/DEBUG/d' /tmp/debug.log
  ```
  *Expected Output:*
  ```text
  INFO: Boot
  ERROR: Failed connection
  ```

---

## 9.4 `awk` (AHO, WEINBERGER, KERNIGHAN)
* **Definition:** A complete scripting language designed for pattern scanning and column-oriented text processing.
* **Syntax:** `awk 'pattern { action }' [file]`
* **Core Concepts:**
  * `$0` (Represents the whole line).
  * `$1`, `$2`, `$3`... (Represent the 1st, 2nd, 3rd columns).
  * `FS` (Input Field Separator; defaults to whitespace). Use `-F` to specify (e.g. `-F:` for csv/etc).
  * `NR` (Number of Records: current line number).
  * `NF` (Number of Fields: total columns in the current line).

### Fields, Conditions, and Reports
* **Example 1:** Extract usernames and their default shells from `/etc/passwd` (fields separated by `:`):
  ```bash
  head -n 2 /etc/passwd | awk -F: '{print $1 " uses shell " $7}'
  ```
  *Expected Output:*
  ```text
  root uses shell /bin/bash
  daemon uses shell /usr/sbin/nologin
  ```
* **Example 2:** Print processes using more than 10% CPU from `ps` command (row filtration):
  ```bash
  ps aux | awk '$3 > 10.0 {print "PID: " $2 " is using CPU: " $3 "%"}'
  ```

---

## 9.5 Combining grep + sed + awk
By combining these tools, you can create powerful analytical pipelines.

### Combined Pipeline Example:
Identify which unique IP address has made the most failed requests from a log file:
```bash
# Simulating access logs
echo -e "192.168.1.10 - 404\n10.0.0.5 - 200\n192.168.1.10 - 404\n192.168.1.12 - 404" > /tmp/nginx.log

grep "404" /tmp/nginx.log | awk '{print $1}' | sort | uniq -c | sort -nr
```
*Expected Output:*
```text
      2 192.168.1.10
      1 192.168.1.12
```

---

## 9.6 100 Practical Command One-Liners

### Log Analysis & Searching (1-20)
1. View nginx traffic: `tail -f /var/log/nginx/access.log | grep "200"`
2. Count total errors: `grep -c "ERROR" /var/log/syslog`
3. Exclude logs containing `INFO`: `grep -v "INFO" /var/log/syslog`
4. Search logs ignoring case: `grep -i "exception" application.log`
5. Extract IP addresses from log: `grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log`
6. Count occurrences of each IP address: `grep -oE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log | sort | uniq -c | sort -nr`
7. Find lines containing either `CRITICAL` or `FATAL`: `grep -E "CRITICAL|FATAL" sys.log`
8. Show 3 lines after matching search line: `grep -A 3 "NullPointerException" app.log`
9. Show 2 lines before matching line: `grep -B 2 "Exception" app.log`
10. Show context (1 line before and after): `grep -C 1 "Connection reset" app.log`
11. List filenames matching "ERROR": `grep -l "ERROR" /var/log/*.log`
12. List filenames NOT matching "ERROR": `grep -L "ERROR" /var/log/*.log`
13. Extract all email addresses: `grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" users.txt`
14. Search logs containing dates: `grep -E "2026-06-0[1-5]" app.log`
15. Search specific service systemd logs: `journalctl | grep "sshd"`
16. Find logs with line numbers: `grep -n "FATAL" system.log`
17. Print matching lines showing position bytes: `grep -b "ERROR" system.log`
18. Grep logs matching exact word only: `grep -w "error" system.log`
19. Count successful GET requests: `grep "GET" access.log | grep -c "200"`
20. Check cron job runs: `grep "CRON" /var/log/syslog`

### System Monitoring & Performance (21-40)
21. Extract active RAM usage: `free -m | awk 'NR==2 {print "Used RAM: " $3 "MB/" $2 "MB"}'`
22. Monitor CPU idle percentage: `top -bn1 | grep Cpu | awk '{print "Idle CPU: " $8 "%"}'`
23. Find top 5 memory processes: `ps aux | sort -rn -k 4 | head -n 5 | awk '{print $2, $4, $11}'`
24. List processes running under user root: `ps aux | awk '$1 == "root" {print $2, $11}'`
25. Read CPU core count: `grep -c ^processor /proc/cpuinfo`
26. Get system load average: `cat /proc/loadavg | awk '{print "1min Load: " $1}'`
27. Count active TCP connections: `ss -t | wc -l`
28. Find listening ports: `ss -plnt | awk '{print $4}' | cut -d: -f2 | sort -u`
29. Get root disk utilization %: `df -h / | awk 'NR==2 {print $5}'`
30. List folders using > 1GB space: `du -h --max-depth=2 /var | grep -E "[0-9.]*G"`
31. Print network card speed: `ethtool eth0 | grep -i speed`
32. Check system reboot history: `last reboot | head -n 5`
33. Get hostname: `hostname`
34. Find Zombie processes: `ps aux | awk '$8=="Z"'`
35. Terminate all zombie processes: `ps -ef | grep defunct | grep -v grep | awk '{print $3}' | xargs kill -9`
36. Trace disk read/write load: `iostat -d 1 2`
37. Count established web ports: `ss -an | grep -c :80`
38. Extract interface IP address: `ip a show eth0 | grep "inet " | awk '{print $2}'`
39. Retrieve MAC address: `ip link show eth0 | grep "link/ether" | awk '{print $2}'`
40. Check active swap space: `swapon --show`

### File & Text Editing (41-60)
41. Replace config value in file: `sed -i 's/PORT=80/PORT=8080/g' config.env`
42. Delete all blank lines: `sed -i '/^$/d' input.txt`
43. Delete comments from script: `sed -i '/^#/d' build.sh`
44. Delete lines 5 to 10: `sed '5,10d' input.txt`
45. Insert comment at line 1: `sed -i '1i# Start of Configuration' settings.conf`
46. Append warning at end of file: `sed -i '$a# WARNING: Auto-generated' settings.conf`
47. Convert lowercase file to uppercase: `tr 'a-z' 'A-Z' < input.txt`
48. Print line 15 of file: `sed -n '15p' input.txt`
49. Remove trailing carriage returns: `sed -i 's/\r//' script.sh`
50. Extract specific JSON key: `grep -o '"version": "[^"]*' package.json | cut -d'"' -f4`
51. Replace multiple spaces with one space: `sed 's/  */ /g' input.txt`
52. Swap column 1 and column 2: `awk '{print $2, $1}' input.txt`
53. Replace delimiters (comma to tab): `sed 's/,/\t/g' file.csv`
54. Remove leading whitespaces: `sed 's/^[ \t]*//' input.txt`
55. Remove trailing whitespaces: `sed 's/[ \t]*$//' input.txt`
56. Append text to lines matching regex: `sed '/target_host/s/$/ # active/' hosts`
57. Prefix string to matching line: `sed '/DB_PASS/s/^/#/' config.env`
58. Print unique rows only: `sort -u file.txt`
59. Exclude duplicate consecutive lines: `uniq input.txt`
60. Generate 10-character random password: `openssl rand -base64 12 | head -c 10`

### Security Auditing (61-80)
61. Find users with UID 0 (Root access): `awk -F: '$3 == 0 {print $1}' /etc/passwd`
62. Find empty password accounts: `sudo awk -F: '($2 == "") {print $1}' /etc/shadow`
63. Trace failed SSH password tries: `grep "Failed password" /var/log/auth.log`
64. Find blocked firewalled packets: `dmesg | grep -i "drop"`
65. List users who run sudo commands: `grep "COMMAND=" /var/log/auth.log | awk '{print $6}' | sort -u`
66. List all files with SUID bit: `find / -perm /4000 -type f 2>/dev/null`
67. Find world-writable files: `find / -perm -0002 -type f -not -path "/proc/*" 2>/dev/null`
68. Audit `/etc/shadow` file permissions: `stat -c "%a %n" /etc/shadow` (Expected: 600 or 000).
69. Check active root login shells: `grep -v "nologin" /etc/passwd`
70. Track SSH key logins: `grep "Accepted publickey" /var/log/auth.log`
71. Extract failed user login lists: `grep "Invalid user" /var/log/auth.log | awk '{print $8}' | sort -u`
72. List files updated in last 24 hours: `find /etc -mtime -1 -type f`
73. Verify SSL certificate expiration local: `openssl x509 -enddate -noout -in cert.pem`
74. Find hidden files in `/tmp`: `find /tmp -name ".*"`
75. Locate files not owned by any user: `find / -nouser 2>/dev/null`
76. Search files not owned by any group: `find / -nogroup 2>/dev/null`
77. Extract ssh config parameters: `grep -E -v "^(#|$)" /etc/ssh/sshd_config`
78. List current crontabs for all users: `for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null; done`
79. Audit list of running ports: `ss -plut`
80. Audit loaded system modules: `lsmod`

### Infrastructure & CI/CD Pipelines (81-100)
81. Check Kubernetes pods statuses: `kubectl get pods | awk 'NR>1 {print $1 " is " $3}'`
82. List pods in Error state: `kubectl get pods | awk '$3 == "Error" {print $1}'`
83. Count running pods: `kubectl get pods | grep -c "Running"`
84. Extract container image tags from deployment yaml: `grep "image:" deployment.yaml | awk '{print $2}'`
85. Get docker container logs with timestamp: `docker logs --timestamps container_id`
86. Remove dangling docker images: `docker rmi $(docker images -f "dangling=true" -q)`
87. Extract host IP dynamically: `curl -s https://ifconfig.me`
88. Read Git current branch name: `git branch --show-current`
89. Compare configuration environments: `diff dev.env prod.env`
90. Extract values from Terraform state: `grep -E -o '"id": "[^"]*"' terraform.tfstate`
91. Check Nginx configuration syntax: `nginx -t`
92. Get AWS instance public IP: `curl -s http://169.254.169.254/latest/meta-data/public-ipv4`
93. Count Kubernetes namespace count: `kubectl get ns | awk 'NR>1' | wc -l`
94. Check Ansible syntax check: `ansible-playbook playbook.yml --syntax-check`
95. Verify HTTP Status code of internal service: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080`
96. Match AWS tag names: `aws ec2 describe-instances | grep -i "Value"`
97. Sort and display list of container memory sizes: `docker stats --no-stream | awk 'NR>1 {print $1, $3}'`
98. Clean up stopped docker containers: `docker rm $(docker ps -a -q -f status=exited)`
99. Search for security keys committed to files: `grep -rnw . -e "AWS_SECRET_ACCESS_KEY" --exclude-dir=.git`
100. Print current UTC time in deployment log format: `date -u +"%Y-%m-%dT%H:%M:%SZ"`

---

## 9.7 Chapter 9 Summary
* `grep` filters lines of text streams using string matches or regular expressions.
* `sed` performs stream modifications (substitutions, insertions, deletions) line-by-line.
* `awk` handles field extraction, computations, and structured reporting.
* Connecting these utilities using Unix pipes (`|`) allows DevOps engineers to build complex automated parsers.

---

## 9.8 Interview Questions
1. **Q: How do you extract columns from a command's output?**
   * *A:* Use `awk '{print $N}'` where `N` is the column index (1-indexed). Alternatively, use the `cut` command (e.g. `cut -d' ' -fN`).
2. **Q: How do you replace every occurrence of a string in a file without opening an editor?**
   * *A:* Use `sed -i 's/old/new/g' filename` to substitute inline.
3. **Q: What does the `sort | uniq -c` sequence do?**
   * *A:* `sort` rearranges lines alphabetically/numerically so duplicate rows sit next to each other. `uniq -c` then aggregates contiguous duplicate lines and prefixes each row with its occurrence count.
