# Termux SSH 서버 설정 핵심 요약 (Samsung S21)

## 1. SSH 설치 및 실행

```bash
pkg install openssh
passwd     # 비밀번호 설정
sshd       # SSH 서버 실행
```

## 2. 접속 명령어 (외부에서)

```bash
ssh -p 8022 u0_a317@rotanevs21.duckdns.org
```

## 3. 자동 시작 설정

### 화면 꺼짐 방지

- 개발자 옵션 > "화면 켜진 상태로 유지" 활성화
    
- `termux-wake-lock` 실행
    
- 앱 설정에서 배터리 절전 최적화 해제
    

### Termux:Boot 설정

```bash
mkdir -p ~/.termux/boot
nano ~/.termux/boot/start-ssh.sh
```

```bash
#!/data/data/com.termux/files/usr/bin/bash
sshd
```

```bash
chmod +x ~/.termux/boot/start-ssh.sh
```

- F-Droid에서 Termux:Boot 설치 필요
    
- Termux 한 번 실행 후 자동 시작됨
    

## 4. 테스트

```bash
curl localhost:8080       # 내부에서 Nginx 확인
curl http://<DDNS>:8080   # 외부에서 확인
```