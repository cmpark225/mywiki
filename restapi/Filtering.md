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
