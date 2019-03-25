# HOST 설정

aws에서 제공하는 퍼블릭 DNS가 너무 길어서 새로 host를 생성해서 연결 하려고 한다.

my.noip.com 에서 무료로 host를 3개까지 제공해준다. 

원하는 host를 생성 한 후
Target을 AWS EC2 인스턴스의 퍼블릭 IP로 연결해줬다.

그리고 apache conf 파일에 ServerName 설정 해줌..

```
<VirtualHost *:80>
ServerName mydomain.com
```

서버 종료 하면 AWS의 퍼블릭 IP가 변경되기 때문에 
동적IP로도 설정할 수 있는 기능이 있는 것 같다. 확인은 안해봄.

*아 이거 호스트도 한달마다 update 해야 함.*


# 인증서 발급

무료로 인증서 발급받기 위해 Letsencrypt를 이용하기로 했다.

## 설치

```
$ sudo apt update -y 
$ sudo apt install letsencrypt -y
```

## 인증서 발급

위에서 만든 도메인으로 인증서를 발급 받았다. (mydomain.com)

```
$ sudo letsencrypt certonly --standalone -d mydomain.com
```

이메일 입력과 정책에 동의 하면 인증서가 발급된다. 

이때 80포트 사용중이면 아래 메시지 나오면서 거부 당한다.ㅠㅠ

```
The program apahce2 (process ID 2311) is already listening on TCP port 80. This will prevent us from binding to that port. Please stop the apache2 program temporarily and then try again.
```

아파치 종료 후 재발급에 성공했다.

```
$ sudo letsencrypt certonly --standalone -d mydomain.com

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at
   /etc/letsencrypt/live/mydomain.com/fullchain.pem. Your
   cert will expire on 2018-12-28. To obtain a new version of the
   certificate in the future, simply run Let's Encrypt again.
 - If you like Let's Encrypt, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le


```

12월 28일에 재발급 받아야 하는 듯...


# 인증서 설정

발급 받은 인증서를 apache에 설정 해준다. 

## http 요청 https로 리다이렉트 처리

```
<VirtualHost *:80>
...

    Redirect permanent / https://mydomain.com/
...
</VirtualHost>
```

근데 만약 http://mydomain.com/abc로 접속하면 
https://mydomain.comabc 로 접속이 된다...

이유 모르겠음

## ssl conf 수정
발급받은 인증서와 키 파일을 설정 해준다


default-ssl.conf
```
<IfModule mod_ssl.c>
    <VirtualHost _default_:443>
    ...
    ServerName mydomain.com

    SSLEngine on

    # 아까 발급 받은 인증서 경로 작성한다. 
    SSLCertificateFile /etc/letsencrypt/live/mydomain.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/mydomain.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/mydomain.com/chain.pem

    SSLHonorCipherOrder on

    # 기존에 Django 사용을 위해 필요했던 설정도 작성 해준다. 
    ...
    </VirtaulHost>
</IfModule>
```


SSL 활성화 및 conf 등록
```
$ sudo a2enmod ssl
$ sudo a2ensite default-ssl.conf
$ sudo service apache2 reload
$ sudo service apache2 restart
```

a2enmod : 아파치2 모듈 활성화 명령어

a2ensite : 새로운 가상호스트 추가

##### apache2 reload 와 restart 차이
reload는 서버 재시작 없이 환경설정을 새로 읽어온다.

restart 서버 재시작

우분투를 기준으로 a2ensite 를 이용해 사이트 on off 할 경우 relaod

a2enmod를 이용해 모듈을 on off 할 경우 restart를 안내한다고 한다.


# 인증서 갱신

 ```
 sudo letsencrypt renew
 ```
 
 갱신 실패 시 아파치 멈추


## 확인

https://www.sslshopper.com/ssl-checker.html#hostname=mydomain.com

위 주소로 내 도메인의 인증서 상태를 확인 할 수 있다. 



ref
- https://blog.illustudio.co.kr/2017/02/23/letsencrypt-무료-ssl-인증서-설치/
