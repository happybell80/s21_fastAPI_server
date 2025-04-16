# FastAPI 기반 Galaxy S21 Termux 서버 구축 요약

## 1. 개발 환경
- **백엔드 프레임워크**: FastAPI
- **프론트엔드 추천**: HTMX 또는 Vanilla JS + TailwindCSS  
  - 리소스 최소화, JS 번들링 불필요, 반응성 좋고 유지보수 용이
- **코드 작성 및 관리**: VSCode + GitHub  
  - SSH를 통해 Windows 데스크탑에서 Galaxy S21 접근

## 2. 개발 장치 및 환경
- **기기**: Galaxy S21 (8GB RAM, 256GB 저장공간)
- **운영 환경**: Android + Termux
- **접속 방식**: SSH (Windows에서 접속)
- **서버 실행**: Uvicorn (FastAPI 실행용 ASGI 서버) + Nginx (리버스 프록시 및 정적 파일 제공)

## 3. 네트워크 및 외부 접근 설정
- **도메인**: rotanevs21.duckdns.org
- **DDNS 서비스**: DuckDNS
- **외부 접속 주소**
  - HTTP: http://rotanevs21.duckdns.org:8080
  - HTTPS: https://rotanevs21.duckdns.org:8443 (추후 설정 예정)
- **AWS EC2 리버스 프록시 계획**
  - EC2:80 → S21:8080 포트 포워딩
  - 예시 Nginx 설정:
    ```nginx
    location / {
        proxy_pass http://S21_IP:8080;
    }
    ```

## 4. 서버 구성 요약 (Galaxy S21 내부)
- Termux 초기 설정:
    ```bash
    pkg update && pkg upgrade
    pkg install curl git socat nginx openssh termux-api python
    ```

- FastAPI 앱 실행 예시:
    ```bash
    pip install fastapi uvicorn
    uvicorn app:app --host 0.0.0.0 --port 8080
    ```

- Nginx 리버스 프록시 설정 (8080 → FastAPI):
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

## 5. SSH 및 보안 구성
- 기본 포트: 8022 → 51117 등으로 변경 권장
- 공개키 인증 및 비밀번호 로그인 차단
- Termux:Boot을 통한 자동 시작:
    ```bash
    mkdir -p ~/.termux/boot
    nano ~/.termux/boot/startup.sh
    ```

    ```bash
    # startup.sh 내용:
    termux-wake-lock
    sshd
    nginx
    uvicorn app:app --host 0.0.0.0 --port 8080
    chmod +x ~/.termux/boot/startup.sh
    ```

## 6. 향후 계획
- AWS EC2에서 Nginx 리버스 프록시 설정 후
- 외부 접속은 `rotanevs21.duckdns.org` → EC2 → Galaxy S21으로 전달
- HTTPS 설정까지 마무리되면, EC2는 단순 포워딩 역할
