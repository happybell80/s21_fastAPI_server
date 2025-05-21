# GooseFarmInvesting.com 프로젝트 계획

## Agents 지시사항 (중요!!!!!)

- 절대 시킨 것 이외의 행동을 하지 않기
- 뭔가를 하려면 충분한 설명을 하고 허락 받기
- 단계별로 확인을 받고 진행하기
- 수정이 완료되면 이 파일 (project_plan.md) 첨가하기. 첨가만 하기.
- 오류 수정한 내용은 상세한 설명과 함께 error_fix.md 파일에 따로 적기(디렉토리 documents)


## 1. 개요

GooseFarmInvesting.com은 실물 자산(RWA, Real World Asset)을 토큰화하여 시장 참여자에게 심층 인사이트와 분석 도구를 제공하는 웹 플랫폼입니다. 본 문서는 프로젝트의 진행 상황과 향후 개발 로드맵을 제시합니다.

## 2. 목적

- RWA 시장 데이터의 수집, 분석, 시각화를 통해 투자 판단을 지원합니다.
- 영어와 한국어를 모두 지원하여 글로벌 및 국내 사용자를 모두 수용합니다.
- 안정적이고 확장 가능한 백엔드 API와 반응형 프론트엔드를 구현합니다.

## 3. 범위

1. **핵심 기능**
   - 토큰화된 자산 현황 대시보드
   - 심층 분석 리서치 블로그
   - 채용 정보 및 회사 소개 페이지
   - 다국어(영/한) 인터페이스 및 토글 기능
2. **비기능 요구사항**
   - 성능: 페이지 로드 2초 이내
   - 보안: HTTPS, CSRF 방어, 입력 검증
   - 접근성: WCAG AA 수준 준수

## 4. 타임라인 및 마일스톤

| 기간           | 작업 항목                                   | 상태     |
|--------------|-----------------------------------------|--------|
| 2023-01-15   | 프로젝트 셋업 및 환경 구성                         | 완료     |
| 2023-01-20   | FastAPI 서버 및 기본 라우팅 구현                  | 완료     |
| 2023-04-10   | 다국어 지원(영/한) 및 언어 토글 기능                  | 완료     |
| 2023-04-22   | JavaScript 오류 수정 및 스무스 스크롤링 개선         | 완료     |
| 2023-04-23   | 모바일·데스크탑 반응형 UI 및 레이아웃 최적화          | 진행 중   |
| 2023-05-01   | 이미지·자산 데이터베이스 통합 및 API 연동            | 예정     |
| 2023-05-10   | 대시보드 페이지 디자인 및 기능 구현                  | 예정     |
| 2023-05-20   | 성능 최적화 및 배포 환경 설정                       | 예정     |

## 5. 기술 스택

- **백엔드**: Python, FastAPI, Uvicorn
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript
- **데이터베이스**: SQLite → PostgreSQL(스케일업 시)
- **인프라**: 
  - 개발: Windows Server 또는 Galaxy S21 + Termux
  - 배포: AWS EC2 인스턴스 (추후)
- **웹 서버**: Nginx (리버스 프록시 및 HTTPS)
- **버전 관리**: GitHub, CI/CD(GitHub Actions)

## 5.A 프로젝트 구조

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
│      project_plan.md                 # 프로젝트 계획서 (현재 문서)
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
│
└─__pycache__                 # Python 캐시 파일
        app.cpython-312.pyc   # 컴파일된 Python 파일
```

## 6. 개발 환경 설정

### 6.1 Termux(Galaxy S21) 개발 환경 (선택적)
- Termux 초기 설정:
  ```bash
  pkg update && pkg upgrade
  pkg install curl git socat nginx openssh termux-api python
  ```
- 기본 개발 도구 설치:
  ```bash
  pip install fastapi uvicorn
  ```
- VSCode 원격 개발 설정:
  - Termux에 SSH 서버 설정
  - VSCode Remote-SSH 익스텐션 사용
  - getconf 에뮬레이션 스크립트 설정 (필요 시)

### 6.2 네트워크 설정
- **도메인**: rotanevs21.duckdns.org 또는 사용자 지정 도메인
- **포트**: 
  - HTTP: 8080
  - HTTPS: 8443 (SSL 인증서 적용 후)
- **Nginx 설정**:
  ```nginx
  # HTTP 설정 (8080 포트)
  server {
      listen 8080;
      server_name yourdomain.com;

      location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
      }

      location /static/ {
          alias /path/to/static/files/;
          expires 1d;
      }
  }

  # HTTPS 설정 (8443 포트)
  server {
      listen 8443 ssl;
      server_name yourdomain.com;

      # SSL 인증서 설정
      ssl_certificate /path/to/cert/fullchain.cer;
      ssl_certificate_key /path/to/cert/private.key;

      # 기타 설정...
  }
  ```

## 7. 위험 요소 및 대응 방안

| 위험 요소                      | 영향                             | 대응 방안                                 |
|-----------------------------|--------------------------------|--------------------------------------|
| 다국어 렌더링 지연               | 사용자 경험 저하                      | SSR(서버 사이드 렌더링) 적용 검토, 캐싱 도입        |
| 대용량 이미지 로딩              | 페이지 로드 시간 증가                  | WebP 변환, 지연 로딩(Lazy Loading) 적용        |
| 폴리필 및 호환성 오류            | 구형 브라우저 미지원                  | 자동화 테스트 도구로 주요 브라우저 호환성 검증     |
| API 응답 지연                  | 데이터 조회 실패 및 UX 저하             | 백엔드 쿼리 최적화, CDN 활용                  |
| 모바일 장치 개발 환경 문제         | 개발 진행 저해                       | GitHub Codespaces 또는 클라우드 개발 환경 활용   |
| 인증서 및 HTTPS 설정 실패        | 보안 취약성                         | Let's Encrypt 인증서 자동화 및 설정 문서화      |

## 8. 차후 일정 및 To-Do 리스트

- [ ] **4/23~4/24**: 모바일 메뉴 스타일 마무리 및 간격 조정
- [ ] **4/25~4/30**: 토큰화 자산 데이터 스키마 설계 및 API 엔드포인트 공개
- [ ] **5/1~5/5**: 대시보드 UI 목업 제작 및 사용자 피드백 수집
- [ ] **5/6~5/10**: SEO 최적화(메타 태그, 사이트맵) 작업
- [ ] **5/11~5/15**: 테스트 자동화(유닛 테스트, e2e 테스트) 설정
- [ ] **5/16~5/20**: SSL/TLS 인증서 설정 및 HTTPS 활성화
- [ ] **5/21~5/25**: AWS 배포 환경 구성 및 CI/CD 파이프라인 설정

## 9. 완료된 작업 체크리스트

- [x] FastAPI 서버 설정
- [x] 기본 웹사이트 구조 구현
- [x] 한국어 페이지 추가
- [x] 브라우저 호환성 개선 (crypto.randomUUID 폴리필 추가)
- [x] JavaScript 오류 수정 (CSS 선택자 오류 해결)
- [x] 언어 전환 기능 개선

## 10. 현재 진행 중인 이슈

- [ ] 모바일 메뉴 UI 개선
- [ ] 이미지 최적화
- [ ] 기본 API 엔드포인트 구현
- [ ] 데이터베이스 스키마 설계

## 11. 자동화 및 배포 전략

### 11.1 개발 자동화
- VSCode Remote-SSH 또는 GitHub Codespaces를 활용한 원격 개발
- 테스트 자동화: pytest를 이용한 단위 테스트 및 통합 테스트
- 린트 및 코드 품질 체크: flake8, black, isort

### 11.2 배포 자동화
- GitHub Actions를 활용한 CI/CD 파이프라인 구축
- 자동 테스트 및 빌드 프로세스
- AWS EC2 또는 Termux 환경으로 자동 배포

### 11.3 모니터링 및 로깅
- 사용자 행동 추적 및 분석
- 서버 성능 모니터링
- 오류 로깅 및 알림 시스템


---

## 업데이트 이력

- 2023-04-22 - 프로젝트 계획 문서 초안 작성
- 2023-04-22 - 프로젝트 디렉토리 구조 추가
- 2023-04-22 20:40 - README.md 파일 업데이트 (project_plan.md 기반)

