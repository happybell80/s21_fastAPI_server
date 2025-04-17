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

# 서버 실행은 통합 스크립트로 일원화
echo "Starting FastAPI via unified script..." >> $LOG_FILE
bash run_server.sh >> $LOG_FILE 2>&1

echo "Boot script completed at $(date)" >> $LOG_FILE 