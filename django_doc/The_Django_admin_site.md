
## Overriding admin templates
admin 모듈이 admin 사이트의 다양한 페이지를 생성하는 데 사용하는 많은 템플릿을 비교적 쉽게 재정의할 수 있다.특정 앱 또는 특정 모델에 대해 템플릿 중 일부를 재정의할 수도 있다.

### Set up your projects admin template directories

admin 템플릿 파일은 contrib/admin/templates/admin 폴더에 있다.

템플렛을 override 하기 위해서는 우선 프로젝트의 템플릿 디렉토리에 admin 디렉토리를 생성해야한다. TEMPLATE_DIRS에 명시되어 있는 어느 디렉토리라도 괜찮다.

이 admin 디렉토리 안에 앱 이름을 가진 서브디렉토리를 만든다. 그리고 나서 모델의 이름을 가진 서브디렉토리를 만든다. admin앱은 디렉토리를 찾을 때 모델 이름을 소문자로 찾는다. 따라서 대소문자를 구분하는 파일 시스템에서 앱을 실행하려면 모두 소문자로 디렉토리 이름을 지정해야 한다.

특정 앱의 admin 템플릿을 override 하기 위해 django/contrib/admin/temlates/admin 디렉토리에서 템플릿을 복사하고 수정한다. 그리고 만들었던 디렉토리 중 하나에 저장한다.

예를들어, 앱 이름이 my_app에서 모든 모델의 수정사항을 볼 수 있는 tool을 추가하고 싶을 경우, contrib/admin/temlates/admin/change_list.html을 우리 프로젝트의 templates/admin/my_app 디렉토리에 에 복사할 것이다, 그리고 필요한 변경을 할 수 있다.

만약 'Page'이름을 가진 모델에만 변경사항 리스트 tool을 추가하고 싶다면, 위와 동일한 파일을 프로젝트의 templates/admin/my_app/page 디렉토리에 복사할 것이다.

### Overriding vs. replacing an admin template
admin 템플릿의 모듈 식 설계로 인해 일반적으로 전체 템플릿을 대체 할 필요가 없으며 권장되지 않는다. 변경이 필요한 템플릿의 섹션만 대체하는 것이 좋다.

위 예제에서 계속해서 Page모델의 History tool옆에 새로운 링크를 추가하려면. change_form.html을 보고 object-tools 블록을 override 하기만 하면 된다. 우리의 새로운 change_form.html이다.:
```
{%{% extends "admin/change_form.html" %}
{% load i18n %}
{% block object-tools %}
{% if change %}{% if not is_popup %}
  <ul class="object-tools">
    <li><a href="history/" class="historylink">{% trans "History" %}</a></li>
    <li><a href="mylink/" class="historylink">My Link</a></li>
    {% if has_absolute_url %}
        <li><a href="../../../r/{{ content_type_id }}/{{ object_id }}/" class="viewsitelink">
            {% trans "View on site" %}</a>
        </li>
    {% endif%}
  </ul>
{% endif %}{% endif %}
{% endblock %}
```
만약 이 파일을 templates/admin/my_app 디렉토리에 위치시킨다면 모든 모델의 change form에 new link가 보일 것이다.

### Tempaltes which may be overridden per app or model

contrib/admin/templates/admin의 모든 템플릿이 앱마다 또는 모델마다 override할수 있는 것은 아니다. 아래 목록만 override가 가능하다.
* app_index.html
* change_form.html
* change_list.html
* delete_confirmation.html
* object_history.html

이런식으로 override 할 수 없는 템플릿의 경우 전체 프로젝트에 대해 override할 수 있다. 새로운 파일을 templates/admin 디렉토리에 위치시키면 된다. 이 기능은 맞춤 404 및 500 페이지를 만드는 데 특히 유용하다.

>change_list_request.html과 같은 일부 관리 템플릿은 사용자 정의 포함 태그를 렌더링하는 데 사용된다. 이것들은 override 될지도 모르지만 그런 경우에는 문제의 태그에 대한 새로운 버전을 만들고 다른 이름을 주는 것이 더 나을 것이다. 그렇게 하면 선택적으로 사용할 수 있다.
