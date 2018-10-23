### Writing action functions
먼저 관리자가 작업을 트리거 할 때 호출되는 함수를 작성해야 한다. 액션 함수는 세 개의 인수를 취하는 일반 함수이다.
* 현재 ModelAdmin
* 현재 요청인 HttpRequest
* 선택된 object의 select를 포함하는 QuerySet

publish-these-articles 함수는 ModelAdmin이나 request객체를 필요로 하지 않고, queryset을 사용한다.
```
def make_published(modeladmin, request, queryset):
    queryset.update(status='p') 
```

> 최고 성능을 위해 queryset의 update 메소드를 사용한다. 다른 유형의 작업은 각 개체를 개별적으로 처리해야 할 수 있는데, 이 경우 쿼리셋에서 반복하면 된다.
``` 
for obj in queryset:
    do_something_with(obj)
```
실제로 액션을 작성하는 것이 전부다. 그러나 선택형이지만 유용한 단계를 하나 더 취하여 관리자에게 "nice" title을 제공한다. 기본적으로 이 작업은 작업 목록에 "Make published"로 표시된다. - 밑줄을 공백으로 변환한 함수 이름. 
이것도 괜찮지만 좀 더 나은 것을 제공할 수 있다, make_publised 함수에 short_description 속성을 줌으로 가독성을 높일 수 있다.

```
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected sotries as published"
```

### Adding actions to the ModelAdmin
다음으로 ModelAdmin에 action을 알려야한다. 이 작업은 다른 옵션 설정과 같다. 그래서 액션 등록에 대한 완전한 admin.py는 다음과 같다.:

```
from django.contrib import admin
from myapp.models import Article

def make_published(modeladmin, request, queryest):
    queryest.update(status='p')
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display=['title', 'status']
    ordering = ['title']
    actions = [make_published]

admin.site.register(Article, ArticleAdmin)
```
이 코드는 아래와 같이 보이는 관리자 변경 리스트를 제공한다.
이것이 전부다. 만약 자신의 행동을 쓰고 싶어할 경우 시작할 만큼은 충분히 알고 있다, 이 문서의 나머지 부분에서는 고급 기술만 다룬다. 


## Advanced action techniques
몇 가지 추가 옵션과 고급 옵션을 활용할 수 있다.

### Action as ModelAdmin methods
위 예는 간단한 함수를 정의하여 make_published action을 보여준다. 이것도 좋지만 view의 코드 디자인쪽으로는 완벽하지는 않다.: 액션은 Article 객체와 밀접하게 연결되어 있기 때문에 액션을 ArticleAdmin 객체 자체에 연결하는 것이 좋다.

```
calss ArticlaAdmin(admin.ModelAdmin):
    ...
    
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryest.update(status='p')
    make_published.short_descirption = "Mark selected stories as published"
```
먼저 make_published가 메소드로 이동했고 modeladmin 파라메터가 self로 이름이 변경되었다. 그리고 두번째로 직접 함수 참조가 아니라 action에 'make_published' 문자열을 넣었다. 이것은 ModelAdmin에게 action을 메소드로 검색하도록 지시한다.

action을 메소드로 정의하면 ModelAdmin 자체에 더 간단하고 관용적인 엑세스로 만들 수 있으므로 관리자가 제공한 메소드를 호출할 수 있다.

예를 들어, 사용자에게 action이 성공적이였다고 알리기 위해 메시지를 줄 수 있다. : 
```
class ArticleAdmin(admin.ModelAdmin):
    ...
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were " % rows_updated
        self.message_upser(request, "%s successfully marked as published." % message_bit)
```

이렇게 하면 작업을 성공적으로 수행 한 후 관리자 자체가 수행하는 작업과 일치하게된다.

### Actions that provide intermediate pages
기본적으로, action 후에 원래의 change list page로 돌아가는 리디렉션이 수행된다. 그러나 몇몇의 동작은 특히 복잡한 작업은 중개 페이지를 반환해야할 경우도 있다. 예를들어 delete action은 선택된 objects를 삭제 하기 확인을 요청해야한다.

중개 페이지를 제공하기 위해 그냥 action에서 HttpResponse를 반환하면 된다. 예를들어 Django의 serialization 함수를 사용해서 선택된 objects들을 JSON으로 덤프하는 함수를 작성할 수 있다.:
```
from django.http import HttpResponse
from django.core import Serializers

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(mimetype="text/javascript")
    serializers.serialize("json", queryset, stream=response)
    return response
```
위 예는 좋은 생각처럼 보이지는 않는다. 가장 좋은 것은 HttpResponseRedirect를 리턴하고 사용자가 작성한 view로 리디렉션하여 GET 쿼리 문자열에 선택한 개체 목록을 전달하는 것이다. 이를 통해 중개 페이지에 복잡한 상호 작용 로직을 제공 할 수 있다. 예를 들어 보다 완전한 export 함수을 제공하려는 경우 사용자가 형식을 선택 하게 하고 가능하면 export에 포함 할 필드 목록을 선택하게 할 수 있다. 가장 좋은 방법은 사용자 정의 export view로 리디렉션하는 작은 작업을 작성하는 것이다.:
```
from django.contrib import admin
form django.contrib.contenttypes.models import ContentType

from django.http import HttpResponseRedirect

def export_selected_objects(modeladmin, request, queryest):
    selected = request.POST.getliist(admin.Action_CHECKBOX_NAME)
    ct = ContentType.objects.get_for_model(queryset.model)
    return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
```

보이는 것 처럼 action은 매우 간단한 부분이다; 모든 복잡한 로직은 export view에있다. 이는 모든 유형의 객체를 처리해야하므로 ContentType을 가진 비즈니스다.

view 작성은 독자가....

### Making actions available site-wide
**AdminSite.add_action(action[, name])**
일부 action은 관리 사이트의 모든 개체에서 사용할 수 있는 경우에 가장 적합한 경우가 있다 --위에 정의 된 내보내기 작업이 좋은 예가 될 수 있음. AdminSite.add_action()을 사용하여 전역으로 사용할 수 있는 action을 만들 수 있다. EX:
```
from django.contrib import admin

admin.site.add_action(export_selected_objects)
```

이것은 액션 이름이 "export_selected_objects"인 export_selected_object action을 전역적으로 사용 가능하게 해준다. AdminSite.add_action()에 두 번째 인수를 전달하여 action 이름을 지정할 수 있다. -- 나중에 action을 제거하기에 좋다.

```
admin.site.add_action(export_selected_objects, 'export_selected')
```



### Disabling actions
가끔 특정 object에서 action을 disable 처리해야할 때가 있다.-- 특히 전역적으로 등록되었을 경우. 여기에 action을 disable 할 수 있는 몇가지 방법이 있다.

#### Disabling a site-wide action
**AdminSite.disable_action(name)**
전역 action 을 제거하고 싶을 경우 AdminSite.disable_aciton()을 호출할 수 있다.
예를들어, 내장되어 있는 "delete selected object" action을 지우고 싶을 경우 이 method를 사용할 수 있다.:
```
admin.site.disable_action('delete_selected')
```
위 작업 후에는 이 action은 더이상 전역적으로 사용할 수 없다.

만약 한개의 특정 모델에서 전역적으로 disabled된 action을 다시 사용하고 싶을 경우, ModelAdmin.action 리스트에 작성하면 된다.:
```
# Globally disable delete selected
admin.site.disable_action('delete_selected')

# This ModelAdmin will not have delete_selected available
class SomModelAdmin(admin.ModelAdmin):
    actions = ['some_other_action']
    ...

# This one will
class AnotherModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected', 'a_third_action']
```

#### disabling all action for a particular ModelAdmin

주어진 ModelAdmin에 대해 일괄 처리를 사용하지 않으려면 ModelAdmin.actions를 None으로 설정하기만하면 된다.:
```
class MyModelAdmin(admin.ModelAdmin):
    actions = None
```
전역 action을 포함한 어떤 action도 허용하지 않고, 표시하지 않는다.

### Conditionally enabling or disabling actions
**ModelAdmin.get_actions(request)**
ModelAdmin.get_actions()를 오버라이드해서 request별로 action 을 사용할지 안할지 선택할 수 있다.

이 함수는 허용된 action의 dictionary를 리턴한다. 키는 action 이름이고, value는 (function, name, short_description) 튜플이다.

대부분이 메서드를 사용하여 수퍼 클래스에서 수집 한 목록에서 조건부로 작업을 제거한다. 예를 들어 이름이 'J'로 시작하는 사용자만 object를 ​​대량으로 삭제할 수 있게 하려면 다음을 수행 할 수 있다.:
```
class MyModelAdmin(admin.ModelAdmin):
    ...

    def get_actions(self, reqeuest):
        actions = super(MyModelAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            del actions['delete_selected']
        return actions
```
