apache 로그를 분석하기 위해 툴을 찾다가
 
사용법이 간단한 것 같은 goaccess를 사용하기로 했다.


# 설치

ubuntu에서 설치는 아래와 같이 하면 된다.

```
$sudo apt-get install goaccess
```


# conf 수정

설치 후에 

/etc/goaccess.conf 파일이 생성되는데 해당 파일의

시간, 날짜, 로그 포맷을 지정해주면 된다. 

기본적인 포맷은 주석처리 되어 있어서 아래와 같이

내가 사용하는 포맷이 있을 경우 해당 포맷의 주석을 해제하기만 하면 된다.

-/etc/goaccess.conf
```
######################################
# Time Format Options (required)
######################################

...

# The following time format works with any of the
# Apache/NGINX's log formats below.
#
time-format %H:%M:%S

...

######################################
# Date Format Options (required)
######################################

...

# The following date format works with any of the
# Apache/NGINX's log formats below.
#
date-format %d/%b/%Y

...

######################################
# Log Format Options (required)
######################################

...

# NCSA Combined Log Format with Virtual Host
log-format %v:%^ %h %^[%d:%t %^] "%r" %s %b "%R" "%u"

...

```

# 실행 

내가 분석하고자 하는 log 파일이 other_vhosts_access.log 와 같다면

아래와 같이 goaccess를 실행시켜 주면 된다.

```
$ goaccess -f other_vhosts_access.log

```

실행하면 콘솔 창으로 분석한 내용을 보여준다.

![terminal](/etc/images/goaccess_terminal.png)

## html 출력
html형식으로 내용을 좀 더 보기 쉽게 만들 수도 있다.

```
$ goaccess -f other_vhosts_access.log > index.html
```

뒤에 > filename 을 붙여주면 html 형식으로 파일을 생성해준다.
![html](/etc/images/goaccess_html.jpeg)


# conf 수정 없이 바로 출력

conf 파일이 정상적으로 load되지 않아서, 

계속해서 error가 발생하며 동작하지 않았다.

직접 command line으로 format 형식을 지정해주니 정상 동작은 한다..

```
goaccess -f ~/other_vhosts_access.log.11 --log-format='%^:%^ %h %^[%d:%t %^] "%r" %s %b "%R" "%u"' --time-format=%H:%M:%S --date-format=%d/%b/%Y >~/index.html
```
