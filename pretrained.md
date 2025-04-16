## FastAPI 서버 구축

### 개발 환경
- **백엔드 프레임워크**: FastAPI
- **프론트엔드 추천**: HTMX 또는 Vanilla JS + TailwindCSS
  - 리소스 최소화, JS 번들링 불필요, 반응성 좋고 유지보수 용이
- **코드 작성 및 관리**: VSCode + GitHub
  - SSH를 통해 Windows 데스크탑에서 Galaxy S21 접근

### 네트워크 및 외부 접근 설정
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

### 서버 구성 (Galaxy S21 내부)
- **Termux 초기 설정**:
    ```bash
    pkg update && pkg upgrade
    pkg install curl git socat nginx openssh termux-api python
    ```

- **FastAPI 앱 실행**:
    ```bash
    pip install fastapi uvicorn
    uvicorn app:app --host 0.0.0.0 --port 8080
    ```

- **Nginx 리버스 프록시 설정**:
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

### 자동 시작 설정
- **Termux:Boot 설정**:
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
    ```
    ```bash
    chmod +x ~/.termux/boot/startup.sh
    ```

### 향후 계획
- AWS EC2에서 Nginx 리버스 프록시 설정
- 외부 접속은 `rotanevs21.duckdns.org` → EC2 → Galaxy S21으로 전달
- HTTPS 설정 완료 후 EC2는 단순 포워딩 역할 수행 