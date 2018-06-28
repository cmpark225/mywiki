## difference between filter and map

filter는 
[x for x in a if f(x)]
조건에 따라 참인 요소를 리스트에 포함 시킴.
iterable 요소 값에 변동이 없다.


map은
[f(x) for x in a]
함수를 적용 시킨 값의 리스트
iterable 요소 값이 함수 적용된 값으로 새로운 리스트를 반환.

```
>>> def f(x):
...     return x*x
>>> a = [1,2,3,4,5]
>>> filter(f, a)
[1, 2, 3, 4, 5]
>>> map(f, a)
[1, 4, 9, 16, 25]
```


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
여러 개의 인수가있는 경우 map ()은 모든 iterable (변환 작업의 일종)에서 해당 항목을 포함하는 튜플로 구성된 목록을 반환한다. 한 iterable이 다른 itereable 보다 짧을 경우는 None 항목으로 구성된다.

```
>>> a = [1,2,3,4,5]
>>> b = [1,2,3]
>>> map(None, a, b)
[(1, 1), (2, 2), (3, 3), (4, None), (5, None)]
```

결과는 항상 list다.
