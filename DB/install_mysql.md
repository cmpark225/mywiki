# 환경
ubuntu 16.04


## 1. 설치
```
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo apt-get install libmysqlclient-dev
```
설치 시 root 비밀번호를 물어본다.

(libmysqlclient-dev는 pip로 mySQL-python 설치 시   EnvironmentError: mysql_config not found 발생해서 설치함)

## 2. Mysql 서버 시작
```
$ service mysql service
```

## 3. 설정
설정 파일 위치는 /etc/mysql/my.cnf 이다. 아래와 같이 클라이언트와 서버쪽 설정 파일을 include 하도록 되어 있다.

```
#
# The MySQL database server configuration file.
#
# You can copy this to one of:
# - "/etc/mysql/my.cnf" to set global options,
# - "~/.my.cnf" to set user-specific options.
# 
# One can use all long options that the program supports.
# Run program with --help to get a list of available options and with
# --print-defaults to see which it would actually understand and use.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

#
# * IMPORTANT: Additional settings that can override those from this file!
#   The files must end with '.cnf', otherwise they'll be ignored.
#

!includedir /etc/mysql/conf.d/
!includedir /etc/mysql/mysql.conf.d/
```

서버쪽 설정을 변경할려면 /etc/mysql/mysql/conf.d/mysqld.cnf 를 수정하면 된다. MySQL 서버는 초기 설치시에 바인딩 어드레스가 127.0.0.1 로 되어 있기 때문에 리모트에서 접속이 불가하다. 리모트에서 접속을 할려면 아래와 같이 bind-address 를 0.0.0.0 으로 한 후 MySQL 서버를 재시작한다.

```
#
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
bin-address            = 0.0.0.0
```

MySQL 서버로 접속해 본다.

```
user@UD-user:~$ mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.23-0ubuntu0.16.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
​```
