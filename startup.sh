#!/data/data/com.termux/files/usr/bin/bash

# Log file for debugging
LOG_FILE=/data/data/com.termux/files/home/termux_boot.log
echo "Boot script started at $(date)" > $LOG_FILE

# Enable wake lock to prevent sleep
termux-wake-lock
echo "Wake lock enabled" >> $LOG_FILE

# Set working directory
cd /data/data/com.termux/files/home
echo "Changed to home directory" >> $LOG_FILE

# Start SSH server
sshd
echo "SSH server started" >> $LOG_FILE

# Start Nginx
nginx
echo "Nginx started" >> $LOG_FILE

# Start the FastAPI application
echo "Starting FastAPI application..." >> $LOG_FILE
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --reload >> $LOG_FILE 2>&1 &

echo "Boot script completed at $(date)" >> $LOG_FILE 