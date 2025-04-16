# VSCode Remote-SSH 사용 가이드

## 기본 설정

1. **VSCode 좌측 사이드바에서 Remote Explorer 아이콘 클릭** (또는 `F1` 키를 누르고 `Remote-SSH: Connect to Host` 입력)

2. **새 SSH 호스트 추가**
   - Remote Explorer 탭에서 "+" 버튼 클릭
   - 다음 형식으로 SSH 연결 문자열 입력:
     ```
     ssh -p 51117 username@rotanevs21.duckdns.org
     ```
   - 연결 정보를 저장할 설정 파일 선택 (보통 첫 번째 옵션 선택)

3. **호스트에 연결**
   - 추가된 호스트 옆의 연결 아이콘(➡️) 클릭
   - 처음 연결 시 호스트 OS 유형 선택 (Linux)
   - 비밀번호 또는 SSH 키 인증 정보 입력

## 프로젝트 열기

1. **연결 후 "Open Folder" 클릭**

2. **작업 디렉토리 경로 입력**
   ```
   /data/data/com.termux/files/home
   ```
   또는 프로젝트가 있는 특정 경로 입력

3. **신뢰 여부 확인 메시지**에서 "Yes, I trust the authors" 선택

## 주요 기능

1. **터미널 접근**
   - 메뉴: Terminal > New Terminal
   - 원격 시스템에서 직접 명령어 실행 가능

2. **파일 편집**
   - 좌측 Explorer에서 파일 탐색 및 편집
   - 모든 변경사항은 원격 시스템에 바로 적용

3. **확장 프로그램**
   - 일부 확장 프로그램은 원격 시스템에 설치 필요
   - "Install in SSH: hostname" 옵션으로 설치

4. **디버깅**
   - 원격 시스템에서 직접 디버깅 가능
   - 디버그 구성은 `.vscode/launch.json`에서 설정

## 문제 해결

1. **연결 실패 시**
   - SSH 서버가 실행 중인지 확인
   - 포트 번호가 올바른지 확인 (51117)
   - 네트워크 연결 및 방화벽 설정 확인

2. **느린 응답**
   - 네트워크 상태 확인
   - "Remote-SSH: Settings" 에서 연결 설정 최적화

3. **인증 문제**
   - SSH 키가 올바른 위치에 있는지 확인
   - 비밀번호가 올바른지 확인

## 연결 종료

- 좌측 하단 상태 표시줄의 "SSH: hostname" 클릭 후 "Close Remote Connection" 선택
- 또는 VSCode 종료

## 참고 사항

- 원격 작업 중에는 모든 파일 작업이 Galaxy S21에서 이루어집니다.
- 편집, 저장, 실행 등의 모든 작업이 S21에 직접 적용됩니다.
- 터미널 명령어도 S21에서 실행됩니다. 