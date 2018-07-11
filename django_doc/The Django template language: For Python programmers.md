## Subclassing Context: RequestContext
##### class django.template.RequestCondext

Django에는 특별한 Context class인  django.template.RequestContext 가 있는데 이건 보통 django.template.Context와 약간 다르게 동작한다.

첫번째 차이점은 HttpRequest를 첫번째 argument로 가지는 것이다. 
```
c = RequestContext(request, {
    'foo':'bar'
})
```

두 번째 차이점은 TEMPLATE_CONTEXT_PROCESSORS 설정에 따라 자동으로 컨텍스트에 몇 개의 변수를 채우는 것이다.

TEMPLATE_CONTEXT_PROCESSORS 설정은 request 개체를 argument로 사용하여 컨텍스트에 병합 할 item dictionary을 반환하는 context processor 라고하는 호출 가능한 튜플이다.

TEMPLATE_CONTEXT_PROCESSERS 디폴트 세팅 값 
```
("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.contrib.messages.context_processors.messages")
```
각각의 프로세서는 순차적으로 적용하기 때문에 첫번째 프로세서와 두번째 프로세서가 동일한 이름을 가질 경우 override된다.

RequestContext를 사용하면 직접 입력 한 변수가 먼저 추가되고 컨텍스트 프로세서에서 제공되는 변수가 추가된다. 즉, 컨텍스트 프로세서가 제공 한 변수를 덮어 쓸 수 있으므로 컨텍스트 프로세서에서 제공하는 변수 이름과 중복되는 변수 이름은 사용하지 않도록 주의해야 한다.

또한 RequestContext에 선택적, 세 번째 위치 인수 인 프로세서를 사용하여 추가 프로세서 목록을 제공 할 수 있다. 이 예에서 RequestContext 인스턴스는 ip_address 변수를 가져온다.

```
def ip_address_processor(request):
    return{'ip_address': request.META['REMOTE_ADDR']}

def some_view(reqest):
    c = RequestContext(request, {
        'foo':'bar',
    }, [ip_address_processor])

    return HttpResponse(t.render(c))
```
만약 render_to_response()를 사용할하여 template를 채울 경우 RequestContext가 아닌 Context 인스턴스를 전달한다. 템플릿 렌더링에서 RequestContext를 사용하려면 render_to_response()에 세번째 인수로(optional) 아래와 같이 RequestContext 인스턴스를 전달한다.

```
def some_view(request):
    return render_to_response('my_template.html', my_data_dictionary, context_instance=RequestContext(request))
```
#### django.contrib.auth.context_processors.auth

TEMPLATE_CONTEXT_PROCESSORS가 해당 processor를 포함한다면 모든 RequestContext는 아래 새개의 변수를 포함한다.

* user
* messages
* perm



## Loading templates

일반적으로, low-level의 Template API를 사용하지 않고 파일 시스템의  파일에 template를 저장한다. template directory로 지정된 디렉토리에 template를 저장해라.

장고는 template-loader 세팅에 따라 여러 위치에 있는 template 디렉토리를 검사한다. 그러나 template 디렉토리들을 지정하는 가장 기본적인 방법은 TEMPLATE_DIRS 설정을 이용하는 것이다.


### The TEMPLATE_DIRS settings

settings 파일의 TEMPLATE_DIRS 설정을 사용하여 template 디렉토리가 무엇인지 알려라. TEMPLATE_DIRS 는 template 디렉토리의 full 경로를 포함한 string 의 list나 tuple로 설정되어야 한다(ies). 

예)

```
TEMPLATE_DIRS = (
	"/home/html/templates/lawrence.com",
	"/home/html/templates/default",
)
```

디렉토리와 template가 웹 서버에서 읽을 수 있는 한 원하는 위치로 이동할 수 있다. 원하는 확장자를 가질 수 있다. .html이나 .txt 또는 확장자가 없을 수도 있다.

경로는 윈도우에서도 Unix 스타일인 슬래시를 사용해야 한다.
