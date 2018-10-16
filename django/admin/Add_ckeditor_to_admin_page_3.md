# Custom Font 추가하기

기본적으로 ckEditor에서 제공하는 Font의 종류도 적고, 한글 폰트도 없어서

구글에서 제공해주는 웹 폰트를 추가하기로 했다.

검색해보니 [Google Web Fonts plugin][https://ckeditor.com/cke4/addon/ckeditor-gwf-plugin]이 있어서,

플러그인을 사용할 예정이다.

## 1. 플러그인 다운로드 후 압축 풀기

ckeditor의 plugin 폴더에 다운로드 받은 플러그인 압축을 푼다.

```
/static/ckeditor/plugins/ckeditor-gwf-plugin$ tree
.
├── LICENSE
├── plugin.js
├── README.md
└── style.css

0 directories, 4 files
```

위와 같이 4개의 파일이 포함되어 있다.

## config.js 파일에 사용할 플러그인 추가

ckeditor/config.js
```
CKEDITOR.editorConfig = function( config ) {
    ...

    config.extraPlugins = 'ckeditor-gwf-plugin';
    ...
}
```

## 폰트 드롭박스에 폰트 추가

사용할 구글 webFont를 선택하기 위한 아이템을 Font 드롭박스에 추가해준다.

ckeditor/config.js
```
CKEDITOR.editorConfig = function( config ) {
    ...

    config.extraPlugins = 'ckeditor-gwf-plugin';
    ...

    config.font_names = "GoogleWebFonts;";
}
```

ckeditor에 Font 드롭박스를 클릭하면 GoogleWebFonts가 추가된 것을 확인 할 수 있다.

그리고 GoogleWebFonts를 클릭 시 또 다른 작은 팝업 창이 뜨며

해당 팝업창의 드랍박스를 통해 구글 웹 폰트를 선택 할 수 있게 된다.



