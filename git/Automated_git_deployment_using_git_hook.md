
Local repository에서 push한 후 

deploy server에서 자동으로 git pull을 받게 하고 싶었다.


### 동작 방식
1. deploy 서버에 bare 저장소 생성
2. bare 저장소에 git hook 등록 (post-receive)
3. local에 bare 저장소를 remote branch로 추가
4. local에서 push -> bare 저장소에서 hook으로 pull 받음



## Deploy server setting

일단 ssh설정이 필요할듯 https://git-scm.com/book/ko/v2/Git-%EC%84%9C%EB%B2%84-%EC%84%9C%EB%B2%84-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0

1. deploy server에 bare 저장소 생성

```
$ git init --bare ~/myproject.git
Initialized empty Git repository in /home/user/myproject.git
```


2. post-receive hook 파일 생성

파일 위치 
```
 ~/myproject.git/hooks$ post-receive
```

코드 
```
#!/bin/bash
TARGET="/var/www"
GIT_DIR="/home/user/myproject.get"
BRANCH="master"

while read oldrev newrev ref
do
  if [[ $ref = refs/heads/$BRANCH ]]; 
  then
    echo "Master $ref received. Deploying ${BRANCH} branch to production..."
    git --work-tree=$TARGET --git-dir=$GIT_DIR checkout -f
  else
    echo "Ref $ref successfully received.  Doing nothing: only the master branch may be deployed on this server."
  fi  
done

```
변수 설명
* TARGET => 코드를 저장할 장소.
* GIT_DIR => bare 저장소 위치. (bare 저장소는 위킹디렉토리가 없는 저장소)
* BRANCH => 가져올 브랜치이름

+) apache restart도 추가하고 싶을 경우

git --work-tree.... 명령어 밑에 아래 코드도 추가해준다

```
...
    git --work-tree=$TARGET --git-dir=$GIT_DIR checkout -f
    PATH=/usr/lib/apache2/bin:$PATH
    restart
  else
...
```

3. hook 모드 수정
```
~/myproject.git/hooks$ chmod x+ post-receive

```

## Local server setting
코드를 실제로 수정하는 local server에 bare 저장소를 remote로 추가한다.

1. remote 브랜치 추가
```
$ git remote add live ssh://user@domain/home/user/myproject.git
```

2. 코드 수정 후 push
```
$ git push live master
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 219 bytes | 219.00 KiB/s, done.
Total 2 (delta 1), reused 0 (delta 0)
remote: Master refs/heads/master received. Deploying master branch to production...
To /home/user/myproject.git/
   71c8246..f40eb04  master -> master
```

3. 결과 확인
   
post-receive에 설정한 TARGET 위치에 가면 push한 내용이 반영된 것을 확인할 수 있다.



ref
* https://www.digitalocean.com/community/tutorials/how-to-set-up-automatic-deployment-with-git-with-a-vps
* 
