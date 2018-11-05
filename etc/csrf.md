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


## django에서 CSRF 공격 막는 방법

#### 1. 미들웨어 추가 'django.middleware.csrf.CsrfViewMiddleware'

(CsrfResponseMiddleware  미들웨어 보다 전에 와야 한다.)

아니면 공격 방지가 필요한 특정한 View에 'django.views.decorators.csrf.csrf_protect' 데코레이터를 사용한다.


#### 2. POST form을 사용하는 템플릿의 form  element안에 csrf_tocken 태그를 사용한다.

```
<form action="" method="post">
{% csrf_token %}
```

해당 작업은 외부 URL로 POST 전송 시에는 피해야 한다. CSRF 토큰이 유출되어 취약성이 발생할 수 있기 때문이다.

#### 3.  뷰에서 'django.core.context_processors.csrf' 사용을 보장해줘야 한다.  아래 두가지 방법 중 하나 사용할 수 있음.

##### 3.1 'django.core.context_processors.csrf'를 사용하는 RequestContextf를 사용한다. 

(settings에 TEMPLATE_CONTEXT_PROCESSORS도 관계 없음.) 만약 generic views나 cotrib apps를 사용하면 전체적으로 RequestContext를 사용하기 때문에 이미 처리되고 있다.

```
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    data = {}

    context = RequestContext(request, data)
    return render_to_response('a.html', context)

```

RequestContext
https://django.readthedocs.io/en/1.3.X/ref/templates/api.html#subclassing-context-requestcontext

##### 3.2 template context에 수동으로 CSRF 토큰을 포함시킨다.

```
from django.core. context_processors import csrf
from django.shortcuts import render_to_response

def my_view(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('a.html', c)
```

### csrf_exempt


django에서는 

{% csrf_token %} 을 이용하여 내가 원하는  form이 맞는지 체크할 수 있다. 

api의 경우 form 을 사용하지 않기 때문에 csrf 사용이 필요 없어 

csrf_exempt 데코레이터를 이용해 

csrf 체크를 하지 않도록 할 수 있다.
