# Working with forms

django.forms는 Django의 form handling library이다.

Django의 HttpRequest 클래스를 사용하여 form 제출을 처리하는 것이 가능하지만 form 라이브러리를 사용하면 일반적인 form 관련된 작업을 처리 할 수 있다. 이것을 사용하면 아래와 같은 일을 할 수 있다:

1. 자동으로 생성된 form 위젯과 함께 HTML form을 표시.
2. 일련의 유효성 검사 규칙에 대해 제출된 데이터 확인
3. 유효성 검사 오류의 경우 form 재 표시.  
4. 제출된 form data를 관련 Python 데이터 유형으로 변환.

## Overview
해당 library는 다음과 같은 개념을 다룬다.:

**widget**
HTML form 위젯에 해당하는 클래스. ex) ``` <input type="text"> ```나 ```<textarea>```. 위젯을 HTML로 렌더링한다. 

**Field**
유효성 검사를 담당하는 클래스. ex) 그 데이터가 유효한 전자 메일 주소인지 확인하는 EmailField

**Form**
스스로 유효성을 검사하고, HTML로 표시하는 방법을 알고 있는 필드 컬렉션.

**Form Media**
form을 렌더링하는데 필요한 CSS, JavaScript 리소스 

라이브러리는 데이터베이스 레이어, 뷰, 템플릿과 같은 다른 Django 구성 요소와 분리된다. Django 설정, django.utils 도움 함수 와 Django의 국제와 hook에 의존한다. (라이브러리를 사용하기 위해 국제화 기능을 사용할 필요는 없다.)

## Form objects
Form 객체는 form 필드 시퀀스와 form을 수락하기 위해 충족되어야 하는 유효성 검사 규칙 모음을 캡슐화 한다. Form 클래스는 django.forms.Form의 하이 클래스로 생성되며 Django의 데이터베이스 모델을 사용했다면 익숙한 선언 스타일을 사용한다. 

예를 들어, 개인 웹 사이트에서 "연락하기" 기능을 구현하는데 사용되는 양식을 고려한다면 :

```
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```
form은  Field 개체로 구성된다. 이 경우 form에는 subject, message, sender 및 cc_myself라는 네 개의 필드가 있다. CharField, EmailField 및 BooleanField는 사용 가능한 팔드 유형 중 세 가지이다. 전체 목록은 Form field에서 찾을 수 있다. 

Django 모델을 직접 추가하거나 편집하기 위해 양식을 사용하는 경우 ModelForm을 사용하여 모델 설명을 복제하지 않아도 된다. 

### Using a form in a view
 view 에서 form을 처리하기 위한 표준 패턴은 아래와 같다:
 ```
 def contact(request):
    if request.method == 'POST': # If the form has been submitted...
    form = ContactForm(request.POST) # A form bound to the POST data
    if form.is_valid():
        # Process the data in form.cleaned_data
        # ...
        return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render_to_response('contact.html', {
        'form':form,
        })
 ```
여기에는 세 가지 코드 경로가 있다.

1. form이 제출되지 않은 경우 ContactForm의 언바운드 인스턴스가 만들어져서 템플릿에 전달된다.
2. form이 제출된 경우 request.POST를 사용하여 form의 바운드 인스턴스가 작성된다. 제출된 데이터가 유효하면 처리되고 사용자는 'thanks' 페이지로 리디렉션된다.
3. form이 제출되었지만 유효하지 않은 경우, 바운드 양식 인스턴스가 템플릿에 전달된다.
   
바운드된 폼과 언바운드 폼의 구분은 중요하다. 언바운드 form은 연결된 데이터가 없다. 사용자에게 렌더링 될 때 비어있거나 기본 값을 포함한다. 바운드된 form은 데이터를 제출했으므로 해당 데이트가 유효한지 여부를 나타내는데 사용 할 수 있다. 유효하지 않은 바운드 form이 렌더링되었을 경우에는 사용자에게 잘못된 위치를 알리는 인라인 오류 메시지가 포함될 수 있다.

바운드 형식과 언바운드형식 간의 차이점에 대한 자새한 내용은 [Bound and unbound forms](https://django.readthedocs.io/en/1.3.X/ref/forms/api.html#ref-forms-api-bound-unbound)를 참조한다.

### Handling file uploads with a form
form으로 파일 업로드를 다루는 방식은 [Binding uploaded files to a form](https://django.readthedocs.io/en/1.3.X/ref/forms/api.html#binding-uploaded-files)을 참조해라

### Processing the data from a form
is_valid()가 True를 리턴했을때, form에 정의된 유효성 검사 규칙을 준수한다는 것을 알고 form제출을 안절하게 처리할 수 있다. 이 시점에서 request.POST에 직접 접근 할 수 있지만 form.cleaned_data에 접근 하는 것이 좋다. 이 데이터는 검증되었을 뿐만 아니라 관련 python 타입으로 변환될 것이다. 위 예에서 cc_myself는 boolean 값이다. 마찬가지로 IntegerField와 FloatField 와 같은 필드는 값을 각각 Python int 와 float로 변환한다. read-only필드는 form.cleaned_data에서 사용할 수 없다 (사용자 정의의 clean() 메소드 값 설정은 아무런 효과가 없다.) 이 필드는 입력 요소가 아닌 텍스트로 표시되므로 서버에 다시 게시되지 않기 때문이다.

위의 예제를 확장해서 form데이터를 처리하는 방법은 아래와 같다:
```
if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']

    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)
    
    form django.core.mail import send_mail
    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/') # Redirect after POST
```

### Displaying a form using a template
form은 Django 템플릿 언어로 작업하도록 설계되었다. 위의 예제에서 컨텍스트 변수 형식을 사용해서 ContactForm인스턴스를 템플릿에 전달했다. 아래는 간단한 예제 템플릿이다:
```
<form action='/contact/' method="post">{% csrf_token %}
{{form.as_p}}
<input type="submit" value="Submit" />
</form>
```
form은 자기 자신 필드만 출력한다; 주변의 <form> 태그와 submit 버튼은 너에게 달려있다.

form.as_p는 각 form 필드와 함께 레이블을 단락으로 묶은 form을 출력한다. 예제 템플릿 출력은 아래와 같다.
```
<form action="/contact/" method="post">
<p><label for="id_subject">Subject:</label>
    <input id="id_subject" type="text" name="subject" maxlength="100" /></p>
<p><label for="id_message">Message:</label>
    <input type="text" name="message" id="id_message" /></p>
<p><label for="id_sender">Sender:</label>
    <input type="text" name="sender" id="id_sender" /></p>
<p><label for="id_cc_myself">Cc myself:</label>
    <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
<input type="submit" value="Submit" />
</form>
```

각 form 필드에는 id_<field-name>으로 설정된 ID 속성이 있으며, 이는 함께 제공되는 레이블 태그에 의해 참조된다. 이는 form이 screen reader software와 같은 보조 기술에 접근 할 수 있도록 하기 위해 중요하다. 또한 레이블과 ID가 생성되는 방식을 사용자가 정의 할 수 있다.

또한 form.as_table을 사용해 테이블 행을 출력하고(자신의 <table> 태그를 제공해야 함.) form.as_ul을 사용해서 목록 항목을 출력 할 수 있다.

### Customizing the form template
생성 된 기본 HTML이 사용자 취향에 맞지 않을 경우 Django 템플릿 언어를 사용해서 form을 표시하는 방식을 완전히 커스텀할 수 있다. 위의 예를 확장한것:
```
<form action="/contact/" method="post">
    {{ form.non_field_errors }}
    <div class="fieldWrapper">
        {{ form.subject.errors }}
        <label for="id_subject">E-mail subject:</label>
        {{ form.subject }}
    </div>
    <div class="fieldWrapper">
        {{ form.message.errors }}
        <label for="id_message">Your message:</label>
        {{ form.message }}
    </div>
    <div class="fieldWrapper">
        {{ form.sender.errors }}
        <label for="id_sender">Your email address:</label>
        {{ form.sender }}
    </div>
    <div class="fieldWrapper">
        {{ form.cc_myself.errors }}
        <label for="id_cc_myself">CC yourself?</label>
        {{ form.cc_myself }}
    </div>
    <p><input type="submit" value="Send message" /></p>
</form>
```

각 명명된 form 필드는 form 위젯을 표시하는데 필요한 HTML을 생성하는 {{form.name_of_field}}을 사용하여 템플릿으로 출력 할 수 있다. {{form.name_of_field.error}}를 사용하면 양식 오류 목록이 표시되고 순서가 지정되지 않은 목록으로 렌더링 된다. 이것은 아래와 같이 보인다.:

```
<ul class="errorlist">
    <li>Sender is required.</li>
</ul>
```

이 리스트는 errorlist 의 CSS 클래스가 있어 스타일을 지정 할 수 있다. 만약 오류 표시를 추가로 사용자 정의하려면 오류를 반복하여 표시 할 수 있다.:
```
{% if form.subject.erroros %}
    <ol>
    {% for error in form.subject.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif%}
```

### Looping over the form's fields
만약 각각의 form field를 위해 같은 HTML을 사용한다면, {% for %} 루프를 사용하여 차례대로 각 필드를 반복하여 중복된 코드를 줄일 수 있다.
```
<form action="/contact/" method="post">
    {% for field in form %}
        <div class="fieldWrapper">
            {{ field.errors }}
            {{ field.label_tag }}: {{ field }}
        </div>
    {% endfor %}
    <p><input type="submit" value="Send message" /> </p>
</form>
```
이 루프 내에서 {{field}}는 BoundField의 인스턴스이다. BoundField에는 템플릿에 유용 할 수 있는 아래와 같은 특성도 있다.

**{{ field.label }}**

필드의 라벨 ex) Email address.

**{{ field.label_tag }}**

해당 HTML의 ```<label>``` 태그에 래핑된 필드의 하위 라벨 ex) ```<lable for="id_email">E-mail address</label>```

**{{ field.html_name }}**

input 요소의 이름 필드에 사용될 필드의 이름. form 접두어가 설정되어 있으면 이를 계정으로 가져온다.

**{{field.help_text}}**

필드와 연관된 도움말.

**{{ field.errors }}**

이 필드에 해당하는 유효성 검사 오류가 포함된 ```<ul class="errorlist"> ```를 출력한다. 오류에 대한 {% for error in field.errors %} 루프의 오류를 사용하여 오류 표시를 사용자 정의 할 수 있다. 이 경우 루프의 각 객체는 오류 메시지가 포함 된 간단한 문자열이다.

**field.is_hidden**

form field가 hidden 필드일 경우 이 속성은 True이다 아닐 경우에는 False. 템플릿 변수로 특히 유용하지는 않지만 다음과 같은 조건부 테스트에 유용 할 수 있다.
```
{% if field.is_hidden %}
    {# Do somthing special }
{% endif %}
```

#### Looping over hidden and visible fields

만약 Django의 기본 form 레이아웃에 의존하지 않고 수동으로 템플릿에 form을 레이아웃 하는 경우 ```<input type="hidden">```필드를 비 숨김 필드와 다르게 처리해야 할 수 있다. 예를들어 hidden 필드에는 아무 것도 표시되지 않으므로 오류 메시지를 필드 옆에 배치하면 사용자에게 혼동을 줄 수 있으므로 해당 오류를 다르게 처리해야 한다.

Django는 hidden_fields() 및 visible_fields()와 같이 숨김 필드와 표시 필드를 독립적으로 반복 할 수 있는 두가지 메서드를 제공한다. 아래는 이 두가지 방법을 사용하는 이전 예제를 수정한 것이다:
```
<form action="/contact/" method="post">
    {% for field in form.visible_fields %}
        <div class="fieldWrapper">

            {# Include the hidden fields in the form #}
            {% if forloop.first %}
                {% for hidden in form.hidden_fields %}
                {{ hidden }}
                {% endfor %}
            {% endif %}

            {{ field.errors }}
            {{ field.label_tag }}: {{ field }}
        </div>
    {% endfor %}
    <p><input type="submit" value="Send message" /></p>
</form>
```
이 예제이는 숨겨진 필드의 오류를 처리하지 않는다. 일반적으로 숨겨진 필드의 오류는 form 조작이 정상적으로 form 상호 작용으로 변경되지 않으므로 form 변조의 신호이다. 그러나 form 오류에 대한 오류 표시도 쉽게 삽입 할 수 있다.

### Reusable form templates
사이트에서 여러 위치의 form에 동일한 렌더링 논리를 사용하는 경우 form의 루프를 독립형 템플릿에 저장하고 include 태그를 사용하여 다른 템플릿에서 재 사용하여 중복을 줄일 수 있다.
```
<form action="/contact/" method="post">
    {% include "form_snippet.html" %}
    <p><input type="submit" value="Send message" /></p>
</form>

# In form_snippet.html:

{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }}: {{ field }}
    </div>
{% endfor %}
``` 
만약 템플릿에 전달 된 양식 객체가 컨텍스트 내에서 다른 이름을 갖는 경우 include 태그의 with 인수를 사용하여 별칭을 지정할 수 있다. 
```
<form action="/comments/add/" method="post">
    {% include "form_snippet.html" with form=comment_form %}
    <p><input type="submit" value="Submit comment" /></p>
</form>
```
이런 일을 자주 하는 경우 맞춤식 inclusion태그를 만드는게 좋다.


