# django-admin.py and manage.py

## Available commands

### syncdb

*django-admin.py syncdb*

INSTALLED_APPS에 있는 모든 앱의 생성되지 않은 테이블에 대해 테이블을 생성한다.
프로젝트에 새로운 applications 추가시 명령어 사용한다.

> syncdb는 이미 있는 테이블에 대해 변경하지 않는다.
syncdb 는 설치되지 않은 모델에 대해서만 테이블을 생성한다. 설치 후 모델 클래스의 변경 사항과 일치하도록 ALTER TABLE문을 절대로 발행하지 않는다. (데이터 손실 위험)
모델을 변경하고 일치시킬 데이터베이스 테이블을 변경하려면 sql 명령을 사용하여 새 SQL 구조를 표시하고 이를 기존 테이블의 스키마와 비교하여 변경 사항을 해결해야 한다.

The --noinput option may be provided to suppress all user prompts.

The --database option can be used to specify the database to synchronize.
