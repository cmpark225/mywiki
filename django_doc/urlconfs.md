## How Django processes a request

django site page에 request를 보낼때 시스템이 어떤 파이썬 코드를 실행할지 결정하는  알고리즘이다. 

1. Django는 사용하기 위한 root URLconf 모듈을 결정한다. 일반적으로 이 값은 ROOT_URLCONF setting의 값이지만, HTTPRequest 오브젝트가 urlconf(set by middleware request processing )속성을 가지고 있으면 그 값은 ROOT_URLCONF setting 대신 사용될 것이다.

2. Django는 파이썬 모듈을 로드하고 urlpatterns 변수를 찾을 것이다.  urlpatterns 변수는 django.conf.urls.defaults.patterns() 함수가 반환하는 형식의 파이썬 리스트다.

3. Django는 각 URL 패턴을 순서대로 실행하고, 요청 된 URL과 일치하는 첫 번째 패턴에서 멈춘다.

4. 정규 표현식 중 하나가 일치하면 Django는 주어진 뷰를 가져오고 호출한다. 뷰는 간단한 파이썬 함수다. 뷰는 첫번째 인수로 HttpRequest와 나머지 인수로 정규식에 캡쳐 된 값을 전달한다.

5. 매치되는 정규 표현식이 없을 경우 또는 exception이 발생했을 경우 Django는 적절한 error-handling view를 적용한다.

## Example

```
from django.conf.urls.defulats import *

urlpatterns = patterns(‘’,
    (r’^articles/2003/$’, ‘news.views.special_case_2003’),
    (r'^articles/(\d{4})/$', 'news.views.year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'news.views.month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'news.views.article_detail'),
)
```

* from django.conf.urls.defaults import * 는 pattersn() 함수를 사용가능하게 만든다.

* URL 에서 값을 캡쳐하기 위해서는 괄호를 주변에 넣으면 된다.

* 모든 url이 포함하고 있기 때문에 시작하는 /를 추가할 필요가 없다. ^/articles 가 아닌 ^articles로 사용한다.

* 각 정규 표현식 문자열 앞에 ‘r’ 은 선택적이지만 추천하는 형식이다.  이것은‘raw’ string임을 말해준다.

## Named groups

파이썬 정규 표현식의 명명된 정규 표현식 그룹 문법인 `(?P<name>pattern )`에서 name 은 그룹의 이름을, pattern은 매치되는 패턴이다. 

위 예제에서 명명된 그룹(named group)을 사용한 예제이다. 

```
urlpatterns = patterns(‘’,
    (r’^articles/2003/$’, ‘news.views.special_case_2003’),
    (r’^articles/(?P<year>\d{4})/$’, ‘news.views.year_archive’),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', 'news.views.month_archive'),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'news.views.article_detail'),
)
```

캡쳐 된 값은 위치 인수가 아닌 키워드 인수로 뷰 함수에 전달된다.

* /articles/2005/03 은 news.views.month_archive(request, ‘2005’, ‘03’) 대신에 news.views.month_archive(request, year=’2005’, month=‘03’) 함수를 호출할 것이다.

* /articles/2003/03/03 은 news.views.article_detail(request, year=’2003’, month=’03’, day=’03’을 호출할 것이다.

## What the URLconf searches against

URLconf는 일반적인 파이썬 스트링 처럼 요청된 url을 검색한다. 여기에는 GET, POST 파라미터나 도메인 이름이 포함되지 않는다.

예를 들어 http://www.example.com/myapp/ 요청 시 URLconf는 myapp/을 찾는다. 
http://www.example.com/myapp/?page=3 요청 시 URLconf는 myapp/을 찾는다.

URLconf는 request method를 보지 않는다. 즉 모든request method는 동일한 URL에 대한 동일한 함수를 rout할 것이다.

## Syntax of the urlpatterns variable

  urlpatterns은  django.conf.urls.defaults.patterns() 함수가 반환하는 형식으로  파이선 리스트여야 한다. urlpatterns 변수를 만들기 위해서는 patterns()를 사용한다.

from django.conf.urls.defaults import *을 URLconf 상단에 사용하면 아래 objects에 접근할 수 있다.

django.conf.urls의 defulats.py를 보면 아래 3개의 함수가 포함되어 있다.

```
def include (arg, namespace=None, app_name=None)
def patterns (prefix, *args)
def url(regex, view, kwargs=None, name=None, prefix='')
```

### patterns
##### patterns(prefix, pattern_description, ...)

함수는 prefix와 임의의 URL 패턴을 받는다. 그리고 Django에 맞는  패턴의 URL 리스트를 반환한다. 
patterns()의 첫번째 인수는 prefix 문자열이다. 남은 인수는 아래 포맷의 튜플이다. :

```
(regular expression, Python callback function [, optional dictionary [, optional name]])
-> (정규 표현식 주소, 호출될 view 함수, ....)
```
optional dictionary와 optional name은 선택적이다. 

ex) urls.py 에서 사용 예
```
from django.conf.urls.defaults import *
from news.views import year_archive

urlpatterns = patterns('', 
    (r'^articles/(\d{4})/$', 'news.views.year_archive'),
)
```

### url
##### url(regex, view, kwargs=None, name=None, prefix='')
tuple 대신에 url 함수로 사용 가능하다. optional dictionary 대신에 이름을 명시 해서 사용하기 편하다. 

```

urlpatterns = patterns('',
    url(r'^index/$', index_view, name="main-view"),
)
```

해당 함수는 5개 arguments를 가지는데 대부분 옵션사항이다.
```
url(regex, view, kwargs=None, name=None, prefix='')
```

name parameter가 왜 유용한지 Naming URL patterns를 확인하면 된다.

prefix 파라메터는 patterns()의 첫번째 argument와 동일한 의미를 가진다.


### include
##### include (<module or pattern_list>)

다른 URLconf 로 부터 포함되어야 하는 전체 python import path를 가진다. 

include ()는 또한 URL 패턴을 반환하는 반복 가능 (iterable)을 인수로 가진다.
See Including other URLconfs below.


root URLconf
```
urlpatterns = patterns(''
    (r'^weblog/', include('django_website.apps.blog.urls')),
)
```

blog URLconf(blog.urls.py)
```
urlpatterns = patterns('django_website.apps.blog.views',
    url(r'^list/$', 'list'),
    url(r'^new/$', 'new')
)
```
## Error handling
Django는 정규표현식과 매칭되는 URL을 찾을 수 없거나 Exception이 raise 되면 error-handling 뷰를 호출한다. 

이런 경우에 사용할 뷰를 류트 URLconf에 설정할 수 있는 두개의 변수로 지정된다. (다른 URLconf에 설정해도 동작 안됌)

### handler404
##### handler404
호출 가능하거나, url pattern에 매칭되지 않을 경우 호출될 views 의 전체 python 경로의 문자열이다.

default : 'django.views.defaults.page_not_found'

root.urls.py
```
handler404 = 'mywebpage.views.page_not_found'
```


### handler500
##### handler500

서버 에러가 발생 했을 경우 호출될 뷰의 import path

서버 에러는 view code에서 runtime에러가 발생했을 때 발생한다.

default : 'django.views.defaults.server_error'

## Notes on capturing test in URLs
캡쳐된 argumnt는 매칭된 정규 표현식과 관계 없이 python 문자열로 뷰로 보내진다. 

예를들어 아래 URLConf에서
```
(r'^articles/(?P<year>\d{4})/$', 'news.views.year_archive')
```
year argument는 \d{4}가 숫자로만 매칭되지만, news.views.year_archive()에 문자열로 보내질 것이다.

해당 이슈는 아래와 같이 default parameters를 뷰에 지정하면 된다.
```
# URLconf
urlpatterns = patterns('',
    (r'^blog/$', 'blog.views.page'),
    (r'^blog/page(?P<num>\d+)/$', 'blog.views.page'),
)

# View (in blog/views.py)
def page(request, num="1"):
    # Output the appropriate page of blog entries, according to num.
```
해당 예에서 두개의 URL patterns 모두 같은 뷰를 가리킨다. (blog.views.page) 

하지만 첫번째 패턴은 URL로부터 어떤 것도 캡쳐하지 않는다. 

만약 첫번째 패턴이 매치되면 page() 함수는 디폴트 값인 1을 사용할 것이다. 두번째 패턴이 매치되면 regex로 부터 캡쳐된 값을 사용할 것이다.

## Performance

urlpatterns에 있는 각각의 정규표현식은 첫번째 접근 시 컴파일 되기 때문에 빠르다.매우 

## The view prefix

중복을 제거하기 위해 공통의 prefix를 patterns()에 명시할 수 있다.

```
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^articles/(\d{4})/$', 'news.views.year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'news.views.month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'news.views.article_detail'),
)
```
위 예에서 각 뷰는 'news.views' 의 common prefix를 가진다. 

각각의 뷰 함수에 적용하기 위해 patterns()의 첫번째 argument에 명시한다.

```
from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    (r'^articles/(\d{4})/$', 'year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'article_detail'),
)
```
prefix에 dot(".")은 포함하지 않는다. Django가 자동으로 해줌

## Multiple view prefixes

공통된 prefix가 없는 urlpatterns을 포함할 경우에는 여러개의 patterns()를 더하면 된다.

Old
```
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.date_based.archive_index'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month'),
    (r'^tag/(?P<tag>\w+)/$', 'weblog.views.tag'),
)
```

New
```
from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$','archive_month'),
)

urlpatterns += patterns('weblog.views',
    (r'^tag/(?P<tag>\w+)/$', 'tag'),
)
```

## Including other URLconfs
이 예에서 정규 표현식은 $를 포함하지 않지만 /(slash)를 끝에 포함한다.
Django가 include ()를 발견 할 때마다, 그 점까지 일치하는 URL 부분을 잘라 버리고 추가 처리를 위해 포함 된 URLconf에 나머지 문자열을 보낸다.

아래 예는 다른 URLconfs를 포함한다.
```
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^weblog/',        include('django_website.apps.blog.urls.blog')),
    (r'^documentation/', include('django_website.apps.docs.urls.docs')),
    (r'^comments/',      include('django.contrib.comments.urls')),
)
```

다른 방법은 추가 URL 패턴을 직접 include 함수로 넘겨 주는 것이다. 
```
from django.conf.urls.defaults import *

extra_patterns = patterns('',
    url(r'^reports/(?P<id>\d+)/$', 'credit.views.report', name='credit-reports'),
    url(r'^charge/$', 'credit.views.charge', name='credit-charge'),
)

urlpatterns = patterns('',
    url(r'^$',    'apps.main.views.homepage', name='site-homepage'),
    (r'^help/',   include('apps.help.urls')),
    (r'^credit/', include(extra_patterns)),
)
```

## Captured parameters
포함된 Urlconf 는 parent urlconf로 부터 어떤 캡쳐된 파라미터도 받을 수 있다 .

```
# In settings/urls/main.py
urlpatterns = patterns('',
    (r'^(?P<username>\w+)/blog/', include('foo.urls.blog')),
)

# In foo/urls/blog.py
urlpatterns = patterns('foo.views',
    (r'^$', 'blog.index'),
    (r'^archive/$', 'blog.archive'),
)
```
위 예에서 캡쳐된 "username"은 포함된 URLconf로 전달된다.

## Defining URL namespace

## Passing extra option to view functions
URLconf는 뷰 함수에 추가의 argument를 전달할 수 있게 hook을 가진다.

모든 URLconf 튜플에는 선택적 세 번째 요소가 있을 수 있다.이 요소는 뷰 함수에 전달할 추가 키워드 인수 dictionary여야 한다.

```
urlpatterns = patterns('blog.views',
    (r'^blog/(?P<year>\d{4})/$', 'year_archive', {'foo': 'bar'}),
)
```
위 예에서 /blog/2005/ 요청 시, Django는 blog.views.year_archive () 뷰를 호출하여 다음 키워드 인수를 전달한다.

```
year='2005', foo='bar'
```
URL pattern 의 캡쳐된 keyword argument와 같은 이름의 dictionary의 arguments가 전달되면 dictionary의 argument가 전달된다.


## Passing extra options to include() 

include()에서도 추가의 option을 전달할 수 있다. include()에 추가 옵션을 전달할 때 URLconf에 포함된 각 라인에 전달될것이다.

예를 들어, 아래 두 URLconf 세트는 기능적으로 동일하다.

Set one:
```
# main.py
urlpatterns = patterns('',
    (r'^blog/', include('inner'), {'blogid': 3}),
)

# inner.py
urlpatterns = patterns('',
    (r'^archive/$', 'mysite.views.archive'),
    (r'^about/$', 'mysite.views.about'),
)
```

Set two:
```
# main.py
urlpatterns = patterns('',
    (r'^blog/', include('inner')),
)

# inner.py
urlpatterns = patterns('',
    (r'^archive/$', 'mysite.views.archive', {'blogid': 3}),
    (r'^about/$', 'mysite.views.about', {'blogid': 3}),
)
```

라인의 뷰가 실제로 그 옵션을 유효한 것으로 받아들이는지 여부에 관계없이 추가 옵션은 포함 된 URLconf의 모든 라인에 항상 전달된다 따라서 포함 된 URLconf의 모든 view에서 전달중인 추가 옵션을 허용하는 경우에만 유용하다.

## Passing callable objects instead of string
일부 개발자는 모듈에 대한 경로가 포함 된 문자열 대신 실제 파이썬 함수 객체를 전달하는 것이 더 자연 스럽다는 것을 알게됩니다. 이 대안이 지원됩니다. 호출 가능한 객체를보기로 전달할 수 있습니다.

예를들어 URLconf가 string으로 주어졌을 경우:
```
urlpatterns = patterns('',
    (r'^archive/$', 'mysite.views.archive'),
    (r'^about/$', 'mysite.views.about'),
    (r'^contact/$', 'mysite.views.contact'),
)
```

그냥 objcet를 import 하면 된다.
```
from mysite.views import archive, about, contact

urlpatterns = patterns('',
    (r'^archive/$', archive),
    (r'^about/$', about),
    (r'^contact/$', contact),
)
```

아래 예는 각각의 뷰를 import하는 것 보다 간결하다.
```
from mysite import views

urlpatterns = patterns('',
    (r'^archive/$', views.archive),
    (r'^about/$', views.about),
    (r'^contact/$', views.contact),
)
```
어떤 스타일을 사용하는지는 너에게 달렸다.

해당 기술을 사용할 경우에는 view prefix는 동작하지 않는다.

## Naming URL patterns

URLconf의 여러 URL 패턴에서 동일한 view 함수를 사용하는 것이 일반적이다.

예를 들어 archive view를 가리키는 두개의  URL pattern이 있다면
```
urlpatterns = patterns('',
    (r'^archive/(\d{4})/$', archive),
    (r'^archive-summary/(\d{4})/$', archive, {'summary': True}),
)
```
