
실제 product에서 history 요청하는 경우가 두가지가 있는데.

* 데이터 요청
* csv 파일로 요청

첫번째 경우는 데이터를 인코딩 해서 보내야 했는데,
두번째 경우는 데이터를 인코딩해서 보내면 제대로 된 결과를 받을 수 가 없었다.

처음에는 Django에서 HttpRequest를 만들 때  
http 헤더 값에 따라서  URL 디코딩을 결정하여 
POST 데이터(QueryDict)를 생성하는 줄 알았으나.
(첫번째와 두번째 경우에서 Http Header의 Content-Type 값만 달랐음.)

raw_post_data를 확인해보니 헤더와 관계 없이 
QueryDict 생성 시 __init__함수에서
python 2.7 내장 함수인 from urlparse import parse_qsl 을 사용하여 
urldecoding을 하고 있었다.

따라서 클라이언트 측에서 urlencoding을 하여 post 데이터를 전송하고 있었는데.

두가지 전송 방식을 확인해보니

첫번째 단순 데이터 요청은 angularjs의 $http를 이용하여 요청하고 있었고,
두번째 csv 파일 요청은 form으로 요청하고 있었다. (submit 전송)

form 요청의 경우 
브라우저에서 알아서 urlencoding 해서 데이터를 전송하고 있었기 때문에 내가 추가적으로 encoding해서 전송할 필요가 없었다.

추가적으로 ajax도 확인하였는데, 
ajax의 경우
data를 string이나 object 형태로 보낼 수 있는데,
string으로 전송할 경우에는 urlencoding 없이 데이터를 전송하고,
object로 전송할 경우에는 서버로 데이터 요청하기 전에 urlencoding을 한 후 전송하고 있다.

http://api.jquery.com/jquery.ajax/#sending-data-to-server

> The data option can contain either a query string of the form key1=value1&key2=value2, or an object of the form {key1: 'value1', key2: 'value2'}. If the latter form is used, the data is converted into a query string using jQuery.param() before it is sent. This processing can be circumvented by setting processData to false. The processing might be undesirable if you wish to send an XML object to the server; in this case, change the contentType option from application/x-www-form-urlencoded to a more appropriate MIME type.


