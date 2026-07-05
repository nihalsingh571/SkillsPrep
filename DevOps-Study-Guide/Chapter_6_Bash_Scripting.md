# Chapter 6: Bash Scripting

## 6.1 Why Bash Matters
In DevOps, **automation** is the core engine. While Python or Go are used for large application development, **Bash (Bourne Again SHell)** is the native script language of the Linux terminal. 

Let's use a real-world analogy:
> **Analogy:** Think of operating system commands as tools in a workshop (hammer, saw, drill).
> * Running commands interactively is like pick up each tool manually to make a chair.
> * A **Bash script** is a pre-programmed robotic assembly arm. It links the tools in a specific sequence, checks if the wood is cut correctly (conditionals), repeats the cuts for four chair legs (loops), and halts automatically if a tool breaks (error handling).

### Shell Basics & Configuration
A shell script is a plain text file containing a list of commands. It starts with a **Shebang** (`#!/bin/bash`) as the very first line, which tells the operating system which interpreter to use to execute the script.

---

## 6.2 Bash Syntax Reference

### 1. Variables
Bash has no strict data types; variables are treated as strings or integers depending on context. Do not use spaces around the `=` sign during assignment.
```bash
NAME="production-server-01"
PORT=8080
echo "Connecting to $NAME on port $PORT"
```

### 2. Environment Variables
System-wide variables inherited by child processes. Define them using `export`:
```bash
export DB_PASSWORD="SuperSecretPassword123"
```

### 3. Conditionals (`if`, `else`, `elif`)
Used to test expressions. Note the spaces inside brackets:
```bash
if [ "$PORT" -eq 8080 ]; then
    echo "Default port active."
elif [ "$PORT" -eq 443 ]; then
    echo "Secure port active."
else
    echo "Alternative port active."
fi
```
*Comparison operators for integers:* `-eq` (equal), `-ne` (not equal), `-gt` (greater than), `-lt` (less than), `-ge` (greater or equal), `-le` (less or equal).

### 4. Loops (`for`, `while`, `until`)
* **For Loop (Iterating over lists):**
  ```bash
  for host in web01 web02 db01; do
      echo "Checking host: $host"
  done
  ```
* **While Loop (Runs while condition is true):**
  ```bash
  counter=1
  while [ $counter -le 3 ]; do
      echo "Attempt: $counter"
      counter=$((counter + 1))
  done
  ```

### 5. Functions & Arguments
Functions bundle reusable logic. Parameters are accessed via positional arguments `$1`, `$2`, etc.
```bash
log_message() {
    local level=$1
    local msg=$2
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] - $msg"
}

log_message "INFO" "Application started."
```

### 6. Arrays
```bash
servers=("srv1" "srv2" "srv3")
echo "First server: ${servers[0]}"
echo "All servers: ${servers[@]}"
```

### 7. Exit Codes
Every command returns an exit status code between `0` (success) and `255` (error). Read the exit code of the last run command using `$?`.
```bash
mkdir /root/secret_dir
if [ $? -ne 0 ]; then
    echo "Failed to create directory. Permission denied."
fi
```

### 8. Cron Jobs
Cron is a time-based job scheduler. Set user cron jobs using `crontab -e`.
```text
# Minute Hour DayOfMonth Month DayOfWeek Command
# Run backup script daily at 2:00 AM
0 2 * * * /opt/backup.sh
```

### 9. Error Handling & Debugging
* **`set -e`**: Exit immediately if any command returns a non-zero exit status.
* **`set -u`**: Exit if the script attempts to use an uninitialized variable.
* **`set -x`**: Print commands and their arguments as they are executed (highly useful for tracing bugs).

---

## 6.3 20 Beginner Scripts

### 1. Hello World
```bash
#!/bin/bash
echo "Hello, DevOps World!"
```

### 2. Print System Info
```bash
#!/bin/bash
echo "Current User: $USER"
echo "Hostname: $HOSTNAME"
echo "Uptime: $(uptime -p)"
```

### 3. Simple Variable Assignment
```bash
#!/bin/bash
GREETING="Welcome to Bash Scripting"
echo "$GREETING, $USER"
```

### 4. User Input Prompt
```bash
#!/bin/bash
read -p "Enter your name: " username
echo "Greetings, $username!"
```

### 5. Check if File Exists
```bash
#!/bin/bash
FILE="/etc/resolv.conf"
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else
    echo "$FILE does not exist."
fi
```

### 6. Check if Directory Exists
```bash
#!/bin/bash
DIR="/var/log"
if [ -d "$DIR" ]; then
    echo "Directory $DIR exists."
fi
```

### 7. Basic Addition
```bash
#!/bin/bash
num1=10
num2=20
sum=$((num1 + num2))
echo "Sum is: $sum"
```

### 8. List Files in Current Directory
```bash
#!/bin/bash
echo "Listing files:"
for file in *; do
    echo "File found: $file"
done
```

### 9. File Creation with Current Date
```bash
#!/bin/bash
date_str=$(date +%Y-%m-%d)
touch "report_${date_str}.txt"
echo "Created report_${date_str}.txt"
```

### 10. Simple Argument Reader
```bash
#!/bin/bash
echo "Script name: $0"
echo "First Argument: $1"
echo "Second Argument: $2"
```

### 11. Read File Line by Line
```bash
#!/bin/bash
touch /tmp/names.txt
echo -e "John\nAlice\nBob" > /tmp/names.txt
while read -r line; do
    echo "Name: $line"
done < /tmp/names.txt
```

### 12. Command Success Checker
```bash
#!/bin/bash
ping -c 1 8.8.8.8 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Internet connection active."
else
    echo "No internet connection."
fi
```

### 13. System Memory Quick Check
```bash
#!/bin/bash
free -h
```

### 14. Disk Space Quick Check
```bash
#!/bin/bash
df -h /
```

### 15. Simple Wait Timer
```bash
#!/bin/bash
echo "Waiting for 5 seconds..."
sleep 5
echo "Done!"
```

### 16. Basic Exit Code Set
```bash
#!/bin/bash
echo "Exiting with code 0"
exit 0
```

### 17. Simple Case Switch
```bash
#!/bin/bash
action=$1
case $action in
    start) echo "Starting service..." ;;
    stop) echo "Stopping service..." ;;
    *) echo "Usage: $0 {start|stop}" ;;
esac
```

### 18. Environment Variable Checker
```bash
#!/bin/bash
if [ -z "$DB_HOST" ]; then
    echo "DB_HOST variable is not set."
else
    echo "Connecting to $DB_HOST"
fi
```

### 19. Generate Random Number
```bash
#!/bin/bash
echo "Random number: $RANDOM"
```

### 20. Count Number of Files
```bash
#!/bin/bash
count=$(ls -1 | wc -l)
echo "Total files: $count"
```

---

## 6.4 20 Intermediate Scripts

### 21. Loop Through Array of IPs
```bash
#!/bin/bash
ips=("8.8.8.8" "1.1.1.1" "127.0.0.1")
for ip in "${ips[@]}"; do
    ping -c 1 "$ip" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$ip is reachable"
    else
        echo "$ip is down"
    fi
done
```

### 22. Interactive Menu
```bash
#!/bin/bash
echo "1. Check Disk"
echo "2. Check Memory"
echo "3. Exit"
read -p "Select option: " opt
case $opt in
    1) df -h ;;
    2) free -m ;;
    3) exit 0 ;;
esac
```

### 23. Log Message Function
```bash
#!/bin/bash
log_event() {
    echo "[$(date)] [LOG]: $1"
}
log_event "Deploy initialization"
```

### 24. Command Line Option Parser
```bash
#!/bin/bash
while getopts "f:v" opt; do
  case $opt in
    f) file=$OPTARG ;;
    v) verbose=true ;;
    *) echo "Invalid option" ;;
  esac
done
echo "File: $file, Verbose: $verbose"
```

### 25. Check if Process is Running
```bash
#!/bin/bash
service="nginx"
if pgrep "$service" >/dev/null; then
    echo "$service daemon running."
else
    echo "$service daemon is STOPPED."
fi
```

### 26. Dynamic Backup Directory Creator
```bash
#!/bin/bash
backup_dir="/tmp/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
echo "Created backup folder $backup_dir"
```

### 27. Search for Pattern in Log File
```bash
#!/bin/bash
logfile="/var/log/syslog"
if grep -q "ERROR" "$logfile" 2>/dev/null; then
    echo "Errors found in $logfile"
else
    echo "No errors found."
fi
```

### 28. Automated Server Setup Utility
```bash
#!/bin/bash
echo "Installing update..."
sudo apt-get update -y > /dev/null
echo "Installing git..."
sudo apt-get install git -y > /dev/null
```

### 29. String Pattern Extractor
```bash
#!/bin/bash
email="devops@example.com"
domain=$(echo "$email" | cut -d'@' -f2)
echo "Domain is: $domain"
```

### 30. Calculate File Sizes
```bash
#!/bin/bash
find . -type f -exec du -sh {} +
```

### 31. Archive Logs Older Than 7 Days
```bash
#!/bin/bash
find /tmp/logs -name "*.log" -mtime +7 -exec tar -rvf archive.tar {} \;
```

### 32. Multi-file Content Append
```bash
#!/bin/bash
for file in /tmp/*.conf; do
    [ -e "$file" ] || continue
    echo "# Config verified" >> "$file"
done
```

### 33. Disk Usage Percentage Monitor
```bash
#!/bin/bash
usage=$(df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1)
echo "Root disk usage is $usage%"
```

### 34. Check Password Strength
```bash
#!/bin/bash
read -s -p "Enter password: " pass
echo
if [ ${#pass} -lt 8 ]; then
    echo "Weak password: Less than 8 characters."
else
    echo "Password strength OK."
fi
```

### 35. Simple JSON Extractor (No JQ)
```bash
#!/bin/bash
json='{"status":"UP","version":"1.0"}'
status=$(echo "$json" | grep -o '"status":"[^"]*' | grep -o '[^"]*$')
echo "Status: $status"
```

### 36. File Encryption Script
```bash
#!/bin/bash
# Encrypts a text file using openssl
echo "Encrypting file..."
echo "SecretData" > sensitive.txt
openssl enc -aes-256-cbc -salt -in sensitive.txt -out sensitive.enc -k "mypass" -pbkdf2
rm sensitive.txt
```

### 37. Send HTTP Post Alert
```bash
#!/bin/bash
webhook_url="http://httpbin.org/post"
curl -X POST -H "Content-Type: application/json" -d '{"text":"System Alert!"}' "$webhook_url"
```

### 38. Network Port Open Checker
```bash
#!/bin/bash
host="localhost"
port=22
nc -z "$host" "$port"
if [ $? -eq 0 ]; then
    echo "Port $port is open on $host"
else
    echo "Port $port is closed on $host"
fi
```

### 39. Auto-clean Temporary Files
```bash
#!/bin/bash
echo "Cleaning tmp folder..."
find /tmp -type f -atime +2 -delete
```

### 40. Execute Script with Timeout
```bash
#!/bin/bash
timeout 5s sleep 10
if [ $? -eq 124 ]; then
    echo "Command timed out after 5 seconds."
fi
```

---

## 6.5 20 Advanced DevOps Scripts

### 41. Automated Rolling Database Backup & Cleanup
```bash
#!/bin/bash
# Description: Automated MySQL Backup with retention rotation
set -euo pipefail
BACKUP_DIR="/opt/db_backups"
DB_USER="root"
DB_PASS="secretpass"
DB_NAME="production_db"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"
# Mock backup creation
echo "Backing up database $DB_NAME..."
echo "MOCK SQL DUMP CONTENT" > "$BACKUP_DIR/${DB_NAME}_$DATE.sql"

# Retention check: Delete backups older than 14 days
find "$BACKUP_DIR" -name "${DB_NAME}_*.sql" -mtime +14 -type f -delete
echo "Backup complete. Old records cleaned."
```

### 42. Server Health Check & Slack Notification
```bash
#!/bin/bash
# Description: Evaluates server parameters and alerts if resource thresholds are exceeded.
set -euo pipefail
THRESHOLD=80
SLACK_WEBHOOK="https://hooks.slack.com/services/T00/B00/X00"

cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')

if (( $(echo "$cpu_usage > $THRESHOLD" | bc -l) )) || (( $(echo "$mem_usage > $THRESHOLD" | bc -l) )); then
    payload="{\"text\": \"🚨 WARNING: High Resource Load! CPU: ${cpu_usage}%, Memory: ${mem_usage}%\"}"
    # In practice: curl -X POST -H 'Content-type: application/json' --data "$payload" "$SLACK_WEBHOOK"
    echo "Alert triggered: $payload"
fi
```

### 43. Clean Log Files Exceeding Maximum Size
```bash
#!/bin/bash
# Description: Truncates log files exceeding 100MB to avoid disk fill.
MAX_SIZE_KB=102400 # 100MB
LOG_DIR="/var/log/app"

mkdir -p "$LOG_DIR"
touch "$LOG_DIR/app.log"
# Populate mock size
truncate -s 120M "$LOG_DIR/app.log"

find "$LOG_DIR" -name "*.log" -type f | while read -r logfile; do
    size=$(du -k "$logfile" | cut -f1)
    if [ "$size" -gt "$MAX_SIZE_KB" ]; then
        echo "Truncating $logfile (Current Size: ${size}KB)"
        cat /dev/null > "$logfile"
    fi
done
```

### 44. AWS EC2 Instance State Monitor & Auto-Start
```bash
#!/bin/bash
# Description: Checks status of target AWS instance and starts it if stopped.
INSTANCE_ID="i-0abcdef1234567890"

# Mock AWS CLI check
echo "Querying AWS EC2 status..."
state="stopped" # Mock output

if [ "$state" == "stopped" ]; then
    echo "Starting instance $INSTANCE_ID..."
    # aws ec2 start-instances --instance-ids "$INSTANCE_ID"
fi
```

### 45. Kubernetes Deployment Health Validator
```bash
#!/bin/bash
# Description: Queries Kubernetes deployment rollout status and rolls back if failed.
DEPLOYMENT_NAME="web-frontend"
NAMESPACE="prod"

echo "Checking rollout status..."
# In practice: kubectl rollout status deployment/$DEPLOYMENT_NAME -n $NAMESPACE --timeout=60s
# Mocking a failure:
rollout_status="failed"

if [ "$rollout_status" != "success" ]; then
    echo "Rollout failed! Reverting deployment..."
    # kubectl rollout undo deployment/$DEPLOYMENT_NAME -n $NAMESPACE
fi
```

### 46. Nginx Log Traffic Analyzer
```bash
#!/bin/bash
# Description: Identifies top 10 IP addresses requesting the website.
LOG_FILE="/tmp/nginx_access.log"
echo -e "192.168.1.50 - -\n192.168.1.50 - -\n10.0.0.12 - -" > "$LOG_FILE"

echo "Top Requesting IPs:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 10
```

### 47. S3 Bucket Synchronization & Logging
```bash
#!/bin/bash
SOURCE_DIR="/var/www/uploads"
BUCKET_NAME="s3://app-production-uploads"

echo "Syncing uploads to S3 bucket $BUCKET_NAME..."
# aws s3 sync "$SOURCE_DIR" "$BUCKET_NAME" --delete
echo "Sync completed at $(date)" >> /var/log/s3_sync.log
```

### 48. Git Repo Status Checker
```bash
#!/bin/bash
# Description: Iterates through local repositories and checks for uncommitted changes.
cd /tmp
git init -b main mock_repo >/dev/null
cd mock_repo
touch file.txt
if [ -n "$(git status --porcelain)" ]; then
    echo "Uncommitted changes detected in mock_repo."
fi
```

### 49. CPU Load Average Alerter
```bash
#!/bin/bash
load1min=$(awk '{print $1}' /proc/loadavg)
cores=$(nproc)
if (( $(echo "$load1min > $cores" | bc -l) )); then
    echo "SYSTEM OVERLOAD: 1-minute load average ($load1min) exceeds CPU core capacity ($cores)."
fi
```

### 50. Port Listener Validator
```bash
#!/bin/bash
required_ports=(80 443 3306)
for port in "${required_ports[@]}"; do
    if ! ss -plnt | grep -q ":$port "; then
        echo "CRITICAL: Port $port is NOT listening!"
    fi
done
```

### 51. Auto-healing Application Process Daemon
```bash
#!/bin/bash
# Description: Restarts the process if it goes down.
process="nginx"
if ! pgrep "$process" >/dev/null; then
    echo "Warning: $process is down. Attempting restart..."
    # sudo systemctl restart nginx
fi
```

### 52. Docker Container Pruner
```bash
#!/bin/bash
# Description: Cleans unused containers, networks, and images to free up space.
echo "Pruning unused Docker assets..."
# docker system prune -af --volumes
```

### 53. SSL Certificate Expiry Alert
```bash
#!/bin/bash
# Description: Validates certificate expiration dates.
domain="google.com"
expiry_date=$(echo | openssl s_client -connect ${domain}:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
echo "Domain: $domain expires on: $expiry_date"
```

### 54. Environment Config Difference Checker
```bash
#!/bin/bash
# Description: Compares active config vs template.
echo "Checking config drift..."
echo "PORT=8080" > /tmp/conf1
echo "PORT=9090" > /tmp/conf2
diff /tmp/conf1 /tmp/conf2 || echo "Config drift detected!"
```

### 55. CI/CD Code Static Analysis Runner
```bash
#!/bin/bash
# Description: Scans scripts in the directory for syntax issues.
echo "Starting ShellCheck scan..."
find . -name "*.sh" | while read -r script; do
    # shellcheck "$script" || echo "Lint errors in $script"
    bash -n "$script"
done
```

### 56. Multi-Server Disk Space Collector
```bash
#!/bin/bash
# Description: Query disk space on multiple hosts via SSH.
servers=("web01" "web02" "db01")
for host in "${servers[@]}"; do
    # ssh -o ConnectTimeout=5 "$host" "df -h /" || echo "Failed to reach $host"
    echo "Connecting to $host..."
done
```

### 57. Tarball Extraction & Verification
```bash
#!/bin/bash
tarfile="/tmp/app.tar.gz"
dest="/opt/app"
# tar -xzf "$tarfile" -C "$dest"
# sha256sum -c app.sha256
echo "Archive extracted and validated."
```

### 58. Automatic IP Blacklister
```bash
#!/bin/bash
# Description: Blacklists IPs making too many bad requests.
LOG="/tmp/bad_req.log"
echo -e "192.168.1.100\n192.168.1.100\n192.168.1.100" > "$LOG"
awk '{print $1}' "$LOG" | sort | uniq -c | while read -r count ip; do
    if [ "$count" -gt 2 ]; then
        echo "Blocking malicious IP $ip (Requests count: $count)"
        # iptables -A INPUT -s $ip -j DROP
    fi
done
```

### 59. Automated Application Deployment Rollout
```bash
#!/bin/bash
set -e
echo "Fetching code updates..."
# git pull origin main
echo "Building app assets..."
# npm run build
echo "Restarting application service..."
# sudo systemctl restart node-app
echo "Deployment successful!"
```

### 60. Host Down Self-healing Gateway DNS Failover
```bash
#!/bin/bash
# Description: Switches system nameservers if primary DNS fails.
primary_dns="8.8.8.8"
fallback_dns="1.1.1.1"

if ! ping -c 2 "$primary_dns" >/dev/null; then
    echo "Primary DNS down! Writing fallback nameserver $fallback_dns to resolv.conf"
    # echo "nameserver $fallback_dns" > /etc/resolv.conf
fi
```

---

## 6.6 Chapter 6 Summary
* Bash scripts translate interactive terminal commands into structured, automated workflows.
* Every script starts with a shebang `#!/bin/bash`.
* Code logic is controlled via variables, conditional comparisons (`-eq`, `-lt`), loops (`for`, `while`), and functions with arguments.
* Error control is managed using command exit codes (`$?`) and debug flags (`set -e`, `set -x`).

---

## 6.7 Interview Questions
1. **Q: What is the meaning of `set -euo pipefail` in Bash scripts?**
   * *A:*
     * `-e`: Exit immediately if any command returns a non-zero exit status.
     * `-u`: Exit if the script attempts to use an undefined variable.
     * `-o pipefail`: Forces a pipeline (e.g. `cmd1 | cmd2`) to return the exit code of the first failing command in the chain, rather than the final command.
2. **Q: How can you pass arguments to a script and read them?**
   * *A:* Arguments are read as positional variables: `$1` is the first parameter, `$2` is the second, up to `$9`. All arguments can be read at once using `$@`, and the total count of inputs is stored in `$#`.
3. **Q: What is the difference between `[` and `[[` in Bash?**
   * *A:* `[` is a synonym for the standard test command (`/usr/bin/test`). `[[` is an advanced Bash-specific keyword shell extension that supports regex matching (`=~`), logical operators (`&&`, `||`) without escaping, and does not perform word splitting on empty strings.
