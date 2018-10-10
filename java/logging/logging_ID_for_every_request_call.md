
## Logging ID for every request call

API에서 기록하고 있는 로그를 각 request별로 구별하기 위해 request마다 ID 추가가 필요하였다.

처음에는 Log4j의 wrapper 함수를 생성하여 생성자에서 ID를 넘겨 받고 그 ID를 이용해서 log를 기록하도록 수정하였다.
하지만 ID를 상위 클래스로 계속 넘겨줘야 했고(super(id)), 다음 개발자가 래퍼 함수를 사용한다는 보장이 없었다. 무엇보다 기존에 Log4j를 사용하고 있는 모든 소스를 래퍼 함수로 변경하는 작업이 있었다.

그래서 request별로 ID를 저장할 새로 를 생성하였다. 
해당 필터 통과시 ID를 만들어 MDC에 저장하고, Log4j.properties에는 해당 키로 pattern을 추가하여 %X{ID} 로그 기록 시 항상 ID도 같이 남기도록 수정하였다.

## What is Log4j MDC (Mapped Diagnostic Context)

To put it simple, the MDC is a map which stores the context data of the particular thread where the context is running. To explain it, come back to our simple application - every client request will be served by different thread of the MyServlet. So, if you use log4j for logging, then each thread can have it’s own MDC which is  global to the entire thread. Any code which is part of that thread can easily access the values that are present in thread’s MDC.

So, how do we make MDC to differentiate logging statements from multiple clients? Simple : Before starting any business process in your code, get the user name (for our Servlet, we can get it from request object) and put that into MDC. Now the user name will be available to the further processing. In your log4j.properties while defining the conversionPattern, add a pattern %X{key} to retrievce the values that are present in the MDC. The key will be userName in our example. It’s like getting a value from a Session object.

## NDC vs MDC

NDC(Nested Diagonostic Context)는 stack이고 
MDC(Mapped Diagnostic Context)는 맵이다.
두가지 모두  context는 스레드 마다 포함된다. 
the context is stored per thred. Each thread could use the same key but have different stored values

NDC의 경우 '%x'를 이용해 로그를 기록하고,
MDC의 경우 '%X{key}'를 이용해 로그를 기록한다.

https://wiki.apache.org/logging-log4j/NDCvsMDC

## Filter

필터를 이용한 웹 프로그래밍 Part1, 필터란 무엇인가!
[http://javacan.tistory.com/entry/58]

Understanding and Using Servlet Filters
[http://otndnld.oracle.co.jp/document/products/as10g/101300/B25221_03/web.1013/b14426/filters.htm]

## Example code

A Filter to put the user name in MDC for every request call

- AuthenticationFilter.java
```
package com.veerasundar.code.log4jmdc;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

import org.apache.log4j.MDC;

/**
 * An example authentication filter which is used to intercept all the requests
 * for fetching the user name from it and put the user name to the Log4j Mapped
 * Diagnostic Context (MDC), so that the user name could be used for
 * differentiating log messages.
 *
 * @author veerasundar.com/blog
 *
 */
public class AuthenticationFilter implements Filter {

	@Override
	public void doFilter(ServletRequest request, ServletResponse response,
			FilterChain chain) throws IOException, ServletException {

		try {
			/*
			 * This code puts the value "userName" to the Mapped Diagnostic
			 * context. Since MDc is a static class, we can directly access it
			 * with out creating a new object from it. Here, instead of hard
			 * coding the user name, the value can be retrieved from a HTTP
			 * Request object.
			 */
			MDC.put("userName", "veera");

			chain.doFilter(request, response);

		} finally {
			MDC.remove("userName");
		}

	}

}
```

- Web.xml

```
<?xml version="1.0" encoding="UTF-8"?>
<web-app id="WebApp_ID" version="2.4"   xmlns="http://java.sun.com/xml/ns/j2ee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"   xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">
    <servlet>
        <description/>
        <display-name>Log4jMdcDemo</display-name>
        <servlet-name>Log4jMdcDemo</servlet-name>
        <servlet-class>com.veerasundar.code.log4jmdc.Log4jMdcDemo</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>Log4jMdcDemo</servlet-name>
        <url-pattern>/Log4jMdcDemo</url-pattern>
    </servlet-mapping>
    <filter>
        <filter-name>AuthFilter</filter-name>
        <filter-class>com.veerasundar.code.log4jmdc.AuthenticationFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>AuthFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
</web-app>
```

- log file

```
0    [http-8084-2]  INFO Log4jMDCDemo  - This is  demo for the Log4j MDC concept - veera
0    [http-8084-2]  INFO Log4jMDCDemo  - From Veerasundar.com/blog - veera
0    [http-8084-2] DEBUG Log4jMDCDemo  - Just some sample messages - veera
```


ref

https://veerasundar.com/blog/2009/10/log4j-mdc-mapped-diagnostic-context-what-and-why/
