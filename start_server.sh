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
pip show watchfiles >/dev/null 2>&1 || { echo "Installing watchfiles for improved reload..."; pip install watchfiles; }

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

# Start the FastAPI application
echo "Starting FastAPI server..."
echo "Access the server at: http://localhost:8080"
echo "API documentation at: http://localhost:8080/docs"
echo "Press Ctrl+C to stop the server"
echo "===================================="

# Run the server 
uvicorn app:app --host 0.0.0.0 --port 8000 --reload 