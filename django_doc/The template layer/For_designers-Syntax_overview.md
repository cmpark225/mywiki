## Template inheritance
Django 템플릿 엔진의 가장 큰 강점 중 하나는 템플릿 상속이다. 템플릿 상속을 사용하면 사이트의 모든 공통 요소가 포함 된 기본 "skeleton"템플릿을 만들고 하위 템플릿에서 재정의 할 수있는 블록을 정의 할 수 있다.

예제를 사용해 템플릿 상속을 이해하는 것이 가장 쉽다. : 
```
<!DOCTYPE HTML>
<html>
<head>
    <link rel="stylesheet" href="style.css" />
    <title>{% block title %} My amazing site {% endblock %}</title>
</head>
<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```
base.hmtl인 이 템플릿은 2개 컬럼 페이지에 사용할 수 있는 간단한 HTML 문서를 정의한다. 하위 템플릿은 빈 block을 채우는 역할을 가진다. 

이 예에서 {% block %} 태그는 하위 템플릿에서 채울수 있는 3개의 블록을 정의한다. 모든 블록 태그는 하위 템플릿이 템플릿의 해당 부분을 재정의 할 수 있다고 템플릿 엔진에게 알리는 역할을 한다.

하위 템플릿은 아래와 같다 :
```
{% extends "base.html" %}

{% block title %} My amazing blog {% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2> {{ entry.title }} </h2>
    <p> {{ entry.body }} </p>
{% endfor %}
{% endblock %}
```

여기에 있는 {% extends %}가 핵심이다. 이것은 테플릿 엔진에게 이 템플릿은 다른 템플릿을 "extends"했다고 알려준다. 템플릿 시스템이 이 템플릿을 평가할때 먼저 부모를 찾는다 -- 이 경우에는 "base.html"이다.

이때 템플릿 엔진은 base.html에 있는 세개의 {% block %} 태그를 알아차리고 하위 템플릿의 내용으로 이 블록들을 변경시킨다. blog_entries의 값에 따라 결과는 아래와 같다.
```
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <link rel="stylesheet" href="style.css" />
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

하위 템플릿은 사이드 바 블록을 정의하지 않았기 때문에 상위 템플릿의 값이 대신 사용된다. 상위 템플릿의 {% block %} 태그 내에있는 콘텐츠는 항상 대체 콘텐츠로 사용된다.

필요에 따라 많은 수준의 상속을 사용할 수 있다. 상속을 사용하는 일반적인 방법 중 하나는 다음 세 가지 수준의 접근 방식이다.
* 사이트의 기본 모양과 느낌을 유지하는 Base.html 템플릿
* 사이트의 각 "section"에 대한 base_SECTIONNAME.html 예: base_new.html, base_sports.html. 이 템플릿들은 모두 base.html을 확장하고 섹션의 특정 스타일 디자인을 포함한다.
* 뉴스 기사 또는 블로그 항목과 같은 각 페이지 유형에 대한 개별 템플릿. 이러한 템플릿은 section 템플릿을 확장한다.

이러한 접근법은 코드 재사용을 극대화하고 섹션 전반의 탐색과 같은 공유 콘텐츠 영역에 항목을 쉽게 추가 할 수 있게 한다.

상속과 관련한 작업을 위한 몇 가지 팁:
* 템플릿에 {% extends %}를 사용할 경우 반드시 템플릿의 첫번째 템플릿 태그여야 한다. 다른 방식으로는 템플릿 상속은 동작하지 않는다.
* base 템플릿에 {% block %} 태그를 더 두는 것이 낫다. 하위 템플릿은 모든 상위 템플릿을 정의할 필요가 없으므로, 여러 블록에서 적절한 기본 값을 채우고 나중에 필요한 템플릿을 정의할 수 있다. 적은 수의 훅보다 더 많은 훅을 가지고 있는 것이 좋다.
* 여러개의 템플릿에서 중복되는 내용을 발견했다면 상위 템플릿의 {% block %}으로 이동해야 한다.
* 컨텐츠를 상위 템플릿으로부터 가져와야 할 경우, {{ block.super}} 변수를 사용하면 된다. 이 기능은 상위 블록의 내용을 완전히 재정의하는 대신 추가하려는 경우에 유용하다. 필요한 경우 {{block.super}}를 사용하여 삽입 한 데이터는 부모 템플릿에서 이미 이스케이프되었으므로 자동으로 이스케이프되지 않는다. 
  
* 가독성을 위해 {% endblock %} 태그에 이름을 줄 수 있다(옵션). 크기가 큰 템플릿에서는 {% block %} 태그가 닫혔는지 확인하는데 유용할 것이다.
```
{% block content %}
...
{% endblock content %}
```

동일한 템플릿에서 같은 이름의 {% block %} 태그를 정의할 수 없는 것을 명심해라. 이런 제한 사항은 block 태그가 "양쪽"방향으로 동작하기 때문에 있다. 즉 block 태그는 단순히 채울 hole을 제공하는 것이 아니라 부모의 hole을 content로 채우는 것을 정의한다(?). 만약 템플릿에 두개의 같은 이름의 {% block %} 태그가 있을 경우 부모의 템플릿은 어떤것이 블록의 내용으로 사용할지 알 수가 없다. 

