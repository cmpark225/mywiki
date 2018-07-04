## merge

### Fast-forward 방식

merge 하려는 브랜치가 현재 브랜치의 기반이 되는 브랜치이기 때문에

포인터를 최신 브랜치로만 이동하면 되는 경우.

master branch
```
master : C1 C2
hotfix : C1 C2 C3 C4
```
hotfix가 가리키는 C4 커밋이 C2 커밋에 기반한 브랜치이기 때문에

브랜치 포인터는 그냥 최신 커밋으로 이동만 하면 된다.

```
$ git status
On branch master

$ git rebase hotfix

master : C1 C2 C3 C4
```

### 3 way merge

merge 하려는 브랜치가 가리키는 커밋이 현재 브랜치의 조상이 아닐경우

```
master : C1 C2 C3
issue : C1 C2 C4 C5
```
(C2 커밋 위치에서 issue 브랜치 생성 후 master 브랜치에 C3 새로운 커밋이 생성됨.)

이때 각 브랜치가 가리키는 커밋 두개랑 공통 조상 하나를 이용해 3-way merge를 한다.

* 각 브랜치가 가리키는 커밋 두개 -> C3, C5
* 공통 조상 하나 -> C2

```
$ git status
On branch master

$ git merge issue

master : C1 C2 C3 C4 C5 C6(merge 커밋)
```


## rebase

```
master : C1 C2 C3
issue : C1 C2 C4 C5
```

공통 커밋으로 이동한 다음 

그 커밋부터 지금까지 checkout한 브랜치가 가리키는 커밋까지 diff를 만들어 임시 저장 후 rebase 할 브랜치가 합칠 브랜치가 가리키는 커밋을 가리키게 하고 임시 저장한 사항을 적용한다.

