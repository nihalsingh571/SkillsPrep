# Chapter 7: Python Automation for DevOps

## 7.1 Why Python for DevOps?
While Bash is excellent for short scripts and command line glue, **Python** is preferred for complex automations.

Let's use a real-world analogy:
> **Analogy:** Think of automated system scripts as vehicles.
> * **Bash** is like a rugged scooter. It's incredibly fast to hop on, maneuvers through system tasks in seconds, and is perfect for short distances. But if you try to drive it across the country with massive payloads (like complex API parsing, error recovery, multi-threading, and object management), it becomes unstable and difficult to drive safely.
> * **Python** is like a robust SUV. It has seatbelts (exception handling), GPS/dashboard (logging), modular engine pieces (libraries), and comfortable seats (clean data structures). It takes a bit more configuration to start, but it handles long-distance, heavy-duty automation reliably.

### When to use Python over Bash:
1. **API Integration:** Interacting with SaaS APIs (AWS, Datadog, Slack, Jira) using JSON payloads.
2. **Advanced Data Parsing:** Extracting values from complex configuration structures (YAML, JSON, XML).
3. **Robust Error Recovery:** Gracefully catching database connection drops, timeouts, or API limits.
4. **Cross-Platform Portability:** Running the same automation script on both Linux servers and Windows/macOS local developer systems.

---

## 7.2 Python Syntax Fundamentals

### 1. Variables & Basic Types
No variable type declaration needed; Python figures it out.
```python
app_name = "frontend"  # String
port = 8080            # Integer
is_active = True       # Boolean
scale_ratio = 1.2      # Float
```

### 2. Collection Types (Data Structures)
* **Lists (Ordered, mutable):**
  ```python
  servers = ["web-01", "web-02", "db-01"]
  servers.append("redis-01")
  print(servers[0])  # Output: web-01
  ```
* **Dictionaries (Key-Value mappings):**
  ```python
  config = {"env": "prod", "port": 443, "db_connected": True}
  print(config["env"])  # Output: prod
  ```
* **Tuples (Ordered, immutable):**
  ```python
  coordinates = (54.210, 10.02)
  ```
* **Sets (Unordered, unique items):**
  ```python
  unique_ips = {"10.0.0.1", "10.0.0.2", "10.0.0.1"}
  print(unique_ips)  # Output: {'10.0.0.1', '10.0.0.2'}
  ```

### 3. File Operations (Read/Write)
Always use the `with` keyword to open files. It guarantees that the file is closed automatically once the code block finishes executing, even if errors occur.
```python
# Writing to a file
with open("deploy.log", "w") as file:
    file.write("Deployment initiated\n")

# Reading from a file
with open("deploy.log", "r") as file:
    content = file.read()
    print(content)
```

---

## 7.3 Data Formats: JSON & YAML

### JSON Parsing
```python
import json

# Parse JSON String to Python Dict
json_data = '{"service": "auth", "status": "UP"}'
parsed_dict = json.loads(json_data)
print(parsed_dict["status"])  # Output: UP

# Write Dict to JSON File
with open("status.json", "w") as f:
    json.dump(parsed_dict, f, indent=4)
```

### YAML Parsing (requires `pyyaml` library)
```python
import yaml

yaml_data = """
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
"""
# Load YAML string
parsed_yaml = yaml.safe_load(yaml_data)
print(parsed_yaml["metadata"]["name"])  # Output: web-pod
```

---

## 7.4 System Modules for OS & Commands

### 1. `os` Module
Used to interact with the underlying operating system.
```python
import os

# Get environment variable
db_host = os.environ.get("DB_HOST", "localhost")

# Check if path exists
if os.path.exists("/etc/nginx"):
    print("Nginx directory found.")
```

### 2. `subprocess` Module
Used to run shell commands from Python.
```python
import subprocess

# Run a simple shell command and capture the output
result = subprocess.run(["uname", "-r"], capture_output=True, text=True, check=True)
kernel_version = result.stdout.strip()
print(f"Kernel Version: {kernel_version}")
```

### 3. Exception Handling
Avoid script crashes by catching errors gracefully.
```python
try:
    with open("non_existent_file.txt", "r") as f:
        data = f.read()
except FileNotFoundError as e:
    print(f"Error: Config file not found. System using defaults. Technical details: {e}")
```

---

## 7.5 Complete Automation Projects

### Project 1: Nginx Log Analyzer
* **Goal:** Reads an access log file, counts hits per IP address, and reports status code counts.
```python
import re
from collections import Counter

def analyze_nginx_logs(log_file_path):
    ip_counter = Counter()
    status_counter = Counter()
    
    # Regular expression to extract IP and HTTP Status Code
    log_pattern = re.compile(
        r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?"\s(?P<status>\d{3})\s'
    )
    
    try:
        with open(log_file_path, "r") as f:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    ip_counter[match.group("ip")] += 1
                    status_counter[match.group("status")] += 1
        
        print("--- TOP 5 REQUESTING IPs ---")
        for ip, count in ip_counter.most_common(5):
            print(f"{ip}: {count} requests")
            
        print("\n--- STATUS CODE SUMMARY ---")
        for status, count in status_counter.items():
            print(f"HTTP {status}: {count} occurrences")
            
    except FileNotFoundError:
        print(f"Log file not found at {log_file_path}")

# Mock Execution setup
with open("/tmp/mock_access.log", "w") as mf:
    mf.write('192.168.1.10 - - [01/Jun/2026:09:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024\n')
    mf.write('192.168.1.10 - - [01/Jun/2026:09:00:02 +0000] "POST /login HTTP/1.1" 401 512\n')
    mf.write('10.0.0.5 - - [01/Jun/2026:09:00:05 +0000] "GET /app HTTP/1.1" 200 4096\n')

analyze_nginx_logs("/tmp/mock_access.log")
```

---

### Project 2: Disk Monitor & Alert Trigger
* **Goal:** Check root disk usage percentage and output warning.
```python
import shutil

def monitor_disk_usage(threshold_percent=85):
    # Retrieve disk statistics for root path
    total, used, free = shutil.disk_usage("/")
    used_percentage = (used / total) * 100
    
    print(f"Current Disk Space Used: {used_percentage:.2f}%")
    if used_percentage > threshold_percent:
        print(f"ALERT: Disk usage exceeds warning threshold of {threshold_percent}%!")
        # Add notification logic (Slack/Email) here.
        return True
    return False

monitor_disk_usage()
```

---

### Project 3: Website Monitoring Tool (Ping API)
* **Goal:** Checks website availability via HTTP requests and returns response latency.
```python
import requests
import time

def monitor_website(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        latency = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print(f"SUCCESS: {url} is UP. Status Code: 200. Latency: {latency:.2f}ms")
        else:
            print(f"WARNING: {url} is down. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"CRITICAL: Cannot connect to {url}. Error: {e}")

monitor_website("https://httpbin.org/get")
```

---

### Project 4: Docker Container Health Automater
* **Goal:** Queries active docker containers and lists those that are not running.
```python
import subprocess
import json

def audit_docker_containers():
    try:
        # Run Docker command querying container statuses in JSON format
        cmd = ["docker", "ps", "-a", "--format", "{{json .}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            print("No docker containers found on host.")
            return
            
        lines = result.stdout.strip().split("\n")
        for line in lines:
            container = json.loads(line)
            name = container.get("Names")
            state = container.get("State")
            status = container.get("Status")
            
            if state != "running":
                print(f"CRITICAL: Container [{name}] is down. Current Status: {status}")
            else:
                print(f"Healthy: Container [{name}] is up.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker engine is not running or docker CLI command not found.")

audit_docker_containers()
```

---

### Project 5: Kubernetes Pod Eviction Alert
* **Goal:** Queries active Kubernetes pods in namespace and detects failed states.
```python
import subprocess
import json

def check_k8s_pods(namespace="default"):
    try:
        # Request Pod statuses from Kubernetes Control Plane in JSON format
        cmd = ["kubectl", "get", "pods", "-n", namespace, "-o", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pod_data = json.loads(result.stdout)
        
        for item in pod_data.get("items", []):
            name = item["metadata"]["name"]
            status_info = item["status"]
            phase = status_info.get("phase")
            
            if phase not in ["Running", "Succeeded"]:
                reason = status_info.get("reason", "Unknown error")
                print(f"ALERT: Pod [{name}] is in failed state: {phase}. Reason: {reason}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Kubernetes CLI (kubectl) not found or cluster unreachable.")

check_k8s_pods()
```

---

### Project 6: AWS S3 Resource Expiry Auditor
* **Goal:** Audit mock AWS resources or files.
```python
import os
import time

def audit_local_artifacts(directory="/tmp"):
    # Simulated AWS S3 storage cleaner. Audits local file storage artifact expirations.
    current_time = time.time()
    retention_seconds = 7 * 86400 # 7 days
    
    print(f"Auditing artifacts in {directory} older than 7 days...")
    for root, dirs, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            try:
                mtime = os.path.getmtime(filepath)
                age = current_time - mtime
                if age > retention_seconds:
                    print(f"Artifact {name} expired (Age: {age/86400:.1f} days). Deleting...")
                    # os.remove(filepath)
            except OSError:
                continue

audit_local_artifacts()
```

---

## 7.6 Chapter 7 Summary
* Python provides structured, scalable, and cross-platform automation capabilities for DevOps engineers.
* Common libraries include `os` (file system check), `subprocess` (shell commands execution), and `requests` (API interaction).
* Configuration models rely on parsing native YAML and JSON configurations.
* Application error recovery is handled via `try-except` blocks.

---

## 7.7 Interview Questions
1. **Q: How does `subprocess.run` differ from `os.system` in Python?**
   * *A:* `os.system` simply spawns the command in a subshell, routing the command output directly to the terminal stdout, and returns the status exit code. `subprocess.run` is a modern interface that allows you to pipe stdout and stderr to variables, execute arguments safely as lists to prevent shell injection, and check for execution exit statuses dynamically.
2. **Q: Why is Python preferred over Bash for REST API parsing?**
   * *A:* Parsing API responses (which are standard JSON formats) is extremely complex in Bash, requiring external utilities like `jq` or convoluted grep logic. Python natively supports dictionary structures and lists, and provides a built-in `json` module, making parsing simple.
3. **Q: How can you write clean, error-resilient automation scripts in Python?**
   * *A:* Use `try-except` blocks for all networking, API, and file inputs. Always specify request timeouts in the `requests` library, use the `logging` framework instead of print statements, and use `with` statements to manage system file buffers.

---

## 7.8 Hands-On Lab
**Objective:** Create a Python script that reads system settings, tests an API endpoint, and handles error responses.

1. Write a script `health.py`:
   ```python
   import os
   import requests
   import sys

   def check_health():
       target_url = os.environ.get("MONITOR_URL", "https://httpbin.org/status/200")
       print(f"Testing connectivity to {target_url}...")
       try:
           response = requests.get(target_url, timeout=3)
           if response.status_code == 200:
               print("SUCCESS: Target is operational.")
               sys.exit(0)
           else:
               print(f"FAILURE: Received status {response.status_code}")
               sys.exit(1)
       except requests.RequestException as e:
           print(f"CRITICAL ERROR: Connection failed. Details: {e}")
           sys.exit(2)

   if __name__ == "__main__":
       check_health()
   ```
2. Execute the script natively using your terminal:
   ```bash
   python3 health.py
   ```
3. Set the environment variable `MONITOR_URL` to an invalid address, execute the script again, and verify that the exception error handler catches it cleanly.
