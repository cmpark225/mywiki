카카오톡에서 링크를 공유할 경우 밑에 미리보기 이미지와 내용 일부가 같이 표시된다. 

해당 이미지를 변경하기 위해서는 html 헤더에 og 태그를 추가해야하는데, 

페이스북에서 사용하는 방식이라고 한다.

The Open Graph protocol 참고

http://ogp.me/


[카카오톡에서 작성한 글](https://devtalk.kakao.com/t/topic/927?u=tom)을 보면 

```
<head>
    <title>Kakao Developers</title>
    <meta property="og:url" content="https://devtalk.kakao.com/">
    <meta property="og:title" content="Kakao DevTalk_">  
    <meta property="og:type" content="website">
    <meta property="og:image" content="https://devtalk.kakao.com/images/devtalk_.png">
    <meta property="og:description" content="카카오 데브톡. 카카오 플랫폼 서비스 관련 질문 및 답변을 올리는 개발자 커뮤니티 사이트입니다.">
    <meta name="description" content="카카오 데브톡. 카카오 플랫폼 서비스 관련 질문 및 답변을 올리는 개발자 커뮤니티 사이트입니다.">
    <meta name="keywords" content="데브톡,devtalk,카카오,디벨로퍼스,개발자,API,플랫폼">
    ... 
</head>
```

위와 같이 html 헤더에 작성한 예를 보여주는데,

기본적으로 

og:url, og:title, og:type, og:image, og:description을 사용하면 원하는 링크 미리보기를 만들 수 있다. 


meta 태그를 사용하면 페이스북이나, 카카오에서 크롤러로 미리 보기를 생성하나 보다.


해당 태그를 적용하고 캐시되는지 바로 적용이 안될 수도 있다.

처음에는 적용이 안된줄 알고 계속 새로고침 해봄 ㅠㅠ 일정 시간 후 적용된 것을 확인했다.





