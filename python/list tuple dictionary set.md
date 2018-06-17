# list 

리스트는 변경 가능하다. 리스트의 현재 위치에서 새로운 요소를 추가하거나 삭제 혹은 기존 요솔ㄹ 덮어쓸 수 있다.

### 리스트 생성
[], list()을 이용해 리스트를 생성할 수 있다.

```
>>> empty_list = []
>>> weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

>>> another_empty_list = list()
```

### 다른 데이터 타입을 리스트로 변환하기.
하나의 단어를 한 문자 문자열의 리스트로 변환
```
>>> string_list = list('like')
>>> string_list
['l', 'i', 'k', 'e']
```
문자열을 구분자로 나누어 리스트로 변환 
```
>>> day = '1/6/2018'
>>> day.split('/')
['1', '6', '2018']
```

튜플을 리스트로 변환
```
>>> a_tuple = ('ready', 'fire', 'aim')
>>> list(a_tuple)
['ready', 'fire', 'aim']
```

### [offset]으로 항목 얻기
리스트는 오프셋으로 하나의 특정 값을 추출할 수 있다. 
```
>>> marxes = ['Groucho', 'Chico', 'Harpo']
>>> marxes[1]
'Chico'
>>> marxex[-1]
'Harpo'
```


