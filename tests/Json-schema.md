Json 데이터에 대한 유효성 검사가 필요할때 json schema를 이용할 수 있다.

## Json 스키마 생성 방법

### 1. schema 추출 페이지 이용

https://jsonschema.net/#/editor

페이지를 통해서 json schema를 추출할 수 있다.

### 2. GenSON 프로그램 이용
- 설치
```
sudo pip install genson
```

## 스키마 검증 방법
:[jsonschema 모듈 사용](https://github.com/Julian/jsonschema)

## JSON schema 기본적인 사용

### Instance

기본적인 데이터 타입은 6가지를 가지며 이는 json data model과 동일하다.

* null
* boolean
* object
* array
* number
* string

### 기본적인 스키마 구조
```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "A default format",
    "description": "This is a schema that matches anything.",
    "type": "object",
}
```

* schema : json schema도 json 타입이기 때문에, json schema 형식이라는 것을 알린다. 
* title : 스키마 제목
* description : 스키마 설명 
* type : 해당 스키마 타입.

### Example object data Type Validation

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Object Type",
    "description": "This is a Example that object data type.",
    "type": "object",
    "required": ["firstName", "lastName"],
    "properties": {
        "firstName": {
            "type": "string"
        }
        "lastName": {
            "type": "string"
        }
        "firstName": {
            "type": "Number"
            "minimum": "0"
        }
    }
}
```

* required : 필수로 포함되어야 하는 키 값
* properties : 검증할 키에 대한 validate 설명

### Example array data Type Validation

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Array Type",
    "description": "This is a Example that Array data type.",
    "type": "array",
    "items": {
        "type": "object",
         "properties": {
             "firstName" : {
                 "type":"string"
             }   
         }
    }
}
```

* items : array의 경우 key 값이 없기 때문에 "items"를 이용해 value를 검증한다.


## 참고 site
* [JSON Schema] (http://json-schema.org/)
* [(flask) jsonschema 를 이용해서 request.json 검사하기] (http://ash84.net/2017/01/03/flask-jsonschema-decorator/)
* [JSON과 PYTHON API의 만남] (https://github.com/mcchae/JSON-Schema/blob/master/JSON-API.md)
