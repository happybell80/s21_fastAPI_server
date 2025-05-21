# Galaxy S21 FastAPI Server

A lightweight FastAPI server implementation designed to run on Samsung Galaxy S21 using Termux.

## 프로젝트 개요

This project demonstrates how to use a mobile device (Samsung Galaxy S21) as a web server by:
- Running FastAPI through Termux
- Setting up Nginx as a reverse proxy
- Making the server accessible via the internet using DDNS
- Using modern web technologies (FastAPI, HTMX, TailwindCSS)

- **다국어 지원**: 영어와 한국어를 모두 지원하여 글로벌 및 국내 사용자를 모두 수용
- **반응형 디자인**: 모바일 및 데스크톱 환경에서 최적화된 사용자 경험 제공
- **확장 가능한 아키텍처**: 데이터 확장 및 기능 추가에 유연하게 대응 가능
- **빠른 성능**: 페이지 로드 2초 이내를 목표로 최적화

## 핵심 기능

- **토큰화된 자산 현황 대시보드**: 실시간 자산 데이터 시각화 및 분석
- **심층 분석 리서치 블로그**: 토큰화 자산 시장에 대한 전문 분석 콘텐츠
- **채용 정보 및 회사 소개**: 기업 정보 및 채용 기회 제공
- **다국어(영/한) 인터페이스**: 언어 전환 기능으로 글로벌 접근성 향상

## 기술 스택

- **백엔드**: Python, FastAPI, Uvicorn
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript
- **데이터베이스**: SQLite (향후 PostgreSQL로 마이그레이션 예정)
- **인프라**: 
  - 개발: Windows Server 또는 Galaxy S21 + Termux
  - 배포: AWS EC2 인스턴스 (예정)
- **웹 서버**: Nginx (리버스 프록시 및 HTTPS)
- **버전 관리**: GitHub, CI/CD(GitHub Actions)

## 설치 및 실행 방법

1. 저장소 클론:
   ```bash
   pkg install git
   git clone https://github.com/yourusername/galaxy-s21-fastapi-server.git
   cd galaxy-s21-fastapi-server
   ```

2. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

3. 서버 실행:
   ```bash
   python app.py
   ```
   또는
   ```bash
   ./run_server.sh
   ```

4. 브라우저에서 접속:
   - 로컬 액세스: http://localhost:8000
   - API 문서: http://localhost:8000/docs

## 디렉토리 구조

```
C:.
│  .gitignore                 # Git에서 무시할 파일 목록
│  app.py                     # FastAPI 메인 애플리케이션 파일
│  gh_actions_key             # GitHub Actions 배포용 SSH 키
│  gh_actions_key.pub         # GitHub Actions 배포용 SSH 공개 키
│  README.md                  # 프로젝트 설명 및 실행 방법
│  requirements.txt           # Python 의존성 패키지 목록
│  run_server.sh              # 서버 실행 스크립트
│  startup.sh                 # 초기 설정 스크립트
│  start_server.sh            # 서버 시작 스크립트
│
├─.github                     # GitHub 관련 설정
│  └─workflows                # GitHub Actions 워크플로우
│          deploy.yml         # CI/CD 배포 파이프라인 설정
│
├─documents                   # 프로젝트 문서
│      development_instructions.md     # 개발 가이드
│      nginx_8443.md                   # Nginx HTTPS 설정 가이드
│      pretrained.md                   # 사전 훈련 모델 정보
│      project_plan.md                 # 프로젝트 계획서
│      s21_fastapi_server_plan.md      # S21 서버 설정 계획
│      termux-ssh-setup.md             # Termux SSH 설정 가이드
│      VSCode-Termux-Setup.md          # VSCode-Termux 연동 가이드
│      vscode_ssh_guide.md             # VSCode SSH 가이드
│
├─static                      # 정적 자산 파일
│  ├─css                      # 스타일시트
│  │      style.css           # 메인 CSS 파일
│  │
│  ├─img                      # 이미지 파일
│  │      Eng-title-from-kpd-2048x1152.png    # 영문 타이틀 이미지
│  │      hipgoose3.jpg                       # 로고 이미지
│  │      websites-under-construction-pages.jpg    # 공사중 이미지
│  │
│  └─js                       # JavaScript 파일
│          main.js            # 메인 JS 파일
│          polyfills.js       # 폴리필 JS 파일
│
├─templates                   # HTML 템플릿
│  │  about.html              # 영문 소개 페이지
│  │  blog.html               # 영문 블로그 페이지
│  │  index.html              # 영문 메인 페이지
│  │
│  ├─includes                 # 영문 공통 컴포넌트
│  │      footer.html         # 영문 푸터
│  │      header.html         # 영문 헤더
│  │
│  └─ko                       # 한국어 템플릿
│      │  about.html          # 한국어 소개 페이지
│      │  blog.html           # 한국어 블로그 페이지
│      │  index.html          # 한국어 메인 페이지
│      │
│      └─includes             # 한국어 공통 컴포넌트
│              footer.html    # 한국어 푸터
│              header.html    # 한국어 헤더
```

## 원격 개발 환경 설정

### Termux(Galaxy S21) 개발 환경 (선택적)

1. Termux 설치 및 초기 설정:
   ```bash
   pkg update && pkg upgrade
   pkg install curl git socat nginx openssh termux-api python
   ```

2. Python 패키지 설치:
   ```bash
   pip install fastapi uvicorn
   ```

3. SSH 접속 설정:
   ```bash
   # Termux에서 SSH 서버 실행
   sshd
   
   # 접속 (다른 기기에서)
   ssh -p 51117 username@rotanevs21.duckdns.org
   ```

4. VSCode Remote-SSH를 통한 개발:
   - VSCode Remote-SSH 익스텐션 설치
   - SSH 호스트 설정 후 연결
   - 원격 디렉토리에서 프로젝트 작업

## 접속 정보

- **로컬 접속**: http://localhost:8080
- **외부 접속**: http://rotanevs21.duckdns.org:8080
- **API 문서**: http://localhost:8080/docs

## 향후 계획

- HTTPS 지원 (SSL/TLS 인증서 적용)
- 데이터베이스 PostgreSQL 마이그레이션
- AWS EC2 배포 환경 구성
- CI/CD 파이프라인 개선
- SEO 최적화 작업

## 라이센스

Copyright © GooseFarmInvesting.com 