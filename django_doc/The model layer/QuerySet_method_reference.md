### Methods that return new QuerySets


#### values

**values(\*fields)**

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

#### values_list

**values_list(\*fields)**

딕셔너리 반환 대신에 iterated가 반복 될 때 튜플을 반환한다는 점을 제외하고 values()와 비슷하다. 

각 튜플은 values_list() 호출로 전달 된 각 필드의 값을 포함한다. -- 첫번째 아이템은 첫번째 필드이다.

```
>>> Entry.objects.values_list('id', 'headline')
[(1, u'First entry', ....)]
```
한개의 필드만 전달할 경우 flat 파라메터도 전달할 수 있다. 이것은 반환되는 결과가 한개의 튜플이 아니라 단일 값임을 의미한다.

```
>>> Entry.objects.values_list('id')
[(1,), (2,), (3, ), ...]

>>> Entry.objects.values_list('id', flat=True)
[1, 2, 3, ...]
```

두개 이상의 필드일때 flat을 전달할 경우 error다. (그냥 무시 되는듯...)

아무 값도 values_list()에 전달하지 않을 경우 모델에 정의된 순서대로 모든 필드를 반환한다.
