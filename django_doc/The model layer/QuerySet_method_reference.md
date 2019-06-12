### Methods that return new QuerySets
새로운 쿼리셋을 반환하는 메소드드

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

#### none

**none()**

EmptyQuerySet 반환 -- none()을 호출하면 객체를 반환하지 않는 쿼리 세트가 만들어지며 결과에 액세스 할 때 쿼리가 실행되지 않는다. 호출자가 QuerySet 객체를 기대하는 경우 와 빈 결과를 반환해야 할 경우 사용될 수 있다. (빈 리스트 대신)

예:

```
>>> Entry.objects.none()
[]
```

#### all

**all()**

현재 쿼리셋의 복사본을 반환(또는 전달한 QuerySet 하위 클래스). 모델 메니저나 쿼리셋을 전달하고 그 결과를 더 필터링하려는 경우에 유용하다. 두 객체 중 하나에서 all()을 안전하게 호출하면 작업할 QuerySet을 확실히 가질 수 있다.


##### select_related

**select_related**
외래 키 관계를 자동적으로 "follow"하는 QuerySet를 리턴 해, 조회를 실행할 때 그 추가의 관련 객체 데이터를 선택한다. 이는 (때로는 많은) 큰 쿼리를 발생시키는 성능 향상이지만 나중에 외래 키 관계를 사용하면 데이터베이스 쿼리가 필요하지 않음을 의미한다.

아래 예는 일반 조회와 select_related() 조회의 차이를 보여준다.

여기 일반적인 조회 방식이다:

```
# 데이터베이스 조회
e = Entry.objects.get(id=5)

# 관계된 Blog 객체를 얻기 위해 데이터베이스 다시 조회
b = e.blog
```

그리고 여기 select_related 조회 방식이다:

```
# 데이터베이스 조회
e = Entry.objects.select_related().get(id=5)

# e.blog 는 이전에 실행되었기때문에, 데이터베이스 조회를 하지 않는다.
# in the previous query (이전 쿼리에서)
b = e.blog
```

select_related() 는 가능한 외래키를 따른다. 만약 아래의 모델을 가지고 있다면:

```
class City(models.Model):
    # ...

class Person(models.Model):
    # ...
    hometown = models.ForeignKey(City)

class Book(models.Model):
    # ...
    author = models.ForeignKey(Person)
```
그리고 Book.objects.select_related().get(id=4)를 호출하면 관련된 Person과 관련된 City를 캐쉬할 것이다.

```
b = Book.objects.select_related().get(id=4)
p = b.author # Doesn't hit the database.
c = p.hometown # Doesn't hit hte database.

b = Book.objects.get(id=4) # 이 예제에서는 select_related() 사용 안함.
p = b.author # Hits the database
c = p.hometown # Hits the database
```
기본적으로 select_related()는 null = True 인 외래 키를 따르지 않는다.

보통, select_related() 사용은 앱이 많은 데이터베이스 호출을 피할 수 있기 때문에 많은 성능 향상을 가질 수 있다. 그러나 깊이 중첩 된 관계가있는 상황에서 select_related()는 때때로 "너무 많은"관계를 따라갈 수 있으며 쿼리가 너무 커서 결국 느려지게 된다.

이러한 상황에서 select_related()에 depth 인수를 사용하여 select_related() 관계의 "레벨"을 실제로 제어 할 수 있다.:

```
b = Book.objects.select_related(depth=1).get(id=4)
p = b.auther # 데이터베이스 조회 안함.
c = p.hometown # 데이터베이스 호출 필요
```

때때로 root모델과 연관이 있는 모든 모델이 아닌 특정 모델만의 접근을 원할 수 있다. 이러한 경우 select_related()에 관련된 필드 이름을 전달 할 수 있으며,  이러한 고나계는 그 관계를 따른다. 필터와 마찬가지로 필드 이름을 두 개의 밑줄로 분리하여 둘 이상의 관계가 있는 모델에 대해서도 이렇게 할 수 있다. 예를들어, 아래와 같은 모델이 있다고 가정하자:

```
class Room(models.Model):
    # ...
    building = models.ForeignKey(...)
class Group(models.Model):
    # ...
    teacher = models.ForeignKey(...)
    room = models.ForeignKey(...)
    subject = models.ForeignKey(...)
```

그리고 room과 subject 속성만 필요하다면, 이렇게 작성할 수 있다:

```
g = Group.objects.select_related('room', 'subject')
```

아래도 가능하다.
```
g = Group.objects.select_related('room__building', 'subject')
```
그리고 building 관계도 가져올 수 있다.

select_related에 전달 된 필드 목록에서 ForeignKey 또는 OneToOneField 관계를 참조 할 수 있습니다. 여기에는 null이 True 인 외래키가 포함된다(기본 select_related() 호출과 달리). 충돌하는 옵션이기 때문에 동일한 select_related() 호출에서 필드 목록과 깊이 매개 변수를 모두 사용하는 것은 오류이다.

select_related에 전달 된 필드 목록에서 OneToOneFields의 반대 방향을 참조 할 수도 있다. 즉, 필드가 정의 된 객체로 OneToOneField를 다시 가로 질러 탐색 할 수 있다. 필드 이름을 지정하는 대신 관련 오브젝트의 필드에 related_name을 하면 된다.

깊이 기반의 select_related를 수행하는 경우 OneToOneFields는 역방향으로 이동하지 않는다.


### Methods that do not return QuerySets
Queryset을 반환하지 않는 메소드


#### create

**create(\*\*kwargs)**

객체를 생성하고 저장을 한번에 하는 편리한 메소드. 

따라서:

```
p = Person.objects.create(first_name="Bruce", last_name="Springsteen")
```
과:
```
p = Person(first_name="Bruce", last_name="Springsteen") 
p.save(force_insert=True)
```
는 동일하다.


force_insert 매개 변수는 문서화되어 있지만 다른 모든 객체가 항상 만들어지는 것이다. 일반적으로 걱정할 필요가 없다. 그러나 모델에 수동으로 설정된 기본 키 값이 포함되어 있고 그 값이 데이터베이스에 이미 존재하면 기본 키가 고유해야하므로 create()를 호출하면 IntegrityError가 실패합니다. 따라서 수동 기본 키를 사용하는 경우 예외를 처리 할 준비가 되어 있어야한다.
