## Simple usage
클래스 기반인 generic views는 두가지 방법으로 사용할 수 있다.
1. **subclassing**

속성이나(ex:template_name), 메소드(ex:get_context_data) 오버라이드 가능 


TemplateView 상속 받아서 template_name속성 오버라이드 함

```
# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```

그 후 URLconf에 뷰 추가. 클래스 기반의 뷰는 클래스이기 때문에 as_view 메서드로 작성한다. as_views가 뷰 진입점이다?

```
# urls.py
from django.conf.urls.default improt *
from some_app.views import AboutView

urlpatterns = patterns('', 
    (r'^about/', AboutView.as_view()),
)
```

2. **URLconf에서 직접 argument로 전달.**

```
from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    (r'^about/', TemplateView.as_view(template_name="about.html")),
)
```

## Generic views of objects
TemplateViews도 유용하지만 generic views는 database의 data를 보여줄때 유용하다. 
Django에는 객체의 리스트 뷰와 디테일 뷰를 매우 쉽게 생성 할 수 있도록하는 내장 뷰가 내장되어 있다.


앞으로 예제에서 아래 모델 사용할거임.


books/models.py
```
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]
    
    def __unicode__(self):
        return self.name

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher)
    publication_date = models.DateField()

```

모든 publisher의 리스트 페이지를 빌드하기 위해서 아래 URLConf를 사용한다.

url.py
```
from django.conf.urls.defaults import *
from django.views.generic import ListView
from books.models import Publisher

urlpatterns = patterns('',
    (r'^publishers/$', ListView.as_view(
        model=Publisher,
    )),
)
```
템플릿 작성을 위해 template_name을 argument로 넘길 수 있지만 Django가 object 이름으로 template 이름을 추측할 수 있다. 위 경우 "book/publisher_list.html" book은 모델이 정의된 app에서 가져오고, publisher는 모델 이름의 소문자 버전이다.

모든 publisher 오브젝트를 포함한 object_list변수가 포함된 컨텍스트에 따라 렌더링 된다.

publisher_list.html
```
{% extends "base.html" %}

{% block content %}
    <h2>Publishers</h2>
    <ul>
        {% for publisher in object_list %}
            <li>{{ publisher.name }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```


## Extending generic views
많은 양의 configuration을 URLconf로 전달하는 것 대신, generic views를 subclass로 상속하고 attributes나 method를 override 하는 것을 추천한다.


### Making "friendly" template context
위 publisher_list.html variable name을 object_list로 사용하고 있었는데, 이는 template author에게 친절하지 않다.

generic view에 context_object_name 속성을 지정하여 변경할 수 있다.

url.py
```
urlpatterns = patterns('',
    (r'^publishers/$', ListView.as_view(
        model=Publisher,
        context_object_name="publisher_list",
    )),
)
```

### Adding extra context
추가 정보 제공이 필요할 수 있다. 예를들어 각 publisher Detail 페이지에서 book 리스트를 보여준다던지.. DetailView는 publisher를 컨텍스트에 제공하지만 해당 템플릿에서 추가 정보를 가져올 수 있는 방법이 없는 것 같다.

그러나 DetailView를 subclass로 get_context_data 메소드를 직접 구현할 수 있다. DetailView와 함께 제공되는 기본 구현에서 표시되는 개체를 템플릿에 추가하기만 하면 된다.

```
from django.views.generic import DetailView
from books.models import Publisher, Book

class PublisherDetailView(DetailView):

    context_object_name = "publisher"
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublisherDetailView, self).get_context_data(**kwargs)
        
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()

        return context
```
template에 전달될 context에 'book_list' 정보를 추가함. Template에서 book_list를 통해 추가 정보를 보여줄 수 있다.

### Viewing subsets of objects

뷰가 처리 할 데이터베이스 모델을 지정하는 *model* 인수는 단일 개체 또는 개체 컬렉션에서 작동하는 모든 generic 뷰에서 사용할 수 있다. 그러나 *model* argument 뿐 아니라 *queryset* argument를 이용해 object의 리스트를 명시할 수 있다.

```
from django.views.generic import DetailView
from books.models import Publisher, Book

class PublisherDetailView(DetailView):

    context_object_name = "publisher"
    queryset = Publisher.objects.all()
```

model=Publisher 는 queryset = Publisher.objects.all()의 축약한 것이다.
queryset을 이용하면 object의 필터된 리스트를 사용할 수 있다.


예를들어 publication_date를 기준으로 order된 리스트를 받고 싶을 경우
```
urlpatterns = patterns('',
    (r'^publishers/$', ListView.as_view(
        queryset=Publisher.objects.all(),
        context_object_name="publisher_list",
    )),
    (r'^books/$', ListView.as_view(
        queryset=Book.objects.order_by("-publication_date"),
        context_object_name="book_list",
    )),
)
```

URLconf에서 argument로 전달하는 대신 서브클래스로 사용할수도 있다.

```
from django.views.generic import ListView
from books.models import Book

class AcmeBookListView(ListView):

    context_object_name = "book_list"
    queryset = Book.objects.filter(publisher__name="Acme Publishing")
    template_name = "books/acme_list.html"
```

### Dynamic filtering

또 다른 일반적인 필요는 목록 페이지에 주어진 객체를 URL의 일부 키로 필터링하는 것이다. 이전에 RULConf에서 publisher 이름으로 하드코딩했는데, 만약 임의의 publisher의 책을 보여주고 싶으면?

ListView는 get_queryset()메소드를 가지고 있고 우리는 메소드를 오버라이드 할수 있다. 이전에 queryset 속성을 return 했지만 이제는 logic을 추가할 수 있다.

이 작업을 수행하는 핵심 부분은 클래스 기반 뷰가 호출 될 때 다양한 유용한 것들이 자체에 저장된다는 것이다. request (self.request)뿐만 아니라 URLconf에 따라 캡처 된 위치 (self.args) 및 이름 기반 (self.kwargs) 인수가 포함된다.

하나의 캡쳐된 그룹을 가지는 URLConf가 있다. 
```
from books.views import PublisherBookListView

urlpatterns = patterns('',
    (r'^books/(\w+)/$', PublisherBookListView.as_view()),
)
```

view.py
```
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from book.models import Book, Publisher

class PublisherBookListView(ListView):
    context_object_name = 'book_list'
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return Book.objects.filter(pubplisher=publisher)
```

queryset에 더 많은 로직을 추가하는 것은 매우 쉽다. 필요하면 self.request.user를 사용하여 현재 사용자 또는 다른 복잡한 logic를 사용하여 필터링 할 수 있다.

동시에 publisher를 context에 추가하여 템플릿에서 사용하는 것도 가능하다.

```
class PublisherBookListView(ListView):
    context_object_name = "book_list"
    template_name = "books/books_by_publisher.html"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PublihserBookListView, self).get_context_data(**kwargs)
        context['publisher'] = self.publisher
        return context 
```


## Performing extra work

마지막 일반적인 패턴은 generic view를 호출하기 전이나 후에 몇 가지 추가 작업을 하는 것이다.

author를 마지막으로 본 사람을 추적하기 위한 last_accessed field가 Author 오브젝트에 있다고 가정한다.

```
# models.py

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    headshot = model.ImageField(upload_to='/tmp')
    last_accessed = models.DateTimeField()
```
물론 geneeric DetailView 클래스는 이 필드에 대해 아무것도 알지 못하지만 다시 한 번 해당 필드를 업데이트하는 custom view를 작성할 수 있다.

우선 URLconf에 author 세부 사항 비트를 추가하여 custom view를 가리킨다.

```
from books.views import AuthorDetailView

urlpatterns = patterns('', 
#...
    (r'^authors/(?<pk>\)/$', AuthorDetailView.as_view()),
)
```

 그리고 새로운 view를 작성한다. get_object는 객체를 retrieve 하는 메소드이다. 따라서 간단히 오버라이드하고 호출을 래핑합니다.


```
import datetime
from books.models import Author
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

class AuthorDetailView(DetailView):

    queryset = Author.objects.all()

    def get_object(self):
        # Call the superclass
        object = super(AuthorDetailView, self).get_object()

        #Record the last accessed date
        object.last_accessed = datetime.datetime.now()
        object.save()

        # Rerurn the object
        retrun object
```

## More than just HTML
각 generic views는 mixins의 시리즈로 구성되어 있다 그리고 각 mixin은 전체 view의 작은 부분에 기여한다.

이 중 일부인 mixin은 (ex:TemplateResponseMixin) 템플릿을 사용하여 컨텐츠를 HTML 응답에 렌더링 하기 위해 설계되어있다. 그러나 다른 렌더링 동작을 하는 자신만의 mixin을 작성할 수 있다.

예를 들어 simple JSON mixin:
```
from django import http
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)
```
그러고 나면 JSONResponseMixin과 BaseDetailView(template 렌더링과 mix하기 전  DetailView)를 합쳐 JSON을 리턴하는 DetailView를 만들 수 있다.

```
class JSONDeetailView(JSONResponseMixin, BaseDetailView):
    pass
```
이 view는 다른 DetailView와 동일한 방식으로 사용 될 수 있으며 response의 형식을 제외하고는 동일하게 동작한다.


query argument나 HTTP header 와 같은 Http request의 속성에 맞게 HTML과 JSON 둘다 봔한할 수 있는 DetailVeiw 하위클래스를 만들 수 있다. 그냥  JSONResponseMixin과 SingleObjectTemplateResponseMixin을 합치면 된다. 그리고 render_to_response()를 오버라이드 해서 사용자가 원하는 응답 요청에 따라 구현하면 된다.

```
class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)
```
파이썬이 메소드 오버로딩을 해결하는 방식 때문에 로컬 render_to_response () 구현은 JSONResponseMixin 및 SingleObjectTemplateResponseMixin에서 제공하는 버전보다 우선으로 취한다.

## Decorating class-based views
 
 클래스 기반 view는 mixins을 사용하는데 제한되지 않는다. decorator도 사용 가능.

 ### Decorating in URLconf
 간단한 방법은 as_views() 메소드의 결과에 데코레이트 하는 것이다. 이 작업을 수행하는 가장 쉬운 방법은 view를 배포하는 URLconf에 있다.

 ```
 from django.contrib.auth.decorators import login_required, permission_required
 from django.views.generic import TemplateView

 from .views import VoteView

 urlpatterns = patterns('',
    (r'^about/', login_required(TemplateView.as_view(template_name="secret.html"))),
    (r'^vote/', permission_required('polls.can_vote')(VoteView.as_view())),
 )
 ```
 이 접근 방식은 인스턴스별로 데코레이터를 적용한다. view의 모든 인스턴스를 decorate 하려면 다른 접근 방식으로 접근해야 한다.

 ### Decorating the class

클래스 기반의 view의 모든 인스턴스에 decorate 하려면 class 정의에 직접 decorate 해야 한다. 이를 위해 decorater를 dispatch()메소드에 적용한다.

클래스 메소드는 독립형 함수와 같지 않으므로 함수 데코레이터를 메소드에 적용 할 수는 없다. 메소드 데코레이터로 변환이 필요하다.

method_decorator 데코레이터는 함수 데코레이터를 메소드 데코레이터로 변환하여 인스턴스 메소드에서 사용 할 수 있도록 한다.

```
from django.contrib.auth.decorators import logrin_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
    template_name = "secret.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedVeiw, self).dispatch(*args, **kwargs)
```
