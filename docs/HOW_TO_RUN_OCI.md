# How to Deploy Workbee Backend on Oracle Cloud Infrastructure (OCI)

This guide explains how to deploy your FastAPI backend on an OCI Compute instance (virtual machine).

---

## 1. Provision an OCI Compute Instance
- Log in to your [OCI Console](https://cloud.oracle.com/).
- Go to **Compute > Instances** and click **Create Instance**.
- Choose an image (Oracle Linux, Ubuntu, etc.), shape, and networking options.
- Add your SSH public key for remote access.
- Launch the instance and note its public IP address.

## 2. Connect to Your Instance
```bash
ssh opc@<your_public_ip>
```
- Use `opc` for Oracle Linux/Ubuntu, or the default user for your image.

## 3. Update System and Install Python
```bash
sudo yum update -y   # or sudo apt update && sudo apt upgrade -y
sudo yum install python3 python3-venv git -y   # or sudo apt install python3 python3-venv git -y
```

## 4. Clone Your Project
```bash
git clone <your_repo_url>
cd <your_project_folder>
```

## 5. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r workbee-Back/requirements.txt
pip install gunicorn uvicorn
```

## 6. Set Environment Variables
```bash
export WORKBEE_SECRET_KEY="your-very-secret-key"
export WORKBEE_DATABASE_URL="sqlite:///./workbee.db"  # Or your production DB URL
```

## 7. Run the App with Gunicorn/Uvicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker workbee-Back.main:app --bind 0.0.0.0:8000
```

## 8. (Recommended) Set Up Nginx as a Reverse Proxy
```bash
sudo yum install nginx -y   # or sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```
- Edit `/etc/nginx/nginx.conf` or `/etc/nginx/sites-available/default` to add:
```
server {
    listen 80;
    server_name <your_public_ip>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- Restart Nginx:
```bash
sudo systemctl restart nginx
```

## 9. Open Firewall Ports
- In the OCI Console, go to **Networking > Virtual Cloud Networks > Subnets > Security Lists**.
- Add an **Ingress Rule** to allow TCP traffic on port 80 (HTTP) and 8000 (if you want direct access).

## 10. (Optional) Use a Process Manager
- Use `systemd` or `supervisor` to keep your app running and restart on failure.

---

Your FastAPI backend should now be accessible at `http://<your_public_ip>/`.

For more, see the [OCI documentation](https://docs.oracle.com/en-us/iaas/Content/home.htm) and [FastAPI deployment docs](https://fastapi.tiangolo.com/deployment/). 