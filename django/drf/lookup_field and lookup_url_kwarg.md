lookup_field , lookup_url_kwarg 차이점 확인

lookup_field, lookup_url_kwarg 모두 GenericAPIView의 attributes다.

## DRF문서 설명

### lookup_field
개별 모델 인스턴스의 개체 조회를 수행하는데 사용하는 모델 필드. 기본 값은 'pk'. 
하이퍼링크된 API를 사용할 때 사용자 지정 값을 사용해야 하는 경우 API 보기와 serializer 클래스가 모두 룩업 필드를 설정하는지 확인해야 한다.

### lookup_url_kwarg
개체 조회에 사용해야 하는 URL 키워드 인수. URL conf에는 이 값에 해당하는 키워드 인수가 포함되어야 한다. 설정을 사용하지 않을 경우 lookup_field와 동일한 값을 사용한다.

=> 즉
lookup_field는 object를 조회할 필드를 지정하는 것이고, 
lookup_url_kwarg는 URL에서 capture된 변수의 이름을 지정하는 것이다.


## 확인 내용 
lookup_url_kwarg는 url의 kwargs에서 값을 가져오는데 사용한다.

예를들어 

url.py
```
url(r'^class/(?P<class_id>\d+)/users/(?P<user_id>\d+')/$', UserView.as_view({'get':'retrieve'}))
```
일 경우 

UserView의 kwargs의 값은 아래와 같다.
```
{
    'class_id': 777,
    'user_id': 1
}
```

lookup_url_kwarg를 'user_id'로 지정한 UserView :
view.py 
```
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    model = User
    lookup_url_kwarg = 'user_id'
```

get method로 객체를 가져올 때 get_object 함수를 이용한다:
rest_framework/generics.py
```
def get_object(self, queryset=None):
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    lookup = self.kwargs.get(lookup_url_kwarg, None)
    ...

    if lookup is not None:
        filter_kwargs = {self.lookup_field: lookup}

    ...
```

위 get_object()함수 내용을 확인해보면
kwargs에서 key가 'user_id'의 값을 가져와
lookup_field에 설정된 키로 객체를 가져온다.
(lookup_field를 설정 안했기 때문에 기본 값인 'pk'가 설정된다.)

객체를 실질적으로 가져오게 될 filter_kwargs 값은 아래와 같다.
```
filter_kwargs = {
    'pk':1
}
```

### lookup_field로 설정된 field 값이 related field일 경우 PUT에서 에러 발생

lookup_field로 설정된 related field 값을 업데이트 할 경우 
해당 pk를 넘겨주면 ValueError가 발생한다.


User model에서 user id가 외래키일 경우 :
models.py
```
class User(models.Model):
    user_id = models.OneToOneField(User, primary_key=True)
    class_id = models.ForeignKey(Class)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
```

여기서 view의 lookup_field가 user_id로 되어 있을 경우
(위 UserView에서 lookup_field만 추가)
view.py 
```
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    model = User
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'
```


URL conf 값이 아래와 같다면
```
{
    'class_id': 777,
    'user_id': 1
}
```

GET은 아래 filter_kwargs로 정상적으로 데이터를 가져 오지만

```
filter_kwargs = {
    'user_id':1
}
```

PUT의 경우
Cannot assign "u'1'": "User.user_id" must be a "User" instance
에러를 발생시킨다.

pre_save()에서 User 객체를 저장할때
lookup_field로 지정된 필드의 값을 저장하는데 
지정된 user_id가 User 인스턴스이기 때문에 ValueError가 발생한 것이다.

lookup_field를 지정하지 않을 경우 기본값은 pk이기 때문에 저장 가능하다.
(Model의 pk의 타입은 long임)

만약 related field를 lookup_field를 지정하고 싶을 경우
related된 model의 pk를 지정해주면 된다.

ex)
lookup_field = 'user_id__id'


