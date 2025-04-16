#!/data/data/com.termux/files/usr/bin/bash

# 시스템 모니터링 의존성 설치 스크립트
echo "=== 시스템 모니터링 의존성 설치 ==="

# Python 패키지 설치
pip install psutil fastapi-utils

echo "=== 설치 완료 ==="
echo "시스템 모니터링을 위한 의존성이 설치되었습니다."
echo "이제 start_server.sh를 다시 실행하여 서버를 재시작하세요." 