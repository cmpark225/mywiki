history 요청하는 경우가 두가지가 있는데.
1. 데이터 요청
2. csv 파일로 요청 


요청 시 첫번째 경우는 데이터를 인코딩 해서 보내야하고, 두번째 경우는 데이터를 인코딩해서 보내면 제대로 된 결과를 받을 수 가 없었음.

Django에서 request를 받고 나서 requests를 생성하는데, 
QueryDict 생성 시 urldecoding을 하고 있어서 

urlparse(parse_qsl)


$http
$download
$ajax
http://api.jquery.com/jquery.ajax/#sending-data-to-server
