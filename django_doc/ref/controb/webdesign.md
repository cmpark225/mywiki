# django.contrib.webdesign

```
{% load webdesign %}

{% lorem 1 p random %}
{% lorem 2 w %}
{% lorem 4 b random %}

```

## Template tags
INSTALLED_APP 에 'django.contrib.webdesign' 추가. 
{% load webdesign%}을 사용하여 템플릿에 태그 접근 권한을 준다.

## lorem

Usage:
```
{% lorem [count] [method] [random] %}
```
lorem 태그에 0~3개 argument 사용 가능. 

argument => 
count : default = 1
method: default = b 
random
