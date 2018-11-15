# File Uploads

Django에서 파일 업로드를 다룰 때, 파일 데이터는 request.FILES에 배치된다. ( request 객체에 대한 추가 정보는 [request and response objects](https://django.readthedocs.io/en/1.3.X/ref/request-response.html)참조 ) 이 문서는 파일이 디스크와 메모리에 저장되는 방법과 기본 동작을 custom 하는 방법에 대해 설명한다.

## Basic file uploads

 FileField를 포함하는 간단한 form을 고려해라:
 ```
 from django import forms

 class UploadFileForm(forms.Form):
     title = forms.CharField(max_length=0)
     file = forms.FileField()
 ```

이 form을 처리하는 뷰는 request.FILES에 파일 데이터를 받는다, FILES는 form의 각 FileField(또는 ImageField 또는 다른 FileField의 서브 클래스)에 대한 키를 포함하는 dictionary 이다. 따라서 위 form의 데이터는 request.FILES['file']로 접근 할 수 있다.

request.FILES는 메소드가 POST 이고 속성으로 enctype="multipart/form-data"를 가지는 <form> 요청 데이터만 포함한다. 아닐경우 request.FILES는 비어있다.

대부분의 경우, 업로드 된 파일을 [Binding uploaded fiels to a form](https://django.readthedocs.io/en/1.3.X/ref/forms/api.html#binding-uploaded-files)에서 설명한대로 request의 파일 데이터를 form으로 전달하기만 하면 된다. 이것은 아래와 같다.:

```
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file

def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form':form})
```

form의 생성자에 request.FILES를 전달해야 하는 것을 명심해라; 이것은 파일 데이터가 form에 바인딩 되는 방법이다.

### Handling uploaded files

**class UploadedFile**

퍼즐의 마지막 조각은 실제 파일 데이터를 request.FILES로 부터 다루는 것이다. 이 dictionary 의 각 항목은 UploadedFile 객체다. -- 업로드된 파일을 둘러싼 간단한 wrapper. 일반적으로 업로드 된 콘텐츠에 액세스 하려면 다음 방법 중 하나를 사용한다:

**read()**

파일에서 업로드 된 전체 데이터를 읽는다. 이 메소드 사용시 주의: 업로드 된 파일이 거대한 경우 메모리로 읽으려고 하면 시스템을 압도할 수 있다. 대신에 chunks()를 사용하는 것이 좋다. 아래 확인

**multiple_chunks()**

업로드 된 파일이 여러 청크로 읽어야 할 만큼 큰 경우 True를 반환한다. 기본적으로 이 값은 2.5MB보다 큰 파일이지만 이것은 구성 가능하다. 아래 확인.


**chunks()**

파일 청크를 반환하는 제너레이터. multiple_chunks()가 True이면 이 메소드를 read() 대신 루프를 이용해 사용해야 한다. 

실제로는 항상 chunks()를 사용하는 것이 좋다.; 아래 예제 참조.

**name**

업로드 된 파일의 이름. ex) my_file.txt 

**size**

업로드 된 파일의 크기. bytes

여기에 UploadedFile에서 이용 가능한 몇 가지 다른 메소드와 속성이 있다.; 자세한 내용은 아래 UploadedFile objects를 참조해라. 

업로드 파일을 모두 처리하는 일반적인 방법은 아래와 같다:
```
def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
```

read()를 사용하는 대신 UplodedFile.chunks()를 반복하면 큰 파일이 시스템의 메모리를 압도하지 않도록 할 수 있다.

### Where uploaded data is stored
업로드된 파일을 저장하기 전에, 데이터를 어딘가 저장해야 한다. 

기본적으로 업로드 된 파일이 2.5MB보다 작은 경우 Django는 업로드 전체 내용을 메모리에 유지한다. 즉, 파일을 저장하면 메모리에서 읽기와 디스크에 쓰기만 되므로 매우 빠르다.

그러나 업로드 된 파일이 너무 크면 Django는 업로드 한 파일을 시스템의 임시 디렉토리에 저장된 임시 파일을 쓴다. Unix와 같은 플랫폼에서는 Django가 /tmp/tmpzfp6T6.upload와 같은 파일을 생성한다는 것을 기대할 수 있다. 만약 업로드가 충분히 크다면 Django가 데이터를 디스크로 스트리밍 할 때 이 파일의 크기가 커지는 것을 볼 수 있다. 

이런 특성들 (2.5MB, /tmp 등등)은 "reasonable defaults"이다. 업로드 동작을 맞춤 설정하거나 완전히 바꿀 수 있는 방법에 대한 자세한 내용을 읽어라.

### Changing upload handler behavior

세가지 설정이 Django의 파일 업로드 행동을 설정한다:

**FILE_UPLOAD_MAX_MEMORY_SIZE**

**FILE_UPLOAD_TEMP_DIR**

**FILE_UPLOAD_PREMISSIONS**

**FILE_UPLOAD_HANDLERS**

기본 값:
```("django.core.files.uploadhandler.MemoryFileUploadHandler",
 "django.core.files.uploadhandler.TemporaryFileUploadHandler",)

```
이것은 "메모리에 먼저 업로드 한 후 임시 파일로 fall back해라" 라는 의미다.

## UploadedFile objects
File에서 상속 받은 것 외에도 모든 UploadedFile 객체는 다음 메소드/속성을 정의한다. 

**UploadedFile.content_type**

파일과 함께 업로드된 content-type 헤더. (e.g. text/plain or application/pdf) 사용자가 제공한 모든 데이터와 마찬가지로 업로드 된 파일이 실제로 이 유형이라는 사실을 믿어서는 안된다. 파일에 콘텐츠 형식 헤더의 "trust but verify(신뢰 가능한 하지만 확인이 필요한)" 라는 내용이 포함되어 있는지 확인해야 한다. 

**UploadedFile.charset**

text/* content-type의 경우 브라우저에서 제공하는 문자 집합(i.e utf8). 여기에서도 "trust but verify"가 가장 좋은 정책이다.  

**UploadedFile.temporary_file_path**

디스크에 업로드 된 파일만 이 method를 가진다.; 임시 업로드 파일의 전체 경로를 반환한다.

## Upload Handlers
사용자가 파일을 업로드하면 Django는 업로드된 파일 데이터를 처리하는 작은 클래스인 업로드 핸들러로 파일 데이터를 전달한다. 업로드 처리기는 기본적으로 FILE_UPLOAD_HANDLERS 설정에서 정의되며, 기본값은 아래와 같다:
```
("django.core.files.uploadhandler.MemoryFileUploadHandler", 
"django.core.files.uploadhandler.TemporaryFileUploadHandler", )
```
MemoryFileUploadHandler와 TemporaryFileUploadHandler는 작은 파일을 메모리로 읽어 들이고 큰 파일을 디스크로 읽어들이는 Django의 기본 파일 업로드 동작을 제공한다.

Django가 파일을 처리하는 방법을 커스텀하는 핸들러를 작성 할 수 있다. 예를 들어, 사용자 정의 할당량을 정의하고, 즉시 데이터를 압축하고, 진행률 막대를 렌더링하고, 데이터를 로컬에 저장하지 않고 직접 다른 저장 위치에 보낼 수 있는 사용자 정의 처리기를 사용 할 수 있다.

### Modifying upload handlers on the fly
가끔 특정 view는 다른 업로드 동작을 필요로한다. 이런 경우에,   request.upoad_handlers를 수정하여 request 마다 upload 핸들러를 override 할 수 있다. 기본적으로 이 목록은 FILE_UPLOAD_HANDLERS로 주어진 upload 핸들러를 포함하지만, 다른 list처럼 이 목록을 수정할 수 있다.  

예를 들어, 일종의 AJAX 위젯에 업로드 진행에 대한 피드백을 제공하는 ProgressBarUploadHandler를 작성했다고 가정한다. 이 핸들러를 다음과 같이 업로드 핸들러에 추가한다:
```
request.upload_handlers.insert(0, ProgressBarUploadHandler())
```
progress bar 핸들러가 다른 핸들러보다 먼저 실행되어야하기 때문에 append() 대신 list.insert() 우선 사용을 원할 것이다. 업로드 핸들러ㄹ는 순서대로 처리되는 것을 기억해라.

업로드 핸들러를 완전히 바꾸려면 새 목록을 할당하면 된다.

```
request.upload_handlers = [ProgressBarUploadHandler()]
```
