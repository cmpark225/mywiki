model이 변경된 후 manage.py syncdb 명령어를 실행하면 

이미 존재한 table에 대해서는 ALTER TABLE을 수행하지 않기 때문에, 

변경된 사항에 대해서 기존 테이블에 적용되지 않는다.

> ##### Syncdb will not alter existing tables
> syncdb will only create tables for models which have not yet been 
installed. It will never issue ALTER TABLE statements to match changes made to a model class after installation. Changes to model classes and database schemas often involve some form of ambiguity and, in those cases, Django would have to guess at the correct changes to make. There is a risk that critical data would be lost in the process. 

model 수정 후 테이블에 적용하고 싶을 경우


1. sql 사용하여 테이블 변경
2. datadump > drop table > syncdb > dataload 를 이용하여 테이블 변경사항 적용

두가지 방법중 선택해서 이용하면 된다.


예를 들어 mysite app의 poll 모델의 변경사항을 적용하고 싶다면

## 1. dumpdata

명령어
```
$ python manage.py dumpdata mysite.poll
[{"pk": 1, "model": "wisdom.postimage", "fields": {"post": 1, "image": "wisdom_images/q8.png"}}, {"pk": 2, "model": "wisdom.postimage", "fields": {"post": 2, "image": "wisdom_images/8b.png"}}]

```
해당 명령어를 실행하면 json 형식으로 DB에 저장되어 있던 데이터들이 출력된다.

데이터를 파일로 저장은 리다이렉션 커맨드를 이용하면 된다.

```
$ python manage.py dumpdata mysite.poll > dump_poll.json
```

## 2. drop table
syncdb 명령어는 이미 존재한 테이블에 대해서 적용되지 않기 때문에 직접 sql을 통해 table을 제거한다.

```
mysql> DROP TABLE mysite_poll;
Query OK, 0 rows affected (0.01 sec)
```

## 3. syncdb
syncdb 명령어를 통해 model에 맞는 테이블을 다시 생성한다.

```
$ python manage.py syncdb
```


## 4. loaddata
dump했던 data를 load 하여 원래 데이터와 동일하게 만든다.

```
$ python manage.py loaddata dump_poll.json
```
