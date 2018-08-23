model의 TextField의 경우 admin site에서 관리할 경우 

textarea를 이용하기 때문에 일반 텍스트만 추가가 가능하다.

admin 페이지에서 TextField 편집시 에디터를 붙여

글을 편집 가능하게 하고 싶어 CKEditor를 추가 하였다.


# CKEditor 추가 

## 1. CKEditor 다운로드

https://ckeditor.com/ckeditor-4/download/

에서 다운로드 받아 압축을 풀어 static 경로에 저장한다.

settings.py
```
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

ckeditor 저장 위치
```
project/static$ ll
drwxrwxr-x  5 user     user 4096  8월  8 14:00 admin/
drwxrwxr-x 10 user     user 4096  8월 23 14:01 ckeditor/
```


## 2. Admin.py 수정
ckeditor를 textField에 적용하기 위해 admin.py를 수정한다.

polls/admin.py
```
from polls.modles import Poll
from django.contrib import admin
from django import forms
from django.db import models

class PollModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget':forms.Textarea(attrs={'class':'ckeditor'})},
    }

    class Media:
        js = ('ckeditor/ckeditor.js', )


admin.stie.register(Poll, PollModelAdmin)
```

**Admin 페이지에 접속하면 TextField 영역이 CKEditor로 변경된 것을 볼 수 있다.**



# Image upload

글 중간에 이미지를 넣기 위해 Image upload 기능을 추가하려고 한다.

Standard Package 버전에 Image upload 기능이 없어 추가함 (Full Package는 있는지 모르겠음)

## 1. ckeditor plugin download
Image upload를 위해 Image upload 플러그인을 다운 받았다.

https://ckeditor.com/cke4/addon/uploadimage

### 1.1. zip 파일을 ckeditor가 있는 plugin 폴더에 압축 해제한다.

```
/static/ckeditor/plugin/uploadimage
```

### 1.2. config.js에 plugin을 추가한다.
/stat/ckeditor/config.js
```
CKEDITOR.editorConfig = function( config ) {
...
    config.extraPlugins = 'uploadimage';
}
```

### 1.3. dependence 있는 plugin을 추가로 설치 한다.

uploadimage 플러그인 다운로드 시 다이얼로그가 뜨는데 맨 아래쪽에 Add-on dependencies 로 추가로 설치가 필요한 plugin 목록이 나온다.

해당 플러그인을 클릭해 설치해주면 된다. 플러그인 설치할때마다 나옴

추가 설치한 플러그인 목록
```
...
        config.extraPlugins = 'filetools';
        config.extraPlugins = 'clipboard';
        config.extraPlugins = 'widget';
        config.extraPlugins = 'notificationaggregator';
        config.extraPlugins = 'uploadwidget';
        config.extraPlugins = 'uploadimage';
        config.extraPlugins = 'notification';
...
```


## 2. Image Upload Path 추가
이미지 업로드 시 업로드 할 URL PATH를 config.js에 추가한다.

/static/ckeditor/config.js
```
CKEDITOR.editorConfig = function( config ) {
...


    config.filebrowserImageUploadUrl = 'upload/'
}
```
CKEditor에서 파일 업로드시 해당 url을 호출하게 된다.

현재 URL이 http://127.0.0.1/admin/polls/1 인 상태에서 

파일 업로드 시 http://127.0.0.1/admin/polls/1/upload/ 를 호출한다.


## 3. config.js 추가

config.js에 사용할 플러그인을 명시한 후

plugin 적용을 위해 admin.py에 config.js도 추가해준다.

polls/admin.py
 ```
 ...

 class PollModelAdmin(admin.ModelAdmin):
 ...
    class Media:
        js = ('ckeditor/ckeditor.js', 'ckeditor/config.js')

admin.site.register(Poll, PollModelAdmin)
 ```


여기까지 한 후 CKEDitor의 Image 버튼을 클릭하면 Upload 탭이 추가된 것을 확인할 수 있다.

근데 업로드 하면 CSRF 에러 남. ㅠㅠ

Forbidden (403)
CSRF verification failed. Request aborted.

