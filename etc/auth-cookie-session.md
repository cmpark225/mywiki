인증 방식

# Cookie
웹 브라우저에 저장되는 작은 데이터 조각.
브라우저는 동일한 서버로 다음 요청 시 저장한 데이터를 함께 전송.


## 사용 예

##### 세션 관리 (Session management)
- 로그인 시 쿠키에 session Id 저장
    - 세션 ID 문자열만 가지면 누구나 로그인 가능

##### 개인화 (Personalization)
- 국제화
    - 사용자가 페이지에서 사용할 언어를 선택했을 경우 다음 페이지 접근시에도 쿠키를 이용해 설정한 언어 출력 가능

## 쿠키 생성
서버에서 응답할 때 헤더를 아래와 같이 설정

```
Set-Cookie: <cookie-name>=<cookie-value>
```

-Response Header
```
HTTP/1.0 200 OK
Content-type: text/html
Set-Cookie: yummy_cookie=choco
Set-Cookie: tasty_cookie=strawberry

[page content]
```

### 쿠키 종류 
##### Session
웹 브라우저 종료 시 삭제 되는 쿠키 
##### Permanent
웹 브라우저 종료 시에도 유지 되는 쿠키
- 쿠키 헤더에 Max-Age나 Expires 명시
        - Set-Cookie: id=a3fWa; Expires=Wed, 21 Oct 2015 07:28:00 GMT;

### 옵션
- secure
- HttpOnly
- Path
- Domain


## 쿠키를 이용한 인증
ID, password를 쿠키에 저장. 
쿠키에 password를 저장한다면 비밀번호 유출이 쉽다. 
쿠키 조작도 쉽기 때문에 문제가 발생할 수 있다.

https://developer.mozilla.org/ko/docs/Web/HTTP/Cookies

# Session
쿠키에 세션을 저장한다.

쿠키는 사용자를 식별하는데만 사용하고, 
실제 데이터는 서버에 파일이나, DB 형태로 저장하는 방식.

