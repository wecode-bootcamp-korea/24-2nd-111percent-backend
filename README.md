# 8percent
<img width="1680" alt="스크린샷 2021-10-01 오후 2 11 53" src="https://user-images.githubusercontent.com/76423949/135737600-91587c29-3efb-4ea8-b8f0-c83d3467679f.png">

개인투자자가 소액으로 가능한 P2P 투자사이트 "8percent"를 클론 코딩 해보았습니다.

[>>시연 동영상 보러가기](https://youtu.be/5wOlzBs6B9I)

## Team

### 111percent

대한민국의 유명 래퍼 Dok2의 노래 "111%"처럼 팀원 모두 수익률 111%를 달성하고자 하는 염원을 담아 팀 이름을 111percent로 작명하였습니다.

### Teamates👨‍👦‍👦👩‍👧

FrontEnd: 김현재, 최파란별, 이지영
BackEnd: 김정수, 하예준

### 작업기간

21.09.13 ~ 21.10.01
<br>
<br>

## 기술 스택

### FE :

- Basic
  `Javascript`, `React(CRA, Hook)`, `Styled-components`
- Other libraries
  `React-router-DOM`, `react helmet`, `slide-slicker`, `dotenv`, `chartjs`, `axios`, `react-icons`

### BE :

- `Phyton`, `Django`, `MySQL`

### Both :

- `Slack`, `Trello`, `Github`, `Git`, `Git-flow`, `Notion`
  <br>
  <br>

## 구현 기능 소개

- 회원가입 / 로그인
- 소셜로그인 (카카오)
- 메인페이지 (겸 리스트 페이지)
- 상세페이지
- 마이페이지
- 입금, 출금, 투자하기 기능

### 개인별 담당 페이지 및 기능 (BE)

**하예준**

`회원가입 / 로그인 API`

- 정규표현식을 활용한 이메일, 비밀번호 유효성 검증
- `Bcrypt`, `jwt`를 통한 Authentication, Authorization 구현
- `uuid4` 모듈을 활용하여 사용자 별 고유의 가상 계좌번호 생성
- 카카오 소셜로그인 시 유저 객체를 생성한 후, 추가 개인정보를 통해 유저 정보 업데이트 로직 구현

`입금, 투자, 출금 APIs`

- `Django DB Transaction` 모듈을 통해 Rollback & Commit 로직 구현
- 거래 데이터 유효성 검사 로직 구현 (금액이 양의 정수형인지, 예치금 금액만큼 투자 또는 출금이 일어나는지)
- 투자 거래 시 `Portfolio` 객체 생성 연동

`투자요약 정보 API`

- `Django aggregate`을 활용하여 투자한 내역의 수익률, 누적 수익금, 자산 정보 제공
- 투자 상태 및 투자 등급, 수익률에 따른 투자 금액 `filter` 구현

**김정수**


# Reference

- 이 프로젝트는 라인프렌즈샵 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
