## Transaction
트랜젝션 특성
#### Atomicity(원자성)
#### Consistancy(일관성)
#### Isolation(고립성)
 순서대로 처리할 경우 성능 문제 발생 / lock -> 어떻게 처리할 건지 선택이 필요.
#### Durability(지속성)

## lock
### 강도로 구분
##### read (shrad)
다른 트랜젝션이 read 가능 write 불가능
##### write (Exclusive)
다른 트랜젝션이 read/write 불가능

#### read/write lock 설정 시 발생할 수 있는 문제
##### blocking
##### Deadlock
두개의 트랜젝션이 서로 다른 트랜젝션을 기다려 
아무런 처리를 할 수 없는 불가능한 상태가 발생 

##### 해결 방안 
1. 트랜젝션을 짧게 가진다.
2. 타임아웃 활용
3. 쿼리 시간을 줄인다(빨리 처리해서 빨리 끝내자)
4. 적절한 Isolation level 선택

### 범위로 구분
row 단위, page 단위 ...어떤 단위로 lock을 가질 것인가.
DB나 엔진 Isolation level에 따라 변할 수 있다.
* row 

* page

* table 
** Srializable Read 레벨을 가질 경우 인서트를 막기 위해 Table lock을 시켜야 한다.

* database


## Isolation level

### 적절한 Isolation level 잘못 선택 시 문제점이 발생한다.
(Isolation level이 약할 경우.)
1. Dirty read
신뢰할 수 없는 값을 읽어감
읽어간 값에 대해서 다른 트랜젝션이 롤백을 수행해서 값이 변경되는 경우.

2. non-Repeatable Read(반복해서 읽을 수 없음)
반복해서 읽을때 마다 값이 바뀜 
(다른 트랜젝션이 계속 업데이트 처리)

3. Phantom Read
값이 생성되고 없어지는 것이 반복적으로 일어남 (데이터에 대해서 신뢰할 수 없음)
(다른 트랜젝션이 계속 인서트 처리)

### level 종류
밑으로 갈 수록 레벨 강도가 높다.

##### Read uncomnuit
커밋하지 않은 데이터를 읽어갈 수 있다. (롤백에 대한 이슈가 있음)
Ex) 데이터 값 0
트랜젝션이 값 1로 변경 아직 commit x 상태
다른 트랜젝션이 데이터 Read 요청 시 commit 전 데이터인 1을 Read

##### Read comunited
커밋할때 까지 대기 후 커밋 하면 데이터 Read
Dirty Read에 문제점에 대해서는 Read comunited 레벨을 선택하여 해결이 가능하다.

##### Repeatable Read
다른 트랜젝션에서 업데이트 불가 (이미 있는 데이터에 대해서는 무결성 보장)
(mysql)


##### Srializable Read
다른 트랜젝션에서 인서트 불가

Ex)
업데이트가 계속 이뤄지는데 사용자가 데이터를 실시간으로 확인(Read)이 필요한 경우와 같이 실시간 데이터가 더 중요한 서비스의 경우 Repeatable Read 레벨까지는 사용할 필요가 없다.

성능 보다 정확성이 중요할 경우에는 Srializable Read 레벨을 사용해야 한다.

자신의 서비스에 맞게 레벨을 선택할 필요가 있다.
