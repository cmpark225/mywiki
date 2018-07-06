## 8.3.1 Counter objects.

counter는 편리하고 빠른 집계를 제공한다.

```
>>> # Tally occurrences of words in a list
>>> from collections import Counter
>>> cnt = Counter()
>>> for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
...     cnt[word] += 1
>>> cnt
Counter({'blue': 3, 'red': 2, 'green': 1})

>>> # Find the ten most common words in Hamlet
>>> import re
>>> words = re.findall(r'\w+', open('hamlet.txt').read().lower())
>>> Couter(words).most_common(10)
[('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631),
 ('you', 554),  ('a', 546), ('my', 514), ('hamlet', 471), ('in', 451)]
```

## class collections.Counter([iterable-or-mapping])

Counter는 해시 가능한 객체를 계산하기 위한 dictionary의 하위 클래스이다.
elements는 dircionary 키로 저장되고, counts는 dictionary 값으로 저장되는 정렬되지 않은 collection 이다. 

카운터는 없는 아이템에 KeyError 대신 0을 반환하는것을 제외하고는 딕셔너리 인터페이스를 가진다.

```
>>> c = Counter(['eggs', 'ham'])
>>> c['bacon']
0
```

Counter에서 elements를 제거하기 위해서는 del을 사용해야 한다. (0으으로 세팅 안됨)
```
>>> del c['sousage']
```
Counter objects는 dictionary 에서 추가로 세개 메소드를 지원한다.

#### elements()
카운트만큼 반복하는 요소에 대한 반복자를 반환. 요소는 임의의 순서로 반환. element의 수가 1보다 작으면 elements()는 무시된다..
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c.elements()
<itertools.chain object at 0x7fb1fcc09310>
>>> list(c.elements())
['a', 'a', 'a', 'a', 'b', 'b']

```

#### most_common([n])
가장 count가 높은 순부터 낮은 순의 n개의 리스트를 반환한다.
n이 생략되거나 None일 경우에는 most_common()은 모든 elements를 반환한다.
동일할 경우에는 임의로 정렬된다.
```
>>> Counter('abracadabra').most_common(3)
[('a', 5), ('r', 2), ('b', 2)]
```

#### subtract([iterable-or-mapping])
iterable or mapping or count에서 count를 뺀다. 
입력 출력 보두 0거나 음수일 수 있다.
(c-d는 결과값으로 음수는 제외한다. )

```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> d = Counter(a=1, b=2, c=3, d=4)
>>> c.subtract(d)
>>> c
Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
```

아래 두개 메소드는 Couters에서 다르게 동작한다.

####  fromkeys(iterable)
해당 메소드는 Counter 에서 구현 안됨
```
>>> c = Couter(a=4, b=2, c=0, d=-2)
>>> c.fromkeys([1, 2, 3])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/collections.py", line 526, in fromkeys
    'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')
NotImplementedError: Counter.fromkeys() is undefined.  Use Counter(iterable) instead.
```

#### update([iterable-or-mapping])
dictionary에서 update할 경우 동일한 키에 대해서 값이 변경되지만, 

Counter에서는 키에 대해 count 되서 저장된다.
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c.update(['a', 'b', 'c'])
>>> c 
Counter({'a': 5, 'b': 3, 'c': 1, 'd': -2})
```

## Counter 객체 작업을 위한 일반적인 패턴:

##### sum(c.values()) 
: total of all counts
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> sum(c.values())
4
```
##### c.clear() 
: reset all counts
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c.clear()
>>> c
Counter()
```
##### list(c) 
: list unique elements
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> list(c)
['a', 'c', 'b', 'd']
```
##### set(c) 
: convert to a set
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> set(c)
set(['a', 'c', 'b', 'd'])
```
##### dict(c) 
: convert to a regular dictionary
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> dict(c)
{'a': 4, 'c':0, 'b':2, 'd':-2}
```
##### c.items() 
: convert to a list of (elem, cnt) pairs
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c.items()
[('a', 4), ('c', 0), ('b', 2), ('d', -2)]
```

##### Counter(dict(list_of_pairs))
: convert from a list of (elem, cnt) pairs
```
>>> c = Counter(dict([('a', 4), ('b', 2), ('c', 0), ('d', -2)]))
>>> c
Counter({'a': 4, 'b': 2, 'c': 0, 'd': -2})
```

##### c.most_common()[:-n-1:-1] 
: n least common elemnets
```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c
Counter({'a': 4, 'b': 2, 'c': 0, 'd': -2})

>>> c.most_common()[:-1-1:-1]
[('d', -2)]
>>> c.most_common()[:-2-1:-1]
[('d', -2),('c', 0)]
```


##### c += Counter() 
: remove zero and negative counts

Counter에서 + 연산 할 경우 결과 값으로 양수만 나오니까
빈 Counter를 더해주면 zero랑 음수를 제거할 수 있다.

```
>>> c = Counter(a=4, b=2, c=0, d=-2)
>>> c
Counter({'a': 4, 'b': 2, 'c': 0, 'd': -2})
>>> c += Couter()
>>> c
Counter({'a': 4, 'b': 2})
```

여러 수학 연산을 사용해 Counter 객체를 결합하여 multisets를 생성한다. 
각 연산은 부호가 있는 숫자를 입력으로 받을 수 있지만, 결과는 0보다 작거나 같은 값을 제외하여 출력한다.

```
>>> c = Counter(a=3, b=1)
>>> d = Counter(a=1, b=2)
>>> c + d               # add two counter together: c[x] + d[x]
Counter({'a': 4, 'b':3})
>>> c - d               # subtract (keeping only positive counts)
Counter({'a':2})
>>> C & d               # min(c[x], d[x])
Counter({'a': 1, 'b': 1})
>>> C | d               # max(c[x], d[x])
Counter({'a': 3, 'b': 2})
```
