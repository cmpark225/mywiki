# Throttling

Throttling은 요청이 승인되어야 하는지를 결정한다는 점에서 권한과 유사하다. Throttle은 임시 상태를 나타내며, 클라이언트가 API에 할 수 있는 요청 속도를 제어하는 데 사용된다.

사용권한과 마찬가지로, 여러개의 throttle를 사용할 수 있다. API는 인증되지 않은 요청에 대해 제한 적인 throttle를 가질 수 있고, 인증된 요청에 대해서는 좀 더 적은 제한의 throttle을 가질 수 있다. 

여러개의 throttles를 사용할 수 있는 다른 시나리오는 일부 서비스가 특히 리소스를 많이 사용하기 때문에 API의 다른 부분에 서로 다른 제약 조건을 적용해야하는 경우다.

burst throttling rate 와 sustained throttling rate를 모두 적용하길 원할 경우에도 여러개의 throtlles를 사용할 수 있다. 예를 들어 1분마다 60번의 최대 요청을 제한하고, 하루에 1000번 요청을 제한할 수 있다

throttle이 반드시 속도 제한 요청을 참조하는 것은 아니다. 예를 들어 스토리지 서비스도 대역폭을 기준으로 조정해야 할 수 있으며, 유료 데이터 서비스는 액세스 중인 특정 수의 레코드에 대해 조정하기를 원할 수 있다.

## How throttling is determined

permissing과 authentication처럼, REST Framework의 throttling은 항상 클래스의 리스트로 정의된다.

뷰를 실행하기 전에 목록에 있는 throttle들이 점검된다. throttle이 검사에 실패하면 예외가 발생한다. throttle 된 예외가 발생하고 뷰의 본문이 실행되지 않는다.

## Setting the throttling policy

default throttling 정책은 DEFAULT_THROTTLE_CLASS와 DETFAULT_THROTTLE_RATES 세팅을 사용하여 전역적으로 설정된다.

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES' :(
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES':{
        'annon': '100/day',
        'user': '1000/day'
    }
}
```

DEFAULT_THROTTLE_RATES에 사용 된 rate 설명에는 throttle기간으로 second, minute, hour 또는 day가 포함될 수 있다.

또한 throttling 정책을 view 나 view를 기반으로한 APIView 클래스를 사용하여 viewset마다 설정할 수 있다. 

```
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

class ExampleView(APIView):
    throttle_classes = (UserRateThrottle, )

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }

        return Response(content)
```

또는 함수 기반의 viwew에서는 @api_view 데코레이터를 사용할 수 있다.

```
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None)
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

## How clients are identified

X-Forwarded-For 및 Remote-Addr HTTP 헤더는 throttling을 위한 클라이언트 IP 주소를 고유하게 식별하는 데 사용된다. X-Forwarded-For 헤더가 존재하면 사용되며, 그렇지 않으면 Remote-Addr 헤더가 사용된다.

고유 한 클라이언트 IP 주소를 엄격하게 식별해야하는 경우 먼저 NUM_PROXIES 설정을 설정하여 API가 실행되는 애플리케이션 프록시 수를 구성해야한다. 이 설정은 0이상의 integer이어야 한다. 0이 아닌 값이 설정될 경우 응용 프로그램 프록시 IP 주소가 먼저 제외 된 후 client IP가 X-Forwarede-For 헤더의 마지막 IP 주소로 식별된다. 0으로 설정될 경우, Remote-Addr 헤더가 식별 IP 주소로 항상 사용된다.

NUM_PROXIES 설정을 구성하면 고유 한 NAT 게이트웨이 뒤에있는 모든 클라이언트가 단일 클라이언트로 취급된다는 것을 이해해야한다.

X-Forwarded-For 헤더의 작동 방식 및 원격 클라이언트 IP 식별에 대한 추가 컨텍스트는 [여기](http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster)에서 찾을 수 있다

## Setting up the cache

REST 프레임 워크가 제공하는 throttle 클래스는 Django의 캐시 백엔드를 사용한다. 적절한 캐시 설정을 설정했는지 확인해야 한다. 간단한 설정의 경우 기본값인 LocMemCache도 괜찮다. 자세한 사항은 Django의 [cache](https://docs.djangoproject.com/en/dev/topics/cache/#setting-up-the-cache)를 확인해라

'default'가 아닌 다른 캐시를 사용해야하는 경우 사용자 정의 조절 클래스를 만들고 캐시 속성을 설정하면된다. 예:

```
class CustomAnonRateThrottle(AnonRateThrottle):
    cache = get_cache('alternate')
```
'DEFAULT_THROTTLE_CLASSES'설정 키에서 또는 throttle_classes 뷰 속성을 사용하여 사용자 정의의 throttle 클래스를 설정하려면 기억해야한다.

# API Reference

## AnonRateThrottle

AnonRateThrottle은 인증되지 않은 사용자만 throttle 한다. 들어온 요청의 IP 주소는 throttle 하기 위해 고유키를 생성하는데 사용된다.

허용된 요청률은 다음 중 한 가지(기본 설정 순서대로)에서 결정된다.
* 클래스의 rate 속성, AnonRateThrotle을 재정의하고 속성을 설정하여 제공할 수 있음.
* DEFAULT_THROTTLE_RATES['anon'] 설정
  
알 수없는 소스의 요청 비율을 제한하려는 경우 AnonRateThrottle이 적절하다

## UserRateThrottle

UserRateThrottle은 API에서 특정 비율의 요청으로 사용자를 제한한다. user id는 throttle 할 고유 키를 생성하는 데 사용된다. 인증되지 않은 요청은 들어오는 요청의 IP 주소를 사용하여 throttle 할 고유 키를 생성한다.

허용된 요청률은 다음 중 한 가지(기본 설정 순서대로)에서 결정된다.

* 클래스의 rate 속성, UserRateThrottle을 재정의하고 속성을 설정하여 제공할 수 있음.
* DEFAULT_THROTTLE_RATES['user'] 설정

API는 동시에 여러 UserRateThrotles를 사용할 수 있다. 이렇게 하려면 UserRateThrotle을 재정의하고 각 클래스에 대해 고유한 "scope"를 설정한다.

예를 들어, 다음 클래스를 사용하여 여러 사용자 스로틀 속도를 구현할 수 있다.

```
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'

```

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES':{
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

UserRateThrottle은 사용자 당 간단한 global rate 제한을 원하는 경우에 적합합니다.

## ScopedRateThrottle

ScopedRateThrottle 클래스를 사용하여 API의 특정 부분을 접근 제한할 수 있다. 이 throttle은 액세스중인 view에 .throttle_scope 속성이 포함 된 경우에만 적용된다. 고유한 throttle key는 요청의 'scope'를 고유한 사용자 id나 ip 주소에 연결하여 만든다.

허용된 요청 rate는 요청 "scope"의 키를 사용하여 DEFAULT_THROTTLE_RATES 설정에 의해 결정된다.

예를들어, 아래 view가 주어졌을때..

```
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...

class ContactDetailView(ApiView):
    throttle_scope = 'contacts'
    ...

class UploadView(APIView):
    throttle_scope = 'uploads'
    ...

```

```
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```

ContactListView나 ContactDetailView로의 사용자 요청은 하루에 총 1000번으로 제한될 것이다. UploadView의 사용자 요청은 하루에 10번으로 제한될 것이다.

# Custom Throttles

custom throttle을 만들기 위해서는, BaseThrottle을 재정의 하고 .allow_request(self, request, view)를 구현한다. 요청이 허용될 경우 메소드는 True를 아닐경우에는 False를 반환한다.

선택적으로 .waite() 메소드를 재정의할 수 있다. .wait()가 구현되었을 경우 다음 요청을 시도하기 전에 대기하는 권장 시간 (초)을 리턴하거나 None을 리턴해야한다. .allow_request()가 이전에 False를 반환 한 경우에만 .wait() 메서드가 호출된다.

## Example

아래 rate throttle 예제는, 10 개의 요청마다 1을 임의로 throttle 한다.
```
class RandomRateThrottle(throttles.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) == 1
```
