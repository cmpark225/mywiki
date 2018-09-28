# Gson

java에서 json을 직렬화, 역직렬화 시 사용한다.


## UserSimple.java

Serialization, Deserializion 설명 시 아래 UserSimple 클래스를 사용한다.

```
public class UserSimple {
    String name;
    String email;
    int age;
    boolean isDeveloper;
}
```

UserSimple 클래스에 따로 settier, getter를 두지는 않는다. 

Gson은 필드 기반으로 동작하기 때문에 getter, setter를 사용하지 않는다고 한다.


## Serialization (object to json)

UserSimple 클래스를 아래 형식의 JSON으로 변환 시키려고 한다.

```
{
    "name" : "tester",
    "email" : "tester@gmail.com",
    "age": 13,
    "isDeveloper": true
}
```


먼저 UserSimple의 객체를 생성한다.

그리고  Gson을 이용해 String 형태로 객체를 JSON으로 변환한다.

main.java
```
// create user object
UserSimple user = new UserSimple(
    "tester",
    "tester@gmail.com",
    13,
    true
    );


// make json string with gson
Gson gson = new Gson();
String userJson = gson.toJson(user);

```

userJson을 확인하면 아래와 같은 결과를 얻을 수 있다.

(GSON이 알파벳 순으로 정렬함.)

```
{
  "age": 13,
  "email": "tester@gmail.com",
  "isDeveloper": true,
  "name": "tester"
}
```

String은 ""로 감싸져있고, integer value는 그냥 출력한다.

## Deserialize (json to object)

아래의 JSON형태의 String을 object로 변환할 것이다.

```
String userJson =  "{'age':13,'email':'tester@gmail.com','isDeveloper':true,'name':'tester'}"; 

```

Gson instance를 생성한 후, 

fromJson()을 이용해 String을 Object로 변환한다.
```
Gson gson = new Gson();

UserSimple user = gson.fromJson(userJson, UserSimple.class);
```

user에서 데이터를 확인할 수 있다.


## annotation

### @SerializedName

직렬화/역직렬할 json의 keyName이 object의 변수 이름과 다를때 

SerializedName annotation을 이용해서, 키 이름을 지정할 수 있다.

예를 들어, Json이 아래와 같을 경우 :
```
String userJson =  "{'myAge':13,'myEmail':'tester@gmail.com','isDeveloper':true,'myName':'tester'}"; 

```
기존 UserSimple 클래스의 멤버변수 이름과 다르기 때문에 fromJson()할 경우 object에 데이터가 정상적으로 입력되지 않는다.

이럴 경우, 각 변수에 SerializedName을 지정하면 된다.

```
public class UserSimple {
    @SerializedName("myName") String name;
    @SerializedName("myEmail") String email;
    @SerializedName("myAge") int age;
    boolean isDeveloper;
}
```

SerializedName을 지정할 경우 직렬화/역직렬화 결과.

#### Serialization (object to json)

UserSimple의 변수 이름은 그대로지만, 

object를 JSON으로 변환하면 SerializedName에 지정된 이름으로 key가 생성된다.

```
{
  "isDeveloper": true,
  "myAge": 13,
  "myEmail": "tester@gmail.com",
  "myName": "tester"
}
```
Gson 2.4버전 이후에는 alternate을 이용해 한 필드에 여러 값을 매핑 시킬 수 있다. (안써봄...)

#### Deserialize (json to object)
```
String userJson =  "{'myAge':13,'myEmail':'tester@gmail.com','isDeveloper':true,'myName':'tester'}"; 

UserSimple user = new Gson().fromJson(userJson, UserSimple.class);
```

user 각 변수에 데이터가 정상적으로 입력된 것 확인 가능하다.


# GsonBuilder

GsonBuilder를 이용하면, 원하는 속성으로 Gson을 만들어 사용할 수 있다. 

(Gson을 Custom하는 느낌??)

예를 들어, object로 변환하려는 Json의 키가 snake case 방식으로 되어 있고,

변환하려는 class의 멤버 변수가 camel 방식으로 되어 있을 경우, 

위의 SerializedName을 이용해서

 ```
 public class UserSimple {
    String name;
    String email;
    int age;
    @SerializedName("is_developer") boolean isDeveloper;
}
 ```
 위와 같이 지정해도 되지만, GsonBuilder를 이용해서
 
 class는 변동 없이 JSON <-> object 변환이 가능하다.

 
기존 UserSimple class 그대로 사용한다.

UserSimple.java
```
 public class UserSimple {
    String name;
    String email;
    int age;
    boolean isDeveloper;
}
```

## Serialize (object to json)

먼저 snake 방식으로 입력 받을 Gson을 instance를 GsonBuilder를 통해 생성한다.

```
Gson gson = new GsonBuilder().setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES).create();
```

이후 생성한 gson을 통해 json을 생성한다.
```
// create user object
UserSimple user = new UserSimple(
    "tester",
    "tester@gmail.com",
    13,
    true
    );


String result = gson.toJson(user);
```

result 결과 
```
{
  "age": 13,
  "email": "tester@gmail.com",
  "is_dveloper": true,
  "name": "tester"   
}
```

## Deserialize (json to object)
위와 동일한 방식으로 gson을 생성한 후 

userJson을 UserSimple object로 변환시킨다.
```
Gson gson = new GsonBuilder().setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES).create();

String userJson =  "{'age':13,'email':'tester@gmail.com','is_developer':true,'name':'tester'}"; 

// json to object 
UserSimple user = gson.fromJson(userJson, UserSimple.class);
```

