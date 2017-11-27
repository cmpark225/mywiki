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

## MEDAI_ROOT

Default: ' ' (Empty string)

설치에 대한 미디어 파일 보관를 위한 디렉토리의 절대 경로

Example: "/home/media/media.lawrence.com/"

## MEDIA_URL

Default: ' ' (Empty string)

MEDIA_ROOT에서 제공되는 미디어를 처리하는 URL

Example: "http://media.lawrence.com/"

## TEMPLATE_DIRS

Default: () (Empty tulpe)

django.template.loaders.filesystem.Loader가 검색 한 템플릿 소스 파일의 위치를 검색순서대로 나열한  목록 


경로는 윈도우에서도 Unix 스타일인 슬래시를 사용해야 한다.

## TEMPLATE_LOADERS

Default:

```
('django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader')
```

string으로 명시된 템플릿 로더 클래스의 튜플. 각각의 로더 클래스는 특정 소스에서 템플릿을 가져 오는 방법을 알고 있다. 선택적으로 문자열 대신 튜플을 사용할 수 있다. 튜플의 첫 번째 항목은 로더의 모듈이어야 하며 초기화하는 동안 후속 항목이 로더에 전달된다.

## USE_I18N

Default: True

internationalization 시스템을 사용할 것인지에 대한 boolean 값이다. False로 세팅하여 off 할 수 있는 방법을 쉽게 제공한다. Django는 internatioalizetion  machinery를 load 하지 않음으로써 몇가지 최적화를 제공한다.


## USE_L10N

Default: False 

데이터가 기본적으로 지역화되는지 여부를 지정하는 boolean 값이다. True로 설정되어 있을 경우 Django는 숫자와 날짜를 현재 locale 포맷으로 출력할 것이다.

