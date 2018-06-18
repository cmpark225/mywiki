# Password management in Django

## How Django stores password

User object의 password 포멧

```
<algorithm>$<iterations>$<salt>$<hash>
```
algorithm은 단방향 hash 를 사용한다.

Django는 기본적으로 SHA256 해시를 이용한 PBKDF2 알고리즘을 사용한다(2.0기준). 다른 알고리즘이나 커스텀 알고리즘을 사용할 수 있다.

Django는 PASSWORD_HASHERS 세팅 값에 따라 알고리즘을 선택한다.
(PASSWORD_HASHERS 해싱 알고리즘 클래스 리스트)
리스트의 첫번째 항목(PASSWORD_HASHERS[0])은 비밀번호를 저장하는데 사용된다. 나머지 목록은 비밀번호를 검증하는데 사용될 수 있다. 즉 다른 알고리즘을 사용하길 원할 경우 선호하는 알고리즘을 PASSWORD_HASHERES의 리스트의 첫번째로 오도록 수정을 해야 한다.
default PASSWORD_HASHERS:

```
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrb.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashesrs.BcryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
```
이에 따라 지원되는 모든 암호를 저장하는 데 PBKDF2를 사용하되 PBKDF2SHA1, argon2, bcrypt 및 숨은 비밀 번호를 확인할 수 있다.

## Password upgrading
사용자가 로그인 했을 때 선호하는 알고리즘(PASSWORD_HASHERS[0])이 아닌 다른 알고리즘으로 비밀번호가 저장되어 있다면 Django는 자동으로 선호 알고리즘으로 upgrade 해준다.이는 사용자가 로그인함에 따라 이전에 설치한 Django 설치 파일의 보안을 자동으로 강화하고 새로운(더 나은)스토리지 알고리즘으로 전환할 수 있음을 의미합니다.

Django는 PASSWORD_HASHERS에 있는 알고리즘을 사용하는 비밀번호만  업그레이드를 할 수 있으므로, 새로운 시스템으로 업그레이드할 경우 *절대 리스트에서 항목을 제거 하면 안된다.* 제거할 경우 목록에 없는 알고리즘을 사용하는 유저는 업그레이드를 할 수 없다. 

## Password upgrading without requiring a login
만약 MD5나 SHA1와 같은 weak hash가 있는 기존 데이터베이스가 있는 경우 사용자가 로그인을 했을 때 업그레이드 되는 것을 기다리지 않고 직접 업그레이드를 할 수 있다.(사용자가 로그인 하지 않을 경우 업그레이드가 될 수 없다.) 이런 경우 'wrapped' password hasher를 사용할 수 있다.

이 예에서는 SHA1 해시 콜렉션을 PBKDF2 (SHA1 (password))를 사용하도록 마이그레이션하고 사용자가 로그인시 올바른 비밀번호를 입력했는지 확인하기 위해 해당 비밀번호 해더를 추가한다.

1. custom hasher 추가

```
from django.econtrib.auth.hashers import PBKDF2PasswordHasher, SHA1PasswordHasher

class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
        return super(PBKDF2WrappedSHA1PasswordHasher, self).encode(sha1_hash, salt, iterations)
    
    def encode(self, password, salt, iterations=None):
        _, _, sha1_hash = SHA1PAsswordHasher().encode(password, salt).split('$', 2)
        return self.encode_sha1_hash(sha1_hsah, salt, iterations)
```


2. data migration 
sha1인 사용자의 비밀번호를 sha256dmfh qusrudgksek.

```
from django.contrib.auth.models import User
from ..hashers import PBKDF2WrappedSHA1PasswordHasher


def migrate_sha1_password():
    users = User.objects.filter(password__startswith='sha1$')
    hasher = PBKDF2WrappedSHA1PasswordHasher()

    for user in users:
        algorithm, salt, sha1_hash = user.password.split('$', 2)
        user.password = hasher.encode_sha1_hash(sha1_hash, salt)
        user.save(update_fields=['password'])

```
하드웨어 속도에 따라 수천 명의 사용자의 마이그래션을 수행 하는 시간은 수 분 정도 걸린다.

3.PASSWORD_HASHERS에 추가
```
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'my_app.hashers.PBKDF2WrappedSHA1PasswordHasher',
]
```

## Manually managing a user's password

django.contrib.auth.hahsers 모듈은 User 모델과 독립적으로 사용할 수 있는 비밀번호 생성과, 검증 함수를 제공한다. 

### check_password(password, encoded)

RETURN
- True : match
- False : not match

데이터베이스에 있는 해시된 비밀번호와 plain-text 비밀번호를 직접ㅈ 검증하고 싶을 경우 check_password()를 사용할 수 있다.


### make_password(password, salt=None, hasher='default')

### is_password_usable(encoded_password)
지정된 문자열이 check_password()에 대해 확인 될 수있는 해시 된 암호인지 확인한다.



