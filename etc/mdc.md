
## What is Log4j MDC (Mapped Diagnostic Context)

To put it simple, the MDC is a map which stores the context data of the particular thread where the context is running. To explain it, come back to our simple application - every client request will be served by different thread of the MyServlet. So, if you use log4j for logging, then each thread can have it’s own MDC which is  global to the entire thread. Any code which is part of that thread can easily access the values that are present in thread’s MDC.

So, how do we make MDC to differentiate logging statements from multiple clients? Simple : Before starting any business process in your code, get the user name (for our Servlet, we can get it from request object) and put that into MDC. Now the user name will be available to the further processing. In your log4j.properties while defining the conversionPattern, add a pattern %X{key} to retrievce the values that are present in the MDC. The key will be userName in our example. It’s like getting a value from a Session object.

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
