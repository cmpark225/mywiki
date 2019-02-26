
# Getting started with GitLab CI/CD

GitLab은 continuous integration 서비스를 제공한다. 만약 .gitlab-ci.yml 파일을 레파지토리의 루트디렉토리에 추가하고, Runner를 사용을 위해 GitLab project를 구성하고나면, 각 커밋이나 푸시는 CI pipline을 트리거한다.(실행한다.) 

.gitlab-ci.yml 파일은 GitLab runner에게 무엇을 해야하는지 말해준다. 기본적으로 세가지 단계로 파이프라인을 실행한다: build, test, deploy. 세가지 단계 모두 사용할 필요는 없다; job이 없는 단계는 단순히 무시된다.

만약 모든 실행이 OK(리턴 값이 0이 아닌 것이 없으면)되면, 커밋과 연관된 녹색 체크 마크를 얻을 것이다. 이것은 코드를 보기 전에 커밋이 테스트에 실패 했는지를 보기 쉽게 만든다. 

대부분의 프로젝트는 개발자들이 무언가를 깨트렸을 때 즉각적인 피드백을 받을 수 있도록 GitLab의 CI 서비스를 사용하여 테스트 스위트를 운영한다.

시험된 코드를 스테이징 및 프로덕션 환경에 자동으로 배포하기 위해 continuous delivery과 continuous deployment를 사용하는 경향이 증가하고 있다.

따라서 요약하면, CI를 동작시기기 위해 필요한 단계는 다음과 같다. 

1. 리파지토리의 루트 디렉토리에 .gitlab-ci.yml 추가
2. Runner 설정

거기서부터, git 리파지토리의 모든 푸시마다, Runner는 자동으로 파이프라인을 시작할 것이고 파이프라인은 프로젝트의 Pipelines 페이지에 나타날 것이다. 

본 가이드는 다음과 같이 가정한다
* 8.0+r의 작동 버전을 가지고 있거나 GitLab.com을 사용하고 있다.
* GitLab에 당신이 CI를 사용하고 싶은 프로젝트가 있다.

## Creating a .gitlab-ci.yml file
 .gitlab-ci.yml을 만들기 전에 우선 이것이 무엇에 관한 것인지 간략하게 설명해보자

### What is .gitlab-ci.yml
.gitlab-ci.yml 파일은 프로젝트에서 CI가 수행하는 작업을 구성하는 곳이다. 이것은 프로젝트의 루트에 위치하고 있다. 

리파지토리에 푸시 할 때마다, GitLab은 .gitlab-ci.yml 파일을 찾고 파일 내용에 따라 Runner에서 작업을 시작한다. 

.gitlab-ci.yml은 리파지토리에 있고 버전 관리가 되기 때문에, 이전 버전은 여전히 성공적으로 포크에서 쉽게 CI를 사용할 수 있고, 분기마다 다른 파이프 라인과 작업을 가질 수 있으며, CI에 대한 단일 진실을 확보할 수 있다. 왜 우리가 .gitlab-ci.yml을 사용하는지에 대한 이유에 대해 [우리 블로그](https://about.gitlab.com/2015/05/06/why-were-replacing-gitlab-ci-jobs-with-gitlab-ci-dot-yml/)에서 좀 더 읽을 수 있다. 

### Creating a simple .gitlab-ci.yml file

> Note: .gitlab-ci.yml은 YAML 파일이기 때문에 들여쓰기에 좀 더 주의를 기울여야 한다. 항상 탭이 아닌 스페이스를 사용한다.

리파지토리의 루트 디렉토리에 .gitlab-ci.yml 이름을 가진 파일을 생성해야 한다. 아래는 Ruby on Rails 프로젝트의 예제이다. 

```
before_script:
    - apt-get update -qq && apt-get instal -y -qq sqlite3 libsqlite3-dev nodejs
    - ruby -v
    - which ruby
    - gem install bundler --no-document
    - bundle install --jobs $(nproc) "${FLAGS[@]}"

rspec:
    script:
        - bundle exec rspec

rubocop:
    script:
        - bundle exec rubocop
```

이것은 대부분 Ruby 어플리케이션에서 동작할 수 있는 가장 간단하고 가능한 설정이다.:
1. 실행할 명령이 서로 다른 rspec과 rubocop(이름이 임의로 지정됨)의 두 가지 작업을 정의.
2. 모든 작업이 실행되기전에, before_script에 정의된 명령이 실행된다.

.gitlab-ci.iml 파일은 작업 실행 방법과 시기에 대한 제약이 있는 작업 집합을 정의한다. 작업은 이름을 가진(예제에서 rspec, rubocop)최상위 요소로 정의되고 항상 script 키워드를 포함해야 한다. 작업은 일자리를 만드는데 사용되며,그 후 Runner들이 선택해 Runner의 환경 안에서 실행한다.

중요한 것은 각각의 작업이 각각으로 부터 독립적으로 실행된다는 점이다.

만약 프로젝트의 .gitlab-ci.yml이 유효한지 확인하기를 원하면, 프로젝트 네임스페이스의 /ci/lint 페이지 아래에 Lint tool이 있다. 또한 프로젝트의 CI/CD->pipelines 와 Pipelines->Jobs 아래 페이지에 가면 "CI Lint" 버튼을 찾을 수 있다. 

.gitlab-ci.yml 문법에 대해 좀 더 알고 싶을 경우 [the reference documentation on .gitlab-ci.yml](https://docs.gitlab.com/ee/ci/yaml/README.html)을 읽어라

### Push .gitlab-ci.yml to GitLab

.gitlab-ci.iml을 만든 후에는 Git 저장소에 추가하여 GitLab에 푸시해야 한다.

```
git add .gitlab-ci.yml
git commit -m "Add .gitlab-ci.yml"
git push origin master
```

이제 Pipelines 페이지로 가면 pipeline이 pending중인 것을 볼 수 있다.

> Note: GitLab이 가져 오는 미러 된 저장소가있는 경우 프로젝트의 Settings > Repository > Pull from a remote repository > Trigger pipelines for mirror updates. 파이프 라인 트리거링을 활성화해야합니다.

커밋 페이지로 이동하여 커밋 SHA 옆에 작은 일시 중지 아이콘을 표시 할 수도 있다. 

![new commit](https://docs.gitlab.com/ee/ci/quick_start/img/new_commit.png)

이것을 클릭하면 해당 커밋의 jobs 페이지로 이동할 것이다.

![single_commit_status_pending](https://docs.gitlab.com/ee/ci/quick_start/img/single_commit_status_pending.png)

.gitlab-ci.yml에 작성했던 이름이 붙여진 pending 작업이 있음을 주목해라. "stuck"은 해당 작업에 대해 구성된 Runner가 아직 없음을 가리킨다.

다음 단계는 pending 중인 작업을 선택하도록 Runner를 구성하는 것이다.

## Configuring a Runner


GitLab에서, runner는 .gitlab-ci.yml에 정의한 작업을 수행한다. Runner는 가상 머신, VPS, 베어 메탈 머신, 도커 컨테이너 또는 컨테이너 클러스터 일 수 있다. GitLab과 Runners는 API를 통해 통신하기 때문에 Runner의 머신은 GitLab 서버에 네트워크로 액세스 할 수 있다.

Runner는 GitLab에서 특정 프로젝트에만 한정되거나 여러 프로젝트를 제공 할 수 있다. 모든 프로젝트를 제공하는 경우 Shared Runner라고 한다.

[Runners](https://docs.gitlab.com/ee/ci/runners/README.html) 문서에서 다른 Runners에 대한 자세한 정보를 찾으십시오.

Settings->CI/CD에서 어떤 Runner가 할당되어 있는지 확인할 수 있다. 러너 설정은 쉽고 간단하다. GitLab에서 지원하는 공식 러너는 Go로 작성되었으며 문서는 https://docs.gitlab.com/runner/에서 찾을 수 있다.

기능적인 러너를 얻으려면 다음 두 단계를 따라야한다.

1. [Install it](https://docs.gitlab.com/runner/install/)
2. [Configure it](https://docs.gitlab.com/ee/ci/runners/README.html#registering-a-specific-runner)

위의 링크를 따라 자신의 러너를 설정하거나 다음 장에서 설명하는 공유 러너를 사용해라. 

Runner가 설정되면 Settings->CI/CD에 따라 프로젝트의 Runner 페이지에서 확인해야 한다.

![runners_activated](https://docs.gitlab.com/ee/ci/quick_start/img/runners_activated.png)

### Shared Runners
GitLab.com을 사용한다면 GitLab에서 제공되는 shared Runners를 사용 할 수 있다.

이들은 GitLab의 인프라에서 실행되며 모든 프로젝트를 구축 할 수있는 특별한 가상 머신이다.

공유 러너를 사용하려면 프로젝트의 Settings->CI/CD로 이동하여 공유 러너 사용을 클릭해야한다.

[Read more on Shared Runner](https://docs.gitlab.com/ee/ci/runners/README.html)

## Seeing the status of your pipeline and jobs
성공적으로 Runner 구성을한 후, 마지막 커밋의 상태가 pending에서 running, success나 failed로 변경 되었는지 확인해야 한다.

프로젝트의 Pipeline 페이지에서 모든 pipeline를 볼 수 있다

![pipelines_status](https://docs.gitlab.com/ee/ci/quick_start/img/pipelines_status.png)

또는 Pipelines->Jobs 페이지에서 모든 작업을 확인할 수 있다.

![build_status](https://docs.gitlab.com/ee/ci/quick_start/img/builds_status.png)

job의 상트를 클릭하여, 해당 job의 로그를 볼 수 있다. 이것은 왜 일이 실패하거나 당신이 예상했던 것과 다르게 행동하는지 진단하는 데 중요하다.

![build_log](https://docs.gitlab.com/ee/ci/quick_start/img/build_log.png)

Commit 및 Merge 요청과 같은 GitLab의 다양한 페이지에서 커밋 상태를 볼 수도 있다



https://docs.gitlab.com/ee/ci/quick_start/README.html
