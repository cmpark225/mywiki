urllib, urllib2, requests

## urllib, urllib2

urllib2.urlopen() function can allow you to specify headers

```
r = Request(url='http://www.mysite.com')
r.add_header('User-Agent', 'awesome fetcher')
r.add_data(urllib.urlencode({'foo': 'bar'})
response = urlopen(r)
```

Note that urlencode() is only in urllib, not urllib2.

## requests

requests 패키지는 설치가 필요하다.


파이썬이 아닌 다른 언어를 사용했다면 아마도 urllib와 urllib2는 사용하기 쉽고, 코드가 많지 않으며, 성능이 저 좋다는 생각이 들 것입니다. 그래서 생각했던 것입니다. 그러나 Requests 패키지는 믿을 수 없을 만큼 유용하고 짧아서 모든 사람이 사용해야 하는 패키지 중 하나입니다.



requests 모듈을 Rest API를 지원합니다.

```
import requests
...

resp = requests.get('http://www.mywebsite.com/user')
resp = requests.post('http://www.mywebsite.com/user')
resp = requests.put('http://www.mywebsite.com/user/put')
resp = requests.delete('http://www.mywebsite.com/user/delete')
```

GET / POST가 매개 변수를 다시 인코딩 할 필요가 없는지 여부와 관계없이 dictionary를 인수로 사용하기만하면 됩니다.

```
userdata = {"firstname": "John", "lastname": "Doe", "password": "jdoe123"}
resp = requests.post('http://www.mywebsite.com/user', data=userdata)
```

게다가 json 디코더가 내장되어 있습니다 (다시말해, json.loads()와 같이 추가적으로 json 모듈을 사용하지 않아도 됩니다)

```
resp.json()
```

또는 response 데이터가 text라면 아래와 같이 사용할 수 있습니다.

```
resp.text
```

위의 설명은 아주 간단한 것만 설명한 내용입니다. 다음은 requests의 기능 list입니다.



출처: http://brownbears.tistory.com/299 [불곰]
