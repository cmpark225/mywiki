# pprint

```
>>> improt pprint
>>> a = {"result": "success","items": [{"name": "apple","price": 3}, {"name":"banana","price":5},\
{"name":"toy","price":50}]}

>>> pp = pprint.PrettyPrinter(indent=4)
>>> pp.pprint(a)
{   'items': [   {   'name': 'apple', 'price': 3},
                 {   'name': 'banana', 'price': 5},
                 {   'name': 'toy', 'price': 50}],
    'result': 'success'}

```
