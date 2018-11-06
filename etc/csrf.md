# csrf (Cross Site Rrequest forgery, CSRF,XSRF) 

사이트 간 요청 위조

인증된 사용자를 이용한 공격 방식. 

사용자가 자신의 의지와는 무관하게 공격자가 의도한 행위(수정, 삭제, 등록등)을 특정 웹사이트에 요청하게 하는 공격. => 요청을 위조 한다

해당 공격은 Server를 대상으로 한다.

## 예

A site에 로그인한 사용자에게 

B site 접속을 유도한 후 

사용자가 A site에 로그인이 되어 있다는 점을 이용해, 

B Stie에서 A site에게 특정 요청을 한다.

ex) A site/api/user/1/delete 호출

위와 같은 요청을 할 경우 현재 A Site에 로그인이되어 있기 때문에 

해당 api가 정상적으로 동작한다.


## 방어.

1. GET 요청에 대해 데이터 변동이 필요한 작업을 수행하지 않는다(수정/삭제와 같은)

2. CSRF 토큰 사용 (아래에서 설명)

3. 유효한 API 콜인지 확인한다. 요청 헤더를 활용하면 쉽게 해결할 수 있다. (예를 들면, 레퍼러를 체크거나, X-Requested-With 헤더가 있는지 확인)
 
4. 인증 정보를 쿠키 대신 헤더로 보낸다. (인증 쿠키를 읽어서 자바스크립트 헤더로 보내는 방식)


# XSS (Cross Site Scripting)

스크립트를 이용한 공격. 

XSS의 경우 공격 대상이 Client이다.

## 예 
1.  특정 로그인한 사용자가 게시글을 클릭할 경우.

클릭한 게시글에 Form이 있어 해당 Form 도 같이 실행 가능하도록 하여 공격하는 방식. 

게시글 내용에 아래와 같은 form을 작성하여 

관리자가 클릭 시 해당 form을 서버에 전송하도록 한다.

```
<form action="" method="post">
<input type="hidden" name="subject" value="test">
<input type="hidden" name="writer" value="aaaa">
<input type="hidden" name="content" value="content test">
</form>
<script> document.forms[0].send.click(); </script>
```

2. 게시글 같은 곳에 script코드를 심어 공격한다.
예를들어 게시글을 작성할 경우 아래와 같은 스크립트가 동작한다면

```
<script> alert("Hi"); </script>
```

스크립트를 통해 다른 정보도 가져올 수 있음을 의미한다.


## 방어 방법 

페이지를 렌더링 할 때 불필요한 태그에 대해 escape 처리를 한다.


https://github.com/pillarjs/understanding-csrf/pull/10/files?short_path=2c41220


## [django에서 CSRF 공격 막는 방법](https://github.com/sally225/mywiki/blob/master/django/csrf_protection_in_django.md)
 







   
