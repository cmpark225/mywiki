## Loading templates

일반적으로, low-level의 Template API를 사용하지 않고 파일 시스템의  파일에 template를 저장한다. template directory로 지정된 디렉토리에 template를 저장해라.

장고는 template-loader 세팅에 따라 여러 위치에 있는 template 디렉토리를 검사한다. 그러나 template 디렉토리들을 지정하는 가장 기본적인 방법은 TEMPLATE_DIRS 설정을 이용하는 것이다.


### The TEMPLATE_DIRS settings

settings 파일의 TEMPLATE_DIRS 설정을 사용하여 template 디렉토리가 무엇인지 알려라. TEMPLATE_DIRS 는 template 디렉토리의 full 경로를 포함한 string 의 list나 tuple로 설정되어야 한다(ies). 

예)

```
TEMPLATE_DIRS = (
	"/home/html/templates/lawrence.com",
	"/home/html/templates/default",
)
```

디렉토리와 template가 웹 서버에서 읽을 수 있는 한 원하는 위치로 이동할 수 있다. 원하는 확장자를 가질 수 있다. .html이나 .txt 또는 확장자가 없을 수도 있다.

경로는 윈도우에서도 Unix 스타일인 슬래시를 사용해야 한다.
