이슈 처리 중

두개의 API에 동일한 http 헤더를 추가했는데, 

header 이름을 다르게 정의해도 각 API에서 헤더 값을 가져오는데는 문제가 없었다.

ex)

A API -> X_MY_HEADER : 1234

B API -> X-MY_HEADER : 1234


A API에는 X하고 언더바로 헤더를 추가하였고, 

B API에서는 X하고 하이픈으로 헤더를 추가했다.

A, B 의 request 확인해보니 모두 HTTP_X_MY_HEADER로 헤더가 정의 되어 있었다.

request의 custom header가 어떻게 HTTP_X_MY_HEADER로 변경 되었는지, 맞는 네이밍 규칙은 무엇인지 확인해보았다.


## Django - HttpRequest.META

헤더 이름을 변경하는 부분을 찾아보니, request를 받는 쪽인

WSGIRequestHandler클래스의 get_environ 함수에서

'-'를 '_'로, 소문자를 대문자로 변경하고 있었다.

```
        for h in self.headers.headers:
            k,v = h.split(':',1)
            k=k.replace('-','_').upper(); v=v.strip()
            if k in env:
                continue                    # skip content length, type,etc.
            if 'HTTP_'+k in env:
                env['HTTP_'+k] += ','+v     # comma-separate multiple headers
            else:
                env['HTTP_'+k] = v
        return env

```

해당 내용은 Django의 HttpRequest.META에서도 확인이 가능하다.

https://django.readthedocs.io/en/1.3.X/ref/request-response.html?#django.http.HttpRequest.META

> With the exception of CONTENT_LENGTH and CONTENT_TYPE, as given above, any HTTP headers in the request are converted to META keys by converting all characters to uppercase, replacing any hyphens with underscores and adding an HTTP_ prefix to the name. So, for example, a header called X-Bender would be mapped to the META key HTTP_X_BENDER.

CONTENT_LENGTH 와 CONTENT_TYPE을 제외하고 request의 HTTP 헤더는 

모두 대문자로, 하이픈은 언더바로 변경되고, HTTP_ prefix가 추가되어 META KEY로 변경된다.


## Custom Http Header Naming Convention

[RFC6648](https://tools.ietf.org/html/rfc6648) 을 확인해보면

Custom header의 Naming convention 은 X-로 시작하는 것을 규칙으로 하고 있는 것을 알 수 있다.

ref https://www.keycdn.com/support/custom-http-headers/
