# fastapi-app/run_server.sh
#!/data/data/com.termux/files/usr/bin/bash

# 현재 스크립트 위치로 이동
cd "$(dirname "$0")"

# 작업 디렉토리 표시
echo "Starting in directory: $(pwd)"

# 기존 프로세스 정리
echo "Checking for existing processes..."
pkill -f "uvicorn.*app:app" || true
pkill -9 -f "uvicorn.*app:app" || true
sleep 2

# 포트 확인
echo "Checking if port 8000 is in use..."
if ss -tulpn 2>/dev/null | grep -q ':8000'; then
  echo "Port 8000 still in use, forcing termination..."
  pkill -9 -f "uvicorn.*app:app" || true
  sleep 2
fi

# 가상환경 활성화
if [ -d "venv" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

# 필요 패키지 확인
if ! command -v uvicorn &>/dev/null; then
  echo "Installing uvicorn..."
  pip install uvicorn fastapi
fi

# 절전 방지
echo "Enabling wake lock..."
termux-wake-lock

# 서버 시작
echo "Starting uvicorn server..."
setsid "$(which uvicorn)" app:app --host 0.0.0.0 --port 8000 >> "$(pwd)/uvicorn.log" 2>&1 &

echo "Server started at $(date)"
