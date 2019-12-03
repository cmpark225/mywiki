# Signals

Django는 내장 코드 세트를 제공하여 Django 자체에서 특정 동작을 사용자 코드에 알릴 수 있다. 여기에는 몇 가지 유용한 알림이 포함된다:

* django.db.models.signals.pre_save & django.db.models.signals.post_save
  * 모델의 save() 메소드가 호출되기 전이나 후에 전송
* django.db.models.signals.pre_delete & django.db.models.signals.post_delete
  * 모델의 delete() 메소드가 호출되기 전이나 후에 전송
* django.db.models.signals.m2m_changed
  * 모델의 ManyToManyField가 변동되었을때 전송
* django.core.signals.request_started & django.core.signals.request_finished
  * HTTP 요청이 시작되거나 종료되었을때 전송

전체 목록과, 각 신호에 대한 자세한 설명은 [built-in signal documentation](https://django.readthedocs.io/en/1.3.X/ref/signals.html)에서 볼 수 있다.

[define and send your own custom signals](https://django.readthedocs.io/en/1.3.X/topics/signals.html#defining-and-sending-signals)도 볼 수 있다.

## Listening to signals
signal을 받기 위해, Signal.connect()메소드를 사용하여 signal이 보내졌을때 호출을 받기 위한 *receiver* 함수를 등록해야한다.
**Signal.connect(**receiver[, sender=None, weak=True, dispatch_uid=None])
Parameter
* receiver - singal에 연결되는 callback function.자세한 내용은 [Receiver functions](https://django.readthedocs.io/en/1.3.X/topics/signals.html#receiver-functions) 참조 
* sender
* weak
* dispatch_uid
  
각 HTTP 요청이 끝난 후 호출되는 signal 등록하여 이것이 어떻게 동작하는지 보자. request_finished 신호에 연결한다.

### Receiver functions
먼저, receiver 함수 정의가 필요하다. receiver는 어느 Python 함수나 메소드일 수 있다. 

```
def my_callback(sender, **kwargs):
    print 'Request finished!'
```

함수가 와일드카드 키워드 인수와 함께(**kwargs), sender 인자를 가지는 것을 확인해라 ; 모든 signal 핸들러는이 인수를 사용해야한다.

senders는 이후에 확인하고, 먼저 **kwargs 인자부터 확인한다. 모든 singal은 keyword 인자를 보내고, keyword 인자는 매번 달라질 수 있다. request_finisned의 경우, 인수를 보내지 않는 것으로 문서화되어 signal 처리를 my_callback(sender)로 작성하고 싶을 수 있다.

이것은 잘못된 것이다. 이렇게 하면 사실 Django는 error를 발생할 것이다. 어떤 시점에서든 인수가 signal에 추가 될 수 있고 receiver가 새로운 인수를 처리 할 수 ​​있어야하기 때문이다.

### Connectiong receiver functions
signal을 receiver에 접속할 수 있는 두가지 방법이 있다. 직접 접속 경로를 작성할 수 있다:

```
from django.core.signals import request_finished
request_finished.connect(my_callback)
```
또는, receiver를 정의할때 receiver 데코레이터를 사용할 수 있다:

```
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(reqest_finished)
def my_callback(sneder, **kwargs):
    print "Request finished"
```

이제 각 request가 끝날때 my_callback 함수는 호출될 것이다. 

> Where should this code live?

### Connecting to signals sent by specific senders
특정 sender가 보낸 신호에 연결

일부 신호는 여러번 전송된다, 하지만 이런 signal의 하위집합만 수신하길 원할것이다. 예를들어, django.db.models.signals.pre_save 신호는 모델이 저장되기 전에 보낸다. 대부분의 경우 모델이 저장되는시기를 알 필요가 없고, 특정 모델이 저장 될 때만 알기 원한다.

이런 경우, 특정 senders가 보낸 신호를 받기 위해 등록 할 수 있다. django.db.models.signals.pre_save의 경우, sender는 저장되는 모델 클래스가 되므로, 특정 모델로 부터 보내진 원하는 signal 나타낼 수 있다:

```
from django.db.models.signals import pre_save
from django.dispatch import receiver
from myapp.models import MyModel

@receiver(pre_save, sender=MyModel)
def my_handler(sender, **kwargs):
    ...
```

MyModel의 인스턴스가 저장될때만 my_handler 함수는 호출될 것이다.

다른 신호는 다른 개체를 발신자로 사용한다. 각 특정 신호에 대한 자세한 내용은 [buil-in signal documentation](https://django.readthedocs.io/en/1.3.X/ref/signals.html) 참조


### Preventing duplicate signals

경우에 따라, signal을 연결하는 모듈을 여러 번 가져올 수 있다. 이것은 receiver 함수가 한번 이상 등록될 수 있고, 단일 signal 이벤트에 대해 여러번 호출될 수 있다.

만약 이런 행위가 문제를 야기할 수 있을 경우(모델이 저장될때마다 email을 보내기 위해 signal을 사용할 경우), receiver 함수를 식별하기 위해 dispatch_uid 인자와 같은 고유의 식별자를 전달한다. 이런 식별자는 대게 문자열이지만, 해시 가능한 객체이면 충분하다. 결과적으로 receiver함수는 각 독득한 dispatch_uid 값에 대해 한번만 신호에 바인딩 된다.

```
from django.core.signals import request_finished

request_finished.connect(my_callback, dispatch_uid='my_unique_identifier')
```

## Defining and sending signals


애플리케이션은 signal 인프라를 활용하고 자체 signal을 제공 할 수 있다.

## Defining signals

class **Signal([providing_args=list])**
모든 signal은 django.dispatch.Signal 인스턴스이다. providing_args는 signal이 리스너에게 제공할 인수 이름의 목록이다. 

예:
```
import django.dispatch

pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])
```

이것은 수신자에게 'toppings'와 'size'인수를 제공 할 pizza_done signal을 선언한다.


언제든지 이 인수 목록을 변경할 수 있으므로 첫 번째 시도에서 API를 가져 오는 것이 필요하지 않다.


### Sending signals

send signal을 전송하기 위한 두가지 방법이 있다.

**Signal.send(sender, **kwargs)**
**Signal.send_robust(sender, **kwargs)**

signal을 전송하기 위해서는 Signal.send()나 Signal.send_robust()를 호출해야 한다. 
sender 인수를 제공해야하며 원하는 만큼 다른 키워드 인수를 제공 할 수 있다.

예를들어, pizza_done signal를 보내는 방법은 다음과 같다:
```
class PizzaStore(object):
    ...

    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self, toppings=toppings, size)

```
send()와 send_robust()는 호출 된 receiver 함수 와 응답 값의 목록을 나타내는 튜플 쌍 [(receiver, response), ...]의 리스트를 리턴한다.

send()는 receiver 함수로 부터 발생한 exception을 처리하는 방법에서 send_robust()와 다르다. send()는 receiver로 부터 발생한 예외에 대해 catch하지 않는다; 단순히 오류가 전파되는것을 허용한다. 따라서 모든 receiver에 오류가 발생했을 때 signal이 표시되는 것은 아니다.(?)

send_robust()는 python의 Exception 클래스로부터 파생된 모든 에러를 catch하고, 모든 receiver가 signal을 알아채는 것을 보장한다. 만약 에러가 발생하면, 에러 인스턴스는 오류가 발생한 receiver의 tuple 쌍안에 반환된다.

## Disconnectiong signals
**Signal.disconnect([**receiver=None, sender=None, weak=True, dispatch_uid=None])

signal로부터 receiver를 연결을 끊기 위해서, Signal.disconnect()를 호출한다. 인수는 Signal.connect ()에 설명되어 있다.

receiver 인수는 연결을 끊기 위해 등록된 receiver를 가리킨다. dispatch_uid가 receiver를 식별하기 위해 사용된다면 None일 수 있다.



