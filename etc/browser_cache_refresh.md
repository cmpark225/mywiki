# javascript, css 강제 refresh 방안

javascript 및 css 파일은 기본적으로 Brower 에 cache 됩니다.
가끔씩 수정한 js, css 파일이 적용되지 않은 것은 바로 이 cache 때문이죠.
Browser 차원에서 cache 를 삭제하면 수정된 js,css 파일이 반영됩니다만, 이용자들에게 일일이 cache 를 삭제하라고 요청할 수는 없는 일이죠.
이런 경우, 강제로 새로 변경된 js, css 파일을 적용할려면<br>js,css 의 URL 뒤에 ?+ Timestamp 형태를 붙여주면 됩니다.
예컨대

- link rel=&quot;stylesheet&quot; href=&quot;/css/common.css<strong>?20140630151000</strong>&quot;
- script type=&quot;text/javascript&quot; src=&quot;/js/meta.js<strong>?20140630151000</strong>&quot;

이련 형태가 되겠죠,
원리는 **cache 가 QueryString 을 포함한 URL 을 기준으로 이루어지기 때문에** 다른 파일로 인식하게 되는 셈이죠.
