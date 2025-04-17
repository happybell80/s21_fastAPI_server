#!/data/data/com.termux/files/usr/bin/bash

# Display banner
echo "===================================="
echo "  Galaxy S21 FastAPI Server Starter"
echo "===================================="

# Set working directory to script location
cd "$(dirname "$0")"

# Enable wake lock to prevent sleep
echo "Enabling wake lock..."
termux-wake-lock

# Check if required packages are installed
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Python is required but not installed. Installing..."; pkg install python; }
command -v pip >/dev/null 2>&1 || { echo "Pip is required but not installed. Installing..."; pkg install python-pip; }
command -v nginx >/dev/null 2>&1 || { echo "Nginx is required but not installed. Installing..."; pkg install nginx; }

# Install Python dependencies if not already installed
echo "Checking Python dependencies..."
pip show fastapi >/dev/null 2>&1 || { echo "Installing FastAPI..."; pip install fastapi; }
pip show uvicorn >/dev/null 2>&1 || { echo "Installing Uvicorn..."; pip install uvicorn; }
pip show jinja2 >/dev/null 2>&1 || { echo "Installing Jinja2..."; pip install jinja2; }

# Check if port 8000 is in use
echo "Checking if port 8000 is in use..."
if ss -tulpn | grep -q ':8000'; then
  echo "Port 8000 is in use. Stopping existing process..."
  pkill -f "uvicorn.*app:app" || true
  sleep 2
  
  # Force kill if still running
  if ss -tulpn | grep -q ':8000'; then
    echo "Forcing termination of process on port 8000..."
    pkill -9 -f "uvicorn.*app:app" || true
    sleep 1
  fi
fi

# Start SSH server if not already running
echo "Starting SSH server..."
pgrep sshd >/dev/null 2>&1 || sshd

# Create directories if they don't exist
mkdir -p static templates

# Copy Nginx configuration if it exists
if [ -f nginx.conf ]; then
    echo "Setting up Nginx configuration..."
    cp nginx.conf /data/data/com.termux/files/usr/etc/nginx/nginx.conf
fi

# Start Nginx
echo "Starting Nginx..."
pkill nginx 2>/dev/null
nginx

# Start the FastAPI application (no reload in production)
echo "Starting FastAPI server in the background..."
echo "Access the server at: http://localhost:8080"
echo "API documentation at: http://localhost:8080/docs"
echo "===================================="

# Run the server in the background instead of foreground
setsid "$HOME/apps/fastapi-app/venv/bin/uvicorn" app:app --host 0.0.0.0 --port 8000 > "$HOME/apps/fastapi-app/uvicorn.log" 2>&1 &

# Print success message
echo "Server started in background. Check uvicorn.log for details." 