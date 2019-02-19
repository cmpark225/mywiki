1. (select ... where condition) + (update ... where condition)
2. update ... where condition


=> 1의 경우 select의 조건이 있을 경우 update도 이뤄지므로
select 조건에 대해 히트가 있을 경우 계산이 두 번 이뤄진다. 
따라서 2번이 더 효율적이다. 

하지만 트리거가 있을 경우 2는 항상 발생하기 때문에 1 사용이 옳다.
