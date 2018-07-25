## Limiting access to logged-in users

### 1. The raw way
원시적 방법. request.user.is_authenticated() 확인하여 login 페이지로 redirect

```
from django.http import HttpResponseRedirect

def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
```

혹은 에러 메시지 출력

```
def my_view(request):
    if not request.user.is_authenticated():
        return render_to_response('myapp/login_error.html')
```

### 2. The login_required decorator
##### decorators.login_required([redirect_field_name=REDIRECT_FIELD_NAME, login_url=None])

```
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
```

* 사용자가 로그인하지 않았을 경우 settings.LOGIN_URL로 redirect 시킨다. query string으로 현재 경로를 전달한다. ex) accounts/login/?next=/polls/3.
* 로그인 했을 경우에는 view를 실행시킨다.

기본적으로 인증 성공시 사용자가 리디렉션되어야하는 경로는 "next"라는 쿼리 문자열 매개 변수에 저장된다. 이 다른 이름을 사용하려면 login_required()에서 redirect_field_name 매개 변수를 사용하면 된다.

```
 from django.contrib/auth.decorators import login_required

 @login_required(redirect_field_name='redirect_path')
 def my_view(request):
     ...
```

login_required()에는 login_url 파라미터도 있다 Ex)
```
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
...
```

login_url파리미터 명시하지 않을 경우 적절한 view를 settings.LOGIN_URL에 매핑해야 한다. 예를 들어 기본값을 사용해서 URLconf에 아래 라인을 추가해라:

```
(r'^accounts/login/$', 'django.contrib.auth.views.login),
```

##### views.login(request[, template_name, redirect_field_name, authentication_form])

django.contrib.auth.views.login:
* GET 호출 시 동일한 URL에 POST전송하는 로그인 폼 표시.
* POST 호출 시 유저 로그인 시도. 로그인에 성공시 next로 redirect한다. next가 없으면 settings.LOGIN_REDIRECT_URL로 redirect하고 로그인에 실패할 경우에는 로그인 폼을 표시한다.

기본적으로 registration/login.html템플릿 로그인 양식을 제공은 내가 해야 한다.
이 템플릿은 네 가지 템플릿 컨텍스트 변수를 전달받는다.

* form : 
* next : 로그인 성공 시 redirect 할 URL (query string 포함)
* site :
* site_name :


Urlconf에 template_name 파라미터로 template를 설정할 수 있다. 예를들어 아래 URLconf 라인은 myapp/login.html을 사용한다.

```
(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'myapp/login.html'}),
```
redirect_field_name을 view에 전달하여 로그인 한 후 리디렉션 할 URL이 포함 된 GET 필드의 이름을 지정할 수도 있다. 기본적으로 이 필드는 next를  호출한다.

content 블럭을 가지는 base.html이 있다고 가정한 registration/login.html 샘플 템플릿이 있다.

```
{% extends "base.html" %}
{% load url from future %}

{% block content %}

{% if form.errors %}
<p>Your username and password didn't match. Please try again.</p>
{% endif %}

<form method="post" action="{% url 'django.contrib.auth.views.login' %}">
{% csrf_token %}
<table>
<tr>
    <td>{{ form.username.label_tag }}</td>
    <td>{{ form.username }}</td>
</tr>
<tr>
    <td>{{ form.password.label_tag }}</td>
    <td>{{ form.password }}</td>
</tr>
</table>

<input type="submit" value="login" />
<input type="hidden" name="next" value="{{ next }}" />
</form>
```
If you are using alternate authentication (see Other authentication sources) you can pass a custom authentication form to the login view via the authentication_form parameter. This form must accept a request keyword argument in its __init__ method, and provide a get_user method which returns the authenticated user object (this method is only ever called after successful form validation).
