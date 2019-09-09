# The Forms API

## Bound and unbound forms

Form 인스턴스는 데이터 집합에 바인딩되거나 바인딩되지 않는다.

* 데이터 집합에 바인딩된 경우, 데이터를 검증하고 HTML에 표시된 데이터와 함께 양식을 HTML로 렌더링할 수 있다.
* 바인딩되지 않은 경우 유효성 검사를 수행할 수 없지만(검증할 데이터가 없기 때문!) 빈 양식을 HTML로 렌더링할 수 있다.


*class* **Form**

바인딩되지 않은 Form 인스턴스를 생성하기 위해서, 클래스를 인스터화한다:

```
>>> f = ContactForm()
```

데이터를 form에 바인딩 하기 위해서는, Form 클래스에 딕셔너리로 데이터를 첫번째 파라메터로 전달한다.

```
>>> data = { 'subject': 'hello',
            'message': 'Hi there',
            'sender': 'foo@example.com',
            'cc_myself': True}
>>> f = ContactForm(data)
```

딕셔너리에서, 키는 Form 클래스에 해당하는 속성에 부합하는 field 이름이다. 값은 검증하기 위한 데이터이다. 이것들은 보통 문자열이지만, 문자열일 필요는 없다; 잠시 후에 보게 될 것처럼, 전달하는 데이터의 종류는 필드에 달려 있다.


**Form.is_bound**

runtime에 form 인스턴스가 바인딩된 상태인지, 바인딩 되지 않은 상태인지 구별하기 위해서는, form의 is_bound 속성 값을 확인한다:

```
>>> f = ContactForm()
>>> f.is_bound
False
>>> f = ContactForm({'subject':'hello'})
>>> f.is_bound
True
```

빈 딕셔너리를 전달할 경우, 빈 데이터를 가지는 bound된 form을 생성하는 것을 명심해라:

```
>>> f = ContractForm({})
>>> f.is_bound
True
```

바인딩된 form 인스턴스가 있고 데이터를 변경하려는 경우 또는 바인딩되지 않은 form 인스턴스를 일부 데이터에 바인딩하기 위해서는 다른 form 인스턴스를 생성해라. Form 인스턴스에서 데이터를 변경 할 수 있는 방법이 없다. Form 인스턴스가 생성되면, 데이터가 있든 없든 데이터가 불변인 것을 고려해야 한다.

## Using forms to validate data

**Form.is_valid()**

Form 객체의 주요 업무는 데이터를 검증하는것이다. 바인딩된 form 인스턴스에서, is_valid () 메서드를 호출하여 유효성 검사를 실행하고 데이터가 유효한지 여부를 지정하는 bool을 반환한다.:

```
>>> data = { 'subject': 'hello',
            'message': 'Hi there',
            'sender': 'foo@example.com',
            'cc_myself':True}
>>> f = ContractForm(data)
>>> f.is_valid()
True
```

유효하지 않은 데이터로 시도해보자, 아래 경우에, subject는 빈값이다(모든 필드가 기본적으로 required 이기 때문에 에러이다.) 그리고 sender는 유효하지 않은 이메일 주소이다.

```
>>> data = { 'subject': '',
            'message': 'Hi there',
            'sender': 'invalid e-mail address',
            'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
false
```

**Form.errors**

에러 메시지의 딕셔너리를 얻기 위해서는 errors 속성에 접근해라:

```
>>> f.errors
{'sender': [u'Enter a valid e-mail address.'], 'subject':[u'This field is required.']}
```
딕셔너리에서, 키는 필드 이름이고, value는 에러 메시지를 나타내는 유니코드 문자열들의 리스트이다. 에러 메시지는 여러개의 에러메시지를 가지고 있을 수 있기 때문에 리스트에 저장되어 있다.

먼저 is_valid()를 호출하지 않아도 errors에 접근할 수 있다. form의 데이터는 is_valid()를 호출하거나, errors에 접근할때나 검증될 것이다.

검증 루틴은 오류 또는 호출 횟수에 관계없이 한 번만 호출된다. 즉, 유효성검사에 부작용이 있을 경우 해당 부작용은 한 번만 트리거된다.

### Behavior of unbound forms

데이터가 없는 양식의 유효성을 확인하는 것은 무의미하지만, 참고로, 바인딩되지 않은 양식은 다음과 같다.:

```
>>> f = ContactForm()
>>> f.is_valid()
False
>>> f.errors
{}
```
## Dynamic initial values

**Form.initial**

런타임에 form fields의 초기값을 선언하기 위해서는 initial을 사용해라. 예를들어, username 필드를 현재 세션의 사용자 이름으로 채우고 싶을 경우.

이 작업을 수행하려면 form에 대한 initial 인수를 사용한다. 이 인수가 지정된 경우 초기 값에 대한 딕셔너리 매핑되는 필드 이름이어야 한다. 초기 값을 지정할 필드만 포함한다. form에 모든 필드를 포함할 필요는 없다. 예를 들어 다음과 같다:

```
>>> f = ContactForm(initial={'subject':''Hi There!'})
```

이런 값은 바운딩 되지 않은 form에만 표시되고, 특정 값이 제공되지 않은 경우 대체 값으로 사용되지 않는다.


필드에서 initial를 정의하고 form을 인스턴스화 할 때 initial를 포함하면 후자의 initial이 우선된다. 아래 예에서, initial은 field 레벨과 form 인스턴스 레벨에서 둘다 제공되었지만, 후자가 우선되었다. 

```
>>> class CommentForm(forms.Form):
    name = forms.CharField(initial='class')
    url = forms.URLField()
    comment = forms.CharField()
>>> f = CommentForm(initial={'name':'instance'}, auto_id=False)
>>> print f
<tr><th>Name:</th><td><input type="text" name="name" value="instance" /></td></tr>
<tr><th>Url:</th><td><input type="text" name="url" /></td></tr>
<tr><th>Comment:</th><td><input type="text" name="comment" /></td></tr>
```

## Accessing "clean" data ##

**Form.cleaned_data**

Form 클래스의 각 필드는 데이터의 유효성을 검사 할뿐만 아니라 데이터를 "정리"하여 일관된 형식으로 정규화한다. 이는 특정 필드에 대한 데이터를 다양한 방식으로 입력 할 수 있어서 항상 일관된 출력을 얻을 수 있기 때문에 좋다.

예를들어, DateField는 Python datetime.date 객체에 대한 입력을 정규화한다. '1994-07-15'형식의 문자열이나, datatiem.date 객체나, 다른 형식의 숫자를 전달하는 것과 관계 없이, DateField는 유효한 한 항상 datetime.date 객체로 정규화할 것이다. 

데이터 집합을 사용하여 form 인스턴스를 생성하고 유효성을 확인했으면 clean_data 속성을 통해 클린 데이터에 액세스할 수 있다.

```
>>> data = { 'subject': 'hello',
            'message': 'Hi there',
            'sender': 'foo@example.com',
            'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'cc_myself': True, 'message': u'Hi there', 'sender': u'foo@example.com', 'subject': u'hello'}
```
CharField나 EmailField와 같은 텍스트 기반의 field의 경우 항상 유니코드 문자열로 입력을 정리한다. 이 문서의 뒷부분에서 인코딩 함의를 다룬다.

만약 데이터가 유효하지 않을 경우, Form 인스턴스는 cleaned_data 속성을 가지지 않는다:

```
>>> data = { 'subject': '',
            'message': 'Hi there',
            'sender': 'invalid e-mail address',
            'cc_myself': True}
>>> f = ContactForm(data)
>>> f.is_valid()
False
>>> f.cleaned_data
Traceback (most recent call last):
...
AttributeError: 'ContactForm' object has no attribute 'cleaned_data'
Traceback (most recent call last):
...
AttributeError: 'ContactForm' object has no attribute 'cleaned_data'
```

Form을 정의할때 추가 데이터를 전달해도, cleaned_data는 항상 Form에 정의된 field에 해당하는 키만 포함한다. 아래 예에서, 여러 개의 추가 필드를 ContactForm 생성자에게 전달하지만 cleaned_data에는 form의 필드만 포함된다:

```
>>> data = {'subject': 'hello',
            'message': 'Hi there',
            'sender': 'foo@example.com',
            'cc_myself': True,
            'extra_field_1': 'foo',
            'extra_field_2': 'bar',
            'extra_field_3': 'baz'}
>>> f = ContactForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data # Doesn't contain extra_field_1, etc.
{'cc_myself': True, 'message': u'Hi there', 'sender': u'foo@example.com', 'subject': u'hello'}
```

cleaned_data는 데이터에 필요하지 않은 필드 값이 포함되지 않은 경우에도 Form의 모든 정의된 필드에 해당하는 key와 value를 포함한다. 아래 예에서, 데이터 딕셔너리는 nick_name 필드의 값을 포함하지 않지만, cleaned_data는 빈값으로 포함하고 있다:

```
>>> class OptionalPersonForm(Form):
        first_name = CharField()
        last_name = CharField()
        nick_name = CharField(required=False)
>>> data = {'first_name': u'John', 'last_name': u'Lennon'}
>>> f = OptionalPersonForm(data)
>>> f.is_valid()
True
>>> f.cleaned_data
{'nick_name': u'', 'first_name': u'John', 'last_name': u'Lennon'}
```

위 예에서, nickn_name은 CharField이고, CharField는 빈 값을 빈 문자열로 처리하기 때문에 cleaned_data의 nick_name 값은 빈 문자열로 설정되었다. 각 필드 타입은 'blank' 값이 무엇인지 알고 있다 -- 예를들어 DataField는 빈 문자열 대신에 None을 가진다. 모든 각 필드가 이런 경우에 어떻게 처리하는지는 아래의 "Built-in Field classes" 섹션에서 각 필드의 "Empty value" 참고 사항을 참조해라.

특정 form 필드 (이름을 기준으로) 또는 form 전체 (다양한 필드의 조합 고려)에 대한 유효성 검사를 수행하는 코드를 작성할 수 있다. 이에 대한 자세한 정보는 [Form 및 필드 유효성 검증](https://django.readthedocs.io/en/1.3.X/ref/forms/validation.html)에 있다.

## Outputting forms as HTML

Form 객체의 두번째 작업은 자신을 HTML로 렌더링 하는 것이다. 이것은 간단히 print 하면 된다:

```
>>> f = ContactForm()
>>> print f
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="text" name="sender" id="id_sender" /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```

만약 form이 바운딩된 데이터일 경우, HTML 출력은 데이터가 알맞게 포함될 것이다. 예를 들어, 필드가 ```<input type = "text">```로 표시되면 데이터는 value 속성에 있다. 필드가 ```<input type = "checkbox">```로 표시되면 해당하는 경우 해당 HTML에 checked = "checked"가 포함된다.

```
>>> data = { 'subject': 'hello',
            'message': 'Hi there',
            'sender': 'foo@example.com',
            'cc_myself': True}
>>> f = ContactForm(data)
>>> print f
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" value="hello" /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" value="Hi there" /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="text" name="sender" id="id_sender" value="foo@example.com" /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" checked="checked" /></td></tr>
```

기본 출력은 각 필드가 ```<tr>```을 가지는 두 개 컬럼의 HTML테이블이다. 아래를 명심해라:

* 유연성을 위해 출력에 ```<table>``` 및 ```</table>``` 태그는 포함되지 않으며 ```<form>``` 및 ```</form>``` 태그 또는 ```<input type = "submit">``` 태그도 포함되지 않는다. 이것은 your job  이다.
*  각 필드 타입은 기본 HTML 표식을 가진다. CharField 와 EmailField는 ```<input type='text'>```를 나타낸다. BooleanField는 ```<input type='checkbox'>```를 나타낸다.  
이것들은 단지 합리적인 기본값 일뿐이다. 위젯을 사용하여 주어진 필드에 사용할 HTML을 지정할 수 있다.
* 각 태그의 HTML name은 ContactForm 클래스의 속성 이름에서 직접 가져온다.
*각 필드의 'Subject:', 'Message:' 그리고 'Cc myself'와 같은 text 라벨은 field 이름을 space는 언더바로 변환하고, 첫번째 글자는 대문자로 생성한다. 
* 각 텍스트 레이블은 HTML <label> 태그로 둘러싸여 있으며, 해당 ID를 통해 해당 양식 필드를 가리킨다. ID는 필드 이름 앞에 'id_'를 붙여서 생성된다. 모범 사례를 따르기 위해 id 속성 및 <label> 태그가 기본적으로 출력에 포함되지만 해당 동작을 변경할 수 있다.
  
form을 print 할 때 <table> 출력이 기본 출력 스타일이지만 다른 출력 스타일도 사용할 수 있다. 각 스타일은 form 객체에서 메서드로 사용할 수 있으며 각 렌더링 method은 유니 코드 객체를 반환한다.

### as_p()

**Form.as_p()**

as_p() 는 form을 ```<p>```태그로 랜더링한다. 각```<p>```는 하나의 필드를 포함한다:

```
>>> f = ContactForm()
>>> f.as_p()
u'<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" /></p>\n<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></p>\n<p><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" /></p>\n<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>'
>>> print f.as_p()
<p><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" /></p>
<p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></p>
<p><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" /></p>
<p><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
```

### as_ul()

**Form.as_ul()**

as_ul()은 ```<li>``` 태그 시리즈로 form을 랜더링한다. 각 ```<li>```는 하나의 필드를 포함한다. ```<ul>``` 이나 ```</ul>```을 포함하지 않기 때문에 유연성을 위해 ```<ul>```에 HTML 속성을 지정할 수 있다. 

```
>>> f = ContactForm()
>>> f.as_ul()
u'<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" /></li>\n<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></li>\n<li><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" /></li>\n<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>'
>>> print f.as_ul()
<li><label for="id_subject">Subject:</label> <input id="id_subject" type="text" name="subject" maxlength="100" /></li>
<li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></li>
<li><label for="id_sender">Sender:</label> <input type="text" name="sender" id="id_sender" /></li>
<li><label for="id_cc_myself">Cc myself:</label> <input type="checkbox" name="cc_myself" id="id_cc_myself" /></li>
```

### as_table()

**Form.as_table()**

마지막으로, as_table()은 HTML ```<table>```로 form을 출력한다. 이것은 print와 같다. form 객체를 print할때 뒤에서 as_table() 메소드를 호출한다.:

```
>>> f = ContactForm()
>>> f.as_table()
u'<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" /></td></tr>\n<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" /></td></tr>\n<tr><th><label for="id_sender">Sender:</label></th><td><input type="text" name="sender" id="id_sender" /></td></tr>\n<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>'
>>> print f.as_table()
<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" /></td></tr>
<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" /></td></tr>
<tr><th><label for="id_sender">Sender:</label></th><td><input type="text" name="sender" id="id_sender" /></td></tr>
<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
```

### Styling required or erroneous form rows

필수 또는 오류가 있는 form 행과 필드의 스타일을 저정하는 것은 매우 일반적이다. 예를 들어 필요한 양식 행을 굵게 표시하고 빨간색으로 오류를 강조 표시해야 할 수 있다. 

Form 클래스는 필요한 행이나 에러가 있는 행을 위해 class 속성을 추가하여 사용할 수 있는 몇 개의 hooks을 가지고 있다.:
간단하게 Form.error_css_class나 Form.required_css_class 속성을 설정하면된다:

```
class ContactForm(Form):
    error_css_class = 'error'
    required_css_class = 'required'

    # ... and the rest of your fields here
```
이 작업을 수행하면 필요에 따라 행에 "error"및 / 또는 "required"클래스가 제공된다. HTML은 다음과 같다.

```
>>> f = ContactForm(data)
>>> print f.as_table()
<tr class="required"><th><label for="id_subject">Subject:</label>    ...
<tr class="required"><th><label for="id_message">Message:</label>    ...
<tr class="required error"><th><label for="id_sender">Sender:</label>      ...
<tr><th><label for="id_cc_myself">Cc myself:<label> ...
```

### Configuring HTML <label> tags 
