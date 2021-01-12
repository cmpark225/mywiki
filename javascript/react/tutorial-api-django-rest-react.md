
https://www.valentinog.com/blog/tutorial-api-django-rest-react/


# setting up a Python virtual environment, and the project
```
$ virtualenv .env
Running virtualenv with interpreter /usr/bin/python2
New python executable in /home/user/data/workspace/test1/.env/bin/python2
Also creating executable in /home/user/data/workspace/test1/.env/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.

$ source .env/bin/activate
(.env) $ mkdir django-drf-react-quickstart
(.env) $ cd django-drf-react-quickstart
(.env) django-drf-react-quickstart$ pip install django djangorestframework
(.env) django-drf-react-quickstart$ django-admin startproject project
(.env) django-drf-react-quickstart$ ll
drwxrwxr-x 3 user user 4096  3월 27 17:29 ./
drwxrwxr-x 4 user user 4096  3월 27 17:28 ../
drwxrwxr-x 3 user user 4096  3월 27 17:29 project/
```

# building a Django application

Django 프로젝트는 많은 application으로 구성되어 있다. 각 어플리케이션은 이상적으로 한가지 일을 한다. 

Django 어플리케이션은 모듈로 되어있고 재사용 가능하다. 예: lead에 대해 생성하고 열거하기 위해 lead 어플리케이션을 만들 수 있다.

다른 프로젝트에 동일한 앱이 필요한 경우 패키지 관리자로부터 lead를 설치할 수 있다.


아래 두개 참고 해라
* [How to write reusable apps](https://docs.djangoproject.com/en/2.0/intro/reusable-apps/)
* [DjangoCon2008:Reusable Apps to learn about app best practices](https://www.youtube.com/watch?v=A-S0tqpPga4&feature=youtu.be)


새로운 어플리케이션 생성을 위해서는 아래를 실행해라:
```
$ django-admin startapp app_name
```

lead 앱 생성을 위해 project 폴더 안으로 이동해라:
```
(.env) django-drf-react-quickstart$ cd project
(.env) django-drf-react-quickstart/project$ ll
total 16
drwxrwxr-x 3 user user 4096  3월 27 17:29 ./
drwxrwxr-x 3 user user 4096  3월 27 17:29 ../
-rwxrwxr-x 1 user user  805  3월 27 17:29 manage.py*
drwxrwxr-x 2 user user 4096  3월 27 17:29 project/
```

app 초기화한다:
```
(.env) django-drf-react-quickstart/project$ django-admin startapp leads
(.env) django-drf-react-quickstart/project$ ll
drwxrwxr-x 4 user user 4096  3월 27 17:42 ./
drwxrwxr-x 3 user user 4096  3월 27 17:29 ../
drwxrwxr-x 3 user user 4096  3월 27 17:42 leads/
-rwxrwxr-x 1 user user  805  3월 27 17:29 manage.py*
drwxrwxr-x 2 user user 4096  3월 27 17:29 project/
```

> Note: 나는 너가 위에 있는 명령어를 실행하는 동안 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있다고 가정한다! YOUR_CODE_DIR VenvDjango 와 같은 무언가일 것이다. 내 전체 경로는 /home/valentino/VenvDjango/django-drf-react-quirckstart/project 이다. 

~/YOUR_CODE_DIR/django-drf-react-quickstart/project 안에 새로운 디렉토리 leads를 확인할 수 있다.

이제 Django에게 새로운 app 사용을 알려주자.

./project/settings.py 를 열고 INSTALLED_APPS안에 앱을 추가한다:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leads', # add the leads app
]
```

다음 섹션에서는 첫번째 모델을 추가한다.

# creating a Django model

**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라

우리 첫 모델을 만들 시간이다. 모델은 테이블의 데이터를 나타내는 object이다. 거의 모든 웹 프레임워크는 모델이라는 개념이 있다. Django도 예외는 아니다.

Django 모델은 하나 혹은 하나이상의 필드를 가진다: 각 필드는 테이블의 컬럼이다. 앞으로 나아가기 전에 lead 어플리케이션의 요구사항을 정의해보자.

첫째 우리는 Lead 모델이 필요하다.

lead를 수집하고 있기 때문에 다음과 같은 필드로 만든 Lead 모델을 생각할 수 있다.:
* a name
* an email
* a message

(예를들어 전화번호와 같이 자유롭게 필드를 추가할 수 있다!)

timestamp 필드를 잊지마라! Django는 create_at 컬럼을 기본적으로 추가해주지 않는다. 

./leads/models.py 를 열고 Lead 모델을 생성한다:
```
from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
```

모델에 대한 간단한 참고 사항 : [Django 필드 문서](https://docs.djangoproject.com/en/2.0/ref/models/fields/)를 확인하는 시간을 가져라.

모델을 계획할때 유스 케이스에 가장 적절한 필드를 선택해라.

그리고 이 모델을 사용하여 다음을 실행하여 마이그레이션을 만든다:
```
(.env) django-drf-react-quickstart/project$ python manage.py makemigrations leads
```

그리고 마지막으로 database에 마이그레이션한다:
```
(.env) django-drf-react-quickstart/project$ python manage.py migrate
```

다음장에 serializers와 views에 대해 이야기할 것이다. 하지만 먼저 testing에 대해 알려줌

# a sprinkle of testing
skip

# Django REST serializers

**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라


serialization이란 무엇인가?

[Django REST serializer](https://www.django-rest-framework.org/api-guide/serializers/)란 무엇인가?

**Serialization**은 object를 다른 데이터 포멧으로 변환하는 행동이다. 

object 변환 후에 우리는 이것을 파일로 저장하거나 네트워크를 통해 전송할 수 있다. 

왜 serialization이 필요한가?

Django 모델에 대해 생각해봐라: 이것은 파이썬 클래스이다. 브라우저에서 파이선 클래스를 JSON으로 어떻게 렌더링 할 것인가?

Django REST serializer 이용!

serializer는 반대로도 작용한다: JSON을 object로 변환

이 방식은 아래가 가능하게 한다:

* 브라우저에서 jsong으로 변환하여 Django 모델을 표시
* API에 JSON 페이로드로 CRUD 요청

요약 : Django REST serializer는 API를 통해 모델에서 동작하는 경우 필수이다.

./leads/serializers.py 파일 새로 생성. LeadSerializer는 우리의 모델과 필드를 가진다.:

```
from rest_framework import serializers
from leads.models import Lead
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'email', 'message')
```

보이는 것과 같이 ModelSerializer를 상속받는다.

Django REST의 ModelSerializer는 ModelForm과 같다.

이것은 모델을 Serializer에 밀집하게 매핑하려는 경우 적합하다.

각 필드를 명시적으로 정의하는 것 외에도 모든 모델 필드를 매핑할 수 있다.

```
from rest_framework import serializers
from leads.models import Lead
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'
```

저장하고 파일을 닫아라. 완벽한 어플리케이션아 한발짝 다가섰다.

다음 장에서는 views와 url에 대해 살펴본다.

# settings up the controll (view)

**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라

다른 프레임워크로 부터 왔다면 Django가 controller가 없다는 것에 놀랄 것이다.

컨트롤러는 요청 작업과 응답을 반환하기 위한 로직을 캡슐화한다. 전통적인 MVC 구조에서는 Model, View, Controller가 있다. 

MVC 프레임워크의 예는 Rails, Phoenix, Larabel이 있다. 

Django는 MVT 프레임워크다. 이것은 Model - View - Template 이다. 뷰는 요청/응답의 생명주기를 관리한다.

Django에는 뷰의 많은 타입이 있다: [function views](https://docs.djangoproject.com/en/2.0/topics/http/views/),  [class based views](https://docs.djangoproject.com/en/2.0/topics/class-based-views/), 그리고 [generic views](https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/) 

일부 개발자는 클래스 기반 대신 함수 기반을 더 선호하지만, 나는 클래스 기반을 선호한다.

내가 Django를 선택할때 나는 개발 속도, DRY(?) 적은 코드에 대해 중시하기 때문이였다.

내 thumb 규칙이 있다:

generic views를 커스터마이징 하는데 걸리는 시간이 뷰를 직접 작성하는데 걸리는 시간보다 많을 경우에만 function view를 사용한다. 

일반 Django와 같이 Django REST 프레임워크에서는 뷰를 작성하는데 몇가지 방법이 있다:

* function based views
* class based views
* generic API views

튜토리얼 범위에서는 generic API veiw를 사용할 것이다. 목적은 코드를 적게 사용하는 것이다.

우리의 간단한 앱은 아래와 같은 일을 해야한다. :

* 모델의 목록 수집
* 데이터베이스의 새로운 object 생성 

[generic API view 문서](https://www.django-rest-framework.org/api-guide/generic-views/#generic-views)를 살펴보면 모델을 나열하고 작성하는 view 가 있음을 알 수 있다.

[ListCreateAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview)

ListCreateAPIViews는 queryset과 serializer_class를 가진다. 

./leads/views.py 파일을 열고 뷰를 생성한다:

```
from leads.models import Lead
from leads.serializers import LeadSerializer
from rest_framework import generics
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
```

코드의 3줄로 우리는 GET과 POST 요청을 다루는 뷰를 생성했다.

무엇이 부족한가? URL 매핑! 즉 URL을 views에 매핑해야 한다. 

어떻게? 다음 섹션으로 넘어가라

# setting up the route (urls)

**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라

Rails, Phoenix 또는 Laravel에서 왔다면 Django에서는 rout 설정이 없다는 것에 놀랄 것이다. 

DRF에는 [resourceful한 라우터](https://www.django-rest-framework.org/api-guide/routers/)가 있지만, URL을 view에 매핑하는 가장 간편한 방법은 URL 매핑이다.

우리의 목적은 LeadListCreate를 api/lead에 연결하는 것이다.

즉 GET과 POST요청을 모델을 열거하고 생성하기 위해 api/lead에 만들기 원한다.

URL 매핑을 구성하려면 ./project/urls.py에있는 앱 URL을 포함해라.
```
from django.conf.urls import url, include
urlpatterns = [
    url('', include('leads.urls')),
]
```

다음으로 ./leads/urls.py 파일 생성
이 파일에서 LeadListCreate를  api/lead/를 연결한다:

```
from django.conf.urls import url
from . import views

urlpatterns = [
    url('api/lead/', views.LeadListCreate.as_view() ),
]
```

마지막으로 rest_framework를 INSTALL_APPS에 사용가능하게 하자.

./project/settings.py를 열고 INSTALLED_APPS에 앱을 추가한다.:

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leads', 
    'rest_framework' # enable rest framework
]
```

이제 다음을 통해 온전함 검사를 실행할 수 있다.
```
(.env) django-drf-react-quickstart/project$ python mansage.py runserver
```

http://127.0.0.1:8000/api/lead/로 이동하면 탐색가능한 API를 볼 수 있다.


> 안될경우 migrate 수행.. 
```
(.env) django-drf-react-quickstart/project$ python mansage.py makemigrations
(.env) django-drf-react-quickstart/project$ python mansage.py migrate
```

해당 페이지에 있는 동안 안에 있는 form으로 데이터 생성을 시도해봐라.

다음 장에서는 Django에서 데이터베이스에 어떻게 seed 하는지를 배울 것이다.

# seeding the database

**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라


database로 옮기기 위해 [Django fixtures](https://docs.djangoproject.com/en/2.0/howto/initial-data/)를 사용할 수 있다. 

Fixtures는 frontend의 데이터를 데모로 주기를 원할때 유용하다.

./leads/fixtures 디렉토리를 생성해라.

그리고 아래에 있는 JSON을 가지는 ./leads/fixtures/leads.json 파일을 생성한다.

```
[
    {
        "model": "leads.lead",
        "pk": 1,
        "fields": {
            "name": "Armin",
            "email": "something@gmail.com",
            "message": "I am looking for a Javascript mentor",
            "created_at": "2018-02-14 00:00:00"
        }
    },
    {
        "model": "leads.lead",
        "pk": 2,
        "fields": {
            "name": "Tom",
            "email": "tomsomething@gmail.com",
            "message": "I want to talk about a Python project",
            "created_at": "2018-01-14 00:00:00"
        }
    }
]
```

파일을 저장하고 닫은 후 fixture를 아래 명령어로 loed 한다:

```
(.env) django-drf-react-quickstart/project$ python manage.py loaddata leads
```

끝!

다음 섹션에서는 간단한 React frontend를 구현할 것이다(마침내!)

# Django and React together

많은 동료 파이썬 개발자들이 간단한 질문으로 고군분투한다. 어떻게 Django와 React를 붙일 것인가?

React router가 라우팅을 가져야 하나? 각 Django 템플릿에 컴포넌트를 마운트 해야 하나? (정신을 잃고 싶다면..)

나는 "그것은 달려있다"라고 말할 것이다. 자바스크립트가 얼마나 필요한지에 달려있다

리엑트와 함께 장고 프로젝트를 세울 수 있는 많은 방법이 있다.

(거의 모든 웹 프레임워크에 공통인) 다음 패턴을 본다.

1. 자체 "프론트" Django 앱으로 대응: 단일 HTML 템플릿을 로드하여 React가 프런트엔드를 관리하게 함(어려움: 중간)

2. 독립형 API로서의 Django REST + 독립형 SPA로 대응(어려움: 어려움, 인증용 JWT 포함)

3. 믹스 앤 매치: Django 템플릿 내의 미니 리액트 앱(어려움: 단순)

여기 내 추천이다.

만약 Django와 React를 방금 시작했다면 2번은 피해라 

1번으로 가라(자체 "프론트" 디장고 앱으로 대응) 만약:

* 앱과 같은 웹 사이트를 구축하는 경우
* 인터페이스에 사용자 상호 작용/AJAX가 많은 경우
* 세션 기반 인증에 문제가 없는 경우
* SEO(?)에 우려가 없을 경우
* React Router로 괜찮을 경우

React를 Django에 가깝게 유지하면 인증 및 기타 사항에 대해 쉽게 추론 할 수 있다.

사용자 등록과 로그인을 위해 [Django 기본 인증](https://docs.djangoproject.com/en/2.0/topics/auth/default/#module-django.contrib.auth.views)을 이용할 수 있다.

좋은 '[세션 인증](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication)을 사용하고 토큰과 JWT에 대해 너무 걱정하지 마라

3번으로 가라(Django 탬플릿 내의 미니 React 앱):

* 웹사이트에 자바스크립트가 많이 필요하지 않다면.
* SEO(?)를 돌봐야 한다면.

우리는 다음장에 1번을 살펴 본다.

그런데 전체 프런트엔드에 리액트를 사용하는 것이 선택사항이 아닌 상황이 여전히 존재한다.

그럴 경우 죄책감을 느끼지 않고 언제나 Vue 던질 수 있다.



# setting up React and webpack
**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라

Django와 React의 가장 좋은 점은 API를 제공하는 endpoint가 Django REST framework라는 것이다. 

React를 사용하여 "frontend"라는 자체 앱을 가진다. 

우리는 이미 Django앱에서 어떻게 app을 생성하는지 알고 있다:

```
(.env) django-drf-react-quickstart/project$ django-admin startapp frontend
```

~/YOUR_CODE_DIR/django-drf-react-quickstart/project 안데 frontend 디렉토리를 확인할 수 있다.


이 프로젝트의 현재 모습은 다음과 같다.:
```
$ ls -1
frontend
leads
manage.py
project
```

React components를 가지기 위한 디렉토리 구조를 준비한다:
```
$ mkdir -p ./frontend/src/components
```

그리고 static 파일들:
```
$ mkdir -p ./frontend/{static, templates}/frontend
```

다음으로 React, webpack 4 그리고 바벨을 설치할 것이다.

앞으로 진행하기 전 빠르게 살펴본다. 

frontend는 독립 실행 형 응용 프로그램이므로 ./frontend에 webpack 및 친구를 설치하는 것이 좋다.

그러나 우리의 의도를 분명히하는 것은 나쁜 생각이 아니다.

package.json을 기본 디렉토리에 넣으면 더 좋을까?

모든 개발자는 리포를 보고 "좋아, 거기에 리액트와 웹팩이 있어"라고 말할 수 있다.

당신은 어떻게 생각하나요? 그렇게 하자.

~/YOUR_CODE_DIR/django-drf-react-quickstart/project/ 에 있다고 가정하고 상위 폴더로 이동한다:
```
$ cd ..
```

그리고 환경을 초기화한다:
```
$ npm init -y
```

다음으로 webpack과 webpack cli를 아래 명령어로 설치한다:
```
npm i webpack webpack-cli --save-dev
```

이제 package.json을 열고 스크립트를 설정한다:
```
"scripts": {
  "dev": "webpack --mode development ./project/frontend/src/index.js --output ./project/frontend/static/frontend/main.js",
  "build": "webpack --mode production ./project/frontend/src/index.js --output ./project/frontend/static/frontend/main.js"
}
```

파일을 저장하고 닫는다.

webpack 4에 대해 좀더 알고 싶으면 [Webpack 4 Tutorial: from 0 Conf to Production Mode](https://www.valentinog.com/blog/webpack-tutorial/)를 확인해라

이제 코드를 번역하기 위해 bable을 설치하자:

```
npm i @babel/core babel-loader @babel/preset-env @babel/preset-react babel-plugin-transform-class-properties --save-dev
```

babel-plugin-transform-class-properties는 ES6 클래스의 정적 속성을 사용하는 데 필요하다.

React 와 prop-types를 받는다:
```
npm i react react-dom prop-type --save-dev
```

프로젝트 폴더 안에 .bablerc 파일을 생성하여 Babel을 설정한다.

```
{
    "presets": [
        "@babel/preset-env", "@babel/preset-react"
    ],
    "plugins": [
        "transform-class-properties"
    ]
}
```

마지막으로 bable-loader을 설정하기 위해 webpack.config.js 파일을 새로 생성한다.:

```
module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  }
};
```

# the React frontend
**Note**: 앞으로 나아가기전에 아직 ~/YOUR_CODE_DIR/django-drf-react-quickstart/project에 있음을 확인해라

어떻게 React frontend 와 연결 할 수 있는지 확인해보자

첫번째로 먼저 ./frontend/views.py에 view를 만든다:
```
from django.shortcuts import render
def index(request):
    return render(request, 'frontend/index.html')
```

이것은 템플릿을 리턴하기 위한 보잘것 없는 function view다.

그리고 나서 ./frontend/templates/frontend/index.html에 템플릿을 생성한다:
```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.6.2/css/bulma.min.css">
  <title>Django DRF - React : Quickstart - Valentino G. - www.valentinog.com</title>
</head>
<body>
  <section class="section">
    <div class="container">
          <div id="app" class="columns"><!-- React --></div>
    </div>
  </section>
</body>
{% load static %}
<script src="{% static "frontend/main.js" %}"></script>
</html>
```

템플릿에서 볼 수 있듯이  webpack bundle인 frontend/main.js를 호출할 것이다

Psst! [Bulma](https://bulma.io/)는 빠른 프로토 타이핑을 위한 가장 좋아하는 CSS 프레임 워크이다! 

fontend를 포함하기 위해 ./project/url.py에 새로운 URL 매핑을 설정하자:
```
urlpatterns = [
    url('', include('leads.urls')),
    url('', include('frontend.urls')),
]
```

다음 ./frontend/urls.py 파일을 새로 생성한다.

이 파일에서 뷰를 root에 연결한다.:
```
from django
```

마지막으로 ./project/settings.py에 frontend app을 사용하기 위한 설정을 해준다.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leads', 
    'rest_framework',
    'frontend' # enable the frontend app
]
```

이 시점에서 아래를 시도할 수 있다:
```
$ python manage.py runserver
```

그리고 http://127.0.0.1:8000/에서 아무것도 볼 수 없을 것이다 왜냐하면 React가 빠졌기 때문이다.

간단한 React frontend를 만들기 위해 우리는 3개의 컴포넌트를 만들 것이다.:

1. App, "mother" 컴포넌트
2. Dataprovider, 데이터를 가져 오기 위한 상태 저장 컴포넌트(렌더링 props  포함)!
3. Table, 데이터 출력을 위한 stateless 컴포넌트(상태 저장 x)

## The App component

React를 <div id = "app"> </ div>에 연결하기위한 메인 컴포넌트.

./frontend/src/components/App.js 파일 생성 :
```
import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
const App = () => (
  <DataProvider endpoint="api/lead/" 
                render={data => <Table data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
```

## The DataProvider component
데이터를 가져오기 위한 stateful(상태 저장) 컴포넌트 (렌더링 props 포함!)

./frontend/src/component/DataProvider.js 파일 생성:
```
import React, { Component } from "react";
import PropTypes from "prop-types";
class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };
  state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    fetch(this.props.endpoint)
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}
export default DataProvider;
```

## The Table component
테이블을 가지는 데이터 표시를 위한 stateless(상태 저장 x) 컴포넌트

./frontend/src/components/Table.js 파일 생성:
```
import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";
const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        Showing <strong>{data.length} items</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            {Object.entries(data[0]).map(el => <th key={key(el)}>{el[0]}</th>)}
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              {Object.entries(el).map(el => <td key={key(el)}>{el[1]}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;
```

컴포넌트는 row를 동적으로 만들기 때문에 React key id를 위해 외부 패키지 의존이 필요하다.

[Bartosz](https://medium.com/@baphemot)가 지적했듯이, shortid를 사용하는 것은 최적이 아닐 수 있다.

React의 shortid에 대한 더 나은 대안은 [weak-key](https://www.reddit.com/r/reactjs/comments/8o5oqe/beginners_thread_easy_question_june_2018/e05jfu8/)이다:

```
npm i week-key --save-dev
```

마지막으로 ./frontend/src/index.js에 webpack 진입점을 생성한다. :
```
import App from "./components/App";
```
파일을 저장하고 닫는다.

이 시점에서 우리는 test 할 준비가 되었다.

webpack을 실행한다:
```
npm run dev
```

개발 서버를 시작한다:
```
python manage.py runserver

```
http://127.0.0.1:8000로 이동한다. 

"Something went wrong"이 보인다면 migrate와 database 이동을 확인해봐라:

```
python manage.py migrate && python manage.py loaddata leads
```

그리고 다시 서버를 실행한다.

마침내 끝내주는 React app(table)을 확인 할 수 있다!

어떻게 보이는가?

매우 간단하다. 하지만 동작한다!

# testing the frontend
skip


# building a React form
skip

이 앱은 매우 간단하고 인위적인 예제를 기반으로 한다.

하지만 React와 Django Rest 를 시작하기에 좋은 출발점이다.

이 시점에서 간단한 django/React 프로젝트의 barebone을 완료했다.

아래와 같은 방법을 배웠다.

* 간단한 django REST API 빌드
* React와 Django 프로젝트 구조 
* React와 Django Rest API 연결

프로젝트에 더 많은 기능을 추가하여 실험 해봐라 (인증).
