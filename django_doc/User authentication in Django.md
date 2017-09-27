Using User Model 

```
from django.contrib.auth.models import User 
```

# Users

class models.User

## Methods

### set_unusable_password()

사용자가 패스워드를 가지지 않은 것으로 표시한다. 빈 문자열을 password로 가지는 것과는 다르다. check_password()는 이 사용자에 대해서 True를 리턴하지 않는다.  Doesn't save the User object(? : DB에 저장되던데?)

어플리케이션이 LDAP 디렉토리와 같은 기존 외부 인증을 사용할때 필요할 것이다.

ex) 
User 생성 시 

```
>>> from django.contrib.auth.models import User
>>> user = User()
>>> user.username = 'testuser'
>>> user.first_name = 'test'
>>> user.last_name = 'user'
>>> user.set_unusable_password()
>>> user.save()
```
DB에 해당 user에 대한 password 값이 !로 저장된것을 확인할 수 있다.
