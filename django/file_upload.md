Image테이블 생성후 
ImageField 추가.

# 에러 발생
```
$ python manage.py syncdb
Error: One or more models did not validate:
wisdom.image: "path": To use ImageFields, you need to install the Python Imaging Library. Get it at http://www.pythonware.com/products/pil/ .
```
### 1. PIL 설치
```
sudo pip install pillow
```

# Image Model 

## 1. Model 생성
```
class PollImage(models.Model):
    image = models.ImageField(upload_to='poll_images/')
```

## 2. 이미지 업로드할 경로 및 URL설정

settings.py
```
BASE_URL = 'http://127.0.0.1:8888/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'images')
MEDIA_URL = BASE_URL + '/images/'
```

##### MEDIA_ROOT

이때 PollImage에 이미지를 업로드할 경우 이미지가 업로드 되는 경로는

프로젝트 경로의 images 폴더 안에 poll_images/다.

=> MEDIA_ROOT + upload_to경로

##### MEDIA_URL
이미지의 URL경로

인스턴스의 이미지의 URL을 확인하고 싶은 경우 shell에서 확인할 수 있다.

```
$ python manage.py shell
>>> from poll.models import PollImage
>>> image = PollImage.objects.get(pk=1)
>>> image.image.url
http://127.0.0.1:8888/images/poll_images/a.jpg
```

## 3. apache 설정
이미지 파일들에 대한 url이 설정되어 있지 않았기 때문에

http://127.0.0.1:8888/images/poll_images/a.jpg

위 경로로 접속 시도시 404에러가 발생한다.

static file서빙처럼 media root를 apache에 설정해준다 


