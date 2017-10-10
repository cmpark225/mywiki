## APPEND_SLASH

Default: True

True로 설정하면 요청 URL이 URLconf의 패턴과 일치하지 않고 슬래시로 끝나지 않으면 동일한 URL에 슬래시가 추가 된 HTTP 리디렉션이 실행된다. 리다이렉트 (redirect)는 POST 요청으로 제출 된 데이터가 손실 될 수 있으니 주의해야 한다.

APPEND_SLASH 설정은 CommonMiddleware가 설치된 경우에만 사용(미들웨어 참조).

## LOCALE_PATHS

Default: () (Empty tuple)

Django가 translation하기 위해 참조하고 있는 디렉토리의 튜플

Example:

```
LOCALE_PATHS = (
	'/home/www/project/common_files/locale',
	'/var/local/translation/locale'
)
```

일반적인 '/ path / to / locale / xx / LC_MESSAGES' 계층 구조가있는 경우 locale 디렉토리 경로 (예 : '/ path / to / locale')를 사용해야한다.

## USE_I18N

Default: True

internationalization 시스템을 사용할 것인지에 대한 boolean 값이다. False로 세팅하여 off 할 수 있는 방법을 쉽게 제공한다. Django는 internatioalizetion  machinery를 load 하지 않음으로써 몇가지 최적화를 제공한다.


## USE_L10N

Default: False 

데이터가 기본적으로 지역화되는지 여부를 지정하는 boolean 값이다. True로 설정되어 있을 경우 Django는 숫자와 날짜를 현재 locale 포맷으로 출력할 것이다.

