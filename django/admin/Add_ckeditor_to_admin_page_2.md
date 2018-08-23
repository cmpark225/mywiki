csrf 문제 해결을 위해 ckeditor-upload 모듈을 추가 시켜 upload url을 연결시켜주었다.


## 1. django-ckeditor 설치
```
$ pip install django-ckeditor
Collecting django-ckeditor
Requirement already satisfied: django-js-asset in /usr/local/lib/python2.7/dist-packages (from django-ckeditor) (1.1.0)
Installing collected packages: django-ckeditor
Successfully installed django-ckeditor-5.6.1

```

## 2. upload url 설정

project/urls.py
```
urlpatterns = patterns('',
...

    url(r'^', include('ckeditor_uploader.urls'))

)
```

## 3. config.js 확인

ckeditor_uploader 모듈의 url.py을 확인하면 

파일 업로드를 하기 위해서는 http://127.0.0.1/upload 로 호출해줘야 한다.

config.js 파일에 filebrowserImageUploadUrl에 경로가 제대로 적혀있는지 확인해봐야 한다.

/static/ckeditor/config.js
```
CKEDITOR.editorConfig = function (config ){
    ...

    config.filebrowserImageUploadUrl = '/upload'
}
```


###### Django 낮은 버전에서 사용.
Django 1.3.7버전에서 하려니 사용이 어려워 코드 수정 후 프로젝트에 추가시켜버렸다....
