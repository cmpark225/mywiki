Django and Apache로 배포하기

사용 버전
OS => ubuntu 16.04
Django => 1.3.7
apache => 2.4.18


1. wsgi 파일 생성

mysite/apache/django.wsgi
```
import os
import sys

path = '/home/user/data/workspace/mysite'
if path not in sys.path:
    sys.path.append(path)

os.envorion['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```

2. mod_wsgi 설치
```
sudo apt-get install libapache2-mod-wsgi
```
 
3. apache conf 파일 설정
```
<VirtualHost *:80>
    ServerName www.mysite.com
    DocumentRoot "/home/user/data/workspace/mysite"
    WSGIScriptAlias / /home/user/data/workspace/mysite/apache/django.wsgi

    <Directory /home/user/data/workspace/mysite>
        Require all granted
    </Directory>
</VirtualHost>
```

4. apache 재시작
