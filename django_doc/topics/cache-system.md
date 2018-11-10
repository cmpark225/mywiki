역동적인 웹 사이트의 근본적인 절충안은 동적인 것이다. site 방문자가 보는 페이지를 만들기 위해 사용자가 페이지를 요청할 때마다 웹서버는 모든 종류의 계산을 수행한다. - 데이터베이스 쿼리 부터 비지니스 로직의 템플릿 렌더링 까지- 이것은 표준 파일 시스템 서버 배열보다 프로세싱 오버헤드 관점에서 볼때 훨씬 비용이 나간다.

대부분의 웹 어플리케이션에서 이런 오버헤드는 큰 문제가 아니다. 대부분 웹 어플리케이션은 washingtonpost.com 이나 slashdot.org가 아니다. 그저 그런 트래픽을 가진 간단한 소-중 사이즈의 사이트들이다. 그러나 중대형 트래픽 사이트의 경우 가능한 많은 오버 헤드를 줄이는 것이 필수적이다. 

그것은 캐싱이 들어오는 곳이다. 

무언가를 캐시하는 것은 계산 비용의 결과를 저장하는 것이다. 그래서 다음번에 계산을 수행하지 않아도 된다. 아래 pseudocode는 어떻게 동적으로 웹페이지를 생성하는지를 설명한다. :
```
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache(for next time)
    return the generated page
```

Django에는 강력한 캐시 시스템이 있다. 이것은 동적인 페이지를 저장할 수 있게 해 각각의 리퀘스트마다 계산하지 않아도 된다. 편의상 Django는 다양한 수준의 캐시 세분성을 제공한다: 특정 뷰의 결과를 캐시할 수 있다. 생성하기 어려운 부분만 캐시 할 수 있다. 또는 완전한 사이트를 캐시 할 수 있다.

Django는 squid와 브라우저 캐시와 같은 "upstream" 캐시에서도 잘 동작한다. 이것들은 직접 제어하지 않지만 힌트를 제공 할 수 있는 캐시 유형이다. (HTTP Header를 통해)

## Setting up the cache
캐시 시스템은 작은 양의 설정만을 필요로 한다. 즉, 캐시된 데이터가 어디에 저장되어야 하는지 알려 줘야 한다. -데이터베이스인지, 파일시스템인지, 메모리에 직접 할 것인지. 이것은 캐시 성능에 영향을 미치는 중요한 결정이다. 그렇다 어떤 캐시 타입은 다른 것 보다 빠르다.

캐시 환경 설정은 설정 파일의 CACHES 설정에 있다. 다음은 캐시에 사용할 수 있는 모든 값에 대한 설명이다.

## Memcached
Django가 사용 할 수 있는 가장 빠르고 효율적인 캐시 유형, Memcached는 원래 LiveJournal.com에서 높은 부하를 처리하고 이후 Danga Interactive에서 오픈소스로 개발 한, 전적으로 메모리 기반 캐시 프레임워크이다. 이것은 Facebook과 Wikipedia 같은  site에서 데이터베이스 접근을 줄이고 극적으로 성능 향상을 위해 사용되었다.

Memcached는 홈페이지에서 자유롭게 이용가능하다. 데몬으로 실행되고 지정된 양의 RAM이 할당된다. 캐시에 있는 임의의 데이터를 추가, 검색 및 삭제 할 수 있는 빠른 인터페이스를 제공한다. 모든 데이터는 메모리에 직접 저장된다. 그래서 데이터베이스나 파일 시스템 사용에 오버헤드가 없다.

Memcached를 설치 한 후에는 memcached 바인ㅇ딩을 설치해야 한다. 사용 할 수 있는 파이썬 memcached 바인딩이 여러개 있다. 가장 일반적으로 python-memcached 와 pylibmc 두개가 있다. 


Django에서 Memcached 사용하기:
*  BACKEND에 'django.core.cache.backends.memcached.MemcachedCache'나 'django.core.cache.backends.memcached.PyLibMCCache'(선택한 memcached 바인딩에 따름)를 설정한다. 
*  LOCATION에 ip:port 값을 설정한다. ip는 Memcached 데몬의 IP주소, port는 memcached가 실행중인 포트이다. 또는 unix:path 값을 설정한다. path는 Memcached Unix socket file 이다.

예제에서, Memcached는 localhost(127.0.0.1)의 11211 포트에서 python-memcached 바인딩으로 실행중이다:
```
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache', 
        'LOCATION': '127.0.0.1:11211',
    }
}
``` 

예제에서, Memcached는 python-memcached 바인딩을 사용하는 로컬 유닉스 소켓 파일 /tmp/memcached.sock을 통해 사용할 수 있다.:
```
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.sock',
    }
}
```
Memcached의 뛰어난 기능 중 하나는 여러 서버에서 캐시를 공유 할 수 있다는 것이다. 이것은 여러대 머신에서 Memcached 데몬을 실행할 수 있다는 의미다. 그리고 프로그램은 머신 그룹을 각각의 머신에서 캐시 값을 복제 할 필요 없이 캐시 하나인 것 처럼 처리할 것이다. 이 기능을 이용하려면 모든 서버 주소를 LOCATION에 세미콜론이나 리스트로 구분 해서 포함하면 된다. 

예를들어, 캐시는 IP 주소 172.19.26.240과 172.19.26.242에서 실행중인 memcached 인스턴스에서 공유된다. 둘다 포트 11211 사용:
```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION':[
            '172.19.26.240:11211',
            '172.19.26.242:11211',
        ]
    }
}
```

아래 예에서, 캐시는 IP 주소 172.19.26.240 (포트 11211), 172.19.26.242 (포트 11212) 및 172.19.26.244 (포트 11213)에서 실행중인 Memcached 인스턴스에서 공유된다.
```
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '172.19.26.240:11211',
            '172.19.26.242:11211',
            '172.19.26.244:11213',
        ]
    }
}
```
Memcached에 대한 마지막 요점은 메모리 기반 캐싱에는 단점이 있다는 점이다.: 캐시 데이터는 메모리에 저장 되어있기 때문에 서버가 crache 되면 데이터를 잃게 된다. 분명 메모리는 영구적인 데이터 저장을 위한 것이 아니다. 그래서 유일한 데이터 저장소로 메모리 기반 캐싱에 의존하면 안된다. 의심할 것도 없이 Django 캐싱 백엔드 중 어느 것도 영구 저장을 위해 사용되서는 안된다 -- 그것들은 모두 저장을 위한 것이 아니라 캐싱을 위한 솔루션이다.-- 메모리 기반 캐싱이 특히 일시적이기 때문에 여기서 이를 지적한다. 

## Database caching
캐시 백엔드로 데이터베이스 테이블을 사용하려면, 우선 데이터베이스에 캐시 테이블을 생성한다. 아래 명령어 사용:
```
python manage.py createcachetable [cache_table_name]
```
[cache_table_name]은 생성하기 위한 데이터베이스의 테이블 이름이다. (이 이름은 데이터베이스에서 아직 사용되지 않고 있는 유효한 데ㅣ블 이름인 한 원하는 대로 사용 할 수 있다.) 이 명령어는 Django의 데이터 베이스 캐시 시스템이 기대하는 적절한 포맷으로 데이터 베이스의 테이블을 생성한다.
일단 그 테이블을 생성하면, BACKEND 세팅에 "django.core.cache.backends.db.DatabaseCache"를 설정하고 LOCATION에 테이블 이름을 설정한다 -- 데이터 베이스 이름은 아래 예에서 my_cache_table 이다:
```
CACHES = {
    'default':{
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
```
데이터베이스 캐싱 백앤드는 settings파일에 명시해둔 데이터 베이스와 동일한 데이터베이스를 사용한다. cache table은 다른 데이터베이스를 사용할 수 없다.

데이터베이스 캐싱은 빠르고 인덱스가 잘된 데이터베이스 서버를 가지고 있다면 가장 잘 동작한다.

#### Database caching and multiple databases
여러 데이터베이스에서 데이터베이스 캐싱을 사용하는 경우 데이터베이스 캐시 테이블에 대한 라우팅도 설정해야 한다. 라우팅을 위해 데이터베이스 캐시 테이블은 django_cache라는 응용 프로그램에 CacheEntry라는 모델로 나타낸다. 이 모델은 모델 캐시에 나타나지 않지만 모델 정보는 라우팅 목적으로 사용될 수 있다.

예를 들어, 다음 라우터는 모든 캐시 읽기 작업을 cache_slave로 지정하고 모든 쓰기 작업을 cache_master로 보낸다. 캐시 테이블은 cache_master로 부터만 싱크될 것이다.:

```
class CacheRouter(object):
    """A router to control all database cache operations"""

    def db_for_read(self, model, **hints):
        "all cache read operations go to the slave"
        if model._meta.app_label in ('django_cache', ):
            return 'cache_slave'
        return None

    def db_for_write(self, model, **hints):
        "All cache write operations go to master"
        if model._meta.app_label in ('django_cache',):
            return 'cache_master'
        return None

    def allow_syncdb(self, db, model):
        "Only synchronize the cache model on master"
        if model._meta.app_label in ('django_cache',):
            return db == 'cache_master'
        return None
```
데이터베이스 캐시 모델에 대한 라우팅 경로를 지정하지 않으면 캐시 백엔드는 기본 데이터베이스를 사용한다.

물론 데이터베이스 캐시 백엔드를 사용하지 않는 다면 데이터베이스 캐시 모델에 대한 라우팅 지침 제공에 대해 걱정할 필요가 없다.
