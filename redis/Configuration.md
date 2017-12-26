
## Setting the Log Location in redis.conf

The Redis log location is specified in Redis's configuration file, redis.conf, often located at /etc/redis/redis.conf 

Open that file for editing:
```
$sudo vi /etc/redis/redis.conf
``` 

Locate the logfile line:

/etc/redis/redis.conf:
```
logfile /var/log/redis/redis-server.log
``` 

Note the location of the log files. You can edit this file path if you want to rename the log file or change its location

 

## Configuring a Redis Password

Configuring a Redis password enables one of its two built-in security feature - the auth command, which requires clients to authenticate to access the database. The password is configured directly in Redis's configuration file, /etc/redis/redis.conf, which you should still have open from the previous step. 


Open that file for editing:
```
$sudo vi /etc/redis/redis.conf
``` 

Scroll to the SECURITY section and look for a commented directive that reads:

/etc/redis/redis.conf:
```
# requirepass foobared
```

Uncomment it by removing the #, and change foobared to a very strong  and very long value.


After setting the password, save the file, and restart Redis:
```
$ sudo systemctl restart redis
```

To test that the password works, access the Redis command line:
```
$ redis cli
``` 

The following output shows a sequence of command used to test whether the Redis password works.

The first command tries to set a key to a value before authentication.
```
127.0.0.1:6397> set key1 10
(error) NOAUTH Authentication required.
```

The second command authenticates with the password specified in the Redis configuration file.
```
127.0.0.1:6379> AUTH your_redis_passwrod
OK
``` 

refer:

https://www.digitalocean.com/community/tutorials/how-to-secure-your-redis-installation-on-ubuntu-14-04

https://redis.io/topics/rediscli

