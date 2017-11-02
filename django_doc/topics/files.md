# Managing files

기본적으로 Django는 MEDIA_ROOT와 MEDIA_URL 세팅을 사용하여 파일을 로컬로 저장한다. 아래 예제는 이러한 default를 사용한다고 가정한다.

그러나 Django는 Django가 파일을 저장하는 위치와 방법을 완벽하게 커스터마이징할 수 있는 맞춤형 파일 스토리지 시스템을 작성하는 방법을 제공한다. 이 문서의 후반부에서는 이러한 스토리지 시스템의 작동 방식을 설명한다.

## Using files in models

FileField 또는 ImageField를 사용할때 Django는 해당 파일을 다룰 수 있는 API를 제공한다.

이미지를 저장하는 ImageField를 사용할때는 아래 모델을 고려해라:

```
class Car(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    photo = models.ImageField(upload_to='cars')    
```

모든 Car 인스턴스에는 첨부된 사진의 세부 정보를 얻는 데 사용할 수 있는 photo attribute가 있다.

```
>>> car = Car.objects.get(name="57 Chevy")
>>> car.photo
<ImageFieldFile: chevy.jpg>
>>> car.photo.name
u'cars/chevy.jpg'
>>> car.photo.path
u'/media/cars/chevy.jpg'
>>> car.photo.url
u'http://media.example.com/cars/chevy.jpg'

```

이 개체는(예제에서 car.photo) 파일 개체이며, 이는 아래에 설명된 모든 방법과 속성을 가지고 있음을 의미한다. 

https://django.readthedocs.io/en/1.3.X/topics/files.html

