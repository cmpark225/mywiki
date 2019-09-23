
## ModelAdmin objects

class **ModelAdmin**

ModelAdmin 클래스는 관리자 인터페이스에서 모델을 나타낸다. 어플리케이션에 admin.py 파일로 저장된다. ModelAdmin의 간단한 예제를 보자:

```
from django.contrib import admin
from myproject.myapp.models import Author

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Author, AuthorAdmin)
```


> Do you need a ModelAdmin object at all?
> 이전의 예제에서, ModelAdmin 클래스는 어떤 커스텀 값을 가지지 않는다(아직). 결과적으로 기본 관리자 인터페이스가 제공된다. 기본 관리자 인터페이스가 괜찮다면, ModelAdmin을 정의하지 않아도 된다. -- ModelAdmin 설명을 제공하지 않고 모델 클래스를 등록 할 수 있다. 앞의 예를 다음과 같이 단순화 할 수 있다.

```
from django.contrib import admin
from myproject.myapp.models import Author

admin.site.register(Author)
```


### ModelAdmin options

ModelAdmin은 매우 유연하다. 인터페이스를 다루기 위한 몇가지 옵션이 있다. 모든 옵션은 ModelAdmin의 하위 클래스에서 정의된다. 

```
class AuthorAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
```

**ModelAdmin.exclude**

이 속성이 제공될 경우, form에서 제외되어야 할 필드이름의 리스트여야 한다.

예를들어 아래 모델에 대해서:
```
class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3)
    birth_date = models.DateField(blank=True, null=True)
```

name과 title 필드만을 포함하는 Author 모델의 form을 원할경우, fields나 exclude를 아래와 같이 작성할 수 있다:
```
class AuthorAdmin(admin.modelAdmin):
    fields = ('name', 'title')

class AuthorAdmin(admin.ModelAdmin):
    exclude = ('birth_date', )
```
모델읃 name, title, birth_date 세개의 필드만 가지고 있으므로, 위에 선언된 form 결과는 같은 필드를 가질 것이다.

**ModelAdmin.list_display**

admin의 change list 페이지에서 표시되는 필드들을 컨트롤하기 위해 list_display를 설정한다. 

EX:
```
list_display = ('first_name', 'last_name')
```
만약 list_display를 설정하지 않았을 경우 admin 사이트는 각 오브젝트의 __unicode__() 값을 컬럼 한개로 표시할 것이다.

list_display에서 사용할 수 있는 네가지 값(방법)이 있다.
* 모델의 필드명. 예:
```
class PersonAdmin(admin.ModelAdmin):
  list_display = ('first_name', 'last_name')
```
*  모델 인스턴스에 대해 하나의 매개 변수를 허용하는 호출 가능 객체. 예:
```
def upper_case_name(obj):
  return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = "Name"

class PersonAdmin(admin.ModelAdmin):
  list_display = (upper_case_name, )
```
* 문자열은 ModelAdmin의 속성을 표시한다. callable과 동일하게 동작한다 예:
```
class PersonAdmin(admin.ModelAdmin):
  list_display = ('upper_case_name', )

  def upper_case_name(self, obj):
  return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = "Name"
```
* 모델의 속성을 나타내는 문자열이다. 이 함수는 호출 가능 함수와 거의 동일하게 동작하지만이 컨텍스트에서는 모델 인스턴스를 가리킨다. 아래는 완전한 모델 예제이다.
```
class Person(models.Model):
  name = models.CharField(max_length=50)
  birthday = models.DateField()

  def decade_born_in(self):
    return self.birthday.strftime("%Y")[:3] + "0's"
  decate_born_in.short_description = "Birth decade"

class PersonAdmin(admin.ModelAdmin):
  list_display = ('name', 'decade_born_in')
```

list_display에 대해 몇가지 특별한 경우가 있다:

* 만약 필드가 ForeignKey 라면 Django는 관련된 오브젝트의 __unicode()__ 를 보여준다. 
  
* ManyToManyField 필드는 지원하지 않는다. 이는 테이블의 각 행에 대해 별도의 SQL 문을 실행해야 하기 때문이다. 그래도 해당 필드를 사용하고 싶다면. 모델에 사용자 정의 메소드를 추가하여 해당 메소드 이름을 list_display에 추가한다.(list_display의 커스텀 메소드는 아래 참조)
  
* 필드가 BooleanField 이거나 NullBooleanField일 경우 Django는 True, False 대신 'on', 'off' 아이콘을 표시한다.
  
* 모델의 메소드나 ModelAdmin의 호출가능한 메소드가 문자열로 주어지면, Django는 기본적으로 HTML-escape으로 출력한다. 메소드의 결과를 벗어나지 않으려면 이 메소드에 값이 True인 allow_tags 속성을 제공한다.
완전한 모델 예제:
```
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=6)

    def colored_name(self):
        return '<span style="color: #%s;">%s %s</span>' % (self.color_code, self.first_name, self.last_name)
    colored_name.allow_tags = True

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'colored_name')
```
* 만약 주어진 문자열이 True나 False를 반환하는 모델의 메소드나 ModelAdmin의 호출가능한 메소드일 경우 Django는 "on", "off" 아이콘을 표시한다. 만약 메소드의 boolean속성에 True를 설정했을 경우에.
  
EX: 
```
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    birthday = models.DateField()

    def born_in_fifties(self):
        return self.birthday.strftime('%Y')[:3] == '195'
    born_in_fifties.boolean = True

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'born_in_fifties')
```

* __str __ () 및 __unicode __ () 메서드는 list_display에서 다른 모델 메서드와 마찬가지로 유효하므로이 작업을 수행해도 된다.:
```
list_display = ('__unicode__', 'some_other_field')
```

* 일반적으로 실제 데이터베이스 필드가 아닌 list_display 요소는 정렬에 사용할 수 없다.(Django는 데이터베이스 수준에서 모든 정렬을 수행하기 때문에)

그러나 list_display의 요소가 특정 데이터베이스 필드를 나타내는 경우 항목의 admin_order_field 특성을 설정하여 이 사실을 나타낼 수 있습니다.

EX:
```
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=6)

    def colored_first_name(self):
        return '<span style="color: #%s;">%s</span>' % (self.color_code, self.first_name)
    colored_first_name.allow_tags = True
    colored_first_name.admin_order_field = 'first_name'

class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'colored_first_name')
```
위의 코드는 Django가 관리자의 color_first_name으로 정렬 할 때 first_name 필드로 정렬하도록 지시한다.

## Overriding admin templates
admin 모듈이 admin 사이트의 다양한 페이지를 생성하는 데 사용하는 많은 템플릿을 비교적 쉽게 재정의할 수 있다.특정 앱 또는 특정 모델에 대해 템플릿 중 일부를 재정의할 수도 있다.

### Set up your projects admin template directories

admin 템플릿 파일은 contrib/admin/templates/admin 폴더에 있다.

템플렛을 override 하기 위해서는 우선 프로젝트의 템플릿 디렉토리에 admin 디렉토리를 생성해야한다. TEMPLATE_DIRS에 명시되어 있는 어느 디렉토리라도 괜찮다.

이 admin 디렉토리 안에 앱 이름을 가진 서브디렉토리를 만든다. 그리고 나서 모델의 이름을 가진 서브디렉토리를 만든다. admin앱은 디렉토리를 찾을 때 모델 이름을 소문자로 찾는다. 따라서 대소문자를 구분하는 파일 시스템에서 앱을 실행하려면 모두 소문자로 디렉토리 이름을 지정해야 한다.

특정 앱의 admin 템플릿을 override 하기 위해 django/contrib/admin/temlates/admin 디렉토리에서 템플릿을 복사하고 수정한다. 그리고 만들었던 디렉토리 중 하나에 저장한다.

예를들어, 앱 이름이 my_app에서 모든 모델의 수정사항을 볼 수 있는 tool을 추가하고 싶을 경우, contrib/admin/temlates/admin/change_list.html을 우리 프로젝트의 templates/admin/my_app 디렉토리에 에 복사할 것이다, 그리고 필요한 변경을 할 수 있다.

만약 'Page'이름을 가진 모델에만 변경사항 리스트 tool을 추가하고 싶다면, 위와 동일한 파일을 프로젝트의 templates/admin/my_app/page 디렉토리에 복사할 것이다.

### Overriding vs. replacing an admin template
admin 템플릿의 모듈 식 설계로 인해 일반적으로 전체 템플릿을 대체 할 필요가 없으며 권장되지 않는다. 변경이 필요한 템플릿의 섹션만 대체하는 것이 좋다.

위 예제에서 계속해서 Page모델의 History tool옆에 새로운 링크를 추가하려면. change_form.html을 보고 object-tools 블록을 override 하기만 하면 된다. 우리의 새로운 change_form.html이다.:
```
{%{% extends "admin/change_form.html" %}
{% load i18n %}
{% block object-tools %}
{% if change %}{% if not is_popup %}
  <ul class="object-tools">
    <li><a href="history/" class="historylink">{% trans "History" %}</a></li>
    <li><a href="mylink/" class="historylink">My Link</a></li>
    {% if has_absolute_url %}
        <li><a href="../../../r/{{ content_type_id }}/{{ object_id }}/" class="viewsitelink">
            {% trans "View on site" %}</a>
        </li>
    {% endif%}
  </ul>
{% endif %}{% endif %}
{% endblock %}
```
만약 이 파일을 templates/admin/my_app 디렉토리에 위치시킨다면 모든 모델의 change form에 new link가 보일 것이다.

### Tempaltes which may be overridden per app or model

contrib/admin/templates/admin의 모든 템플릿이 앱마다 또는 모델마다 override할수 있는 것은 아니다. 아래 목록만 override가 가능하다.
* app_index.html
* change_form.html
* change_list.html
* delete_confirmation.html
* object_history.html

이런식으로 override 할 수 없는 템플릿의 경우 전체 프로젝트에 대해 override할 수 있다. 새로운 파일을 templates/admin 디렉토리에 위치시키면 된다. 이 기능은 맞춤 404 및 500 페이지를 만드는 데 특히 유용하다.

>change_list_request.html과 같은 일부 관리 템플릿은 사용자 정의 포함 태그를 렌더링하는 데 사용된다. 이것들은 override 될지도 모르지만 그런 경우에는 문제의 태그에 대한 새로운 버전을 만들고 다른 이름을 주는 것이 더 나을 것이다. 그렇게 하면 선택적으로 사용할 수 있다.
