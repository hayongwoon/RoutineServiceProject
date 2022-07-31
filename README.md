# Routine Service is ...
### project version check
- Django              4.0.3
- djangorestframework 3.13.1
- Python 3.9.7

## routine 기능에서는 다음과 같은 기능을 제공합니다.
- 유저의 회원가입/로그인/로그아웃 기능
- 매 주별 해야할 일 등록/수정/삭제/조회 기능
- 일정이 지난 후 진행한 일에 대한 해결 여부 기록
- 특정 날짜에 대한 루틴 정보와 루틴에 대한 결과를 담은 리스트 조회

### 세부 설명
- routine과 routine_result는 OnetoOne 필드로 구성 되어 있고, 루틴 생성 시 해결여부 또한 초기값 **result=NOT**으로 생성 됩니다.
- 루틴이 생성되고 루틴 결과를 업데이트 하는 유저의 시나리오는 한 주의 시작인 **일요일**에 등록을 하고, 루틴 결과는 루틴 등록 전 지난 주 루틴들에 대해 업데이트(NOT or TRY or DONE)를 함.

## 기능 추가 설명
1. 유저의 로그인은 email로 진행했으며, 로그인 방식은 장고에서 제공하는 메소드를 활용한 세션방식으로 구성
2. 유저의 회원가입은 비밀번호 8자 이상의 숫자, 문자, 특수문자 조합


## URI & METHOD
|API|endpoint|method|
|------|---------|---|
|회원가입|users/sginup/|POST|
|로그인|users/login/|POST|
|로그아웃|users/logout/|POST|
|루틴 생성|routines/|POST|
|루틴 단일조회|routines/|GET|
|루틴 수정|routines/|PUT|
|루틴 삭제|routines/|DELETE|
|루틴 목록 조회|routines/todo-list/|GET|
|루틴 결과 수정|routines/result|PUT|


## API 문서
1. Domain: localhost
2. Port: 8000
3. API LIST
<details>
<summary>회원가입</summary>
    <div markdown="1">
    - endpoint: /users/signup/
    - method: POST
    - Request = {
        "email": "test@test.com",
        "password": "test1234!!",
        "username": "하용운"
    }
    </div>
</details>