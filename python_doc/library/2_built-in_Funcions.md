

## filter(function, iterable)

function이 리턴 값이 true인 iterable 요소로 리스트를 구성.

function이 None일 경우에는 iterable 요소 중  false인 값이 제거된 리스트를 반환한다.
```
>>> a = [1,0,2,3,0,4,0,5]
>>> filter(None, a)
[1, 2, 3, 4, 5]
```

만약 iterable이 string이나 tuple일 경우 동일한 타입을 반환한다. 그 외에는 리스트 반환.
```
>>> filter(None, 'abcdef')
'abcef' 
>>> filter(None, (1,0,2,0,0,0,3,4,5))
(1, 2, 3, 4, 5)
```

filter(function, iterable)은 [item for item in iterable if function(item)] 과 동일하다. 

function이 None일 경우에는 [item for item in iterable if item] 와 동일하다. 


## map(function, iterable, ...)
모든 iterable 아이템에 function을 적용하여 반환한다. 

iterable 인수는 시퀀스나 반복 가능한 객체일 수 있다. 

여러 개의 인수가있는 경우 map ()은 모든 iterable (변환 작업의 일종)에서 해당 항목을 포함하는 튜플로 구성된 목록을 반환한다. 

한 iterable이 다른 itereable 보다 짧을 경우는 None 항목으로 구성된다.

```
>>> a = [1,2,3,4,5]
>>> b = [1,2,3]
>>> map(None, a, b)
[(1, 1), (2, 2), (3, 3), (4, None), (5, None)]
```

결과는 항상 list다.


## reduce(function, iterable[, initializer])

```
>>> reduce(lambda x, y: x*y, [1,2,3])
6

>>> reduce(lambda x, y: x*y, [1,2,3], 'a')
'aaaaaa'
```
> initializer가  None가 아닐 경우 최초 x에 initializer값이 들어간다.
> 
> 이후 누적된 값이 x로 적용된다. ((('a' * 1) * 2) *3) = 'aaaaaa'


반복 가능 항목을 왼쪽에서 오른쪽으로 누적 적으로 두 개의 인수의 함수를 적용하여 반복 가능한 값을 단일 값으로 줄인다. 예를들어 reduce(lambda x, y: x*y, [1, 2, 3, 4, 5])는 ((((1*2)*3)*4)*5)를 계산한다. x는 누적된 값이고, y는 iterable의 업데이트 값이다. initializer가 있을 경우에는 iterable의 항목 앞에 위치한다.

 대략 아래처럼 동작한다.

```
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial vlaue')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
    return accum_value
```
