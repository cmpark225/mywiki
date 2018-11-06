
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



# Django에서 csrf 토큰을 확인하는 방식

## GET 요청
csrf 토큰을 처리하는 순서 대로 크게 3가지로 구분할 수 있다.

(request 미들웨어, 뷰, response 미들웨어)

### 1. request 미들웨어

request.META['CSRF_COOKIE']를 설정한다.

: 쿠키에 csrftoke(settings.CSRF_COOKIE_NAME 값)이 있는지 체크한다.

쿠키에 csrftoke이 없을 경우에는 토큰을 새로 생성하고 cookie_is_new도 True로 설정한다.

django/middleware/csrf.py
```
def process_view(self, request, callback, callback_args, callback_kwargs):
    ...

    try:
        request.META["CSRF_COOKIE"] = _sanitize_token(request.COOKIES[settings.CSRF_COOKIE_NAME])
        cookie_is_new = False 
    except KeyError:
        # 쿠키에 csrf 값이 없을 경우 새로 생성한다.
        request.META["CSRF_COOKIE"] = _get_new_csrf_key()
        cookie_is_new = True 
```


### 2. 뷰

RequestContext를 이용하여 csrf_token 값을 전달한다. (위 내용의 옆 부분 참고 - 3.  뷰에서 'django.core.context_processors.csrf' 사용을 보장해줘야 한다.  아래 두가지 방법 중 하나 사용할 수 있음.)

django/core/context_processors.py
```
def csrf(request):
    def_get_val():
        token = get_token(request) 
        # get_token에서 request.META["CSRF_COOKIE_USED"] = True설정 
        ....
    return {'csrf_token': _get_val() }
```

리턴 값으로 {"csrf_toke":'dsfjalskfdsa'}을 전달함으로써

템플릿에서 

{% csrf_token %}을 이용 form 에 csrf 값을 hidden으로 세팅할 수 있다.

django/template/defaulttag.py
```
class CsrfTokenNode(Node):
    def render(self, context):
        # 위 context에서 return 해준 csrf_token 값 가져옴
        csrf_token = context.get('csrf_token', None) 
        ...
        return mark_safe(u"<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s'></div>" % csrf_token)
```


### 3. response 미들웨어
csrf token을 사용할 경우. (뷰에서 ReqeustContext를 통해 csrf 설정 시 사용 여부가 설정된다. CSRF_COOKIE_USED=True)

쿠키에 csrf_token값을 저장한다.

django/middleware/csrf.py
```
def process_response(self, request, response):
    ...
    if not request.META.get("CSRF_COOKIE_USED", False):
        return response

    # 쿠키 세팅
    #위에 1번 process_view에서 설정한 request.META['CSRF_COOKIE']
    response.set_cookie(settings.CSRF_COOKIE_NAME, request.META['CSRF_COOKIE'], max_age= 60 * 60 * 24 * 7 * 52, doamin=setteings.CSRF_COOKIE_DOMAIN)

    ...
```


## POST 요청

### request 미들웨어

쿠키에서 CSRF_COOKIE값을 가져온다. 

쿠키에서 가져온 값과 Form에서 보내온 값이 맞는지 비교한다.

Form에서 가져온 값이 없을 경우에는 헤더 값을 잠조한다.

django/middleware/csrf.py
```
def process_view(self, request, callback, callback_args, callback_kwargs):
    ...

    if request.method == 'POST':
       ...
       # 요청으로 온 csrf 값 확인(먼저 body, 이후 헤더 확인)
       request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
       if request_csrf_token == "":
        request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN'. '')

        # 요청으로 온 값과, 쿠키의 csrf 비교
        if not constant_time_compare(request_csrf_token, csrf_token):

```






   
