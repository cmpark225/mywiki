
HTTP 요청에 대해서 인증 처리가 되지 않은 경우, status code 401을 통해 클라이언트에 리소스 접근에 필요한 인증 정보를 통지하게 된다. 

- response

```
HTTP/1.1 401 UNAUTHORIZED
www-authenticate: Basic realm="api"
```

## Basic 인증

Basic 인증은 유저 이름과 패스워드로 인증. 유저 이름과 패스워드는 Authorization 헤더에 넣어 요청마다 전송한다. Authorization헤더의 내용은 "유저아이디:패스워드"로  구성하고 Base64 인코딩한 문자열이 된다. 해당 내용은 간단히 디코딩이 가능하기 때문에 네트워크 상에서 암호가 흘러다닌다고 생각할 수 있다. 보다 높은 정도의 보안강도를 위해서는 SSL과 TLS를 사용해 HTTPS 통신을 사용해야 한다.

- request

```
GET /api/employees/1234 HTTP/1.1
Authorization: Basic YmFkcmk6U2VjcmV0U2F1Y2U=
```
