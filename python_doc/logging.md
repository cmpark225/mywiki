
로거는 직접 인스턴스화되지 않지만 항상 모듈 수준의 함수 logging.getLogger(name)을 통해 사용된다. 같은 이름의 getLogger() 호출은  동일한 Logger 인스턴스를 반환한다.

이름은 계층 구조를 가진다. ex) foo.bar.baz


class logging.Logger

### Logger.propagate
이 값이 True일 경우 상위 로거로 전달된다. false일 경우 로깅 메시지가 상위 로거의 핸들로러 전달되지 않는다. 
Default : True 

### Logger.setLevel(level)
로거의 level 설정. 설정된 레벨보다 낮을 경우 메시지는 무시된다. 로그 생성시 level은 NOTSET으로 설정된다. (NOTSET : 로그 작성기가 루트 로거 일 때는 모든 메시지 처리, 루트가 아닐 경우에는 부모레벨을 따라감)루트 로거는 레벨이 WARNING으로 생성 된다. 

NOTSET 부모에게 위임은 NOTSET이 아닌 다른 상위 수준이 발견되거나 루트에 도달 할 때까지 상위 조상 로거 체인이 통과 함을 의미합니다.

조상이 NOTSET이 아닌 다른 레벨에서 발견되면 조상의 레벨은 조상 검색이 시작된 로거의 유효 레벨로 간주되어 로깅 이벤트가 처리되는 방식을 결정하는 데 사용됩니다.

루트에 도달하고 NOTSET 레벨이 있으면 모든 메시지가 처리됩니다. 그렇지 않으면 루트 레벨이 유효 레벨로 사용됩니다.

### Logger.isEnabledFor(lvl)
입력받은 lvl 수준의 메시지 처리가 가능한지 확인.

### Logger.getEffectiveLevel()
이 로거의 유효 수준을 나타냅니다. NOTSET 이외의 값이 setLevel ()을 사용하여 설정되면 반환됩니다. 그렇지 않으면, 계층 구조는 NOTSET 이외의 값이 발견 될 때까지 루트를 향해 탐색되고 그 값이 리턴됩니다. 반환되는 값은 정수이며 일반적으로 logging.DEBUG, logging.INFO 등 중 하나입니다.

https://docs.python.org/2.7/library/logging.html
