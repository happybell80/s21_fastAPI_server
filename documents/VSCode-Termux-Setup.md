# VS Code Remote-SSH on Termux (Galaxy S21) Setup Guide

## 1. 개요
Termux 환경(안드로이드)에서 VS Code Remote-SSH를 이용해 원격 편집을 시도할 때 마주친 이슈와 해결 방안을 정리한 가이드입니다.

---

## 2. 필수 사전 조건
- Termux 설치 및 최신화:
  ```bash
  pkg update && pkg upgrade
  ```
- OpenSSH 설치:
  ```bash
  pkg install openssh
  ```
- Git 설치:
  ```bash
  pkg install git
  ```

---

## 3. Node.js 설치
VS Code Server 구동을 위해 Node.js가 필요합니다.
```bash
pkg install nodejs
node -v  # 버전 확인, 예: v23.11.0
```

---

## 4. getconf 에뮬레이트 스크립트
VS Code는 `getconf _POSIX_VERSION` 체크를 수행합니다. `getconf`가 없으면 아래와 같이 간단한 쉘 스크립트로 대체하세요.

```bash
cat << 'EOF' > $PREFIX/bin/getconf
#!/data/data/com.termux/files/usr/bin/env sh
# VS Code Cursor Server 용 getconf 에뮬레이트
case "$1" in
  _POSIX_VERSION) echo 200809 ;;
  *) echo ;;
esac
EOF
chmod +x $PREFIX/bin/getconf
```

---

## 5. GLIBC / musl 문제 해결 방법

### A) Alpine 리눅스 컨테이너 (`proot-distro`)
Termux 자체는 Bionic libc 기반이므로, VS Code Server의 GLIBC 체크를 통과하려면 proot-distro로 가벼운 컨테이너를 사용하세요.

```bash
pkg install proot-distro
proot-distro install alpine
proot-distro login alpine
# 컨테이너 내부
apk update
apk add openssh nodejs libstdc++
# SSH 서버 실행 후 로컬 포워딩 또는 포트 개방
```

이제 VS Code에서 `ssh-remote+localhost:<포트>` 로 접속하면 됩니다.

### B) 클라우드 VM / code-server 대안
- **원격 VM**: Ubuntu/Debian 올린 뒤 VS Code Server 설치 → SSH 접속
- **code-server**: Termux에 직접 실행하여 브라우저로 접속
  ```bash
  pkg install yarn
  yarn global add code-server
  code-server --bind-addr 0.0.0.0:8080
  ```

---

## 6. GitHub Codespaces 활용 (추천)
Termux 환경 설정 없이도 GitHub Codespaces를 사용하면, 웹 브라우저에서 바로 VS Code 에디터 경험을 제공합니다.

1. 프로젝트를 GitHub에 푸시:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```
2. GitHub 웹페이지에서 **Code → Codespaces → New codespace** 클릭
3. 웹 상에서 편집 및 터미널 사용

---

## 7. 요약
- **Node.js 설치** 및 **getconf 스크립트**를 적용하면 기본적인 `node: not found` 이슈 해소
- **GLIBC 체크 실패** 시 `proot-distro` Alpine 컨테이너 사용 권장
- 추가로 클라우드 VM 또는 **code-server**, **GitHub Codespaces** 활용 가능