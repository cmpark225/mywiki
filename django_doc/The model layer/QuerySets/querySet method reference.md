#### values
**values(*fields)**
model 인스턴스 대신 iterable을 사용할때 딕셔너리를 반환하는 ValuesQuerySet을 반환한다.

각 딕셔너리는 모델 오브젝트의 속성 이름에 해당하는 키로 오브젝트를 나타낸다.

이 예에서는 values ​​()의 딕셔너리를 일반 모델 객체와 비교한다.

```
# This list contains a Blog object.
>>> Blog.objects.filter(name__startswith='Beatles')
[<Blog: Beatles Blog>]

#This list conains a dictionary.
>>> Blog.objects.filter(name__startswith='Beatles').values()
[{'id':1, 'name':'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]
```


