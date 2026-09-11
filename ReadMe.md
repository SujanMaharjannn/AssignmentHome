# IT Infrastructure & DevOps Trainee: Practical Implementation Documentation

## Introduction
This document explains how we built, secured, containerized, monitored, and backed up our Linux server environment step-by-step from scratch.

## Environment Details
* **Hypervisor:** Proxmox
* **Operating System:** Ubuntu 24.04
* **IP Address:** `192.168.100.130`
* **User Created:** `trainee`

---

## Task 1: Environment Setup, System Verification, and Security Hardening

### Task 1.1: What was the goal?
Before doing anything, we needed to check our virtual machine's basic information and set up a safe workspace so we don't accidentally break things using the root user.

* **How we did it:**
  * **Checked System Info:** We ran commands like `hostnamectl` (to see the server name), `ip a` (to check our IP address `192.168.100.130`), and `cat /etc/os-release` (to confirm we are running Ubuntu 24.04 on Proxmox).
  * **Created a Safe User:** Instead of doing everything as the all-powerful `root` user, we created a normal user named `trainee` using `sudo adduser trainee` and gave them administrative powers using `sudo usermod -aG sudo trainee` (where `-aG` safely adds them to the sudo group).

---

### Task 1.2: What was the goal? (SSH Hardening & Key-Based Authentication)
The goal was to block password logins entirely and use key based authentication instead.

* **How we did it:**
  * **Enabled SSH on Boot:** We made sure SSH starts automatically if the server reboots using `sudo systemctl enable ssh`.
  * **Edited the SSH Config:** We opened `sudo nano /etc/ssh/sshd_config` and made three crucial changes:
    1. Changed the default port from `22` to `2222` (so bots scanning port 22 won't even find our door).
    2. Turned off password login completely (`PasswordAuthentication no`).
    3. Blocked root from logging in directly (`PermitRootLogin no`).
  * **Added Keys:** From our local computer, we generated a secure key using `ssh-keygen -t ed25519 -C "Trainee"` and copied the public key (`.pub`) into the server's `~/.ssh/authorized_keys` file so only our specific computer is allowed to log in.

---

### Task 1.3: What was the goal? (Local Firewall Configuration - UFW)
A firewall acts as a digital security guard, blocking unwanted users.

* **How we did it:**
  * We configured the rules *before* turning on the firewall so we wouldn't accidentally lock ourselves out:
    ```bash
    sudo ufw default deny incoming    # Block everything coming in by default
    sudo ufw default allow outgoing   # Allow our server to download updates safely
    sudo ufw allow 2222/tcp           # Open our custom SSH port
    sudo ufw allow 80/tcp             # Open standard web traffic port (HTTP)
    sudo ufw allow 443/tcp            # Open secure web traffic port (HTTPS)
    sudo ufw enable                   # Turn the firewall on
    ```
    
After enabling all these, rebooted the ssh service `sudo systemctl restart ssh`.
The reboot was completed and the all the necessary task that we were assigned in the Task 1 was completed after successful login in the VM via key-based authentication. 

---

## Task 2: Containerization & Nginx Reverse Proxy

### Task 2.1: What was the goal?
Instead of installing Python, databases, and web servers directly onto our host computer where they can conflict with each other, we needed to run them inside isolated "boxes" called containers using Docker.

* **How we did it:**
  * We created a `docker-compose.yml` file to manage three services running together:
    1. **Nginx (The Traffic Cop / Reverse Proxy):** Sits at the front door. It serves our static files (`index.html`) directly. However, when a request needs backend processing, Nginx acts as a reverse proxy—safely forwarding that traffic behind the scenes to our Flask app instead of exposing Flask directly to the internet.
    2. **Flask Backend (`backendS2`):** A lightweight Python application handling backend logic. When Nginx forwards traffic here, Flask responds with our custom greeting message.
    3. **PostgreSQL Database:** A secure, isolated database container storing data safely on a private internal Docker network.
  * We launched the whole stack in the background using:
    ```bash
    docker compose up -d
    ```

---

## Task 3: Scripting and Automated Backups

### Task 3.1: What was the goal? (CPU Usage Check Script)
We needed to write a custom bash script that checks how hard the server's CPU is working so we can monitor system health.

* **How we did it:**
  * Created a shell script file that reads system performance metrics (using utilities like `top` or `vmstat`).
  * Added conditional logic inside the script to print warning alerts if CPU usage crosses safety thresholds.
  * Made the script executable using `chmod +x script_name.sh` so it can be run anytime.

---

### Task 3.2: What was the goal? (Automated Database Backups & Cron Jobs)
If a database crashes, we need a safety copy. The goal was to automatically back up our PostgreSQL database every day without manual work.

* **How we did it:**
  * **The Backup Command:** We used `docker exec` combined with `pg_dump` to extract a clean copy of the database and save it into a timestamped file on our host machine.
  * **Automation via Cron (`crontab -e`):** 
    * We opened the background job scheduler by typing `crontab -e`.
    * We added a scheduled time rule (running automatically at midnight every day) to execute our backup script in the background seamlessly.

---

## Task 4: Monitoring Stack (Prometheus & Node Exporter)

### Task 4.1: What was the goal?
To keep an eye on hardware stats (like memory, CPU load, and disk space), we needed a dedicated monitoring setup.

* **How we did it:**
  * **Node Exporter:** Installed on the server to harvest raw hardware metrics and expose them on port `9100`.
  * **Prometheus:** Configured via `prometheus.yml` to regularly "scrape" (pull) data from Node Exporter every 15 seconds.
  * **Verification:** We opened the Prometheus web dashboard in our browser and verified that our targets were active and showing a status of **UP**.

---

## Task 5: Version Control & GitHub Synchronization

### Task 5.1: What was the goal?
To save our code history and back up our entire assignment configuration to GitHub.

* **How we did it:**
  * **Initialized Git:** Set up local tracking inside our project folder:
    ```bash
    git init
    git config user.name "SujanMaharjannn"
    git config user.email "soohjaan07@gmail.com"
    ```
  * **Staged & Committed Files:** Gathered all configuration files (`docker-compose.yml`, `nginx.conf`, scripts, and this README) and saved a snapshot:
    ```bash
    git add .
    git commit -m "Initial-Commit with complete project implementation"
    ```
  * **Pushed to GitHub:** Connected our local folder to our remote GitHub repository (`AssignmentHome`) using a secure Personal Access Token (PAT) so GitHub accepts our push without permission errors:
    ```bash
    git remote add origin [https://github.com/SujanMaharjannn/AssignmentHome.git](https://github.com/SujanMaharjannn/AssignmentHome.git)
    git branch -M main
    git push -u origin main
    ```
