# fastapi-app/run_server.sh
#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")"
termux-wake-lock
setsid "$HOME/apps/fastapi-app/venv/bin/uvicorn" app:app --host 0.0.0.0 --port 8000 >> "$HOME/apps/fastapi-app/uvicorn.log" 2>&1 &
