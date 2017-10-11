# Request parsing

## .DATA

request.DATA는 request body의 파싱된 content를 리턴한다.  
다음을 제외 request.POST 속성과 비슷하다.:

* POST 외 다른 HTTP method들의 content 파싱을 지원한다.  이는 PUT과 PATCH request의 content 접근이 가능한 것을 의미한다.
* 유연한 request 파싱을 지원한다. form data 외 json 데이터도 form data와 같이 handling이 가능하다.
