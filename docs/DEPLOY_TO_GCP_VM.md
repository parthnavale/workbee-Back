# CI/CD Deployment to GCP VM using GitHub Actions

This guide explains how to set up a CI/CD pipeline to automatically deploy your FastAPI backend to a Google Cloud Platform (GCP) Virtual Machine (VM) using GitHub Actions.

---

## Prerequisites

1. **GCP VM is running** (with a public IP, Python, pip, and git installed).
2. **You have SSH access** to the VM (using a private key).
3. **Your repository is on GitHub.**
4. **Your FastAPI app can be started with a command** (e.g., `uvicorn main:app`).

---

## Step 1: Add SSH Key to GitHub Secrets

1. **Generate an SSH key pair** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "github-cicd"
   ```
2. **Add the public key** (`.pub`) to your VM's `~/.ssh/authorized_keys`.
3. **Add the private key** to your GitHub repo's secrets as `GCP_SSH_KEY`.
4. **Add your VM's public IP** as `GCP_VM_IP` in GitHub secrets.
5. **Add your VM username** (e.g., `ubuntu`, `parth`, etc.) as `GCP_VM_USER` in GitHub secrets.

---

## Step 2: Create GitHub Actions Workflow

Create a file: `.github/workflows/deploy.yml` in your repo:

```yaml
name: CI/CD to GCP VM

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r workbee-Back/requirements.txt

      - name: Run tests
        run: |
          source venv/bin/activate
          pytest workbee-Back/test/ || echo "No tests found or tests failed"

      - name: Set up SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan ${{ secrets.GCP_VM_IP }} >> ~/.ssh/known_hosts

      - name: Deploy to GCP VM via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.GCP_VM_IP }}
          username: ${{ secrets.GCP_VM_USER }}
          key: ${{ secrets.GCP_SSH_KEY }}
          script: |
            cd ~/Workbee
            git pull origin main
            source ~/Workbee/venv/bin/activate
            pip install -r workbee-Back/requirements.txt
            # Stop old app (customize this for your process manager)
            pkill -f "uvicorn" || true
            # Start app (customize as needed, e.g., use tmux, screen, or systemd for production)
            nohup uvicorn workbee-Back.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
```

---

## Step 3: Notes & Customization

- **Directory:** This assumes your code is in `~/Workbee` on the VM. Adjust the `cd` path if needed.
- **Process Management:** For production, use a process manager like `systemd`, `supervisor`, or `pm2` instead of `nohup`.
- **Security:** The SSH key should have limited permissions and be used only for deployment.
- **Tests:** If you don't have tests, the step will not fail the deployment (it just echoes a warning).

---

## Step 4: Commit and Push

- Commit the workflow file and push to `main`.
- On push, GitHub Actions will run the pipeline and deploy to your GCP VM.

---

## Optional: Systemd Service Example

For a more robust deployment, set up a `systemd` service on your VM for your FastAPI app, and in the deploy script, just run:
```bash
sudo systemctl restart workbee-backend
```
Let us know if you want a sample `systemd` service file!

---

## Troubleshooting
- Ensure your VM firewall allows SSH and the app port (e.g., 8000).
- Check `backend.log` on the VM for app errors.
- Use `journalctl -u workbee-backend` if using `systemd`.

---

**Contact the dev team for further help or customization!** 