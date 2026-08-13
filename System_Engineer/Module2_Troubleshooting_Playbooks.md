# Module 2: System Engineer Troubleshooting Playbooks & Interview Prep

Welcome to the Troubleshooting Playbooks for System Engineers. This guide is tailored for freshers (0–1 year experience) looking to clear System Administrator and Infrastructure walk-in interviews. Given your background in DevOps (Docker, K8s, AWS, CI/CD), you already have a strong foundation, but this module bridges the gap into raw, on-premise, and OS-level system administration troubleshooting.

---

## PART 1: THE TROUBLESHOOTING FRAMEWORK

Every senior System Engineer uses a structured approach to solve problems. Do not jump straight to the OS or application. Use the **Layered Troubleshooting Approach** (based on the OSI model, tailored for SysAdmins):

```text
Layer 1: Physical (cable, hardware, power, LED indicators)
    ↓
Layer 2: Network Connectivity (link up? ping gateway?)
    ↓
Layer 3: IP Configuration (correct IP? subnet? gateway?)
    ↓
Layer 4: DNS (resolving? nslookup working?)
    ↓
Layer 5: Port/Service (service running? port open?)
    ↓
Layer 6: Operating System (drivers? updates? disk space? CPU/RAM?)
    ↓
Layer 7: Application (app crash? dependencies? config?)
    ↓
Layer 8: User/Permission (right account? right permissions? AD login?)
    ↓
Layer 9: Logs/Monitoring (Event Viewer, journalctl, /var/log)
    ↓
Layer 10: Escalate / Document
```

### When to use each layer:
- **Layer 1:** User says "PC won't turn on" or "No internet" (is the cable plugged in? Are switch port lights blinking?).
- **Layer 2 & 3:** User says "Cannot reach the server." (Check `ipconfig` / `ifconfig`, ping gateway).
- **Layer 4:** "I can ping 8.8.8.8 but can't open google.com." (DNS issue).
- **Layer 5:** "Server is up, but web app is down." (Is port 80/443 open? Is Nginx/Apache running?).
- **Layer 6:** "Server is extremely slow." (Check CPU, RAM, Disk IO).
- **Layer 7 & 8:** "I get Access Denied on a shared folder." (Check NTFS/Share permissions, Active Directory).
- **Layer 9:** "Application crashes randomly." (Check Windows Event Viewer or Linux `/var/log`).

---

## PART 2: COMPLETE TROUBLESHOOTING PLAYBOOKS

### PLAYBOOK 1: No Internet Access
**Problem Statement:** User says: "My computer has no internet."
**Initial Questions to Ask User:**
1. Are you connected via WiFi or Ethernet cable?
2. Is the network icon showing a red cross, a yellow triangle, or connected?
3. Can you access any internal company sites, or is everything down?

**Layered Diagnosis Steps:**
1. Check Physical: Ensure ethernet cable is securely plugged in.
2. Check IP: Open CMD, run `ipconfig`. Look for a valid IP (not 169.254.x.x).
3. Ping Gateway: `ping <default_gateway_ip>`.
4. Ping External IP: `ping 8.8.8.8`.
5. Ping Domain: `ping google.com`.

**Most Likely Causes:**
1. Unplugged cable or WiFi disabled.
2. DHCP failure (getting APIPA 169.254.x.x).
3. Switch port down or router issue.

**Fix for Each Cause:**
1. Re-plug cable / enable WiFi adapter.
2. Run `ipconfig /release` then `ipconfig /renew`.
3. Check network switch or contact network team.

**Verification Steps:**
Open browser and navigate to a fresh website.

**Escalation Trigger:**
If multiple users in the same area have the same issue (switch failure).

**Interview Answer Version:**
"First, I'd check the physical connection and the network icon status. Then, I'd open CMD and run `ipconfig` to verify if they have a valid IP address. If they do, I'll ping the default gateway to check local connectivity, then ping 8.8.8.8 to check external routing, and finally ping a domain to verify DNS. This structured approach isolates the issue quickly."

---

### PLAYBOOK 2: Connected to WiFi but No Internet
**Problem Statement:** User says: "I'm connected to WiFi but websites aren't loading."
**Initial Questions to Ask User:**
1. Does the WiFi icon have a yellow exclamation mark?
2. Are you connected to the correct company SSID?
3. Did you recently change your password?

**Layered Diagnosis Steps:**
1. Run `ipconfig /all` to check DNS servers and Default Gateway.
2. `ping 8.8.8.8` (checks internet without DNS).
3. `nslookup google.com` (checks DNS resolution).
4. Run `tracert 8.8.8.8` to see where the traffic drops.

**Most Likely Causes:**
1. Captive portal authentication required.
2. DNS server is unreachable.
3. IP conflict or DHCP pool exhaustion on the wireless controller.

**Fix for Each Cause:**
1. Ask user to open browser and log in to the portal.
2. Flush DNS: `ipconfig /flushdns` or manually set DNS to 8.8.8.8 for testing.
3. Check DHCP server for available leases.

**Verification Steps:**
Browse to an external site.

**Escalation Trigger:**
If the entire SSID is broadcasting but not routing traffic.

**Interview Answer Version:**
"If WiFi is connected but there's no internet, I immediately suspect DNS or routing. I'd ping 8.8.8.8 to see if packets leave the network. If that works, I run `nslookup` to test DNS. Usually, flushing the DNS or having the user authenticate through the captive portal resolves this."

---

### PLAYBOOK 3: Slow Internet
**Problem Statement:** User says: "Internet is very slow today."
**Initial Questions to Ask User:**
1. Is it slow for all websites or just one specific app?
2. Are you on a VPN?
3. Is anyone else around you experiencing the same issue?

**Layered Diagnosis Steps:**
1. Run a speed test (fast.com or speedtest.net).
2. Run `ping 8.8.8.8 -t` and watch for latency spikes (>100ms) or dropped packets.
3. Open Task Manager -> Performance -> Ethernet/WiFi to see if a background app is consuming bandwidth.
4. Run `tracert 8.8.8.8` to identify network bottlenecks.

**Most Likely Causes:**
1. Background downloads (Windows Updates).
2. ISP routing issue / high latency.
3. VPN encryption overhead.

**Fix for Each Cause:**
1. Stop the downloading process or wait for it to finish.
2. Escalate to ISP if tracert shows drops outside the network.
3. Disconnect and reconnect VPN.

**Verification Steps:**
Consistent ping responses under 50ms.

**Escalation Trigger:**
If tracert shows consistent drops at the edge router.

**Interview Answer Version:**
"I'd start by running a continuous ping to 8.8.8.8 to look for packet loss or high latency. Then, I'd check Task Manager to ensure no local applications are hogging bandwidth. If it's a localized issue, I'd check their physical connection; if it's systemic, I'd run a traceroute and escalate to the network team."

---

### PLAYBOOK 4: DNS Not Working
**Problem Statement:** User says: "I can't access websites but I can ping the IP address."
**Initial Questions to Ask User:**
1. Have you tried a different browser?
2. Are you using the VPN?

**Layered Diagnosis Steps:**
1. Run `nslookup google.com`. Look at the Server responding.
2. Run `ipconfig /all` to verify primary and secondary DNS servers.
3. Try an alternative DNS: `nslookup google.com 8.8.8.8`.

**Most Likely Causes:**
1. Local DNS cache corruption.
2. Incorrect statically assigned DNS.
3. Corporate DNS server is down.

**Fix for Each Cause:**
1. Run `ipconfig /flushdns`.
2. Change network adapter settings to obtain DNS automatically.
3. Escalate to server team.

**Verification Steps:**
Able to browse via domain name.

**Escalation Trigger:**
If `nslookup` fails for all users pointing to the corporate DNS server.

**Interview Answer Version:**
"This is a classic DNS issue. I would run `nslookup` to confirm the domain isn't resolving. Next, I'd run `ipconfig /flushdns` to clear the local cache. If that fails, I would manually query a public DNS like 8.8.8.8. If the public DNS works but the internal one fails, I know the corporate DNS server has an issue."

---

### PLAYBOOK 5: DHCP Not Assigning IP / Getting 169.x.x.x
**Problem Statement:** User says: "My IP address shows 169.254.x.x and I can't connect."
**Initial Questions to Ask User:**
1. Did you just plug in, or were you connected before?
2. Are you using a docking station?

**Layered Diagnosis Steps:**
1. Run `ipconfig /release` then `ipconfig /renew`.
2. Check physical link lights on the NIC.
3. If using a dock, plug the cable directly into the laptop.
4. Try assigning a static IP temporarily to test connectivity to the gateway.

**Most Likely Causes:**
1. DHCP server pool is full.
2. Port security (MAC filtering) on the switch blocked the port.
3. DHCP Relay (IP Helper) on the router is down.

**Fix for Each Cause:**
1. Clear old DHCP leases on the server.
2. Network team must reset the switch port.
3. Network team to check routing.

**Verification Steps:**
`ipconfig` shows an IP in the correct corporate subnet.

**Escalation Trigger:**
If static IP works but DHCP fails, escalate to the network/server team managing DHCP.

**Interview Answer Version:**
"A 169.254 IP means APIPA—the PC can't reach the DHCP server. I'd try `ipconfig /release` and `/renew`. If it still fails, I'd assign a static IP to see if I can ping the gateway. If I can, it's a DHCP service issue. If I can't, it's a Layer 1 or Layer 2 switch issue."

---

### PLAYBOOK 6: IP Address Conflict
**Problem Statement:** User says: "A window appeared saying 'IP address conflict' and now I can't connect."
**Initial Questions to Ask User:**
1. Is this a new device on the network?
2. Has anyone else reported this?

**Layered Diagnosis Steps:**
1. Run `ipconfig /release`.
2. Run `ipconfig /renew` to pull a new lease.
3. If static, change the IP address.
4. Check the ARP table `arp -a` to find the conflicting MAC address.

**Most Likely Causes:**
1. Two devices assigned the same static IP.
2. A static IP is set within the DHCP scope, and the server handed it out.

**Fix for Each Cause:**
1. Switch one device to DHCP.
2. Exclude the static IP from the DHCP pool on the server.

**Verification Steps:**
Device connects successfully without the warning prompt.

**Escalation Trigger:**
If a rogue DHCP server is handing out conflicting IPs.

**Interview Answer Version:**
"An IP conflict means two MAC addresses claim the same IP. I would run `ipconfig /release` and `/renew` to get a fresh IP from the server. To find the culprit, I'd ping the conflicting IP from another machine, look at the ARP table (`arp -a`), and use the MAC address to track down the rogue device."

---

### PLAYBOOK 7: Cannot Ping the Gateway
**Problem Statement:** User says: "I can't reach any network resource."
**Initial Questions to Ask User:**
1. Are other people around you working fine?
2. Did you recently move desks?

**Layered Diagnosis Steps:**
1. Check `ipconfig` for the gateway IP.
2. Ping localhost (`ping 127.0.0.1`) to ensure the TCP/IP stack is working.
3. Ping the local IP to ensure the NIC is active.
4. Check switch port and cabling.

**Most Likely Causes:**
1. Bad ethernet cable or wall jack.
2. Switch port is configured for the wrong VLAN.
3. Windows Firewall blocking outbound ICMP (rare for gateway).

**Fix for Each Cause:**
1. Replace cable / try a different jack.
2. Contact network team to change VLAN.

**Verification Steps:**
`ping <gateway_ip>` returns replies.

**Escalation Trigger:**
If the switch port needs reconfiguration.

**Interview Answer Version:**
"If I can't ping the gateway, I'm isolated. I ping 127.0.0.1 to check the TCP/IP stack, then ping my own IP to verify the NIC. If both work, the issue is on the wire or the switch. I'd verify the physical cabling and then check if the switch port is in the correct VLAN."

---

### PLAYBOOK 8: Slow Windows PC
**Problem Statement:** User says: "My computer has become very slow in the last week."
**Initial Questions to Ask User:**
1. When was the last time you restarted (not just shut down)?
2. Do you have many browser tabs or heavy apps open?

**Layered Diagnosis Steps:**
1. Open Task Manager (Ctrl+Shift+Esc). Check CPU, Memory, and Disk columns.
2. Look at "Uptime" in the Performance tab. (Fast Startup can cause high uptimes even if shut down).
3. Check available space on the C: drive.
4. Check Startup apps in Task Manager.

**Most Likely Causes:**
1. High system uptime (memory leaks).
2. HDD usage at 100% (common on older drives).
3. Windows Updates running in the background.

**Fix for Each Cause:**
1. Reboot the PC.
2. Replace HDD with SSD, or disable SysMain (Superfetch) service.
3. Let updates finish.
4. Disable unnecessary startup programs.

**Verification Steps:**
System feels responsive, Task Manager baselines return to normal idle (<10% CPU, <50% RAM).

**Escalation Trigger:**
If hardware failure (failing drive) is suspected.

**Interview Answer Version:**
"I always start with Task Manager. I check the Performance tab for uptime—often users 'shut down' but Fast Startup keeps uptime running for weeks. I check for bottlenecks in CPU, Memory, or Disk IO. Disabling heavy startup apps, running Windows updates, and a clean reboot solves 90% of slow PC issues."

---

### PLAYBOOK 9: High CPU Usage
**Problem Statement:** User says: "My laptop fan is very loud and everything is freezing."
**Initial Questions to Ask User:**
1. What application were you using when it started?
2. Is the laptop sitting on a soft surface blocking vents?

**Layered Diagnosis Steps:**
1. Open Task Manager -> Details tab, sort by CPU.
2. Identify the specific process (e.g., `chrome.exe`, `TiWorker.exe`).
3. On Linux: Run `top` or `htop`, press 'P' to sort by CPU.
4. Check system temperature using third-party tools if available.

**Most Likely Causes:**
1. Runaway process or memory leak.
2. Windows Modules Installer Worker (Updates).
3. Antivirus scan running.

**Fix for Each Cause:**
1. End task on the rogue process.
2. Wait for updates/scans to finish, or schedule them for off-hours.

**Verification Steps:**
Fan speed drops, CPU idles below 10%.

**Escalation Trigger:**
If a critical line-of-business app consistently spikes CPU and crashes.

**Interview Answer Version:**
"I open Task Manager and sort processes by CPU usage to identify the culprit. If it's a non-critical app, I kill it. On Linux, I use `htop` or `top`. If it's a system process like Windows Update, I advise the user to let it finish. Persistent high CPU by legitimate apps might require reinstalling the app or upgrading hardware."

---

### PLAYBOOK 10: High RAM Usage
**Problem Statement:** User says: "My computer is lagging and shows 'low memory'."
**Initial Questions to Ask User:**
1. How many Chrome/Edge tabs do you have open?
2. Are you working with large Excel files or databases?

**Layered Diagnosis Steps:**
1. Task Manager -> Processes -> Sort by Memory.
2. On Linux: `free -m` to check available RAM and swap. Run `top` and sort by memory (Shift+M).
3. Check Virtual Memory (Pagefile) settings on Windows.

**Most Likely Causes:**
1. Too many browser tabs.
2. Memory leak in an application.
3. Insufficient physical RAM for the workload.

**Fix for Each Cause:**
1. Close tabs/apps.
2. Restart the leaky application.
3. Increase swap space (Linux) or pagefile (Windows), or physically upgrade RAM.

**Verification Steps:**
Memory usage drops below 80%.

**Escalation Trigger:**
If production server RAM is exhausted leading to Out Of Memory (OOM) killer terminating services.

**Interview Answer Version:**
"I check Task Manager (or `free -m` on Linux) to see total vs available memory. I identify the top consuming process. If it's a memory leak, I restart the process. If it's normal usage but maxing out, I look at expanding the pagefile/swap temporarily and suggest a RAM upgrade for a permanent fix."

---

### PLAYBOOK 11: Low Disk Space Warning
**Problem Statement:** Windows: "You are running out of space on C: drive."
**Initial Questions to Ask User:**
1. Did you recently download large files?
2. Is your recycle bin empty?

**Layered Diagnosis Steps:**
1. Open File Explorer, check C: drive properties.
2. Run Disk Cleanup (cleanmgr) as Administrator.
3. Use a tool like TreeSize Free or WinDirStat (or visually inspect large folders like Downloads, Temp).
4. Empty Recycle Bin.

**Most Likely Causes:**
1. Large user downloads or videos.
2. Windows Update leftover files (Windows.old).
3. Massive log files in `C:\Windows\Temp`.

**Fix for Each Cause:**
1. Delete or move large files to a network drive.
2. Run Disk Cleanup and select "Clean up system files".

**Verification Steps:**
At least 15-20% free space on C: drive.

**Escalation Trigger:**
None usually required, unless the disk is completely full and the OS is unbootable.

**Interview Answer Version:**
"I first run Windows Disk Cleanup as Admin to clear out Temp files, old Windows Update files, and the recycle bin. If more space is needed, I use a tool like TreeSize to visually map out which directories hold the largest files, and work with the user to move them to cloud or network storage."

---

### PLAYBOOK 12: Linux Server Disk Full
**Problem Statement:** Alert: "/var filesystem is 100% full on production server."
**Initial Questions to Ask User:** (Usually an alert, not a user).

**Layered Diagnosis Steps:**
1. SSH into the server. Run `df -h` to confirm which partition is full.
2. Run `du -sh /* 2>/dev/null` or `cd /var && du -sh * | sort -rh | head -10` to find the largest directories.
3. Check for deleted but open files holding space: `lsof +L1`.
4. Check log rotations.

**Most Likely Causes:**
1. Runaway application logs in `/var/log`.
2. Docker containers/images consuming space in `/var/lib/docker`.
3. Process holding onto a deleted log file.

**Fix for Each Cause:**
1. Truncate logs: `> /var/log/syslog` (Do NOT delete the file with `rm`, truncate it).
2. Run `docker system prune` if applicable.
3. Restart the service holding the deleted file.

**Verification Steps:**
`df -h` shows space reclaimed.

**Escalation Trigger:**
If you need to resize an LVM volume and aren't comfortable doing it in production.

**Interview Answer Version:**
"I SSH in and run `df -h` to verify the full mount. Then I use `du -sh * | sort -rh` to drill down into the largest directories. Often it's log files. I NEVER `rm` a live log file; instead, I truncate it using `> filename` so the process doesn't hold the inode. If a file was deleted but space wasn't freed, I use `lsof +L1` to find the PID and restart the service."

---

### PLAYBOOK 13: Linux Service Stopped
**Problem Statement:** Alert: "nginx service is not running on the server."
**Initial Questions to Ask User:** Did anyone recently change configuration files?

**Layered Diagnosis Steps:**
1. Check status: `systemctl status nginx`.
2. Attempt restart: `systemctl restart nginx`.
3. If it fails, check logs: `journalctl -u nginx -f` or `tail -n 50 /var/log/nginx/error.log`.
4. Test configuration syntax: `nginx -t`.

**Most Likely Causes:**
1. Syntax error in the config file.
2. Port 80/443 is already in use by another service (e.g., Apache).
3. Permissions issue on the web root.

**Fix for Each Cause:**
1. Fix the typo identified by `nginx -t`.
2. Run `netstat -tulpn | grep 80` to find the conflicting PID and kill it.
3. `chown` or `chmod` the files correctly.

**Verification Steps:**
`systemctl status nginx` shows "active (running)" and the website loads.

**Escalation Trigger:**
If the application requires complex dependency troubleshooting.

**Interview Answer Version:**
"I check the service status with `systemctl status nginx`. If it's failed, I immediately test the config with `nginx -t` because a syntax error is the most common cause. Then I look at `journalctl -u nginx` for specific error logs. If it says address already in use, I run `netstat -tulpn` to find and stop the conflicting service."

---

### PLAYBOOK 14: Linux Server Unreachable (Cannot SSH)
**Problem Statement:** Alert: "Server is not responding to SSH connections."
**Initial Questions to Ask User:** Is the server virtual or physical?

**Layered Diagnosis Steps:**
1. Ping the server to check Layer 3 connectivity.
2. Use `nmap -p 22 <server_ip>` or `telnet <ip> 22` to check if port 22 is open.
3. Log in via hypervisor console (vCenter/AWS EC2 Console) or iLO/iDRAC.
4. Once in console, check if `sshd` is running (`systemctl status sshd`).
5. Check if the disk is 100% full (prevents login).

**Most Likely Causes:**
1. Network firewall/security group blocking port 22.
2. `sshd` service crashed.
3. Kernel panic or server crashed/rebooting.

**Fix for Each Cause:**
1. Update firewall rules.
2. Restart `sshd` via console.
3. Reboot server via hypervisor.

**Verification Steps:**
Successful SSH connection from a client machine.

**Escalation Trigger:**
If the server kernel panicked and won't boot.

**Interview Answer Version:**
"First, I ping the server. Then I test port 22 using telnet or nmap. If the network is fine but SSH is down, I access the server via its out-of-band management console like vCenter or AWS Systems Manager. From there, I check if `sshd` is running, if the disk is 100% full, or if firewall rules were modified."

---

### PLAYBOOK 15: SSH Not Working / Permission Denied
**Problem Statement:** User says: "I get 'Permission denied' when trying to SSH to the server."
**Initial Questions to Ask User:**
1. Are you using a password or an SSH key?
2. Did it work yesterday?

**Layered Diagnosis Steps:**
1. Run SSH in verbose mode: `ssh -v user@host`.
2. Check file permissions on the client's private key (must be 600 or 400).
3. (As admin on server) Check `/var/log/auth.log` or `/var/log/secure` for reasons.
4. Verify the public key is in `~/.ssh/authorized_keys` with correct permissions.

**Most Likely Causes:**
1. Wrong password / account locked out.
2. SSH key permissions are too open on client side (`chmod 0644 id_rsa` will fail).
3. Server `authorized_keys` has wrong permissions (must be 600).

**Fix for Each Cause:**
1. Unlock account or reset password.
2. Run `chmod 400 ~/.ssh/id_rsa`.
3. Fix server permissions: `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys`.

**Verification Steps:**
Successful login without errors.

**Escalation Trigger:**
PAM configuration issues.

**Interview Answer Version:**
"I ask the user to run `ssh -v` for verbose output. Usually, 'Permission denied' with keys means the private key permissions are too loose—SSH requires them to be 400 or 600. If it's a server-side issue, I log in with my admin account and check `/var/log/secure` or `auth.log` to see exactly why the SSH daemon rejected the connection."

---

### PLAYBOOK 16: User Cannot Log In to Windows
**Problem Statement:** User says: "My password is correct but I can't log in."
**Initial Questions to Ask User:**
1. Is CAPS lock on?
2. Are you connected to the network/VPN?
3. What is the exact error message?

**Layered Diagnosis Steps:**
1. Check if the error is "The referenced account is currently locked out".
2. Check if the error is "The trust relationship between this workstation and the primary domain failed."
3. Ask user to connect via ethernet if password was recently changed.

**Most Likely Causes:**
1. AD Account is locked out due to bad attempts (mobile phone trying old password).
2. Trust relationship broken (computer hasn't connected to AD in months).
3. Cached credentials issue.

**Fix for Each Cause:**
1. Unlock account in Active Directory Users and Computers (ADUC).
2. Log in with local admin, remove from domain, and rejoin.
3. Connect to VPN at the login screen so AD sees the new password.

**Verification Steps:**
User reaches the desktop successfully.

**Escalation Trigger:**
Domain controller replication issues.

**Interview Answer Version:**
"I first verify the exact error. If it's a lockout, I unlock it in Active Directory and ask them to update their passwords on mobile devices. If they get the 'Trust Relationship' error, it means the machine's secure channel with AD is broken, so I log in locally, leave the domain, and rejoin it."

---

### PLAYBOOK 17: User Cannot Access a Shared Folder
**Problem Statement:** User says: "I can't open the shared drive. It says access denied."
**Initial Questions to Ask User:**
1. Could you access it before?
2. What is the exact path (e.g., `\\server\share`)?

**Layered Diagnosis Steps:**
1. Verify network connectivity to the file server (`ping`).
2. Check user's AD groups (`net user username /domain`).
3. Check the folder's Share Permissions AND NTFS Security permissions.
4. Open Computer Management -> Shared Folders to check active sessions.

**Most Likely Causes:**
1. User was removed from the security group.
2. NTFS permissions are more restrictive than Share permissions.
3. Kerberos ticket expired (needs logoff/logon).

**Fix for Each Cause:**
1. Add user back to the AD group.
2. Adjust NTFS permissions.
3. Have the user lock and unlock, or restart their PC to refresh group policy/tickets.

**Verification Steps:**
User can read/write a test file in the directory.

**Escalation Trigger:**
Data corruption on the file server.

**Interview Answer Version:**
"File access depends on the most restrictive permission between Share Permissions and NTFS Permissions. I check the user's AD groups to ensure they have rights. If I add them to a new group, I remind them to log off and log back on to refresh their Kerberos ticket, otherwise, the new permissions won't apply."

---

### PLAYBOOK 18: Printer Not Working
**Problem Statement:** User says: "I'm trying to print but nothing is happening."
**Initial Questions to Ask User:**
1. Is there an error on the physical printer screen?
2. Are you getting an error on your PC?

**Layered Diagnosis Steps:**
1. Physical: Does the printer have paper, toner, and power?
2. Network: Can you ping the printer's IP?
3. Local PC: Open Print Queue. Are jobs stuck?
4. Restart Print Spooler service (`services.msc` -> Print Spooler -> Restart).

**Most Likely Causes:**
1. Print Spooler service hung.
2. IP address of printer changed.
3. Paper jam or out of toner.

**Fix for Each Cause:**
1. Clear spooler: Stop service, delete files in `C:\Windows\System32\spool\PRINTERS`, start service.
2. Update printer port to the correct IP.
3. Fix physical printer issue.

**Verification Steps:**
Print a test page.

**Escalation Trigger:**
Hardware failure requiring a vendor technician.

**Interview Answer Version:**
"Printing issues are usually either physical or spooler related. I ping the printer to confirm network connectivity. Then I check the local print queue for stuck jobs. The quickest fix is usually restarting the Print Spooler service. If jobs are stubbornly stuck, I stop the service, clear the `System32\spool\PRINTERS` folder, and start it again."

---

### PLAYBOOK 19: Application is Not Responding / Crashing
**Problem Statement:** User says: "My application keeps crashing after the Windows update."
**Initial Questions to Ask User:**
1. Does it give a specific error code?
2. Does it happen immediately on launch or during a specific action?

**Layered Diagnosis Steps:**
1. Check Task Manager to kill hung processes.
2. Open Windows Event Viewer -> Application log -> Filter for Errors. Look for Faulting Application Name and Faulting Module (e.g., a specific .dll file).
3. Try running the app as Administrator or in Compatibility Mode.
4. Check for application-specific logs.

**Most Likely Causes:**
1. Corrupted configuration file.
2. Incompatible Windows Update or missing dependency (like .NET framework).
3. Antivirus blocking the executable.

**Fix for Each Cause:**
1. Repair or reinstall the application.
2. Roll back the recent Windows Update.
3. Add an exception in the AV console.

**Verification Steps:**
Application launches and functions normally.

**Escalation Trigger:**
Application bug requiring vendor support.

**Interview Answer Version:**
"When an app crashes, I go straight to the Windows Event Viewer, specifically the Application Logs. I look for the Error event matching the crash time to find the faulting module, which is often a missing `.dll` or `.NET` framework issue. Based on that, I'll repair the installation, check for updates, or roll back a patch if it broke the app."

---

### PLAYBOOK 20: Blue Screen of Death (BSOD)
**Problem Statement:** User says: "My computer showed a blue screen and restarted."
**Initial Questions to Ask User:**
1. Did you plug in a new device recently?
2. Can you boot into Windows, or does it loop?

**Layered Diagnosis Steps:**
1. Get the Stop Code from the user (e.g., `IRQL_NOT_LESS_OR_EQUAL`).
2. Boot into Safe Mode if it's boot-looping.
3. Use a tool like BlueScreenView or WinDbg to analyze the memory dump file (`C:\Windows\Minidump`).
4. Run `sfc /scannow` and `chkdsk /f`.

**Most Likely Causes:**
1. Bad or recently updated hardware driver (GPU, network card).
2. Failing RAM (Memory management errors).
3. Corrupted OS files.

**Fix for Each Cause:**
1. Boot to Safe Mode and roll back the device driver.
2. Run Windows Memory Diagnostic. Replace RAM if faulty.
3. Run DISM and SFC tools to repair OS files.

**Verification Steps:**
System runs under load without crashing.

**Escalation Trigger:**
Persistent hardware failures requiring motherboard replacement.

**Interview Answer Version:**
"For a BSOD, I ask for the Stop Code. I grab the `.dmp` file from `C:\Windows\Minidump` and analyze it to find the exact driver that caused the crash. 90% of the time it's a bad hardware driver, so I boot into Safe Mode and roll back or update that specific driver. If it's a memory management error, I'll run a RAM diagnostic."

---

### PLAYBOOK 21: Computer Overheating
**Problem Statement:** User says: "My laptop is extremely hot and shutting down randomly."
**Initial Questions to Ask User:**
1. Do you hear the fan spinning?
2. Are you using it on a bed or soft surface?

**Layered Diagnosis Steps:**
1. Check CPU load in Task Manager to ensure it's not a software issue causing heat.
2. Feel the exhaust vent for airflow.
3. Check system event logs for "Kernel-Power" thermal shutdown events.

**Most Likely Causes:**
1. Dust blocking the heatsink/fan.
2. Dried out thermal paste.
3. Fan hardware failure.

**Fix for Each Cause:**
1. Use compressed air to clean vents.
2. Dispatch hardware tech to repaste/replace fan.

**Verification Steps:**
System stays on under stress test.

**Escalation Trigger:**
Requires taking apart the chassis (depends on company hardware policy).

**Interview Answer Version:**
"Overheating is usually physical, but I first check Task Manager to ensure a rogue process isn't pegging the CPU at 100%. If software is fine, I check the Event Viewer for thermal shutdown codes. Then I advise cleaning the vents with compressed air, or I route the ticket to hardware dispatch for a fan replacement."

---

### PLAYBOOK 22: Driver Problem
**Problem Statement:** User says: "My webcam / external display / USB device is not being detected."
**Initial Questions to Ask User:**
1. Have you tried a different USB port?
2. Did it work before a recent update?

**Layered Diagnosis Steps:**
1. Open Device Manager (`devmgmt.msc`).
2. Look for devices with a yellow triangle or under "Unknown Devices".
3. Right-click -> Update Driver, or Uninstall device and scan for hardware changes.
4. Go to manufacturer website (Dell/HP/Lenovo) to download the specific driver.

**Most Likely Causes:**
1. Generic Windows driver installed instead of OEM driver.
2. USB port disabled in BIOS/UEFI.
3. Faulty device.

**Fix for Each Cause:**
1. Install correct driver.
2. Enable in BIOS.
3. Test device on another PC.

**Verification Steps:**
Device appears in Device Manager without errors and functions correctly.

**Escalation Trigger:**
Port failure on motherboard.

**Interview Answer Version:**
"I open Device Manager and look for any yellow exclamation marks indicating a driver issue. I'll uninstall the problematic device and let Windows redetect it, or I'll go directly to the vendor's site like Dell Command Update to pull down the correct OEM drivers."

---

### PLAYBOOK 23: Windows Update Failing
**Problem Statement:** User says: "Windows updates are failing with an error code."
**Initial Questions to Ask User:**
1. What is the exact error code (e.g., 0x80070002)?
2. Do you have enough disk space?

**Layered Diagnosis Steps:**
1. Check free disk space.
2. Run the Windows Update Troubleshooter.
3. Clear the Software Distribution folder.
4. Run `sfc /scannow` to check for system corruption.

**Most Likely Causes:**
1. Corrupted update cache.
2. Antivirus interference.
3. Lack of disk space.

**Fix for Each Cause:**
1. Open CMD as admin:
   `net stop wuauserv`
   `net stop bits`
   Rename `C:\Windows\SoftwareDistribution` to `SoftwareDistribution.old`
   `net start wuauserv`
   `net start bits`
2. Retry update.

**Verification Steps:**
Updates download and install successfully.

**Escalation Trigger:**
If WSUS server is pushing broken updates.

**Interview Answer Version:**
"When Windows Updates get stuck, the update cache is usually corrupted. I open an admin command prompt, stop the Windows Update and BITS services, rename the `SoftwareDistribution` folder to force Windows to create a fresh one, and then restart the services. That clears out the corruption and usually fixes the issue."

---

### PLAYBOOK 24: Cannot Access a Website (specific site)
**Problem Statement:** User says: "I can access Google but I can't access our company portal."
**Initial Questions to Ask User:**
1. Are you on the VPN?
2. What browser are you using?

**Layered Diagnosis Steps:**
1. Try an incognito/private window.
2. Clear browser cache and cookies.
3. Ping the domain to see if it resolves internally or externally.
4. Check proxy settings or PAC file.

**Most Likely Causes:**
1. Stale browser cache/cookies.
2. Split-tunnel VPN issue (traffic not routing correctly).
3. Web server is actually down.

**Fix for Each Cause:**
1. Clear cache (Ctrl+Shift+Del).
2. Reconnect VPN or update routing tables.
3. Check the server status.

**Verification Steps:**
Site loads in standard browser mode.

**Escalation Trigger:**
If multiple users on the VPN can't access it, escalate to Network/Firewall team.

**Interview Answer Version:**
"If one specific site fails, I first isolate the browser by testing in Incognito mode. If it works there, I clear their cache and cookies. If it still fails, I ping the site to check DNS resolution and verify if the VPN split-tunneling is routing the traffic correctly to the internal network."

---

### PLAYBOOK 25: VPN Not Connecting
**Problem Statement:** User says: "I'm working from home and I can't connect to the company VPN."
**Initial Questions to Ask User:**
1. Is your home internet working?
2. Are you using the correct multi-factor authentication (MFA) code?

**Layered Diagnosis Steps:**
1. Verify home internet (ping 8.8.8.8).
2. Check the VPN client logs for authentication errors vs timeout errors.
3. Verify AD account is not locked out.
4. Check if their home router is blocking IPsec or OpenVPN ports.

**Most Likely Causes:**
1. Expired password or locked AD account.
2. MFA push notification was ignored.
3. Captive portal on public WiFi blocking VPN ports.

**Fix for Each Cause:**
1. Reset/unlock account.
2. Ensure user accepts the Duo/Authenticator prompt.
3. Connect to a different network.

**Verification Steps:**
VPN client shows "Connected" and user can ping an internal IP.

**Escalation Trigger:**
VPN gateway certificate expired or firewall appliance down.

**Interview Answer Version:**
"I check their underlying internet connection first. Then I look at the VPN client logs. If it's an immediate rejection, it's usually a locked AD account or an MFA timeout. If it hangs and times out, their local network might be blocking VPN protocols like IPsec, which happens often on hotel or public WiFis."

---

## PART 3: LEVEL 5 & 6 INTERVIEW QUESTIONS WITH ANSWERS

**Q1: "A user's computer suddenly has no internet. Walk me through your troubleshooting process."**
- **Short Answer:** "I use the OSI layer approach. Layer 1: Check physical cables and WiFi toggles. Layer 3: Run `ipconfig` to check for a valid IP. If valid, I ping the gateway. If that works, I ping 8.8.8.8 to verify routing, and finally `nslookup` or ping a domain to check DNS."
- **Commands:** `ipconfig`, `ping`, `nslookup`, `tracert`.
- **What NOT to say:** "I'd reinstall the network driver immediately."
- **Strong Interview Line:** "I isolate the failure point systematically—local PC, local network, internet, or DNS—before making any changes."

**Q2: "You receive an alert that a Linux server is running out of disk space. What do you do?"**
- **Short Answer:** "I SSH in and run `df -h` to verify. Then I use `du -sh /*` to find the largest directories, which are usually logs in `/var/log`. I will safely truncate the logs using `> filename.log` rather than deleting them, so the running service doesn't hold the space."
- **Commands:** `df -h`, `du -sh *`, `> file.log`, `lsof +L1`.
- **What NOT to say:** "I run `rm -rf` on the log files."
- **Strong Interview Line:** "I ensure I truncate live files instead of removing them, to prevent zombie processes from holding onto the inode space."

**Q3: "A user says DNS is not resolving. What are the first 5 things you check?"**
- **Short Answer:** "1. Run `nslookup` to see the failure. 2. Run `ipconfig /all` to verify what DNS server is assigned. 3. Ping the DNS server to check reachability. 4. Run `ipconfig /flushdns` to clear local cache. 5. Test resolution against a public DNS like 8.8.8.8."
- **Commands:** `nslookup`, `ipconfig /flushdns`.
- **What NOT to say:** "I change their DNS to Google DNS permanently."
- **Strong Interview Line:** "Testing against a known good public DNS quickly tells me if the issue is our internal DNS server or the client's network stack."

**Q4: "An employee says their computer is very slow. How do you diagnose this?"**
- **Short Answer:** "I open Task Manager and check the CPU, Memory, and Disk usage to identify bottlenecks. I look at system uptime to ensure they have actually rebooted recently. If a specific app is hogging resources, I kill it. If it's disk IO on an older HDD, I recommend an SSD upgrade."
- **Commands:** Task Manager, `resmon`, Event Viewer.
- **What NOT to say:** "I tell them to buy a new laptop."
- **Strong Interview Line:** "Users often confuse 'sleep' with 'shut down', so checking system uptime is my first step to rule out memory leaks from long uptimes."

**Q5: "A service on a Linux server has stopped. How do you restart it and find out why it stopped?"**
- **Short Answer:** "I check the status with `systemctl status <service>`. Then I look at the logs using `journalctl -u <service> -n 50`. If it's a web server like Nginx, I test the config syntax with `nginx -t` before attempting `systemctl restart <service>`."
- **Commands:** `systemctl status/restart`, `journalctl -u`, `<service> -t`.
- **What NOT to say:** "I just keep rebooting the server."
- **Strong Interview Line:** "I always check the logs before restarting, because once it restarts successfully, the forensic evidence of why it crashed might be harder to find."

**Q6: "A user gets a 'Permission denied' error on Linux. What could be the cause and how do you fix it?"**
- **Short Answer:** "It's either file permissions or ownership. I run `ls -l` to check the read/write/execute bits and the owner/group. Depending on the need, I use `chmod` to fix permissions or `chown` to fix ownership. For SSH, I ensure `~/.ssh` is 700 and the private key is 400."
- **Commands:** `ls -l`, `chmod`, `chown`.
- **What NOT to say:** "I just run `chmod 777` to make it work."
- **Strong Interview Line:** "I strictly follow the principle of least privilege, assigning only the exact permissions needed, never falling back on 777."

**Q7: "Two users report an IP address conflict. What do you do?"**
- **Short Answer:** "I ask one user to open CMD and run `ipconfig /release` and `ipconfig /renew`. If there's a rogue device with a static IP causing this, I ping the IP and check `arp -a` to get the MAC address, then work with networking to track or block that MAC."
- **Commands:** `ipconfig /release`, `arp -a`.
- **What NOT to say:** "I ignore it and hope DHCP fixes it."
- **Strong Interview Line:** "Resolving the client is easy via `/renew`, but finding the root cause requires hunting down the rogue MAC address in the ARP table."

**Q8: "After a Windows update, an application stopped working. How do you troubleshoot?"**
- **Short Answer:** "I check Event Viewer -> Application logs to find the exact crash module. I test running the app as Administrator or in Compatibility Mode. If it's definitely tied to the update, I uninstall that specific KB patch from 'Programs and Features' and pause updates until a vendor fix is released."
- **Commands:** `eventvwr.msc`, `appwiz.cpl`.
- **What NOT to say:** "I wipe the machine and reinstall Windows."
- **Strong Interview Line:** "Updates often change DLLs or .NET versions. Event Viewer points me straight to the failing dependency."

**Q9: "You need to find what process is consuming 100% CPU on a Linux server. What commands do you use?"**
- **Short Answer:** "I use `top` or `htop`. In `top`, I press 'P' to sort by CPU usage. Once I identify the PID, if it's a runaway process, I use `kill -15 <PID>` to terminate it gracefully, or `kill -9` if it's unresponsive."
- **Commands:** `top`, `htop`, `kill`.
- **What NOT to say:** "I just run `killall`."
- **Strong Interview Line:** "I always prefer `kill -15` (SIGTERM) first to allow the process to clean up its sockets and child processes."

**Q10: "A user cannot access a shared folder. What are the possible reasons?"**
- **Short Answer:** "1. They don't have Network connectivity. 2. They aren't in the correct Active Directory Security Group. 3. The Share permissions are correct, but NTFS security permissions are denying access. 4. Their Kerberos ticket is stale and they need to log off/on."
- **Commands:** `net user /domain`, `ping`.
- **What NOT to say:** "I make them a local admin."
- **Strong Interview Line:** "Effective access is the most restrictive combination of Share and NTFS permissions. I always check both tabs."

---

## PART 4: SCENARIO-BASED INTERVIEW QUESTIONS (LEVEL 6)

**SCENARIO 1:**
"An employee calls and says: My laptop is connected to WiFi with full bars but no website is loading. What will you do?"
- **Response:** "First, I calmly assure the user I'll get them connected. I ask them to open Command Prompt. I guide them to type `ping 8.8.8.8`. If replies come back, the internet is working, and the issue is likely DNS. I'll have them type `nslookup google.com`. If that times out, I walk them through `ipconfig /flushdns`. If the `ping 8.8.8.8` failed, I check if there is a captive portal they need to authenticate to, or if they have an IP conflict. Once resolved, I have them open a fresh browser tab to verify."

**SCENARIO 2:**
"You're the only IT person in the office. At 9 AM, 5 employees report they can't access the internet. It was working yesterday. What's your approach?"
- **Response:** "Since this is a multi-user outage, it's a systemic issue, not a client issue. I immediately ask: Are they all on the same floor? On the same WiFi or ethernet? I check my own machine first. I ping the local gateway to see if the internal network is up. If internal is up, I ping 8.8.8.8 to test the ISP. If the ISP is down, I contact them immediately. If the issue is localized to one floor, I check the network closet to see if a switch lost power or uplink. I communicate a quick status update to the office so they know IT is on it."

**SCENARIO 3:**
"A developer comes to you and says the Linux server they use for development is not responding. No one can SSH into it. What do you do?"
- **Response:** "I first try to ping the server. If it pings, the network is up. I try `telnet <ip> 22` to see if the SSH port is accepting connections. If it's not, the `sshd` service might have crashed or the server is hung. I will log into the hypervisor (vCenter or AWS Console) and open the virtual console. From there, I can see if there is a kernel panic, if the disk is full, or I can simply restart the SSH service. If it's a hardware crash, I restart the VM."

**SCENARIO 4:**
"Your monitoring alert shows the /var/log partition on a Linux server is at 95%. No application team is available right now. What do you do?"
- **Response:** "I SSH into the server and run `df -h` to confirm the alert. I navigate to `/var/log` and run `du -sh * | sort -rh | head -5` to find the largest logs. If I find a massive `syslog` or application log, I will NOT delete it because the application will hold the file handle and not release the space. Instead, I run `> /var/log/largefile.log` to truncate the file to zero bytes. This instantly clears space and prevents the server from crashing. I document the action and email the app team."

**SCENARIO 5:**
"A new employee joined today. You need to set up their Windows laptop from scratch. Walk me through the process."
- **Response:** "1. Unbox and connect to power and network. 2. Install base OS image (via SCCM/WDS or USB). 3. Join the laptop to the Active Directory domain. 4. Run all Windows Updates and update OEM drivers (BIOS, firmware). 5. Install standard corporate software (Office 365, AV, VPN). 6. Ensure BitLocker disk encryption is enabled and backed up to AD. 7. Test user login. 8. Hand over the device with a brief orientation on VPN and IT support procedures."

**SCENARIO 6:**
"An employee's Windows PC shows BSOD every time they open a specific application. How do you handle this?"
- **Response:** "I gather the Stop Code from the BSOD screen. I boot the PC, navigate to `C:\Windows\Minidump`, and use a tool like BlueScreenView to identify the faulting driver. If the crash is tied to a specific app, it's often a graphics acceleration issue or an anti-cheat/antivirus conflict. I would boot into Safe Mode, update the application, update the GPU drivers, and disable 'hardware acceleration' within the app. I'll test by opening the app repeatedly to verify stability."

**SCENARIO 7:**
"The company printer suddenly stopped working for everyone. Users are waiting. What's your priority and action plan?"
- **Response:** "My priority is minimizing business impact. I physically check the printer for paper jams, empty toner, or error codes. If hardware is fine, I ping the printer's IP to ensure it's on the network. If the network is fine, the issue is likely the Print Server. I remote into the Print Server, open `services.msc`, and restart the Print Spooler service. This usually clears up hung queues and pushes the waiting jobs through."

**SCENARIO 8:**
"A user reports receiving a suspicious email with an attachment, and their system is now behaving strangely. How do you respond?"
- **Response:** "I treat this as a critical security incident. First, I tell the user to step away from the keyboard and I immediately disconnect the machine from the network (pull the ethernet cable and disable WiFi) to prevent lateral movement of malware. I do NOT turn off the PC, as memory forensics might be needed. I notify the Security/SOC team. If I must handle it, I boot an offline antivirus scanner, image the drive for forensics, and re-image the machine from scratch."

**SCENARIO 9:**
"Your manager asks you to create a new user account in Windows with specific folder access permissions. Walk through the steps."
- **Response:** "I open Active Directory Users and Computers (ADUC). I create the user object with the required naming convention and a strong temporary password (forcing reset on next logon). I assign them to the appropriate Security Groups (e.g., 'Finance_Team'). On the file server, I ensure that the 'Finance_Team' group has the correct NTFS permissions (Modify/Read/Write) to the requested folder. I verify access by logging in as a test user in that group."

**SCENARIO 10:**
"The CEO's laptop is not connecting to the projector in the boardroom. A meeting starts in 10 minutes. What do you do?"
- **Response:** "I bring a spare HDMI cable and a spare laptop just in case. I calmly check the physical connections (dongles, HDMI ports). I press `Win + P` and ensure it's set to 'Duplicate' or 'Extend'. If it doesn't detect, I go to Display Settings and click 'Detect'. If it still fails, I swap the cable or the dongle. In a high-pressure VIP scenario, having a backup plan (the spare laptop) ensures the meeting starts on time while I troubleshoot the CEO's device offline."

---

## PART 5: FOLLOW-UP QUESTION BANKS

### Follow-ups for DNS questions:
- **What is the difference between DNS and DHCP?**
  DNS translates human-readable names (google.com) to IP addresses. DHCP dynamically assigns IP addresses and network config to devices.
- **What command checks DNS resolution on Linux? On Windows?**
  Linux: `dig` or `nslookup`. Windows: `nslookup` or `Resolve-DnsName`.
- **What is an A record? What is a CNAME? What is an MX record?**
  A record maps a name to an IPv4 address. CNAME maps an alias to another domain name. MX record points to the mail server.
- **What happens when DNS fails?**
  Users cannot access websites or servers by name, but can still access them via direct IP address.
- **What is /etc/hosts and how does it relate to DNS?**
  It is a local file that overrides DNS. The OS checks the hosts file for IP mappings before querying a DNS server.

### Follow-ups for networking questions:
- **What is the difference between ping and traceroute?**
  Ping tests reachability and latency to a destination. Traceroute shows the exact path (every router/hop) the packet takes to get there.
- **What does a response time of >100ms mean?**
  High latency. It means packets are taking a long time to travel, causing slow loading times, often due to physical distance or network congestion.
- **What is the meaning of "Request Timeout" in ping?**
  The packet reached a destination or dropped, and no reply was received within the waiting period (could be firewall blocking ICMP, or server is offline).
- **How do you find which port a service is listening on?**
  Windows: `netstat -ano`. Linux: `netstat -tulpn` or `ss -tulpn`.

### Follow-ups for Linux process questions:
- **What is the difference between kill -9 and kill -15?**
  `kill -15` (SIGTERM) asks the process to terminate gracefully. `kill -9` (SIGKILL) forces the kernel to instantly terminate the process.
- **What happens to child processes when parent is killed?**
  If gracefully killed, parent cleans them up. If killed with -9, they may become orphan processes and are usually adopted by systemd (init).
- **What is a zombie process?**
  A process that has completed execution but still has an entry in the process table because its parent hasn't read its exit status.
- **How do you run a process that continues after logout?**
  Use `nohup command &`, or run it inside a terminal multiplexer like `tmux` or `screen`.

### Follow-ups for permission questions:
- **What is SUID, SGID, and Sticky Bit?**
  SUID runs a file with owner privileges (like `passwd`). SGID runs with group privileges. Sticky Bit on a directory ensures only the file owner can delete their files (like `/tmp`).
- **What does chmod 777 mean and why is it dangerous?**
  It grants Read, Write, and Execute permissions to the Owner, Group, and Anyone on the system. It's a massive security risk.
- **What is the difference between chown and chmod?**
  `chown` changes who owns the file. `chmod` changes what permissions people have on the file.
- **How do you give a user sudo access?**
  Add them to the `wheel` group (RHEL) or `sudo` group (Debian), or edit the `/etc/sudoers` file using `visudo`.

### Follow-ups for disk questions:
- **What is the difference between df and du?**
  `df` reports total disk space usage of filesystems. `du` estimates space usage of specific files and directories.
- **How do you find the largest files on a Linux system?**
  `find / -type f -exec du -h {} + | sort -rh | head -n 10`
- **What is an inode? What happens when inodes are exhausted?**
  An inode is a data structure storing metadata about a file. If exhausted (too many small files), you cannot create new files even if there is free disk space.
- **What is LVM?**
  Logical Volume Manager. It allows you to abstract physical disks into logical volumes, allowing easy resizing and snapshotting without downtime.

---

## PART 6: LINUX LOG FILES REFERENCE

Knowing exactly where to look separates a junior from a mid-level engineer. Memorize these locations:

| Problem | Log File | Command |
|---|---|---|
| **Login failures / SSH** | `/var/log/auth.log` (Debian/Ubuntu)<br>`/var/log/secure` (RHEL/CentOS) | `grep 'Failed' /var/log/auth.log` |
| **General system events** | `/var/log/syslog` (Debian/Ubuntu)<br>`/var/log/messages` (RHEL/CentOS) | `tail -f /var/log/syslog` |
| **Service crashes (systemd)**| `journalctl` | `journalctl -u nginx -f` |
| **Disk/Hardware errors** | `/var/log/kern.log` or Kernel Ring Buffer | `dmesg | grep -i error` |
| **Application logs** | `/var/log/<appname>/` | `tail -100 /var/log/nginx/error.log` |
| **Boot messages** | `/var/log/boot.log` | `journalctl -b` |
| **Cron jobs** | `/var/log/cron` | `grep CRON /var/log/syslog` |
| **Package installs** | `/var/log/dpkg.log` or `/var/log/yum.log` | `tail -50 /var/log/dpkg.log` |

---

## PART 7: WINDOWS EVENT VIEWER GUIDE

When dealing with Windows issues, `eventvwr.msc` is your primary tool. You filter by Event IDs. Memorize the most common ones:

| Event ID | Meaning | Which Log | Typical Scenario |
|---|---|---|---|
| **4624** | Successful login | Security | Auditing who accessed a server. |
| **4625** | Failed login | Security | Troubleshooting bad passwords or lockouts. |
| **4648** | Explicit credential logon | Security | Used "Run as administrator". |
| **6005** | Event log service started | System | Indicates the system successfully booted up. |
| **6006** | Event log stopped | System | Indicates the system was cleanly shut down. |
| **41** | Kernel power failure | System | Unexpected restart / BSOD / pulled power plug. |
| **7034** | Service crashed unexpectedly | System | Finding out why Print Spooler or SQL died. |
| **7036** | Service started/stopped | System | Auditing normal service state changes. |
| **1001** | Windows Error Reporting | Application| Tracing an application crash (Faulting module). |

---
*End of Module 2. Review these playbooks thoroughly. In the interview, always vocalize your thought process systematically (Layer 1 up to Layer 7) before suggesting complex fixes.*
