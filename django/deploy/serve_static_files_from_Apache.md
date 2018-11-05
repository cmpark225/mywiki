django를 apache 서버와 연동 후에

프로젝트 admin 페이지를 들어가면 admin 관련 css파일들을 찾을 수 없어

404 Not Found 에러가 발생한다.

이때 static 파일을 apache에서 serving하도록 설정이 필요하다.


## 1. settings.py의 STATIC_ROOT 설정

settings.py
```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

 배포를 위해 collectstatic 명령어로 static file들이 수집되는 디렉토리 절대 경로.

 Example: "/home/example.com/static/"
 



## 2. collectstatic 커맨드 실행
```
$ python manage.py collectstatic
You have requested to collect static files at the destination
location as specified in your settings file.

This will overwrite existing files.
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Copying '/usr/local/lib/python2.7/dist-packages/django/contrib/admin/media/img/admin/nav-bg-grabber.gif'

...
```
STATIC_ROOT로 static파일들을 모은다

## 3. static 파일이 있는 디렉토리 apache conf로 설정
apache - default.conf
```
# Set static files
Alias /static/ /home/user/data/workspace/mysite/static/ #static 파일 경로
<Directory /home/user/data/workspace/mysite/static>
    order deny, allow
    Allow from all
</Directory>
```   

Alias /static/ /home/user/data/workspace/mysite/static/

=> /static/ 경로로 오는 요청을 /home/user/data/workspace/mysite/static/ 파일시스템 장소로 대응한다.(var/www 같이)

[Alias 지시어 관련 내용](https://httpd.apache.org/docs/2.4/ko/mod/mod_alias.html?#Alias)




