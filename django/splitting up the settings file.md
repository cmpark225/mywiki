https://code.djangoproject.com/wiki/SplitSettings#Differentsettingsindifferentfiles
여러 명이서 개발할 경우, 혹은 local 설정과 deploy 설정이 다를 경우

settings.py의 설정이 각각 다르게 적용되야 하는 경우가 있다.

git과 같은 버전 관리 툴에 settings.py가 올라가 있어서

각자 위치에서 자신의 환경에 맞게 settings.py를 수정하고 push를 안하며 개발할 수 있지만, 실수로 push할 경우 문제 생길 수 있다.

아래에는 settings.py는 유지하면서, 

각자의 settings 설정을 가지는 방법을 설명한다.

(내가 생각하기에 유용한 내용만)

# ini-style file for deployment
init 파일을 각자 생성해서 개별 설정은 해당 파일에서 읽어오게 하는 방식.

각 위치에 settings.ini 파일이 있어야 한다.

settings.ini 파일에서 읽어오기 때문에 버전관리가 어렵다.

버전 관리를 위해서는 settings.ini를 가져오는 부분에

분기처리를 해서 파일이름을 각자 가지고 해당 파일을 읽도록 해야할 것 같다.


### settings.ini


/etc/whatever/**settings.ini**
```
[database]
DATABASE_USER: bla
DATABASE_PASSWORD: XXXXXXXX
DATABASE_HOST: dev
DATABASE_PORT:
DATABASE_ENGINE: mysql
DATABASE_NAME: blo
TESTSUITE_DATABASE_NAME: test_blo

[secrets]
SECRET_KEY: random-string-of-ascii
CSRF_MIDDLEWARE_SECRET: random-string-of-ascii

[cookies]
SESSION_COOKIE_DOMAIN:

# all settings in debug section should be false in productive
environment
# INTERNAL_IPS should be empty in productive environment
[debug]
DEBUG: true
TEMPLATE_DEBUG: true
VIEW_TEST: true
INTERNAL_IPS: 127.0.0.1
SKIP_CSRF_MIDDLEWARE: true

[email]
SERVER_EMAIL: django@localhost
EMAIL_HOST: localhost

# the [error mail] and [404 mail] sections are special. Just add
lines with
#  full name: email_address@domain.xx
# each section must be present but may be empty.
[error mail]
Adam Smith: adam@localhost

[404 mail]
John Wayne: john@localhost
```

/path/to/whatever/**settings.py**
```
rom ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('/etc/whatever/settings.ini')

DATABASE_USER = config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST = config.get('database', 'DATABASE_HOST')
DATABASE_PORT = config.get('database', 'DATABASE_PORT')
```

### config.json 파일 생성
동일한 동작 방식으로 json 파일로 생성해서 읽어오는 방식은 아래 참고.

https://github.com/sally225/mywiki/blob/master/django/deploy/change_secret_key.md#22-config-%ED%8C%8C%EC%9D%BC%EC%97%90%EC%84%9C-secret_key-%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0


# Multiple setting files importing from each other
settings.py 파일의 맨 마지막에 아래 코드를 추가하여 
```
from setteings_local import *
```
settings.py에 있는 설정들을 settings_local의 설정으로 덮어쓰는 방식. 


/path/to/whatever/**settings.py**
```
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# why is this here?
#PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))


PROJECT_DIR = BASE_DIR

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Mr Sysadmin', 'sysadmin@domain.tld'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_DIR, 'project.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'en-us'
SECRET_KEY = 'secret'

#[more default and app wide settings]

from settings_local import *
```

/path/to/whatever/**settings_local.py**
```
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# don't want emails while developing
ADMINS = ()
MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'mydbname'
DATABASE_USER = 'mydbuser'
DATABASE_PASSWORD = 'mydbpassword'
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''

SECRET_KEY = 'random-string-of-ascii'

#[more user/machine specific settings]
```

settings.py는 버전관리에 포함되고

settings_local은 제외된다.

# Development/Machine Dependant Settings Configuration ¶
