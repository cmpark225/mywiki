## How to convert queryset to json 

```
from django.core.serializers.json import DjangoJSONEncoder
 
import json
"""from django.utils import simplejson as json"""
 
form example.model import test_model
 
def retJSON():
    test_queryset = test_model.objects.all()
    get_JSON_serializable = \[o for o in test_queryset.values()\]"""\[o for o in test_queryset.values()\] makes JSON serializable format."""
    return json.dumps(get_JSON_serializable, ensure_ascii=False, cls=DjangoJSONEncoder)"""DjangoJSONEncoder makes datetime type to ISOformat string. and json.dumps() return json string."""
```
