## Configuring Apache to permit CGI

In order to get your CGI programs to work properly, you'll need to have Apache configured to permit CGI execution.

There are several ways to do this.



### ScriptAlias

The ScriptAlias directive tells Apache that a particular directory is set aside for CGI programs.

Apache will assume that every file in this directory is a CGI program, and will attempt to execute it, when that particular resource is requested by a client.

The ScriptAlias directive looks like:

```

ScriptAlias /cgi-bin/ /usr/local/apache2/cgi-bin/

```

The example shown is from your defult httpd.conf configuration file, if you installed Apache in the default location. The ScriptAlias directive is much like the Alias directive, which defines a URL prefix that is to mapped to a particular directory. Alias and ScriptAlias are usually used for directories that are outside of the DocumentRoot directory. The difference between Alias and ScriptAlias is that ScriptAlias has the added meaning that everything under that URL prefix will be considered a CGI program. So, the example above tells Apache that any request for a resource beginning with /cgi-bin/ should be served form the directory /usr/loca/apache2/cgi-bin/. and should be treated as a CGI program.

For example, if the URL http://www.example.com/cgi-bin/test.pl is requested, Apache will attempt to execute the file /usr/local/apache2/cgi-bin/test.pl and return the output. Of course, the file will have to exist, and be executable, and return output in a particular way, or Apache will return an error message.



## Writing a CGI program

There are two main differences between "regular" programming, and CGI programming.

First, all output from your CGI program must be preceded by a MIME-type header. This is HTTP header that tells the client what sort of content it is receiving. MOST of the time, this will look like:

```

Content-type: text/html

```

Secondly, your output needs to be in HTML, or some other format that a browser will be able to display, Most of the time, this will be HTML, but occasionally you might write a CGI program that outputs a gif image, or other non-HTML content.

Apart from those two things, writing a CGI program will look a lot like any other program that you might write.



### Your First CGI program

The following is an example CGI program that prints one line to your browser. Type in the following, save it to a file called first.pl, and put it in your cgi-bin directory.

```

#!/usr/bin/perl

print "Content-type: text/html\n\n";

print "Hello, World.";

```

Even if you are not familiar with Perl, you should be able to see what is happening here. The first line tells Apache (or whatever shell you happen to be running under) that this program can be executed by feeding the file to the interpreter found at the location /usr/bin/perl. The second line prints the content-type declaration we talked about, followed by two carriage-return newline pairs. This puts a blank line after the header, to indicate the end of header HTTP headers, and the beginning of the body. The third line prints the string "Hello, World.". And that's the end of it.

If you open your favorite browser and tell it to get the address

```

http://www.example.com/cgi-bin/first.pl

```

or wherever you put your file, you will see the on line Hello, World. appear in your browser window. It's not very exciting, but once you get that working, you'll have a good chance of getting just about anything working.


## But it's still not working

There are four basic things that you may see in your browser when you try to access your CGI program from the web:

### The output of your CGI program

    Great! That means everything worked fine. If the output is correct, but the browser is not processing it correctly, make sure you have the correct Content-Type set in your CGI program.
refer:

https://httpd.apache.org/docs/2.2/en/howto/cgi.html#configuring
