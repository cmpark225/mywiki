## How to use it
view에서 CSRF 보호를 활성화 하기 위해서는 아래 단계를 수행한다.

1. 미들웨어 클레스인 MIDDLEWARE_CLASSES 리스트에 'django.middleware.csrf.CsrfViewMiddleware' 미들웨어를 추가한다.(CsrfResponseMiddleware가 사용 중일 경우 CsrfResponseMiddleware 전에 와야 하며, CSRF 공격이 처리되었다고 가정하는 view 미들웨어보다 먼저 와야 한다.)

또는 보호려는 특정한 view에 django.views.decorators.csrf.csrf_protect 데코레이터를 사용할 수 있다.(아래 참조)

2. POST form을 사용하는 템플릿의 경우 form이 내부 URL용인 경우 <form> 엘리먼트 안에 csrf_token 태그를 사용한다. EX:

```
<form action="" method="post"> {% csrf_token %}
```
외부 URL을 대상으로 하는 POST양식의 경우 CSRF 토큰이 유출되어 취약점으로 이어질 수 있으므로 이를 수행해서는 안된다. 

## How it works

CSRF 보호는 아래 사항을 기반으로 한다:

1. 다른 사이트에서 접근할 수 없는 랜덤 값으로 설정된 CSRF 쿠키. 

이 쿠키는 CsrfViewMiddleware로 부터 설정된다. 이것은 영구적이지만 만료되지 않는 쿠키를 설정할 방법이 없으므로, django.middleware.csrf.get_token()(CSRF 토큰을 검색하기 위해 내부적으로 사용되는 함수)을 호출한 모든 응답과 함께 전송된다. 

2. 모든 나가는 POST form에는 'csrfmiddlewaretoken'이라는 숨겨진 form 필드가 있다. 이 필드의 값은 CSRF 쿠키 값이다. 

이 부분은 template tag로 수행된다. (legacy method는 CsrfResponseMiddleware에 의해 수행된다.)

3. 모든 들어오는 POST 요청에서, CSRF 쿠키는 있어야 하며, 'csrfmiddlewaretoken' 필드가 있어야 하며 정확해야 한다. 만약 그렇지 않을경우 사용자는 403 에러가 표시된다.

이 확인은 CsrfViewMiddleware.로 수행된다.

4. 추가적으로, HTTPS 요청에서는 CsrfViewMiddleware가 엄격한 referer 확인을 수행한다. 이는 HTTP 'Set-Cookie'헤더가 클라이언트에 의해 수용되기 때문에 세션 독립적인 nonce를 사용할 때 HTTPS에서 가능한 Man-In-The-Middle공격을 처리하는데 필요하다. 사이트에서 HTTPS Referer 헤더가 HTTP에서 충분히 안정적이지 않으므로 HTTP 요청에 대해 Referer 확인이 수행되지 않는다.


이렇게하면 웹 사이트에서 비롯된 양식만 POST데이터를 다시 사용할 수 있다.

이것은 의도적으로 HTTP POST요청만 대상으로 한다. GET요청은 결코 잠재적으로 위험한 부작용을 가져서는 안된다.(9.11 안전한 메소드, HTTP 1.1, RFC 2616 참조). 따라서 GET 요청을 사용하는 CSRF 공격은 무해하다. 

CsrfResponseMiddleware는 응답을 수정하기 전에 Content-Type을 확인하고 'text/html' 또는 'application/xml+xhtml'로 제공되는 페이지만 수정한다.
