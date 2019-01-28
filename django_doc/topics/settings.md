# Django settings

## Designating the settings
Django를 사용 할 때, 어떤 settings를 사용하는지 알려줘야 한다. DJANGO_SETTINGS_MODULE을 환경 변수로 사용하여 이 작업을 수행한다.

DJANGO_SETTINGS_MODULE 값은 Python 경로 구문이어야 한다(예: mysite.settings). 설정 모듈은 import search path 경로에 있어야 한다는 점을 유의해야 한다. 

### The django-admin.py utility
django-admin.py를 사용 할 때, 환경 변수를 한 번 설정하거나, 유틸리티를 실행 할 때마다 settings 모듈을 명시적으로 전달할 수 있다. 

예 (Unix Bash shell):
```
export DJANGO_SETTINGS_MODULE=mysite.settings
django-admin.py runserver
```

예 (Windows shell):
```
set Django_SETTINGS_MODULE=mysite.settings
django-admin.py runserver
```

--settings 커맨드라인 인자 사용:
```
django-admin.py runserver --settings=mysite.settings
```

### On the server (mod_wsgi)
실제 서버 환경에서, WSGI 어플리케이션에 어떤 settings 파일을 사용하는지 알려줘야 한다. os.environ으로 이 작업을 수행한다:
```
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
```
더 자세한 정보와 django WSGI 어플리케이션의 다른 공통 요소를 얻으려면 Django mode_wsgi documentation을 읽어라.


## Default settings

필요하지 않을 경우 Django settings 파일은 정의될 필요가 없다. 각 settings는 실용적인 디폴트 값을 가지고 있다. 이런 default 값들은 django/conf/global_settings.py에 있다.

Django가 컴파일 설정에 사용하는 알고리즘:
* global_settings.py에서 settings를 Load 한다
* 필요에 따라 전역 설정을 재 정의하여 명시된  settings 파일에서 settigns를 Load 한다.

설정 파일은 중복되므로 settings 파일에서 global_settings에서 import하지 않아야 한다는 점에 유의한다.

### Seeing which settings you've changed
default settings에서 당신의 settigns 중 어느 것이 다른지 보기 쉬운 방법이 있다. 'python manage.py diffsettings' 명령은 현재 settigns 파일과 Django의 default settings 사이에 다른 점을 보여준다.

좀 더 자세한 정보는, [diffsettings](https://django.readthedocs.io/en/1.3.X/ref/django-admin.html#django-admin-diffsettings) 문서 참조.

## Using settings in Python code

당신의 Django app에서, django.conf.settings를 import 하여 settigns를 사용한다. 예:
```
from django.conf import settings

if settings.DEBUG:
    # Do something
```

django.conf.settings는 모듈이 아니라 object인 것을 명심해라. 따라서 각각의 settings의 import는 불가능 하다:
```
from django.conf.settings import DEBUG # 동작 안함
```
또한 코드는 global_settigns 또는 자신의 설정 파일에서 가져오지 않아야 한다는 점에 유의 해야 한다. django.conf.settings는 기본 설정과 사이트별 설정의 개념을 추상화하며, 단일 인터페이스를 제공한다. 또한 설정을 사용하는 코드를 설정 위치에서 분리해라. 

## Altering settings at runtime
어플리케이션이 실행 중일때 settings를 수정하면 안된다. 예를들어. 뷰에서 아래와 같이 하면 안된다:
```
from django.conf import settings
settings.DEBUG = TRUE # Don't do this!
```
설정에 대한 할당은 settings file에서만 이뤄져야 한다.

## Security
settings 파일은 데이터베이스 비밀번호와 같은 민감한 정보를 포함하기 때문에, 접근을 제한 하기 위한 모든 시도를 해야 한다. 예를 들어, 사용자와 웹 서버의 사용자만 읽을 수 있도록 파일 사용 권한을 변경햐라. 이것은 특히 공유 호스트 환경에서 중요하다.   

## Available settings
이용 가능한 세팅에 대한 모든 리스트는 해당 문서에서 확인할 수 있다. [settigns reference](https://django.readthedocs.io/en/1.3.X/ref/settings.html)

## Createing your own settings
당신의 Django app을 위해 자신만의 설정을 만들 수 있다. 다음 규칙을 따르면 된다.

* 설정 이름은 모두 대문자.
* 이미 있는 설정 이름은 사용하지 않는다.
  
sequence한 설정인 경우, list 보다는 tuples를 시용한다. 하지만 이것은 그냥 규칙일 뿐이다.

## Using settings without setting DJANGO_SETTINGS_MODULE
몇몇의 경우, DJANGO_SETTINGS_MODULE 환경 변수를 생략하고 싶을 수 있다. 예를 들어, 템플릿 시스템을 단독으로 사용하는 경우 설정 모듈을 가리키는 환경 변수를 설정하지 않아도 된다.

이 경우 Django의 설정을 수동으로 설정할 수 있다. 아래를 호출함으로써:

**django.conf.settings.configure(default_settings, **settings)**

예)
```
from django.conf import settings

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True, 
    TEMPLATE_DIRS=('/home/web-app/myapp', '/home/web-apps/base'))
```

configure에 원하는 만큼 많은 키워드 인수를 전달해라. 각 키워드 인수는 settings와 값을 나타낸다. 각 인수 이름은 위에서 설명한 설정과 동일한 이름을 가진 모두 대문자여야 한다. 만약 특정 설정이 configure()에 전달되지 않고 나중에 해당 설정이 필요하다면, Django는 default 설정 값을 사용할 것이다. 

Django를 이 방식으로 설정하는 것이 가장 중요하다. 더 큰 응용 프로그램 내부에서 프레임 워크를 사용할 때 좋다.

결과적으로, settings.configure()를 통해 구성 할 때, Django는 프로세스의 환경변수를 수정하지 않는다(TIME_ZONE의 설명서 참조). 이러한 경우에 이미 환경을 완벽하게 제어하고 있다고 가정한다.

### Custom default settings

기본값을 django.conf.global_settings가 아닌 다른 곳에서 오길 원한다면, default_settings 인수(또는 첫 번째 위치 인수)로 기본 설정을 제공하는 모듈이나 클래스를 구성 호출에 전달할 수 있다.

이 예에서는, default 설정 값을 myapp_fefaults에서 가져오고 myapp_defaults의 값과 관계 없이 DEBUG 세팅 값은 TRUE로 설정 된다:
```
from django.conf import settings
from myapp import myapp_defaults

settings.configure(default_settings=myapp_defaults, DEBUG=True)
```

아래 예에서는, myapp_defaults를 위치 인수로 사용한다. 위와 동일하다:
```
settings.configure(myapp_defaults, DEBUG=True)
```

일반적으로, 이런 식으로 기본 값을 재 지정 할 필요는 없을 것이다. Django default는 당신이 안전하게 사용 할 수 있을 정도로 충분히 오래 되었다. 새 기본 모듈을 전달하면, Django 기본 값을 완전히 대체하므로 가져오는 코드에서 사용 할 수 있는 모든 가능한 설정에 대한 값을 지정해야 한다는 점을 유의해야 한다. 전체 목록은 django.conf.settings.global_settings에서 참고 해라. 

### Either configure() or DJADNGO_SETTINGS_MODULE is required
DJANGO_SETTINGS_MODULE 환경 변수를 설정하지 않았다면, 코드가 settings를 읽기 전 어느 곳이라도 configure()를 호출해야 한다. 

DJANGO_SETTINGS_MODULE을 설정하지 않거나, configure()를 호출하지 않는다면, settings가 처음 접근될때 Django는 ImportError 예외를 발생시킬 것이다.

만약 DJANGO_SETTINGS_MODULE이 설정되고, 어떻게든 settings 값이 접근된 후, configre()를 호출하면, settings가 이미 설정되었기 때문에 Django는 RuntimeError를 발생시킨다.

또한 한번 이상 configure()를 호출하거나, 설정 값이 접근 된 후 configure()을 호출해도 에러가 발생한다.

즉 configure()나 DJANGO_SETTINGS_MODULE 중 하나만 사용해야 한다. 둘 다 사용하거나 둘다 사용하지 않으면 안된다. 
