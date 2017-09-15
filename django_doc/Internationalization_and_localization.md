
크게 세가지로 나뉜다

1. Internationalization(국제화) : 개발자가 지역화 지원을 위해 준비
2. Localization(지역화) : 번역가가 번역, 지역 형식에 맞게 변환
3. Deployment of translaiton



*.py, *.html 
=(makemessage)=> locale/ko_kr/LC_message/django.po 
: source 코드에서 사용 중인 문자열을 추출하여 *.po 파일로 생성한다. 
=(compilemessage)=>locale/ko_kr/LC_messsage/django.mo 
: Django에서 사용할 수 있게 message를 compile 한다.


