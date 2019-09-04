# Field options

## null

*Field.null*

True일 경우 Django는 데이터베이스에 빈 값을 NULL로 저장한다. 디폴트 값은 False이다.

빈 문자열 값은 항상 NULL이 아닌 빈 문자열로 저장된다.  정수, 부울 및 날짜와 같은 문자열이 아닌 필드에 대해서만 null = True를 사용한다.  두 가지 유형의 필드의 경우, 양식에서 빈 값을 허용하려면 blank = True로 설정 해야 한다. null 매개 변수는 데이터베이스 저장 영역에만 영향을 준다.

특별한 이유가없는 한 CharField 및 TextField와 같은 문자열 기반 필드에서 null을 사용하지 않아야 한다.  문자열 기반 필드에 null = True가 있으면 "no data"에 대해 가능한 두 개의 값 (NULL 및 빈 문자열)이 있음을 의미 한다. 대부분의 경우, "데이터 없음"에 대해 가능한 두 가지 값을 갖는 것은 불 필요 하다. Django 규칙은 NULL이 아닌 빈 문자열을 사용하는 것이다.


## blank

*Field.blank*

True일 경우 필드는 blank를 허용한다. Default는 False. 

null과는 다르다. **null은 데이터베이스와 연관되어 있고, blank는 유효성과 연관되어 있다.**
field가 blank=True라면 *Django admin 페이지에서* 유효성 검사 시 빈 값을 허용한다. field가 blank=False일 경우 필요한 필드이다.

### ManyToManyField

*ManyToManyField.through*

Django는 many-to-many 관계를 관리하기 위해 자동으로 생성한다. 하지만 intermediary 테이블을 수동으로 명시하고 싶을 경우, 사용하기 위한 intermediate 테이블을 나타내는 Django model을 명시하기 위해 through 옵션을 사용할 수 있다.

이 옵션의 가장 일반적인 용도는 [다대다 관계에 추가 데이터](https://django.readthedocs.io/en/1.3.X/topics/db/models.html#intermediary-manytomany)를 연결하려는 경우 이다.











