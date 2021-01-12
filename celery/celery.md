# What's a Task Queue?

Task queues는 스레드 또는 시스템에서 작업을 분배하는 메커니즘으로 사용된다.

task queue의 입력은 task라고 불리는 작업의 유닛이다. 전용 worker 프로세스는 새 작업을 수행하기 위해 지속적으로 task queue를 모니터링한다.

Celery는 메시지를 통해 통신하며, 대개 브로커를 사용하여 클라이언트와 작업자를 중재한다. 클라이언트가 task을 시작하기 위해 큐에 메시지를 추가하면 브로커는 해당 메시지를 작업자에게 전달한다.

Celery 시스템은 여러 작업자와 브로커로 구성되어 고 가용성 및 수평 확장을 제공한다.


핸들러(django)-> 브로커(Redis) -> 워커(celery)

Celery는 메시지 송수신을 위해 message transport가 필요하다. 

# Application
우선 Celery instans가 필요하다. 우리는 Celery application 또는 그냥 짧게 app이라고 부른다. 이 인스턴스는 작업 생성 및 작업자 관리와 같이 Celery에서 수행하려는 모든 작업의 ​​시작점으로 사용되므로 다른 모듈에서 가져 오기가 가능해야한다.

Celery 첫번째 인자는 현재 모듈의 이름이다. 이 이름은 tasks가 \_\_main__ 모듈에 정의될 때 자동으로 생성되기 위해서만 필요하다. 

두번째 인자는 사용하려는 message broker의 URL을 지정하는 broker keyword이다. 

application은 thread-safe 하기 때문에, 여러 celery appliaction은 구성, 구성 요소 및 작업이 다른 여러 Celery 응용 프로그램이 동일한 프로세스 공간에 존재할 수 있다.

```
>>> from celery import Celery
>>> app = Celery()
>>> app
<Celery __main__:0x100469fd0>
```

마지막 라인은 application의 문자열 표현을 보여준다.: app class의 이름 (Celery), 현재 메인 모듈의 이름(\_\_main__), object의 메모리 주소 (0x100469fd0)

## Main Name 

Celery에서 task를 전송할 때, message는 어떤 소스 코드를 포함하지 않는다, 실행하기를 원하는 task의 이름만 포함한다.이것은 인터넷에서 host name이 동ㅈ가하는 방식과 비슷하다: 모든 worker는 task 이름을 *task registry*라는 실제 기능에 매핑한다.

task를 정의할때마다, 해당 task는 local registry에도 추가된다.:

```
>>> @app.task
... def add(x, y):
...     return x+y

>>> add
<@task: __main__.add>

>>> add.name
__main__.add

>>> app.tasks['__main__.add']
<@task: __main__.add>
```
Celery가 해당 기능이 속한 모듈을 감지 할 수 없을 때마다 기본 모듈 이름을 사용하여 task 이름의 시작을 생성한다.

제한된 사용 사례에서만 발생하는 문제가 있다.

1. 작업이 정의 된 모듈이 프로그램으로 실행되는 경우
2. 애플리케이션이 Python shell(REPL)로 작성된 경우


예를 들어, 여기서 tasks 모듈은 app.worker_main()으로 worker를 시작하는데도 사용된다.

tasks.py
```
from celery import Celery
app = Celery()

@app.task
def add(x, y): return x + y

if __name__ == '__main__':
    app.worker_main()
```

이 모듈이 실행될때 tasks는 __main__으로 시작되는 이름이 될 것이다, 

```
$ celery worker -A tasks --loglevel=INFO
 -------------- celery@UD-user v3.1.23 (Cipater)
---- **** ----- 
--- * ***  * -- Linux-4.15.0-109-generic-x86_64-with-Ubuntu-18.04-bionic
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         __main__:0x7fb67cd6d390
- ** ---------- .> transport:   redis://127.0.0.1:6379/0
- ** ---------- .> results:     redis://127.0.0.1:6379/0
- *** --- * --- .> concurrency: 8 (prefork)
-- ******* ---- 
--- ***** ----- [queues]
 -------------- .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . task.add

================================
print add 
<@task: task.add of __main__:0x7fb67cd6d390>
```

하지만 다른 프로세스에서 모듈을 가져 오면 task을 호출 할 때 task 이름이 "tasks"(모듈의 실제 이름)로 시작한다. :
```
>>> from tasks import add
>>> add.name
'task.add'
```

특정 다른 이름을 main module에 명시할 수 있다:

```
>>> app = Celery('tasks')
>>> app.main
'tasks'

>>> @app.task
... def add(x, y):
...     return x+y

>>>> add.name
'tasks.add'
```


## Calling the task
task를 호출하기 위해 delay() method를 사용할 수 있다.

```
>>> from tasks import add
>>> add.delay(4, 4)
```

task 호출은 AsyncResult 인스턴스를 리턴한다. 이 인스턴스는 task의 상테 체크나, task가 종료되기를 기다리거나, 리턴되는 값을 얻을때 사용할 수 있다.(혹은 task가 실패했을 때 exception과 traceback을 가져올때)



