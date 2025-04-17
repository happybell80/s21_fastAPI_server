#!/data/data/com.termux/files/usr/bin/bash

# Log file for debugging
LOG_FILE=/data/data/com.termux/files/home/termux_boot.log
echo "Boot script started at $(date)" > $LOG_FILE

# Enable wake lock to prevent sleep
termux-wake-lock
echo "Wake lock enabled" >> $LOG_FILE

# Set working directory
cd /data/data/com.termux/files/home/apps/fastapi-app
echo "Changed to app directory: $(pwd)" >> $LOG_FILE

# Start SSH server
sshd
echo "SSH server started" >> $LOG_FILE

# Start Nginx
nginx
echo "Nginx started" >> $LOG_FILE

# Check if port 8000 is already in use
if ss -tulpn | grep -q ':8000'; then
  echo "Port 8000 is in use, stopping existing process..." >> $LOG_FILE
  pkill -f "uvicorn.*app:app" || true
  sleep 2
  # Force kill if still running
  if ss -tulpn | grep -q ':8000'; then
    echo "Forcing termination of process on port 8000" >> $LOG_FILE
    pkill -9 -f "uvicorn.*app:app" || true
    sleep 1
  fi
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
  echo "Virtual environment activated" >> $LOG_FILE
fi

# Start the FastAPI application (no reload in production)
echo "Starting FastAPI application..." >> $LOG_FILE
setsid uvicorn app:app --host 0.0.0.0 --port 8000 >> uvicorn.log 2>&1 &

echo "Boot script completed at $(date)" >> $LOG_FILE 