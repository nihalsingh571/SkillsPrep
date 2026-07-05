# Chapter 3: Process Management

## 3.1 What is a Process?
A **Process** is a running instance of a program in memory. Every time you enter a command, launch a service, or execute a script, the Linux kernel sets up a resource environment (including memory, file descriptors, and CPU time) and assigns it a unique number called a **Process ID (PID)**.

To understand processes, here is a simple analogy:
> **Analogy:** A program is a recipe printed in a cookbook (static code on disk). 
> A **Process** is the chef active in the kitchen, actively cooking the meal using the ingredients (active memory allocation and CPU execution).

### Process Lifecycle
Every process is spawned by another process. The parent process uses a system call called `fork()` to copy itself, and then `exec()` to load the new program code. The original creator process is the **Parent Process** (associated with a Parent Process ID, or **PPID**).

```
              [Process Spawned (fork)]
                         │
                         ▼
             ┌──────────────────────┐
             │    READY / RUNNING   │◄──────┐
             │       (State R)      │       │
             └───────────┬──────────┘       │
                         │                  │ Interrupt
             Wait / Block│                  │ Over
             (e.g. I/O)  │                  │
                         ▼                  │
             ┌──────────────────────┐       │
             │   SLEEP / BLOCKED    │───────┘
             │   (State S or D)     │
             └───────────┬──────────┘
                         │
                         │ Execution Complete (exit)
                         ▼
             ┌──────────────────────┐
             │    ZOMBIE / DEFUNCT  │
             │       (State Z)      │
             └───────────┬──────────┘
                         │
                         │ Parent Reads Exit Code (wait)
                         ▼
                    [TERMINATED]
```

---

## 3.2 Key Process Terms
* **PID (Process ID):** A unique numerical identifier assigned to each active process.
* **PPID (Parent Process ID):** The PID of the process that spawned this process.
* **Daemon Process:** A background process that runs continuously, detached from any controlling terminal, waiting for specific requests or system tasks (e.g., `sshd`, `nginx`, `cron`). Daemons usually have `systemd` (PID 1) as their parent.
* **Zombie Process (Defunct):** A process that has completed execution but still has an entry in the system process table. This happens because the parent process has not yet read the child's exit status using the `wait()` system call.
* **Orphan Process:** A running process whose parent has terminated. The system automatically re-parents orphans to the system initialization daemon (`systemd`, PID 1) so they can be cleaned up properly.

---

## 3.3 Linux Process States
In listings (like `ps`), you will see state characters:

| State Code | Name | Description |
| :--- | :--- | :--- |
| **R** | Running / Runnable | Process is actively executing on a CPU core or waiting in the CPU run queue. |
| **S** | Interruptible Sleep | Process is waiting for an event or resource (like user input or disk read) and can be woken up by signals. |
| **D** | Uninterruptible Sleep | Process is waiting for hardware I/O. It cannot be interrupted or killed by signals until the I/O completes. |
| **Z** | Zombie / Defunct | Process has completed execution but remains in the process table until the parent reads its status. |
| **T** | Stopped | Process has been suspended by a signal (like `Ctrl+Z` or SIGSTOP). |

---

## 3.4 Foreground vs Background Processes
* **Foreground Processes:** Run in the terminal directly, blocking input access. You must wait for them to finish before typing another command.
* **Background Processes:** Run detached from terminal input, allowing you to run other commands in parallel.
  * Append `&` to a command to launch it in the background:
    ```bash
    sleep 100 &
    ```
  * Press `Ctrl+Z` to suspend a running foreground process, and type `bg` to let it continue executing in the background.

---

## 3.5 Process Management Commands

### 1. `ps` (Process Status)
* **Definition:** Snapshot list of active system processes.
* **Syntax:** `ps [options]`
* **Common Flags:**
  * `aux` (BSD style): `a` (all users), `u` (user-oriented output format), `x` (processes without controlling terminals).
  * `-ef` (System V style): `-e` (select all processes), `-f` (full listing format).
* **Example:**
  ```bash
  ps aux | grep nginx
  ```
* **Expected Output:**
  ```text
  root      4502  0.0  0.1  56200  4012 ?        Ss   08:00   0:00 nginx: master process /usr/sbin/nginx
  www-data  4503  0.0  0.2  56600  8120 ?        S    08:00   0:02 nginx: worker process
  ```
* **Real DevOps Use Case:** Checking if an application service is running and verifying its PID/User.

---

### 2. `top` & `htop` (Real-time Monitors)
* **Definition:** Dynamic real-time view of running processes, CPU usage, memory usage, and load averages.
* **Syntax:** `top` (standard) or `htop` (interactive, colorful, requires installation).
* **Top Navigation:**
  * `M` (Sort by Memory usage).
  * `P` (Sort by CPU usage).
  * `q` (Quit).
* **Real DevOps Use Case:** High CPU/Memory consumption diagnosis.

---

### 3. `kill`, `killall`, `pkill` (Terminating Processes)
* **Definition:** Sends a signal to a process to terminate it or modify its behavior.
* **Common Signals:**
  * **SIGTERM (15):** The default termination signal. Safely asks the process to exit, allowing it to close files and clean up resources.
  * **SIGKILL (9):** Forces the process to terminate immediately. The process cannot catch or ignore this signal. Use as a last resort.
  * **SIGHUP (1):** Hangup signal. Often used to reload configurations without restarting the daemon.
* **Syntax:**
  * `kill -[signal] <PID>`
  * `pkill [options] <process_name>` (Kills processes matching name).
  * `killall <process_name>` (Kills all processes of name).
* **Examples:**
  ```bash
  sleep 200 &
  # Assume PID returned is 12345
  kill -15 12345
  ```
  *Expected Output:*
  ```text
  [1]+  Terminated              sleep 200
  ```

---

### 4. `jobs`, `bg`, `fg` (Job Control)
* **Definition:** Controls background and suspended processes inside the current shell session.
* **Syntax:**
  * `jobs` (Lists current session jobs).
  * `fg %[job_id]` (Brings job to foreground).
  * `bg %[job_id]` (Runs suspended job in background).
* **Example:**
  ```bash
  sleep 300 &
  jobs
  ```
  *Expected Output:*
  ```text
  [1]+  Running                 sleep 300 &
  ```

---

### 5. `nice` & `renice` (Process Niceness/Priority)
* **Definition:** Sets or alters the execution priority of a process. Niceness values range from `-20` (highest priority) to `19` (lowest priority). Default niceness is `0`.
* **Syntax:**
  * `nice -n <niceness_value> <command>` (Start command with custom niceness).
  * `renice -n <niceness_value> -p <PID>` (Alter running process niceness).
* **Example:**
  ```bash
  # Launch a CPU-intensive backup script with low priority (niceness 15)
  nice -n 15 tar -czf backup.tar.gz /var/www
  ```

---

## 3.6 Real-World Troubleshooting Scenarios

### Scenario A: High CPU Utilization Debugging
* **Problem:** Server alerts trigger due to 100% CPU usage.
* **Resolution Steps:**
  1. Open terminal and run `top` (or `htop` if installed).
  2. Press `P` to sort by CPU usage. Identify the top CPU consumer process and its PID (e.g., `python3 script.py` at PID 9852).
  3. Inspect what the process is doing using `strace` or checking application logs.
  4. If the process is stuck or runaway, terminate it cleanly:
     ```bash
     kill -15 9852
     ```
  5. If it refuses to shut down, force terminate it:
     ```bash
     kill -9 9852
     ```

### Scenario B: Clearing Zombie Processes
* **Problem:** `ps aux` shows processes with state `Z` or `[defunct]`. They are taking up PID space.
* **Resolution Steps:**
  1. Find the Zombie PID and its Parent PID:
     ```bash
     ps -ef | grep defunct
     ```
     *Output:*
     ```text
     ubuntu   9101   9000  0 08:30 ?   00:00:00 [python] <defunct>
     ```
     *Note:* Here, the zombie process is PID `9101` and its parent PPID is `9000`.
  2. You cannot kill a zombie process directly because it is already dead. You must notify the parent process to read its exit code, or terminate the parent process:
     ```bash
     kill -15 9000
     ```
  3. If parent processes are killed or restarted, the zombie process becomes an orphan and is adopted by PID 1 (`systemd`), which automatically reaps it.

---

## 3.7 Chapter 3 Summary
* A process is an active, running program allocated with memory and resources.
* Processes are identified by a PID and spawned by parent processes (PPID).
* Process states include Running (R), Sleeping (S/D), Stopped (T), and Zombie (Z).
* Jobs can be managed in the background (`&`, `bg`) or foreground (`fg`).
* Processes are terminated using signals like `SIGTERM (15)` (graceful) and `SIGKILL (9)` (forced).

---

## 3.8 Interview Questions
1. **Q: What is the difference between SIGTERM and SIGKILL?**
   * *A:* `SIGTERM (15)` is a polite request for termination. The process can capture the signal, release database connections, save state, and shutdown gracefully. `SIGKILL (9)` goes straight to the kernel to terminate the process immediately. The process cannot catch, ignore, or block `SIGKILL`.
2. **Q: What is a load average in Linux?**
   * *A:* The load average shows the average number of processes in runnable or uninterruptible sleep state (R and D states) over the last 1, 5, and 15 minutes. On a 4-core system, a load average of 4.0 means the CPU cores are exactly fully utilized.
3. **Q: How do you identify which process is listening on a particular port?**
   * *A:* You use the socket stat command `ss` or `netstat` combined with process options, for example: `sudo ss -lptn 'sport = :80'` or `sudo netstat -plnt | grep :80`.

---

## 3.9 Practice Questions
1. What command shows a live list of processes sorted by memory usage?
2. How do you send a configuration reload command (`SIGHUP`) to a process with PID `2350`?
3. How do you push a running foreground command to the background?
4. Write the command to terminate all processes running under the name `apache2`.

---

## 3.10 Hands-On Lab
**Objective:** Control execution priorities, manage background jobs, and execute terminations.

1. Launch a background task that sleeps for 1000 seconds:
   ```bash
   sleep 1000 &
   ```
2. Verify it is running using `jobs` and check its status with `ps aux`:
   ```bash
   jobs
   ps aux | grep "sleep 1000"
   ```
3. Suspend it by bringing it to the foreground with `fg %1`, and then pressing `Ctrl+Z`.
4. Check its state using `jobs` (it should display `Stopped`).
5. Resume it in the background using `bg %1`.
6. Terminate it gracefully using its job ID:
   ```bash
   kill -15 %1
   ```
7. Verify it is terminated by checking the output of the `jobs` command.
