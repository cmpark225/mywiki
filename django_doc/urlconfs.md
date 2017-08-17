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

규칙은 from django.conf.urls.defaults import *을 URLconf 상단에 사용하는 것이다. 이것은 너의 모듈이 이러한 object들에 접근할 수 있게 한다. :

### patterns

함수는 prefix와 임의의 URL 패턴을 받는다. 그리고 Django에 맞는  패턴의 URL 리스트를 반환한다. 
patterns()의 첫번째 인수는 prefix 문자열이다. 남은 인수는 아래 포맷의 튜플이다. :

```
(regular expression, Python callback function [, optional dictionary [, optional name]])
```

optional dictionary와 optional name은 선택적이다. 


### url

### include


## Error handling

### handler404

### handler500


## Notes on capturing text in URLs
각각 캡쳐된 아규먼트는 정규식이 어떤 종류의 일치를 하는지와 관계 없이,  평문의 Python string으로 view에 보내진다. 

```
(r’^articles/(?P<year>\d{4}/$)’, ‘news.views.year_archive’),
```

news.views.yaer_archive()의 yaer argument는 \d{4}가 integer string만 매치되더라도 integer가 아닌 string이 된다.


편리한 트릭은 view의 argument에 디폴트 파라메터를 명시하는 것이다. 예를들어

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

위 예제에서, 두개의 URL patterns는 같은 view를 가리키고 있다 – blog.views.page – 그러나 첫번째 패턴은 URL에서 아무것도 캡쳐하지 않는다. 만약 첫번째 패턴에 매치된다면, page() 함수는 default argument 인 num을 1로 사용할 것이다. 두번째 패턴이 매치된다면 page()는 정규식에 캡쳐된 어떤 숫자 값이라도 사용할 것이다.

## Performance

urlpatterns에 있는 각각의 정규식은 처음 엑세스 될 때 컴파일 된다. 이는 시스템을 놀랍도록 빠르게 만든다.

## The view prefix

코드 중복을 제거하기 위해 patterns()에 있는 공통적인 prefix를 명시할 수 있다.

URLconf  예제

```
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^articles/(\d{4})/$', 'news.views.year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'news.views.month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'news.views.article_detail'),
)
```

위 예에서 각각의 views는 공통적인 prefix를 가진다. – ‘news.views’.  url 패턴의 각 항목에 대해 이를 입력하는 대신에  각각의 view 함수에 적용할 prefiex를 지정하기 위해 patterns() 함수의 첫번째 argument를 사용할 수 있다.
아래는 간결하게 사용될 수 있는 예제를 보여준다.

```
from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
    (r'^articles/(\d{4})/$', 'year_archive'),
    (r'^articles/(\d{4})/(\d{2})/$', 'month_archive'),
    (r'^articles/(\d{4})/(\d{2})/(\d+)/$', 'article_detail'),
)
```

앞에 dot(“.”)을 놓지 않은 것을 명심해라. Django는 자동으로 .을 붙여준다

## Multiple view prefixes
