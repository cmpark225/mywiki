Using User Model 

```
from django.contrib.auth.models import User 
```

# Users

class models.User

## Methods

### check_password(raw_password)

raw string이 사용자 비밀번호가 일치할 경우 True를 반환한다. (비교할때 암호를 hashing 처리한다.)
=> 입력받은 암호를 hashing 처리하여 이미 hashing된 암호와 비교

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

### has_usable_password()

해당 사용자에게 set_unsuable_password()가 호출되었으면 False를 반환한다. 

```
>>> user.has_usable_password()
False
```


#### Manager functions

class models.UserManager

User 모델은 아래의 help function인 custmom manager를 가진다:

##### create_user(username, email, password=None)

생성, 저장, 그리고 User를 리턴한다.

username과 password를 입력한 값으로 설정한다.  도메인을 자동으로 소문자로 설정한다. 그리고 User object는 is_active가 True인 상태로 return 된다. 

password가 없을 경우 set_unusable_password()가 호출된다.


### Basic usage

#### Creating users

user를 생성하는 가장 기본적인 방법은 django에서 제공하는 create_user() helper function을 사용하는 것이다.

```
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# 이 시점에 user는 이미 데이터베이스에 저장된 user object이다.
# 다른 field를 변경하고 시을 경우 attributes 변경이 가능하다.
>>> user.is_staff = True
>>> user.save()
```


