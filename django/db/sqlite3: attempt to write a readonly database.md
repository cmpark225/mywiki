
apache와 연동 후
vhost접속 시도 시 

sqlite3: attempt to write a readonly database


에러 발생


1. 
```
sudo chown www-data db.sqlite3
```

2. unable to open database file 에러 발생 시 

```
chown www-data .
```
