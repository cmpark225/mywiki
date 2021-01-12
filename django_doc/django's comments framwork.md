# Django's comments framework

Django는 간단하지만 커스터마이징 가능한 comments 프레임워크를 포함한다. 내장된 comments 프레임워크는 어떤 모델에도 사용 가능하므로, blog entries, photos, book chapters 등 어떤 것에도 comments 를 사용할 수 있다. 

## Quick start guide

comments 앱을 사용하기 위해서는 아래 단계를 수행한다.:

1. INSTALLED_APPS에 'django.contrib.comments'를 추가하여 comments 프레임워크 설치.
2. manage.py syncdb 실행. Django가 comment 테이블 생성함.
3. urls.py에 comments 앱의 URL 추가
```
urlpatterns = patterns('', 
    ...
    (r'^comments/', include('django.contrib.comments.urls')),
)
```
4.아래의 comment 템플릿 태그를 사용하여 템플릿에 comment을 포함한다.

[comment 설정](https://django.readthedocs.io/en/1.3.X/ref/contrib/comments/settings.html)을 검토할 수도 있다. 

## Comment template tags
