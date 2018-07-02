기존에 가지고 있던 브랜치에 rebase 후 remote 브랜치로 push할 경우

commit 메시지가 중복으로 표시되는 문제(?)가 발생.


git book - 브랜치 rebase 하기 참조에서도 하지 말라고 나옴 ㅠㅠ [link](https://git-scm.com/book/ko/v2/Git-%EB%B8%8C%EB%9E%9C%EC%B9%98-Rebase-%ED%95%98%EA%B8%B0#r_rebase_peril)

**일반적인 해답을 굳이 드리자면 로컬 브랜치에서 작업할 때는 히스토리를 정리하기 위해서 Rebase 할 수도 있지만, 리모트 등 어딘가에 Push로 내보낸 커밋에 대해서는 절대 Rebase 하지 말아야 한다.**

rebase한 경우와 merge한 경우 commit 메시지 중복 확인을 위해 테스트 진행. 

1, 2, 3번 까지는 동일하게 진행 하고,

4번부터 rebase, merge로 나누어 확인해봄. 

### branch 종류

1. origin/master
2. master (local)
3. origin/dev
4. dev (local)

# Test 진행
### 1. make a new branch to develop new feature

C2 까지 커밋 완료 상태에서 

새로운 기능 개발을 위해 dev 브랜치를 생성함.

```
$ git log --graph --oneline
* cbdfc89 C2
* b2c9c5c C1
```

##### 브랜치 상태
```
origin/master : C1 C2
master : C1 C2

origin/dev : C1 C2
dev : C1 C2
```

### 2. commit to feature/AURORAUI-test

새로운 기능을 추가하여 dev 브랜치에 commit함. 
C3, C4 커밋이 추가됨

브랜치 그래프 
```
$ git status
On branch dev

$ git log --graph --oneline
* 8812fe7 C4
* 5f26f65 C3
* cbdfc89 C2
* b2c9c5c C1
```

##### 브랜치 상태
```
origin/master : C1 C2
master : C1 C2

origin/dev : C1 C2 C3 C4
dev : C1 C2 C3 C4
```


### 3. fixed bug to master branch
기존 기능의 버그로, master에서 수정 작업이 일어남
C5, C6 커밋이 추가됨

브랜치 그래프
```
$ git status
On branch master

# git log --graph --oneline
* e7ea0f8 C6
* b440ea9 C5
* cbdfc89 C2
* b2c9c5c C1
```

##### 브랜치 상태
```
origin/master : C1 C2 C5 C6
master : C1 C2 C5 C6

origin/dev : C1 C2 C3 C4
dev : C1 C2 C3 C4
```

# rebase 

### 4. rebase the changes to dev branch
수정된 버그를 새로운 브랜치에 적용하기 위해 rebase 실행

```
$ git checkout dev
Switched to branch 'dev'

$ git rebase master
First, rewinding head to replay to your work on top of it
Applying: C3
Applying: C4

$ git log --graph --oneline
* 933dc31 C4
* ba86f81 C3
* e7ea0f8 C6
* b440ea9 C5
* cbdfc89 C2
* b2c9c5c C1
```

기존 C3, C4의 hash 값과, (8812fe7 C4, 5f26f65 C3)

rebase 이후 hash 값이 다름.(933dc31 C4, ba86f81 C3)


##### 브랜치 상태
```
origin/master : C1 C2 C5 C6
master : C1 C2 C5 C6

origin/dev : C1 C2 C3 C4
dev : C1 C2 C5 C6 C3 C4
```

### 5. Push to remote branch
remote de 브랜치에 적용을 위해 push시도

```
$ git push origin dev
! [rejected]        dev -> dev (non-fast-forward)
error: failed to push some refs to 'https://github.com/sally225/git_test.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

pull 후 다시 시도

```
$  git pull origin dev
From https://github.com/sally225/git_test
 * branch            dev        -> FETCH_HEAD
Merge made by the 'recursive' strategy.

$ git log --graph --oneline
*   5858bed Merge branch 'dev' of https://github.com/sally225/git_test into dev
|\  
| * 8812fe7 C4
| * 5f26f65 C3
* | 933dc31 C4' - new
* | ba86f81 C3' - new
* | e7ea0f8 C6
* | b440ea9 C5
|/  
* cbdfc89 C2
* b2c9c5c C1

```

##### 브랜치 상태
```
origin/master : C1 C2 C5 C6
master : C1 C2 C5 C6

origin/dev : C1 C2 C5 C6 C3' C4' C3 C4
dev : C1 C2 C5 C6 C3 C4
```

C3, C4 중복 commit 발생. 


## 이유

local에서 rebase 실행 시 

branch 생성 전까지 돌아가서 bug fix commit인 C5와 C6을 추가 후 

새로운 커밋인 C3'과 C4'을 추가 함.(remote에는 C3, C4가 남아있는 상태.)

**remote에는 기존 커밋인 C3, C4가 남아 있는 상태이므로, 기존 커밋은 유지한 상태로**

**local에 있는 커밋 이력이 추가됨,**

```
*   5858bed Merge branch 'dev' of https://github.com/sally225/git_test into dev
|\  
| * 8812fe7 C4 - 기존에 있던 commit 이력도 함께 merge 됨
| * 5f26f65 C3 - 기존에 있던 commit 이력도 함께 merge 됨
* | 933dc31 C4'
* | ba86f81 C3'
* | e7ea0f8 C6
* | b440ea9 C5
|/  
* cbdfc89 C2
* b2c9c5c C1
```

**따라서 local repository를 제외하고, 기존에 있던 커밋을 rebase 하면 안된다.**

**대신 merge 사용이 필요.**


# merge
### 4. merge master into dev 
수정된 버그를 새로운 브랜치에 적용하기 위해 merge 실행

```
$ git checkout dev
Switched to branch 'dev'

$ git merge master
Merge made by the 'recursive' strategy.
 a.txt | 1 +
 b.txt | 1 +
 2 files changed, 2 insertions(+)

$ git log --graph --oneline
*   30459f1 Merge branch 'master' into dev
|\  
| * e7ea0f8 C6
| * b440ea9 C5
* | 8812fe7 C4
* | 5f26f65 C3
|/  
* cbdfc89 C2
* b2c9c5c C1
```

##### 브랜치 상태
```
origin/master : C1 C2 C5 C6
master : C1 C2 C5 C6

origin/dev : C1 C2 C3 C4
dev : C1 C2 C3 C4 C5 C6 CM
```

### 5. Push to remote branch
remote dev 브랜치에 적용을 위해 push시도
아무런 문제 없이 remote dev에 push가능하다.

```
$ git push origin dev
Username for 'https://github.com': cmpark225@gmail.com
Password for 'https://cmpark225@gmail.com@github.com': 
Counting objects: 2, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 329 bytes | 0 bytes/s, done.
Total 2 (delta 0), reused 0 (delta 0)
To https://github.com/sally225/git_test.git
   feaaf84..30459f1  dev -> dev

$ git log --graph --oneline
*   30459f1 Merge branch 'master' into dev
|\  
| * e7ea0f8 C6
| * b440ea9 C5
* | 8812fe7 C4
* | 5f26f65 C3
|/  
* cbdfc89 C2
* b2c9c5c C1

```


##### 브랜치 상태
```
origin/master : C1 C2 C5 C6
master : C1 C2 C5 C6

origin/dev : C1 C2 C3 C4 CM
dev : C1 C2 C3 C4 C5 C6 CM (merge commit)
```
