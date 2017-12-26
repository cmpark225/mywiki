

## Download, Compile, and Install Redis

### Donwload and Extract the Source Code

Since we won't need to keep the source code that we'll compile long term (we can always re-download it),

we will build in the /tmp directory. Let's mode there now:

```
$ cd /tmp
```

Now, download the latest stable version of Redis. This is always available at a stable download URL:

http://download.redis.io/redis-stable.tar.gz

download page :  https://redis.io/download

```
$ curl -0 http://download.redis.io/redis-stable.tar.gz
```

Unpack the tarball by typing:
```
$ tar xzvf redis-stable.tar.gz
```

Move into the Redis source directory structure that was just extracted:

```
$ cd redis-stable
```

### Build and Install Redis

Now, we can compile the Redis binaries by typing:

```
$ make
```

After the binaries are compiled, run the test suite to make sure everything was built correctly. You can do this by typing:

```
$ make test
```

This will typically take a few minutes to run. Once it is complete, you can install the binaries onto the system by typing:
```
$ sudo make install 
```

### Configure Redis
Now that Redis is installed, we can begin to configure it.



To start off, we need to create a configuration directory. We will use the conventional /etc/redis directory, which can be created by typing:

```
$ sudo mkdir /etc/redis 
```

Now, copy over the sample Redis configuration file included in the Redis source archive:

```
$ sudo cp /tmp/redis-stable/redis.conf /etc/redis
```

Next, we can open the file to adjust a few items in the configuration:
```
$sudo vi /etc/redis/redis.conf
```

In the file, find the supervised directive. Currently, this is set to no. Since we are running an operating system that uses the systemd init system, we can change this to systemd:

/etc/redis/redis.conf:
```
 . . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

. . .
```

next, find the dir directory. This option specifies the directory that Redis will use to dump persistent data.

We neet to pick a location that Redis will have wirte permission and that isn't viewable by normal users.



We will use the /var/lib/redis directory for this, which we will create in a momnet:

/etc/redis/redis.conf:
```
 . . .

# The working directory.
#
# The DB will be written inside this directory, with the filename specified
# above using the 'dbfilename' configuration directive.
#
# The Append Only File will also be created inside this directory.
#
# Note that you must specify a directory here, not a file name.
dir /var/lib/redis

. . .
```

Save and close the file when you are finished.





## Create a Redis systemd Unit File

Next, we can create a systemd unit file so that the init system can manage the Redis process.

Create and open the /etc/systemd/system/redis.service file to get started:
```
$ sudo vi /etc/systemd/system/redis.service
```

Inside, we can begin the [Unit] section by adding a description and defining a requirement that networking be available before starting this service ([Unit] 섹션에 네트워킹이 가능해야 한다는 요구 사항 정의):

/etc/systemd/system/redis.service:
```
[Unit]
Description=Redis In-Memory Data Store
After=network.target
```

In the [Service] section, we need to specify the service's behavior. For security purposes, we should not run our service as root. We should use a dedicated user and group, which we will call redis for simplicity. We will create these momentarily. 



To start the service, we just need to call the redis-server binary, pointed at our configuration. To stop in, we can use the Redis shutdown command, which can be executed with the redis-cli binary. Also, since we want Redis to recover from failures when possible, we will set the Restart directive to "always":

/etc/systemd/system/redis.service:
```
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always
```

Finally, in the [Install] section, we can define the systemd target that the service should attach to if enabled (configured to start at boot)

(서비스가 연결되어야 하는 시스템 대상을 정의. 부팅시 시작되도록 구성됨):

/etc/systemd/system/redis.service:
```
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and close the file when you are finished.



## Create the Redis User, Group and Directories

Now, we just have to create the user, group, and directory that we referenced in the previous two files.

Begin by creating the redis user and group. This can be done in a single command by typing:

```
$ sudo adduser --system --group --no-create-home redis
```

Now, we can create the /var/lib/redis directory by typing:

```
$ sudo mkdir /var/lib/redis
```

We should give the redis user and group ownership over this directory:
```
$ sudo chown redis:redis /var/lib/redis
```

Adjust the permissions so that regular users cannot access this location:
```
$ sudo chmod 770 /var/lib/redis
```

## Start and Test Redis

Now, we are ready to start the Redis server.



### Start the Redis Service

Start up the systemd service by typing:
```
$ sudo systemctl start redis
```

Check that the service had no errors by running:

```
$sudo systemctl status redis
```

You should see something that looks like this:

```
Output
● redis.service - Redis Server
   Loaded: loaded (/etc/systemd/system/redis.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2016-05-11 14:38:08 EDT; 1min 43s ago
  Process: 3115 ExecStop=/usr/local/bin/redis-cli shutdown (code=exited, status=0/SUCCESS)
 Main PID: 3124 (redis-server)
    Tasks: 3 (limit: 512)
   Memory: 864.0K
      CPU: 179ms
   CGroup: /system.slice/redis.service
           └─3124 /usr/local/bin/redis-server 127.0.0.1:6379       

. . .
```

### Test the Redis Instance Functionality

To test that your service is functioning correctly, connect to the Redis server with the command-line client:
```
$ redis-cli
```

In the prompt that follows, test connectivity by typing:
```
127.0.0.1:6379> ping
```

You should see:
```
Output
PONG
```

Check that you can set keys by typing:
```
127.0.0.1:6379> set test "It's working!"
OK
```

Now retrieve the value by typing:
```
127.0.0.1:6397> get test
"It's working!"
```

Exit the Redis prompt to get back to the shell:
```
127.0.0.1:6397> exit
```

As a final test, let's restart the Redis instance:
```
$ sudo systemctl restart redis
```

Now, connect with the client again and confirm that your test value is stall available:
```
$redis-cli
127.0.0.1:6379> get test
```

The value of your key should still be accessible:
```
Output
"It's working"
```

## Enable Redis to Start at Boot

If all of your tests worked, and you would like to start Redis automatically when your server boots, you can enable the systemd service.

To do so, type:
```
$ sudo systemctl enable redis
Created symlink from /etc/systemd/system/multi-user.target.wants/redis.service to /etc/systemd/system/redis.service.
```





refer:

https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04
