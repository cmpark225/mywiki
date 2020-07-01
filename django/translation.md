Django는 GNU gettext format을 사용한다.

# 관련 용어

국제화(i18n, internationalization): 개발자가 지역화 지원을 위해 소프트웨어적으로 준비하는 것

지역화(l8n, localization): 번역가가 번역하고 지역 형식에 맞게 변환하는 것


# 관련 파일
다국어 지원 관련 파일은
po, mo 파일이 있다.

PO 파일은 사람이 직접 읽고 편집할 수 있도록 만들어져 있고, 어떤 문자와 맞춰질 것인지 정의 할 수 있다.

po file 포맷

```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2020-06-30 04:11-0500\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

msgid ""
msgstr ""
                        
```


mo 파일은 프로그램에서 읽어들이는 파일이고 바이너리 파일이다.



# How to use gettext in Django

## In views.py

```
from django.http import HttpResponse
from django.utils.translation import ugettext as _


def home(request):
    output = _("Hello")
    return HttpResponse(output)

```

ugettext 함수를 사용하면 language code에 맞는 언어가 출력된다.

### comment
comment 추가 할 경우 po 파일에 해당 comment가 추가된다.

views.py
```
    # Translators: This message appears on the home page only
    output += _("Welcome to my site")

```
django.po
```
#. Translators: This message appears on the home page only
#: myapp/views.py:10
msgid "Welcome to my site"
msgstr ""
```

### Change the Language code
```
from django.utils import translation

def home(reqest):
    translation.activate('ko-kr')
    request.LANGUAGE_CODE = translation.get_language()

```

출력 언어는 request.LANGUAGE_CODE를 기준으로 하기 때문에
request.LANGUAGE_CODE를 변경 해준다. 

request.LANGUAGE_CODE는 
HTTP 헤더 값 accept-language 을 가져온다.


## Make the po file
```
$ mkdir locale 
$ python manage.py makemessage -l ko
$ tree locale
locale
└── ko
    └── LC_MESSAGES
        └── django.po

```

makemessage를 사용하여 po 파일을 만들 경우 
py에서 ugettext를 사용한 Text로 msgid가 po파일에 생성 된다.

ex) 위에서 사용한 _("Hello")의 Hello가 msgid가 된다
```
#: myapp/views.py:26
msgid "Hello"
msgstr ""

```

msgstr을 추가한 후 다시 makemessage 명령어를 실행해도 기존 msg는 그대로 남아 있다.


## make the mo file
```
$ python manage.py compilemessages
processing file django.po in /home/user/data/workspace/myproj/locale/ko/LC_MESSAGES

$ tree locale
locale
└── ko
    └── LC_MESSAGES
        ├── django.mo
        └── django.po

```

