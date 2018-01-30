* class threading.local *

thread 로컬 데이터를 나타내는 클래스. 스레드 로컬 데이터는 값이 스레드에 특정한 데이터다. 스레드 로컬 데이터를 관리하려면 로컬 (또는 하위 클래스)의 인스턴스를 만들고 속성을 저장한다.

```
mydata = threading.local()
mydata.x = 1
```

인스턴스의 값은 개별 스레드마다 다르다.

=> 현재 스레드(current_thread())에 해당 인스턴스에 대해서 데이터 저장이 가능하다.
인스턴스 생성 시 current_thread()__dict__에 해당 인스턴스의 id를 키로 만들어 값을 저장하기 때문에
(key = 'local_key', 'thread.local.' + str(id(self))) 
동일한 스레드에서 인스턴스를 여러개 생성할 경우 각 인스턴스마다 값이 달라질 수 있다.

