# Nginx 설정 및 HTTPS 가이드

## 1. Nginx 설정 파일 수정하기

### 현재 문제점 및 해결 방법
- 현재 포트 8080이 이미 사용 중
- SSL 인증서 경로 설정 필요
- user 지시문으로 인한 경고 메시지 제거 필요

### 수정된 전체 nginx.conf 파일

```nginx
# /data/data/com.termux/files/usr/etc/nginx/nginx.conf

# user 지시문 제거 (경고 메시지 방지)
worker_processes 1;

events {
    worker_connections 1024;
}

http {
    include mime.types;
    default_type application/octet-stream;

    # HTTP 설정 (8080 포트)
    server {
        listen 8080;
        server_name rotanevs21.duckdns.org;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Serve static files directly
        location /static/ {
            alias /data/data/com.termux/files/home/fastapi-app/static/;
            expires 1d;
        }

        # Enable WebSocket support
        location /ws {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

        # Improve performance
        gzip on;
        gzip_types text/plain text/css application/json application/javascript;
    }

    # HTTPS 설정 (8443 포트)
    server {
        listen 8443 ssl;
        server_name rotanevs21.duckdns.org;

        # SSL 인증서 설정
        ssl_certificate /data/data/com.termux/files/home/.acme.sh/rotanevs21.duckdns.org_ecc/fullchain.cer;
        ssl_certificate_key /data/data/com.termux/files/home/.acme.sh/rotanevs21.duckdns.org_ecc/rotanevs21.duckdns.org.key;

        # SSL 최적화 설정
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
        }

        # Serve static files directly
        location /static/ {
            alias /data/data/com.termux/files/home/fastapi-app/static/;
            expires 1d;
        }

        # WebSocket 지원
        location /ws {
            proxy_pass http://127.0.0.1:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

        # 성능 최적화
        gzip on;
        gzip_types text/plain text/css application/json application/javascript;
    }
}
```

## 2. Nginx 재시작 방법

### 기존 Nginx 프로세스 완전히 종료하기
```bash
# 기존 Nginx 프로세스 강제 종료
pkill -9 nginx

# runsv 프로세스가 남아있는지 확인
ps aux | grep nginx
```

### 새 설정 테스트 및 적용
```bash
# 설정 파일 문법 검사
nginx -t

# Nginx 시작
nginx
```

## 3. SSL 인증서 파일 확인

인증서 파일 경로가 올바른지 확인:
```bash
# 인증서 파일 확인
ls -la /data/data/com.termux/files/home/.acme.sh/rotanevs21.duckdns.org_ecc/
```

다음 파일들이 반드시 있어야 합니다:
- `fullchain.cer` (인증서 체인 파일)
- `rotanevs21.duckdns.org.key` (개인 키 파일)

## 4. 서버 설정 순서

1. 기존 nginx 프로세스 중지
2. 설정 파일 수정
3. FastAPI 애플리케이션 실행 (8000 포트)
   ```bash
   cd ~/fastapi-app
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```
4. Nginx 시작 (8080 및 8443 포트 리스닝)
   ```bash
   nginx
   ```

## 5. 문제 해결

### 8080 포트 사용 중 오류 시
```bash
# 8080 포트 사용 중인 프로세스 확인
ps aux | grep 8080

# 또는
ss -tuln | grep 8080

# 해당 프로세스 종료
kill -9 [PID]
```

### SSL 인증서 문제 발생 시
1. 인증서 경로가 올바른지 확인
2. 인증서 파일 권한 확인 (읽기 권한 필요)
   ```bash
   chmod 644 /data/data/com.termux/files/home/.acme.sh/rotanevs21.duckdns.org_ecc/fullchain.cer
   chmod 600 /data/data/com.termux/files/home/.acme.sh/rotanevs21.duckdns.org_ecc/rotanevs21.duckdns.org.key
   ```

### 서버 로그 확인
```bash
cat /data/data/com.termux/files/usr/var/log/nginx/error.log
```

## 6. 포트 포워딩 및 방화벽 설정

1. 라우터에서 8080 및 8443 포트를 Galaxy S21의 내부 IP로 포워딩
2. 방화벽 설정에서 해당 포트 개방 확인
3. DuckDNS에서 도메인이 현재 외부 IP로 제대로 설정되었는지 확인 