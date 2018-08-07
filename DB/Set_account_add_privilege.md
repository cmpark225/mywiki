### mysql 접속
```
$ mysql -u root -p
```


### 사용자 확인
```
mysql> use mysql;
mysql> select host, user from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | debian-sys-maint |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
+-----------+------------------+
```

### 사용자 추가

```
mysql> create user dev@localhost identified by 'password';
mysql> select host, user from user;
+-----------+------------------+
| host      | user             |
+-----------+------------------+
| localhost | debian-sys-maint |
| localhost | dev              |
| localhost | mysql.session    |
| localhost | mysql.sys        |
| localhost | root             |
+-----------+------------------+
```

dev라는 localhost에서 접근 가능한 계정을 생성했다. 


외부에서 접근 가능한 유저를 생성하기 위해서는 

'dev'@'%'와 같이 % 를 이용하여 외부 접근을 허용한다.


ex) 192.168.x.x로 시작하는 모든 IP의 원격 접속을 허용하고 싶을 경우
dev@'192.168.%'

### 사용자 제거
```
mysql > drop user 'dev';
```

### 데이터 베이스 권한 부여
```
mysql > grant select, insert, update on database.* to dev@localhost identified by 'password'

mysql > show grants for dev@localhost;
+-------------------------------------------------------------------------+
| Grants for dev@localhost                                                |
+-------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'dev'@'localhost'                                 |
| GRANT SELECT, INSERT, UPDATE, CREATE ON `wisdom`.* TO 'dev'@'localhost' |
+-------------------------------------------------------------------------+

```

database.* 의 경우 해당 database의 모든 table 접근을 허용한다. 

*.*은 모든 접근 가능. 

database.table 은 해당 table만 접근 가능

### 권한 적용
```
mysql> flush privileges;
```

### 권한 삭제 
```
mysql> revoke all on dbname.table from dev@localhost;
```

### 권한 확인
```
mysql> show grants for dev@host;
+-------------------------------------------------------------------------+
| Grants for dev@localhost                                                |
+-------------------------------------------------------------------------+
| GRANT USAGE ON *.* TO 'dev'@'localhost'                                 |
| GRANT SELECT, INSERT, UPDATE, CREATE ON `wisdom`.* TO 'dev'@'localhost' |
+-------------------------------------------------------------------------+

```

참고 사이트:
http://ourcstory.tistory.com/45
