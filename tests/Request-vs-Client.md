# The request factory

RequestFactory는 test client와 동일한 API를 사용한다. 그러나 브라우저와 같이 동작하는 대신에 RequestFactory는 view에서 첫번째 argument로 사용할 수 있는 request 인스턴스를 만들어내는 방법을 제공한다. 이것은 다른 함수를 테스트하는 것과 같은 방식으로 view function을 테스트 할 수 있다는 것을 의미한다. – 정확하게 알려진 입력을 가진 블랙 박스로서 특정 출력을 테스트 한다. 

RequestFactory의 API는 test client API의 약간 제한적인 하위 집합이다. 
- HTTP 접근 메소드로 get(), post(), put(), delete(), head(), options(), trace() 만 가진다.
- 이 메소드는 다음을 제외하고는 같은 인수를 모두 허용한다. 요청을 생상하는 factory 일 뿐이므로 응답을 처리하는 것은 사용자의 몫이다.
- middleware을 지원하지 않는다. 뷰가 제대로 동작하기 위해서는 Session 과 authentication 속성이 테스트 자체에서 제공되어야 한다.

# Request vs Client

RequestFactory 는 request를 리턴하고,
Client는 response를 리턴한다.

Client는 완벽한 request-response cycle을 fake로 사용한다. 

=======================================================

RequestFactory and Client have some very different use-cases. To put it in a single sentence: RequestFactory returns a request, while Client returns a response.

The RequestFactory does what it says - it's a factory to create request objects. Nothing more, nothing less.

The Client is used to fake a complete request-response cycle. It will create a request object, which it then passes through a WSGI handler. This handler resolves the url, calls the appropriate middleware, and runs the view. It then returns the response object. It has the added benefit that it gathers a lot of extra data on the response object that is extremely useful for testing.

The RequestFactory doesn't actually touch any of your code, but the request object can be used to test parts of your code that require a valid request. The Client runs your views, so in order to test your views, you need to use the Client and inspect the response. Be sure to check out the documentation on the Client.
