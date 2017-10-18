# Making queries

Django는 당신이 create, retrieve, update, delete 오브젝트 할 수 있도록 API를 제공한다.  이 문서는 어떻게 이 API를 사용할 수 있는지를 설명한다.

```
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __unicode__(self):
        return self.headline
```

## creating objects

Django는 직관적인 시스템을 사용한다 : 모델 클래스는 데이터베이스 테이블을,  해당 클래스의 instance는 데이터베이스 테이블의 특정한 레코드를 표현한다.

```
>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()
```

해당 작업은 INSERT SQL을 수행한다. Django는 당신이 save() 하기 전까지 database에 반영하지 않는다.
save() 메소드는 return 값이 없다. 

object 생성과 save 를 한번에 처리하기 위해서는 ‘create()’  메소드를 사용해라.


## saving changes to objects

 이미 데이터베이스에있는 객체의 변경 사항을 저장하려면 save ()를 사용해라.

```
>> b5.name = 'New name'
>> b5.save()
```

해당 작업은 UPDATE SQL을 수행한다. Django는 당신이 save() 하기 전까지 database에 반영하지 않는다.


### Saving ForeignKey and ManyToManyField fields

## Retrieving objects

QuerySet은 데이터베이스의 오브젝트의 컬렉션을 표현한다.
QuerySet은 모델 매니저를 사용해 얻을 수 있다. 각 모델은 objects라고 부르는 매니저를 최소한 한개는 가진다.     objects 매니저는 모델 클래스를 사용해서 직접적으로 접근할 수 있다.

```
>>> Blog.objects
<django.db.models.manager.Manager object at ...>
>>> b = Blog(name='Foo', tagline='Bar')
>>> b.objects
Traceback:
    ...
AttributeError: "Manager isn't accessible via Blog instances."
```

모델 매니저는 모델의 데이터 베이스 테이블의 모든 objects인 ‘root’ Query Set으로 동작한다.


### Retrieving all obejcts

테이블에서 오브젝트를 가져오는 가장 간단한 방법은 모든 오브젝트를 가져오는 것이다. 
이럴때 매니저를 통해 all() 메소드를 사용한다.

```
>>> all_entries = Entry.objects.all()
```

all() 메소드는 데이터베이스의 모든 오브젝트의 쿼리셋을 반환한다.


### Retrieving specific objects with filters

Queryset을 오브젝트의 완전한 subset으로 정제한다. 
subset을 생성하기 위해서는 filter 조건을 추가하여 QuerySet을 정의 해야 한다.
가장  흔한 두가지 방법은 filter, exclude가 있다.

1. filter(**kwargs)
:파라미터와 매치하는 queryset 반환
2. exclude(**kwargs)
: 파라미터와 매치하지 않는 queryset 반환

ex)

```
Entry.objects.filter(pub_date__year=2006)
```

all()을 추가할 필요가 없다.(ex -- Entry.objects.all().filter(.....). ) 이것은 동작하겠지만, all()은 루트 queryset으로 부터 모든 오브젝트를 얻기 원할때만 필요하다.



#### Chaining filters

정제된 queryset 결과는 queryset이기 대문에 chain이 가능하다.

```
>>> Entry.objects.filter(
...     headline__startswith='What'
... ).exclude(
...     pub_date__gte=datetime.now()
... ).filter(
...     pub_date__gte=datetime(2005, 1, 1)
... )
```

 데이터베이스의 모든 항목에 대한 초기 QuerySet을 가져 와서 필터를 추가 한 다음 제외 항목을 추가 한 다음 다른 필터를 추가 한다. 최종 결과는 ‘What’으로 시작하는 headline, 2005-01-01 ~ 오늘날짜의 pub_date을 포함한 QuerySet이다. 
(왜 root QuerySet에서 Filter 검색으로  chain 하면 and 이고, multi-value 에서는 or이 되는거지)


#### Filtered QuerySets are unique

QuerySet을 정의할 때마다 이전 QuerySet에 바인딩 된 새로운 QuerySet을 얻게 된다. 각 상세 검색은 저장되고 사용되며 재사용될 수 있는 별개의 고유 한 QuerySet을 생성한다.

ex)

```
>> q1 = Entry.objects.filter(headline__startswith="What")
>> q2 = q1.exclude(pub_date__gte=datetime.now())
>> q3 = q1.filter(pub_date__gte=datetime.now())
```

3개의 QuerySet이 있다. 첫 번째 QuerySet은  headline이 “What”으로 시작하는 정보의 모든 것을 포함한다. 두번째 QuerySet은 첫번째 Queryset 의 하위 집합이며, pub_date가 현재보다 큰 레코드를 제외하는 추가적인 조건이 있다. 세번째 QuerySet은 첫번째 QuerySet의 하위 집합이며, pub_date가 현재보다 큰 레코드를 가지는 추가조건이 있다. 초기의 QuerySet q1은 추가적인 작업에 영향을 받지 않았다.

 

#### QuerySets are lazy




### Retrieving a Single object with get

쿼기에 매칭되는 한개의 object만 있더라도 .filter() 는 항상 QuerySet을 반환한다. - 이렬 경우에는 QuerySet이 한개의 element만 포함한다

```
>>> one_entry = Entry.objects.get(pk=1)
```

filter()와 같은 방식으로  get()을 사용하여 어떤 query  표현식을 사용할 수 있다.

.get()을 사용하는 것가 sliice [0]의 .flter()를 사용하는 것의 차이점에 대해서 주의해야 한다. 만약 query에 매칭되는 결과가 없을 경우, .get()은 DoesNotExist exception을 발생시킨다. 이 예외는 쿼리가 수행되는 모델 클래스의 속성이다.

이와 유사하게 get() 쿼리에 한개 이상의 매칭되는 아이템을 가질 경우 MultipleObjectsReturned, 예외를 발생시킨다.

### Limiting QuerySets

Python의 array-slicing 문법을 사용해 QuerySet을 특정 수의 결과로 제한해라. 이것은 SQL의 LIMIT과 OFFSET 과 동일하다. 

 예를들어 아래 예문는 처음 5개 오브젝트를 반환한다(LIMIT 5):

```
>>> Entry.objects.all()[:5]
```

6~10번째 object를 반환한다.

```
>>> Entry.objects.all()[5:10]
```


음수로 된 인덱싱 ex) Entry.objects.all()[-1]) 은 지원하지 않는다.
일반적으로 slicing된 QuerySet은 새로운 QuerySet을 반환한다. 
