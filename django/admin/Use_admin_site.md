# Admin site 사용

1. settings.py의 INSTALLED_APPS에 'django.contrib.admin' 추가
2. DB 테이블 생성을 위해 python manage.py syncdb 명령어 실행. 
3. urls.py에 admin 사용을 위한 주소 && admin.autodiscover() 추가
   
urls.py
```
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

```

## 모델 수정 가능하도록 admin site에 추가.
현재 mysite 폴더 구조가 아래와 같을 때

polls app의 Poll 모델을 admin site 인터페이스에 추가하려고 한다.

```
├── manage.py
├── myproject
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── polls
│   ├── __init__.py
│   ├── models.py
│   ├── views.py

```

polls app에 admin.py 파일을 만들고 아래과 같이 Poll 모델을 추가한다.

polls/admin.py
```
from polls.models import Poll
from django.contrib import admin

admin.site.register(Poll)
```

서버 재시작하면 Poll추가된 것을 확인할 수 있다.
(일반적으로 코드가 수정되면 서버가 재시작 되지만, 파일 추가에는 재시작 안된다.)

## Customize the admin form

### re-ordering the fields
admin site의 add 페이지나 edit페이지의 Fields 위치를 아래 코드로 조정할 수 있다. 

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question']

admin.site.register(Poll, PollAdmin)
```

model admin object 생성 후 register의 두번째 argument로 전달하면 된다.

### split the form up into fieldsets
field 분리 하기.  model admin object에 fieldsets 정의해준다.

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question']}),
        ('Date information', {'fields':['pub_date']}),
    ]

admin.site.register(Poll, PollAdmin)
``` 

fieldsets의 각 튜플의 첫번째 엘리먼트는 fieldset의 타이틀이다.

None일 경우에는 타이틀을 제외 시킨다.

그리고 각 fieldset에 HTML class를 아래와 같이 설정할 수 있다.

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question']}),
        ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
    ]
```
Django에서 'collapse'클래스를 제공하는데 pub_date 필드에 collapse 클래스를 추가해 처음에는 해당 필드가 Hide된 상태로 출력되도록 했다. 


## Adding related objects

현재 Poll 모델은 여러개의 Choices를 가지고 있는데, Poll admin page에는 Choice는 표시되고 있지 않다.

Choice를 표시하기 위해 두가지 방법이 있다.

1. Poll 처럼 Choice 를 등록 시킨다.
polls/admin.py
```
from polls.models import Choice

admin.site.register(Choice)
```
이제 Choice admin page에서 "Poll" field의 select box를 이용해 database에 있는 모든 poll을 선택할 수 있다.

2. Poll admin에 Choice를 Inline으로 추가

Choice amdin page에서 Poll을 선택해 하나씩 추가하는 것 보다. 

Poll object 생성 시 Choice를 직접 추가하는 것이 더 효율 적이다.

choice 를 registoer()를 지우고 아래와 같이 수정한다.

polls/admin.py
```
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['question']}),
        ('Date information', {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
```
위 코드는 Choice object를 Poll admin page에서 수정하고, fields를 3개를 기본적으로 가지는 것을 의미한다.

만약 Choice의 각 필드 입력이 공간을 많이 차지할 경우

admin.StackedInline 대신  admin.TabularInline을 사용하면 된다.

polls/admin.py
```
class ChoiceInline(admin.TabularInline)
```

## Customize the admin change list
"change list" page 수정

기본적으로 Django는 각 object의 str()을 표시한다. 하지만 가끔 각 필드를 표시하는 것이 좀 더 유용할 수 있다. 이럴때 list_display admin option을 사용한다. list_display는 change list page 에서 컬럼으로 보여줄 field를 튜플로 가진다.

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    # ...
    list_display = ('quesion', 'pub_date')
```

model의 method도 list_display에 포함시킬 수 있다.

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    # ...
    list_display = ('quesion', 'pub_date', 'was_published_today')
```
컬럼 헤더를 누르면 sort가 가능한데, method의 경우 지원하지 않는다.

그리고 Was published today의 경우 기본적으로 컬럼명을 method 이름으로 하고 있지만 models.py 에서 short_description attribute로 헤더 이름 변경 할 수 있다.

polls/models.py
```
class Poll(models.Model):
    # ...
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = "Published today?"
```

admin.py에 list_filter를 아래 처럼 추가하면 "Filter"가 sidebar가 추가 되서 pub_date로 필터링할 수 있다.

polls/admin.py
```
class PollAdmin(admin.ModelAdmin):
    # ...
    list_display = ('question', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
```
표시되는 필터의 유형은 필터링중인 필드 유형에 따라 다fmek. pub_date는 DateTimeField이므로 Django는 DateTimeFields에 대한 기본 필터 옵션 인 "Any date," "Today," "Past 7 days," "This month," "This year."를 제공 한다.


search type 추가
```
search_fields = ['question']
```

날짜 별 drill down 아래 코드 추가 시 페이지 맨 위에 pub_date의 최상위인 연도가 표시된다.

```
date_hierarchy = 'pub_date'
```

페이징은 기본적으로 50개 표시로 제공된다. 

