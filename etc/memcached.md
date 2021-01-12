List all keys
 
# 접속
```
user@UD-user:~$ telnet 127.0.0.1 11211
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
```

# 종료

```
ctrl + ]

telet > q
```
 

# List the items
item List에서 slab id를 가져온다.

slab id는 'items' 뒤에 있는 숫자다.

```
stats items
STAT items:1:number 1
STAT items:1:age 32214
STAT items:1:evicted 0
STAT items:1:evicted_nonzero 0
STAT items:1:evicted_time 0
STAT items:1:outofmemory 0
STAT items:1:tailrepairs 0
STAT items:1:reclaimed 0
STAT items:1:expired_unfetched 0
STAT items:1:evicted_unfetched 0
STAT items:1:crawler_reclaimed 0
STAT items:1:crawler_items_checked 0
STAT items:1:lrutail_reflocked 0
STAT items:2:number 3
STAT items:2:age 32935
STAT items:2:evicted 0
STAT items:2:evicted_nonzero 0
STAT items:2:evicted_time 0
STAT items:2:outofmemory 0
STAT items:2:tailrepairs 0
STAT items:2:reclaimed 0
STAT items:2:expired_unfetched 0
STAT items:2:evicted_unfetched 0
STAT items:2:crawler_reclaimed 0
STAT items:2:crawler_items_checked 0
STAT items:2:lrutail_reflocked 0
STAT items:3:number 2
STAT items:3:age 744
STAT items:3:evicted 0
STAT items:3:evicted_nonzero 0
STAT items:3:evicted_time 0
STAT items:3:outofmemory 0
STAT items:3:tailrepairs 0
STAT items:3:reclaimed 2
STAT items:3:expired_unfetched 1
STAT items:3:evicted_unfetched 0
STAT items:3:crawler_reclaimed 0
STAT items:3:crawler_items_checked 0
STAT items:3:lrutail_reflocked 0
STAT items:7:number 1
STAT items:7:age 1589
STAT items:7:evicted 0
STAT items:7:evicted_nonzero 0
STAT items:7:evicted_time 0
STAT items:7:outofmemory 0
STAT items:7:tailrepairs 0
STAT items:7:reclaimed 0
STAT items:7:expired_unfetched 0
STAT items:7:evicted_unfetched 0
STAT items:7:crawler_reclaimed 0
STAT items:7:crawler_items_checked 0
STAT items:7:lrutail_reflocked 0
STAT items:8:number 1
STAT items:8:age 540
STAT items:8:evicted 0
STAT items:8:evicted_nonzero 0
STAT items:8:evicted_time 0
STAT items:8:outofmemory 0
STAT items:8:tailrepairs 0
STAT items:8:reclaimed 0
STAT items:8:expired_unfetched 0
STAT items:8:evicted_unfetched 0
STAT items:8:crawler_reclaimed 0
STAT items:8:crawler_items_checked 0
STAT items:8:lrutail_reflocked 0
STAT items:10:number 1
STAT items:10:age 769
STAT items:10:evicted 0
STAT items:10:evicted_nonzero 0
STAT items:10:evicted_time 0
STAT items:10:outofmemory 0
STAT items:10:tailrepairs 0
STAT items:10:reclaimed 0
STAT items:10:expired_unfetched 0
STAT items:10:evicted_unfetched 0
STAT items:10:crawler_reclaimed 0
STAT items:10:crawler_items_checked 0
STAT items:10:lrutail_reflocked 0
STAT items:13:number 1
STAT items:13:age 687
STAT items:13:evicted 0
STAT items:13:evicted_nonzero 0
STAT items:13:evicted_time 0
STAT items:13:outofmemory 0
STAT items:13:tailrepairs 0
STAT items:13:reclaimed 0
STAT items:13:expired_unfetched 0
STAT items:13:evicted_unfetched 0
STAT items:13:crawler_reclaimed 0
STAT items:13:crawler_items_checked 0
STAT items:13:lrutail_reflocked 0
STAT items:28:number 2
STAT items:28:age 540
STAT items:28:evicted 0
STAT items:28:evicted_nonzero 0
STAT items:28:evicted_time 0
STAT items:28:outofmemory 0
STAT items:28:tailrepairs 0
STAT items:28:reclaimed 0
STAT items:28:expired_unfetched 0
STAT items:28:evicted_unfetched 0
STAT items:28:crawler_reclaimed 0
STAT items:28:crawler_items_checked 0
STAT items:28:lrutail_reflocked 0
STAT items:29:number 1
STAT items:29:age 7166
STAT items:29:evicted 0
STAT items:29:evicted_nonzero 0
STAT items:29:evicted_time 0
STAT items:29:outofmemory 0
STAT items:29:tailrepairs 0
STAT items:29:reclaimed 0
STAT items:29:expired_unfetched 0
STAT items:29:evicted_unfetched 0
STAT items:29:crawler_reclaimed 0
STAT items:29:crawler_items_checked 0
STAT items:29:lrutail_reflocked 0
STAT items:39:number 1
STAT items:39:age 769
STAT items:39:evicted 0
STAT items:39:evicted_nonzero 0
STAT items:39:evicted_time 0
STAT items:39:outofmemory 0
STAT items:39:tailrepairs 0
STAT items:39:reclaimed 0
STAT items:39:expired_unfetched 0
STAT items:39:evicted_unfetched 0
STAT items:39:crawler_reclaimed 0
STAT items:39:crawler_items_checked 0
STAT items:39:lrutail_reflocked 0
END
```

# Get cache dump

각각의 slab id에 대한 cache dump를 요청한다.
(dump 하기 위한 key 최대 개수도 지정해야 한다. 100)

```
stats cachedump 3 100
ITEM :1:aurorauser__spectrum_api_token [40 b; 1539766876 s]
ITEM :1:aurorauser_chanmi.park_spectrum_api_token [40 b; 1539768152 s]
END 
 
stats cachedump 39 100
ITEM :1:customers [464165 b; 1508233926 s]
END
```

# Get value

가져온 key 값으로 value를 가져온다. 

```
get :1:customers
  
END
``` 
