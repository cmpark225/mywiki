urllib2.urlopen으로 request 전송 시 
response의 status 코드가 200<= code <=300일 경우 
HTTPError에러를 발생시킨다. (raise HTTPError)


return 값을 확인할 때 => e.read()
