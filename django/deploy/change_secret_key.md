git에 secret key가 올라가있는 것이 마음에 걸려 검색해보니. 
secret key는 공개된 장소에 올리지 말라고 한다.

이미 올라가 있는 secret_key는 새로 만들어 변경하고,
변경된 값을 환경변수에 저장하여 가져오도록 수정하고자 한다.



# 1. secret key 변경
git에 올라가있는 secret key를 변경하기 위해 

아래 코드 실행 하여 새로운 secret key를 생성한다.

```
import string, random

# Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)
```

# 2. secret_key 저장

secret_key를 환경 변수에 저장하여 setting.py에서 가져오도록 설정 하였는데,

runserver를 통해서는 정상적으로 동작 했지만, apache를 통해 서비스를 제공할 경우 

Cannot concatenate 'str' and 'NoneType' objects

위 에러가 발생하며 정상 동작하지 않았다. 

os.environ.get('SECRET_KEY')에 실패하여 SECRET_KEY값이 NoneType이기 때문에 발생한 에러 같다.

따라서 환경변수 저장 -> config 파일에서 읽어오는 방식으로 변경하였다.


## 2.1 환경변수에서 secret_key 가져오기.


### 2.1.1 secret_key 저장

환경변수에서 가져오기 위해 

secret_key를 환경변수에 저장했다.

```
$ vim /etc/environment

MY_SECRET_KEY="dasfdfjdslf2132ja1241dskslf'sdkdjd<>D..."
```

### 2.1.2 secret_key 가져오기
그리고 settings.py에서는 os.environ을 통해 secret key를 가져온다.

settings.py
```
SECRET_KEY = os.environ.get('MY_SECRET_KEY')
```


## 2.2 config 파일에서 secret_key 가져오기

### 2.2.1 config.json 생성

config.json 파일을 생성해서 secret_key를 저장했다.
(secret_key 말고 다른 중요 값 저장할 예정)

config.json
```
{
    'SECRET_KEY':'ddsfasdfsadasfdsafdsaf'
}
```

### 2.2.2 secret_key 가져오기

settings.py에서 config.json을 로드한 후 해당 값을 가져온다.
```
from django.core.exceptions import ImproperlyConfigured 

config_file = os.path.join(BASE_DIR, 'config.json')

with open(config_file) as f:
    config = json.loads(f.read())

def get_config(setting_key, config=config):
    try:
        return config[setting_key]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(setting_key)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_config('WISDOM_SECRET_KEY')
```

### 2.2.3 .gitignore에 config.json 추가
secret_key가 git에 올라기는걸 막는 목적으로 시작한거니까...

저장소에 올라가지 않도록 .gitignore에 해당 파일을 추가한다.

.gitignore
```
config.json
```



참고 사이트:
https://wayhome25.github.io/django/2017/07/11/django-settings-secret-key/
