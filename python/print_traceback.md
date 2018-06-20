
The exception handling block 
```
except Exception as ex:
    print(ex)
```
will only print the exception message and not its traceback.

That’s good to know, but we need more info than this to debug properly. 

Namely the line that raised the exception, together with its stack trace.

The traceback module, part of the stdlib, will help us with this:

```
import traceback

try:
    raise Exception(“nop”)
except Exception as ex:
    traceback.print_exc()
```

# Output:
Traceback (most recent call last):
  File “<stdin>”, line 2, in <module>
Exception: nop


#### format_exc([limit])
This is like print_exc(limit) but returns a string instead of printing to a file.

