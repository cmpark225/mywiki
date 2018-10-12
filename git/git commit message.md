git commit message를 작성할때 참고하면 좋을 것 같다.

1. 제목과 본문을 한 줄 띄워 분리하기
2. 제목은 영문 기준 50자 이내로
3. 제목 첫글자를 대문자로
4. 제목 끝에 . 금지
5. 제목은 명령조로
6. 본문은 영문 기준 72자마다 줄 바꾸기
7. 본문은 어떻게보다 무엇을, 왜에 맞춰 작성하기


## 커밋 메시지의 제목은 명령조로

현재 commit message를 명령조로 작성하고는 있었는데,

git 빌트인 컨벤션과 맞추기 위한 것은 처음 알았다. 

> 명령문은 git 커밋의 제목으로는 아주 딱입니다. 그 한가지 좋은 이유는 git 스스로가 자동 커밋을 작성할 때 명령문을 사용하고 있습니다. 예를 들어, 기억을 되돌아보면 git merge를 실행했을 때 커밋 메시지 기본값이 이렇습니다.
>> Merge branch 'myfeature'

> git revert 명령어를 실행하면 어떤 메시지가 기본값으로 들어갈까요?
>> Revert "Add the thing with the stuff"
>> This reverts commit cc87791524aedd593cff5a74532befe7ab69ce9d.

> Github에서 풀 리퀘스트의 "Merge" 버튼을 클릭하면 자동으로 채워지는 메시지가 어땠나요?
>> Merge pull request #123 from someuser/somebranch

> 이처럼 커밋 메시지를 명령문으로 작성한다는 것은, git의 빌트-인 컨벤션(Built-in Convention)을 그대로 따른다는 것을 의미합니다. 때문에 커밋 제목을 명령문으로 작성하면, 자동 메시지로 채워진 커밋 사이에 자연스레 녹아듭니다. 앞선 항목에서 설명드린 git shortlog와 같은 타 명령어에도 연계되어 잘 어울리죠.

https://meetup.toast.com/posts/106

## 커밋 메시지로 이슈 닫기

그리고 커밋 메시지로 이슈를 자동 종료 시키는 기능도 유용하게 쓰일 것 같다.

```
키워드 #이슈번호
```

해당 방법으로 이슈를 처리할 경우 브랜치가 master에 merge될 경우 자동 처리된다고 한다.


* close
* closes
* closed
* fix
* fixes
* fixed
* resolve
* resolves
* resolved

http://minsone.github.io/git/github-commits-closing-issues-via-commit-messages
