# Simple GCP VM Setup for Workbee Backend

This guide explains how to deploy your FastAPI backend and MySQL database on a single, cost-effective Google Cloud Platform (GCP) VM using the Free Tier.

---

## 1. Create a Free Tier GCP Account & Project
- [Sign up for GCP Free Tier](https://cloud.google.com/free) if you haven't already.
- Create a new project in the GCP Console.

---

## 2. Create a Free VM (e2-micro)

1. Go to **Compute Engine > VM Instances**.
2. Click **Create Instance**.
3. Choose:
   - **Machine type:** e2-micro (free tier)
   - **Region/Zone:** Any free tier eligible (e.g., us-central1)
   - **Boot disk:** Ubuntu 22.04 LTS
   - **Allow HTTP and HTTPS traffic**
4. Click **Create**.

---

## 3. SSH Into Your VM

- In the GCP Console, click **SSH** next to your VM.

---

## 4. Install Required Software

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git mysql-server -y
```

---

## 5. Set Up MySQL

```bash
sudo systemctl start mysql
sudo mysql_secure_installation
```
- Set a root password and answer prompts.
- Create your database and user:
  ```bash
  sudo mysql -u root -p
  CREATE DATABASE workbee_db;
  CREATE USER 'workbee_user'@'localhost' IDENTIFIED BY 'yourpassword';
  GRANT ALL PRIVILEGES ON workbee_db.* TO 'workbee_user'@'localhost';
  FLUSH PRIVILEGES;
  EXIT;
  ```

---

## 6. Set Up Your FastAPI App

```bash
git clone <your-repo-url>
cd Workbee/workbee-Back
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
- Update your FastAPI database config to use:
  ```
  mysql+pymysql://workbee_user:yourpassword@localhost/workbee_db
  ```

---

## 7. Open Firewall Port for FastAPI

- In GCP Console:  
  Go to **VPC network > Firewall** → **Create Firewall Rule**:
  - Name: allow-fastapi
  - Source IP: 0.0.0.0/0
  - Port: tcp:8000

---

## 8. Run Your API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
- Your API is now accessible at `http://<EXTERNAL_IP>:8000`

---

**This setup is free (within free tier limits) and very simple.**  
You can always migrate to managed services later if you need more scalability or reliability. 