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
