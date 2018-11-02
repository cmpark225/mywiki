# Class-based views
view는 요청을 받아 응답을 반환하는 호출 가능 객체다. 이것은 단순한 함수 이상의 것이 될 수 있으며 Django는 뷰로 사용할 수있는 몇 가지 클래스의 예제를 제공한다. 이를 통해 상속과 믹스를 이용하여 뷰를 구조화하고 코드를 재사용 할 수 있다. 나중에 간단히 할 일들에 대한 몇 가지 generic view가 있지만 유스 케이스에 맞는 재사용 뷰 구조를 직접 디자인 할 수도 있다. 자세한 내용은 클래스 기반 뷰 참조 문서를 참조해라.


## Basic examples
Django는 광범위한 애플리케이션에 적합한 기본 뷰 클래스를 제공한다. 모든 뷰는 URL에 뷰를 연결하고 HTTP 메소드를 디스패치 하는 등의 간단한 기능을 처리하는 iew class를 상속받는다. RedirectView는 간단한 HTTP redirect 기능을 하고, TemplateView는 template을 render하기 위해 base class를 확장한다.

## Simple usage in your URLconf
generic view를 사용하느 가장 간단한 방법은 URLconf에 직접 생성하는 것이다. 만약 class-based view에서 몇개의 간단한 속성만 변경하기 위해서는 간단하게 as_view() 호출로 전달하면 된다.:

```
from django.conf.urls import patterns
from django.views.generic import TemplateView

urlpatterns = patterns('', 
    (r'^about/', TemplateView.as_view(template_name="about.html")),
)
```
as_view()로 전달된 argument들은 class의 속성에 override 된다. 이 예에서는 TemplateView의 template_name을 설정한다. 비슷한 override 패턴은 RedirectView의 url 속성에 사용될 수 있다.


## Subclassing generic views
두 번째,보다 강력한 방법은 generic 뷰를 사용하여 기존 뷰를 상속하고 새 값이나 메소드를 제공하기 위해 하위 클래스의 속성 (예 : template_name) 또는 메소드 (예 : get_context_data)를 override하는 것이다. 
예를 들어 하나의 템플릿 about.html만 표시하는 view가 있다고 가정한다. Django는 이것을 하기 위한 generic 뷰를 가지고 있다(TemplateView). 그래서 서브 클래스를 만들고 템플릿 이름을 오버라이드 할 수 있다 :

```
# some_app/views.py
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "about.html"
```
그런 다음이 새로운 view를 URLconf에 추가하면 된다. TemplateView는 함수가 아닌 클래스이므로 클래스 기반의 뷰에 함수와 비슷한 엔트리를 제공하는 대신 as_view) 클래스 메소드를 가리킨다.

```
# urls.py
from django.conf.urls import patterns
from some_app.views import AboutView

urlpatterns = pattenrs('', 
    (r'^about/', AboutView.as_view()),
)
```
내장의 generic view 사용법에 대한 추가 정보는  generic class based views의 다음 topic을 참고해라.


### Supporting other HTTP methods
누군가가 뷰를 API로 사용하여 HTTP를 통해 우리의 book 라이브러리에 접근 한다고 가정한다. API 클라이언트는 매회 접속 한 후 마지막 방문 이후 발행된 도서 데이터를 다운로드 한다. 그런데 만약 새로운 책이 없다면 book을 데이터베이스에서 가져와 렌더링하고 클라이언트에게 보내는 것은 CPU와 bandwidth를 낭비하는 것이다. 더 나은 방식은 API에게 최신 book이 출간되었는지를 물어보는 것이다.

URLconf에서 도서 목록 보기로 URL을 매핑한다:
```
from django.conf.urls import patterns
from books.views import BookListView

urlpatterns = patterns('',
    (r'^books/$', BookListView.as_view()),
)
```

그리고 뷰에서는:
```
from django.http import HttpResponse
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView)
    model = Book

    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse('')
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

```

만약 뷰가 GET 요청을 받으면 plain-and-simple 오브젝트 리스트가 반환된다.(book_list.html 템플릿 사용) 그러나 클라이언트가 HEAD 요청을 하면 응답에 빈 body가 생기고 Last-Modified 헤더는 가장 최근의 책이 언제 발행되었는지를 나타낸다. 이 정보를 바탕으로 클라이언트는 전체 object list를 다운로드 여부를 정할 수 있다.
