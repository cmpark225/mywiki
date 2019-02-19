spectrum API 호출 시 delete method를 이용해 request.DATA 접근 시 UnsupportedMediaType 예외가 발생한다.

 

restframework에서 request.DATA는 request의 body의 값을 파싱해서 리턴하고 있다. body를 파싱하는 모듈은 spectrum settings에서 설정하고 있다.

현재 spectrum에서 사용 중인 파싱 모듈은 YAML, XML, JSON, FORM 만 있다

production_settings.py
```
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.YAMLParser',
        'rest_framework.parsers.XMLParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    )
}
```

POST 메소드로 보낼 경우에는 Django에서 Post데이터를 처리해주는데(reqeust.post로 데이터 접근 가능.)

그 외 메소드로 보낼 경우, settings에 설정한 파싱 모듈로 body를 파싱 해야 한다. 

현재 sepctrum의 경우 multipart파싱 모듈 설정이 안되어 있어서,

Post 메소드가 아닌 다른 메소드로 api 호출 시

Http 헤더의 content-type이 multipart일 경우 파싱이 안되서 unsupportedMediaType예외가 발생한다.
