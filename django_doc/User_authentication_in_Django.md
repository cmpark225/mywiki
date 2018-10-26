## Overview

인증 시스템은 아래로 이루어져 있다.
* Users
* Permissions :  사용자가 특정 작업을 수행할 수 있는지에 대한 Binary flag(yes/no)
* Groups: 둘 이상의 사용자에게 레이블 및 사용 권한을 적용하는 일반적인 방법



## Installation
Django 어플리케이션의 django.contrib.auth에서 인증을 제공한다. 

1. settings의 INSTALLED_APPS에 'django.contrib.auth'와 'django.contrib.contenttypes'를 추가한다. (django.contrib.auth의 Permission 모델이 django.contrib.contenttypes 의존성을 가진다.)
2. manage.py syncdb 명령어 실행 한다.

djang-admin.py startproject로 프로젝트 생성시 편의를 위해 django.contrib.auth와 django.contrib.contenttype은 기본적으로 생성된다. 만약 위 두개 앱이 이미 포함되어 있다면 manage.py syncdb 명령어만 실행하면 된다. 이 명령어는 원할 경우 여러번 수행할 수 있다.

# Using User Model 

```
from django.contrib.auth.models import User 
```

# Users

class models.User

## Fields
User 오브젝트는 아래 필드를 포함한다.

### username
### first_name
### last_name
### email
### password
### is_staff
Boolean. 사용자가 admin site에 접근할 수 있는지에 대해 지정

### is_active
Boolean. 해당 사용자가 active인지 지정. application이 foreign key를 가졌을 경우 외래키가 손생되지 않기 때문에 계정을 지우는 것 대신 해당 flag를 False 처리하는 것을 권한다.

이것은 사용자가 로그인을 할 수 있는지 여부를 반드시 컨트롤하지는 않는다. 
인증 backedns는 is_active flag를 검사할 필요가 없으므로, is_active가 False인 경우 로그인을 거부하려면 사용자가 자신의 login view에서 체크해야 한다. 그라니 login()뷰가 사용하는 AuthenticationForm은 has_perm과 같은 권한 검사 메소드와 장고 관리자의 인증처럼 이 검사를 수행한다. 이러한 모든 함수/메소드는 비활성 사용자에 대해 False를 반환한다.

### is_superuser
Boolean. 명시적 지정 없이 모든 권한을 가졌는지에 대해 지정.

### last_login
사용자의 마지막 로그인 시간. 현재 date/time을 기본 값으로 가짐.

### date_joined
계정이 생겼을 때의 datetime 계정이 생성됐을 때 현재 date/time을 기본 값으로 가짐.

## Methods
**class models.User**
User 오브젝트는 두개의 many-to-many field를 가진다. : User.groups 와 user_permissions. User 오브젝트는 related object에 대해 Django model과 같은 방식으로 접근한다.
```
myuser.groups = [group_list]
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions = [permission_list]
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()
```
이러한 자동 API 메소드 외에도 User 객체에는 다음과 같은 맞춤 메소드가 있다.

### is_anonymous()
항상 False를 반환한다. 이 메소드로 User와 AnonymousUser를 구분한다.

일반적으로 이 메소드에 is_authenticated()를 사용하는 것이 좋다. (?)

### is_authenticated()
항상 True반환. 사용자가 인증되었는지를 알려주는 방식이다. 이것은 권한이나 active를 의미하지 않는다. 단지 유효한 username과 password를 제공했음을 나타낸다. 

### get_full_name()
first_name과 last_name을 space로 구분하여 합친 값을 반환한다. 

### set_password(raw_password)
raw_password를 받아 해당 값을 해시하여 사용자 패스워드를 세팅한다. User 오브젝트를 저장하지 않는다. (비밀번호 변경 시 user.save()해야 함.)

### check_password(raw_password)

raw string이 사용자 비밀번호가 일치할 경우 True를 반환한다. (비교할때 암호를 hashing 처리한다.)
=> 입력받은 암호를 hashing 처리하여 이미 hashing된 암호와 비교

### set_unusable_password()

사용자가 패스워드를 가지지 않은 것으로 표시한다. 빈 문자열을 password로 가지는 것과는 다르다. check_password()는 이 사용자에 대해서 True를 리턴하지 않는다.  Doesn't save the User object(? : DB에 저장되던데?)

어플리케이션이 LDAP 디렉토리와 같은 기존 외부 인증을 사용할때 필요할 것이다.

ex) 
User 생성 시 

```
>>> from django.contrib.auth.models import User
>>> user = User()
>>> user.username = 'testuser'
>>> user.first_name = 'test'
>>> user.last_name = 'user'
>>> user.set_unusable_password()
>>> user.save()
```
DB에 해당 user에 대한 password 값이 !로 저장된것을 확인할 수 있다.

### has_usable_password()

해당 사용자에게 set_unsuable_password()가 호출되었으면 False를 반환한다. 
```
>>> user.has_usable_password()
False
```

### get_group_permissons(obj=None)
### get_all_permissions(obj=None)
### has_perm(perm, obj=None)
### has_perms(perm_list, obj=None)
### has_models_perms(package_name)
### get_and_delete_messages()
### email_user(subject, message, from_email=None)
### get_profile()

## Manager functions

**class models.UserManager**

User 모델은 아래의 help function인 custmom manager를 가진다:

### create_user(username, email, password=None)

생성, 저장, 그리고 User를 리턴한다.

username과 password를 입력한 값으로 설정한다.  도메인을 자동으로 소문자로 설정한다. 그리고 User object는 is_active가 True인 상태로 return 된다. 

password가 없을 경우 set_unusable_password()가 호출된다.

### make_random_password(length=10, allowd_chars='abcdefghjkmnpqrstuvwsyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
주어진 길이와, 허용된 문자들로 이루어진 랜덤 비밀번호를 리턴한다.
(기본 allowd_chars에서 혼란을 피ㅎ기 위해 일부 문자열을 포함하지 않는다.)
* i,l,I and 1 (소문자 i, 대문자 I, 소문자 l 그리고 숫자 1)
* o,O and 0 (소문자 o, 대문자 O 그리고 숫자 0)


### Basic usage

#### Creating users

user를 생성하는 가장 기본적인 방법은 django에서 제공하는 create_user() helper function을 사용하는 것이다.

```
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# 이 시점에 user는 이미 데이터베이스에 저장된 user object이다.
# 다른 field를 변경하고 시을 경우 attributes 변경이 가능하다.
>>> user.is_staff = True
>>> user.save()
```
또한 Django admin site에서 user를 생성할 수 있다. Admin site를 URL /admin/으로 사용한다면 Add user 페이지는 /admin/auth/user/add/ 이다. 

#### Changing password
"manage.py changepassword *username*"은 커멘드 라인에서 사용자의 페스워드를 변경할 수 있는 메소드를 제공한다. 이것은 엔터 두번으로 사용자의 비밀번호를 변경할 수 있도록 해준다. 두개가 일치하면 즉시 사용자 비밀번호는 변경된다. 만약 사용자 이름이 없을 경우에는 현재 사용자의 비밀번호 변경을 시도한다.

```
user@UD-user:~/data/workspace/myproject$ python manage.py changepassword
Error: user 'user' does not exist

# 현재 로그인된 사용자의 이름이 'user'라서 자동으로 'user'를 찾는 듯.
```

또한 set_password()를 이용해 프로그램에서 비밀번호를 변경할 수 있다.
```
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username__exact='john')
>>> u.set_password('new password')
>>> u.save()
```

password 속성을 직접 변경해서는 안된다. 


###Storing additional information about users
만약 사용자와 연관된 추가적인 정보를 저장하고 싶다면 Django는 이 목적을 위해 사이트 별 관련 모델을 지정하는 방법을 제공한다. ("user profile")

이 기능을 사용하려면 저장할 추가 정보 또는 사용 가능한 추가 방법에 대한 필드가 있는 모델을 정의하고 모델에서 사용자 모델에 OneToOneField 사용자를 추가한다. 이렇게 하면 각 사용자에 대해 모델의 인스턴스(instance)를 하나만 생성할 수 있다. (추가 정보가 있는 model을 생성하고 User를 OneToOneField로 지정하라는 말인듯)

이 모델이 특정 사이트에 대한 사용자 프로파일 모델임을 나타내려면 다음 항목으로 구성된 문자열로 AUTH_PROFILE_MODULE 설정을 입력한다:

1. 사용자 프로파일 모델이 정의된 응용프로그램(대소문자 구분)이름. (즉 manage.py startapp으로 생성한 어플리케이션 이름 )
2. model class 이름(대소문자 구분 안함.)

예를들어 profile model의 이름이 UserProfile이고 accounts 어플리케이션 안에 정의 되었다면, 적절한 setting은 :
```
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
```
사용자 프로파일 모델이 이 방법으로 정의되고 지정된 경우 각 User 개체에는 해당 User와 연결된 사용자 프로파일 모델의 인스턴스를 반환하는 메소드를 가진다 (get_profile())

get_profile() 메소드는 없을 경우 profile을 생성하지 않는다. User model에 django.db.models.signals.post_save 신호에 대한 handler를 등록해야 하며 handler에서 created = True이면 연관된 사용자 프로파일을 작성해야 한다.


## Authentication in Web requests
지금까지 문서에서는 인증 관련 오브젝트를 다루기 위해 필요한 저수준 API를 다뤘다. 더 높은 수준에서 Django는 이 인증 프레임워크를 request object 시스템에 연결할 수 있다.

먼저 settings의 MIDDLEWARE_CLASSES에 SessionMiddleware와 AuthenticationMiddleware를 추가하여 설치한다. 

이러한 미들웨어를 설치하면 뷰에서 request.user에 접근할 수 있다. request.user는 현재 로그인한 사용자를 나태내는 User object를 제공한다. 만약 사용자가 로그인한 상태가 아닐경우에 request.user에 AnonymousUser 인스턴스가 설정될 것이다. 다음과 같이 is_authenticated()를 사용하여 구분할 수 있다.:

```
if request.user.is_authenticated():
    # Do something for authenticated users.
else:
    # Do something for anonymous users.
```
### How to log a user in

Django는 django.contrib.auth:authenticate()와 login() 두개의 함수를 제공한다.

**authenticate()**
인증하기 위해 authenticate() 사용시 username과 password를 준다. 이것은 username, password 두개의 키워드 arguments를 취한다 그리고 주어진 username에 대해 password가 유효하다면 User object를 반환한다. 만약 password가 유효하지 않다면 authenticate()는 None을 반환한다. Ex:
```
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    if user.is_active:
        print "You provided a correct username and password!"
    else:
        print "Your account has been disabled!"
else:
    print "Your username and password were incorrect."
```

**login()**

뷰에서 사용자 로그인을 위해 login()을 사용한다. 이것은 HttpRequest object와 User object를 취한다. login()은 Django의 세션 프레임워크를 이용해 user의 ID를 세션에 저장하므로 전에 언급한대로 session 미들웨어를 설치해야 한다. 

아래 예는 authenticate()와 login() 둘다 사용하는지를 보여준다. :
```
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = autenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
    else:
        # Return an 'Invalid login' error message.
```

>>> Calling authenticate() first
>>> 수동으로 사용자를 로깅할 경우에는 login()호출하기 전에 authenticate()를 호출해야 한다. authenticate()는 인증 백엔드에서 해당 사용자를 성공적으로 인증한 속성을 사용자에게 설정한다. 이 정보는 로그인 프로세스 중에 나중에 필요하다. 


### Limiting access to logged-in users

#### The raw way
페이지에 접근을 제한하기 위한 raw way는 request.user.is_authenticated()를 확인하는 것이다. 그리고 로그인 페이지로 redirect 시킨다.

```
from django.http import HttpResponseRedirect

def my_view(request):
    if not requet.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    # ...
```
또는 에러 메시지를 출력한다.

```
def my_view(request):
    if not request.user.is_authenticated():
        return render_to_response('myapp/login_error.html')
```

#### The login_required decorator
*decorators.login_required([redirect_field_name=REDIRECT_FIELD_NAME, login_url=None])*

편의를 위해 login_required() 데코레이터를 사용할 수 있다.:
```
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
```

login_required()는 아래와 같이 수행한다.

* 만약 사용자가 로그인이 안되어 있을 경우 현재 경로를 query string으로 전달하여 settigns.LOGIN_URL로 리디렉션 시킨다 ex) /accounts/login/?next=/polls/3/.
* 로그인 되어 있다면 view를 실행한다. view는 사용자가 로그인 되어있다고 가정한다. 

기본적으로 인증에 성공하면 사용자를 리디렉션해야 하는 경로는 query string의 'next' param에 저장된다. next 대신 다른 이름을 사용하려면 login_required()의 redirect_field_name 매개변수를 사용한다 
```
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='my_redirect_field')
def my_view(request):
    ...
```
redirect_field_name을 사용할 경우 리디렉션 경로를 저장하는 템플릿 컨텍스트 변수에서는 redirect_field_name 값을 키로 사용하지 않고 해당 값을 사용하기 때문에 로그인 템플릿도 사용자가 지정해야 한다.

login_required()는 login_url 파라메터도 가진다. Ex:
```
from django.contrib.auth.decorators import login_requried

@login_required(login_url="/accaounts/login/")
def my_view(request):
    ...
```
login_url을 명시하지 않을 경우 settings,LOGIN_URL에 적절한 Django view를 매핑해야한다. 예를들어 default값을 사용할경우 URLconf에 아래 내용을 추가해야한다.
```
(r'^accounts/login/$', 'django.contrib.auth.views.login'),
```

*views.login(request[, template_name, redirect_field_name, authentication_form)*

django.contirb.auth.login은 아래와 같은 작업을 한다.
* GET이 호출되었을 경우 login form을 보여준다. POST와 같은 URL이다. 
* POST가 호출되었을 경우 로그인을 시도한다. 만약 로그인이 되었을 경우 뷰는 next에 명시된 URL로 리디렉션을 시킨다. next가 없을 경우 settings.LOGIN_REDIRECT_URL로 리디렉션 시킨다(settings.LOGIN_REDIRECT_URL의 기본 값은 /accounts/profile/임). 로그인이 실패했을 경우 login form을 다시 보여준다. 

기본적으로 registeration/login.html 템플릿에서 로그인 양식을 제공하는건 사용자의 책임이다. 이 템플릿은 4가지 템플릿 컨텍스트 변수를 전달한다.

* form
    * 로그인 폼을 나타낼 Form 오브젝트.
* next
    * 로그인 성공 후 리디렉션 시킬 URL. query string 포함한다. 
* site
    * 현재 site(SITE_ID에 따라 다름).만약 site 프레임워크가 설치되어 있지 않을 경우 현재 HttpRequest에서 사이트 이름과 도메인을 가져오는 RequestSite 인스턴스가 세팅된다.  
* site_name
    * site.name 만약 site 프레임워크가 설치되어 있지 않을 경우 requset.META['SERVER_NAME']값이 세팅된다. 

registration/login.html 템플릿을 호출하지 않으려면 URLconf의 뷰의 추가 인수를 통해 template_name 파라미터를 전달할 수 있다. 예를 들어 아래의 URLconf 는 myapp/login.html을 대신 사용한다.:
```
(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name':'myapp/login.html'})
```

redirect_field_name를 뷰로 전달하여 로그인 후 리디렉션할 URL이 포함된 GET 필드의 이름도 지정할 수 있다.  기본적으로 이 필드는 next이다.

시작점으로 사용할 수 있는 registration/login.html 템플릿이다. 이 템플릿은 content block을 포함하는 base.html을 가지고 있다고 가정한다 :

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

대체 인증을 사용하는 경우(기타 인증 소스 참조) certification_form 매개 변수를 통해 사용자 지정 인증 양식을 로그인 보기에 전달할 수 있다. 이 양식은 __init__ 메서드에서 요청 키워드 인수를 수락하고 인증된 사용자 개체를 반환하는 get_user 메서드를 제공해야 한다(이 방법은 양식 유효성 검사에 성공한 후에만 호출됨).
