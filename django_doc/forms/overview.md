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
HTML form 위젯에 해당하는 클래스. ex) <input type="text"> 나 <textarea>. 위젯을 HTML로 렌더링한다. 

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

1. form이 제출되지 않은 경우 ContactForm의 unbound 인스턴스가 만들어져서 템플릿에 전달된다.
2. form이 제출된 경우 request.POST를 사용하여 form의 bound 인스턴스가 작성된다. 제출된 데이터가 유효하면 처리되고 사용자는 'thanks' 페이지로 리디렉션된다.
3. form이 제출되었지만 유효하지 않은 경우, bound된 양식 인스턴스가 템플릿에 전달된다.
   

   

