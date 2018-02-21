>>> Q.objects.filter(id=6).values()
[{'short': u'oui', 'deleted': False, 'language_id': 3L, 'long': u'oui', 'place_holder': u'oui', 'id': 6L, 'question_id': 8L}]
>>> from django.forms.models import model_to_dict
>>> model_to_dict(Q.objects.filter(id=6)[0])
{'short': u'oui', 'language': 3L, 'deleted': False, 'question': 8L, 'long': u'oui', 'place_holder': u'oui'}



import json
from django.core import serializers

def getObject(request, id):
    obj = MyModel.objects.get(pk=id)
    data = serializers.serialize('json', [obj,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, mimetype='application/json')
