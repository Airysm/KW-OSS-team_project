# KW-OSS-team_project

광운대학교 OSS개발 팀프로젝트

//Discord Bot//
 
## 구현 할 예정인 기능
1. 식단 랜덤 룰렛
2. 디스코드 내 미니게임 (ex. RPG)
3. 게임 전적 검색 (ex. 레인보우식스)
4. 팀 밸런스 매칭
5. 서버 내 파일 저장 및 공유 시스템

---

## 봇 추가하는 방법
1. 프로젝트 코드를 다운로드 하거나, fork 하여 컴퓨터에 저장
2. [디스코드 개발자 홈페이지](https://discord.com/developers)에 접속(로그인 필요)
3. Applications 탭의 오른쪽 상단의 'New Application' 버튼 클릭
4. 이름 입력
5. Bot 탭에 들어가 'Add Bot' 버튼 클릭
6. TOKEN 칸 밑의 'Copy' 버튼 클릭
7. 다운로드 받은 프로젝트 폴더에 '.env' 파일 생성
8. '.env' 파일을 메모장 등으로 열고 'DISCORD_TOKEN=복사한 토큰 붙여넣기' 작성
9. 다시 디스코드 개발자 홈페이지로 돌아가서 OAuth2 탭 클릭
10. SCOPES를 'bot'으로 설정하고, BOT PERMISSIONS을 'Administrator'로 설정 혹은 원하는 대로 설정
11. SCOPES칸 밑쪽에 있는 URL을 복사하고, 해당 페이지로 이동
12. 봇을 추가할 서버를 선택하고 '계속하기' 버튼 클릭(해당 서버에 자신이 '서버 관리 권한'이 있어야 함)

## 봇 실행 방법
1. 파이썬으로 bot.py 실행 (cmd 창에서 python bot.py)

---

## 봇 실행이 되지 않을때!!
1. 파이썬이 설치 되었는지 확인
2. cmd 창에 ```pip install -r requirements.txt``` 명령을 실행해서 필요한 모듈 설치
3. 파이썬 환경변수가 제대로 설정되었는지 확인
