user@UD-user:~$ redis-cli
 
 
# Change the selected database
127.0.0.1:6379> select 1
OK
 
# get all key
127.0.0.1:6379[1]> keys *
(empty list or set)
 
 
127.0.0.1:6379[1]> select 0
OK
 
 
# set key
127.0.0.1:6379 > set mykey somevalue
OK
 
 
 
# get 'mykey'
127.0.0.1:6379 > get mykey
"somevalue"
 
 
# del key
127.0.0.1:6379 > del mykey
(integer) 1

# 사용중인 메모리 확인

```
user@UD-user:~$ redis-cli "info" |grep "used_memory_human:"
used_memory_human:594.70K
```
