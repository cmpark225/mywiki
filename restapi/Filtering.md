# Generic Filtering
기본 queryset을 재정의 할 수 있을뿐만 아니라 REST 프레임워크는 복잡한 검색 및 필터를 쉽게 구성 할 수 있는 일반 필터링 백엔드를 지원한다.

## Setting filter backends
전역으로 기본 filter backend를 사용하려면 settings의 DEFAULT_FILTER_BACKENDS를 설정한다. 예:
```
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackends',)
}
```
view를 기반으로 한 GenericAPIView를 이용해 뷰 또는 viewset마다 필터 백엔드를 설정할 수 있다. 
```
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import filters
from rest_framework import generics

class UserListView(generics.ListAPIView):
    queryset = User.objcets.all()
    serializer = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
```

# API Guide
## DjangoFilterBackend

DjangoFilterBackend 클래스는 [django-filter package](https://github.com/carltongibson/django-filter/tree/0.5.4)를 사용하여 높은 수준의 필드 필터링 사용자 정의가 가능하다.

REST 프레임워크의 DjangoFilterBackend를 사용하기 위해서는 django-filte를 설치해야 한다.

```
pip install django-filter
```

### Specifying filter fields

필요한 것은 간단한 equality-based 필터링이다. 필터링 할 필드 집합을 나열하는 view 또는 viewset에 filter_fields 속성을 설정할 수 있다.
```
class ProductList(generics.ListAPIview):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ('category', 'in_stock')
```
이것은 주어진 필드로 자동으로 FilterSet 클래스를 만들어준다.그리고 아래와 같은 요청을 할 수 있다.:
```
http://example.com/api/products?category=clothig&in_stock=True
```

### Specifying a FilterSet
고급 필터링 요구 사항의 경우 뷰에서 사용해야하는 FilterSet 클래스를 지정할 수 있다. 예 :
```
import django_filters
from myapp.models import Product
from myapp.serializers import ProductSerializer
from rest_framework import generics

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name='price', lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    class Meta:
        model = Product
        fields = ['category', 'in_stock', 'min_price', 'max_price']


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_class = ProductFilter
```
이는 아래와 같은 요청을 할 수 있다:
```
http://example.com/api/products?category=clothing&max_price=10.00
```

 django-filter를 사용해 관계를 확장할 수 있다. 각 Product가 Manufacturer 모델의 외래키를 가지고 있다고 가정할때 Manufacturer 이름을 사용하여 필터링하는 필터를 만든다. 예:

```
 import django_filters
 from myapp.models import Product
 from myapp.serializers import ProductSerializer
 from rest_framework import generics

 class ProductFilter(django_filters.FilterSet):
     class Meta:
         model = Product
        fields = ['category', 'in_stock', 'manufacture__name']
```
이는 아래와 같이 호출할 수 있다.:
```
http://example.com/api/products?manufacturer__name=foo
```

이것은 좋은 일이지만 Django의 이중 밑줄 규칙을 API의 일부로 나타낸다. 대신 명시적으로 필터 인수의 이름을 지정하려면 FilterSet 클래스에 필터 인수를 명시적으로 포함시킬 수 있다.
```
import django_filters
from myapp.models import product
from myapp.serializers import ProductSerializer
from rest_framework import generics

class ProductFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(name="manufacturer__name")

    class Meta:
        model = Product
        fields = ['category', 'in_stock', 'manufacturer']
```
그리고 아래와 같이 호출할 수 있다.
```
http://example.com/api/products?manufacturer=foo
```


## OrdringFilter
OrderingFilter 클래스는 간단한 쿼리 매개 변수로 제어된 결과 정렬을 지원한다. 기본적으로 쿼리 매개 변수의 이름은 'ordering'이지만, ORDERING_PARAM 설정으로 재정의할 수 있다.

예를들어. username으로 user 정렬:
```
http://example.com/api/users?ordering=username
```

클라이언트는 필드네임에 prefix로 '-'을 표기하여 역순으로 정렬할 수 있다.:
```
http://example.com/api/users?ordering=-username
```

여러개도 명시할 수 있다:
```
http://example.com/api/users?ordering=account, username
```

### Specifying which fields may be ordered against
ordring filter에서 허용할 필드를 명시적으로 지정하는 것이 좋다.

뷰의 ordering_fields 속성에 세팅해 사용할 수 있다.:

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('username', 'email')
```
이렇게 하면 비밀번호 hash 필드 또는 민감한 데이터에 대한 정보 유출을 예방할 수 있다.

만약 뷰의 ordering_fields 속성을 명시하지 않으면 필터 클래스는 serializer_class 속성에 지정된 serializer의 읽을 수있는 필드를 필터링 할 수 있도록 허용한다.

만약 view가 민감한 데이터를 포함하고 있지 않음을 확신하면. '__all__'을 이용해 어떤 모델 필드나 쿼리셋의 정렬을 허용할 수 있다.
```
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_filters = '__all__'
```

### Specifying a default ordering
만약 뷰에 ordering 속성이 있다면 default ordering으로 사용된다.

일반적으로 초기 쿼리 세트에서 order_by를 설정하여 이 작업을 제어 할 수 있지만 뷰의 ordering 매개 변수를 사용하면 렌더링 된 템플릿에 컨텍스트로 자동 전달할 수있는 방식으로 순서를 지정할 수 있다. 이렇게 하면 열 머리글을 결과를 정렬하는 데 사용하는 경우 자동으로 렌더링 할 수 있다.

```
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering = ('username', )
```

ordering 속성은 string이나 string으로 이루어진 list/tuple 이다.

## Custom generic filtering
일반적인 filtering backend를 제공하거나, 다른 개발자가 사용하기 위한 설치 가능한 app을 작성할 수 있다. 

이렇게 사용하기 위해서는 .filter_queryset(self, request, queryset, view) 메소드를 오버라이드 한다. 이 메소드는 새로운 필터된 queryset을 반환한다.

클라이언트가 검색 및 필터링을 수행 할 수있을뿐만 아니라 일반 필터 백엔드는 특정 요청이나 사용자에게 표시되어야하는 객체를 제한하는 데 유용 할 수 있습니다

### Example

예를 들어 사용자가 만든 개체 만 볼 수 있도록 사용자를 제한해야 할 수 있습니다.
```
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

뷰에서 get_queryset ()을 재정 의하여 동일한 동작을 얻을 수 있지만 필터 백엔드를 사용하면이 제한을 여러보기에 더 쉽게 추가하거나 전체 API에 적용 할 수 있습니다.
