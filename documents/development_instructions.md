# Development Instructions: FastAPI Server on Galaxy S21

## Project Overview
This project aims to build a FastAPI server on a Samsung Galaxy S21 using Termux, making it accessible via the internet using DDNS.

## Development Environment

### Hardware
- **Server device**: Samsung Galaxy S21 (8GB RAM, 256GB storage)
- **Development device**: Windows desktop/laptop (for remote coding)

### Software Stack
- **Backend framework**: FastAPI
- **Server**: Uvicorn (ASGI)
- **Proxy**: Nginx
- **Remote access**: SSH
- **Frontend tech**: HTMX or Vanilla JS + TailwindCSS
  - Note: Chosen for minimal resource usage and no JS bundling required
- **Development tools**: VSCode + GitHub

## Network Configuration

### Domain Settings
- **Domain**: rotanevs21.duckdns.org
- **DDNS service**: DuckDNS
- **Access URLs**:
  - HTTP: http://rotanevs21.duckdns.org:8080
  - HTTPS: https://rotanevs21.duckdns.org:8443 (planned for future)

### AWS Integration (Future Plan)
- EC2 instance will serve as a reverse proxy
- Traffic flow: rotanevs21.duckdns.org → EC2:80 → S21:8080
- Sample Nginx config for EC2:
  ```nginx
  location / {
      proxy_pass http://S21_IP:8080;
  }
  ```

## Setup Instructions

### 1. Termux Initial Setup
```bash
pkg update && pkg upgrade
pkg install curl git socat nginx openssh termux-api python
```

### 2. SSH Server Setup
```bash
# Install OpenSSH if not included above
pkg install openssh

# Set password
passwd

# Start SSH server
sshd
```

### 3. Security Enhancements
```bash
# Change SSH port (edit /data/data/com.termux/files/usr/etc/ssh/sshd_config)
# Set: Port 51117

# Set up public key authentication
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# Add your public key to ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Disable password login (edit sshd_config)
# Set: PasswordAuthentication no
# Set: ChallengeResponseAuthentication no

# Apply changes
pkill sshd
sshd
```

### 4. FastAPI App Setup
```bash
# Install FastAPI and Uvicorn
pip install fastapi uvicorn

# Create a simple app (app.py)
# Run the app
uvicorn app:app --host 0.0.0.0 --port 8080
```

### 5. Nginx Configuration
- Create/edit Nginx config file:
```nginx
server {
    listen 8080;
    server_name rotanevs21.duckdns.org;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 6. Auto-start Setup
```bash
# Create boot directory
mkdir -p ~/.termux/boot

# Create startup script
nano ~/.termux/boot/startup.sh
```

Contents of startup.sh:
```bash
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
sshd
nginx
uvicorn app:app --host 0.0.0.0 --port 8080
```

```bash
# Make executable
chmod +x ~/.termux/boot/startup.sh
```

Additional preparations:
- Enable "Keep screen on" in developer options
- Disable battery optimization for Termux
- Install Termux:Boot from F-Droid

## Development Workflow

1. Connect to Galaxy S21 from Windows via SSH:
   ```bash
   ssh -p 51117 username@rotanevs21.duckdns.org
   ```

2. Use VSCode Remote SSH extension for development

3. Test locally on the device first:
   ```bash
   curl localhost:8080
   ```

4. Test external access:
   ```bash
   curl http://rotanevs21.duckdns.org:8080
   ```

## Next Steps

1. Implement the FastAPI application
2. Set up the AWS EC2 reverse proxy
3. Configure HTTPS with SSL certificates
4. Implement monitoring and reliability measures 