git에 secret key가 올라가있는 것이 마음에 걸려 검색해보니. 
secret key는 공개된 장소에 올리지 말라고 한다.

이미 올라가 있는 secret_key는 새로 만들어 변경하고,
변경된 값을 환경변수에 저장하여 가져오도록 수정하고자 한다.



## 1. secret key 변경
```
import string, random


# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)
```

2. 환경변수 설정 
```
$ vim /etc/environment

MY_SECRET_KEY="dasfdfjdslf2132ja1241dskslf'sdkdjd<>D..."
```

3. settings.py에서 secret_key 가져오는 방식 변경

settings.py
```
SECRET_KEY = os.environ.get('MY_SECRET_KEY')
```

참고 사이트:
https://wayhome25.github.io/django/2017/07/11/django-settings-secret-key/
