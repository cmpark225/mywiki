## How can I see the raw SQL queries Django is running?

Make sure your Django DEBUG setting is set to True. Then, just do this:

```
>>> from django.db import connection
>>> connection.queries
[{'sql': 'SELECT polls_polls.id, polls_polls.question, polls_polls.pub_date FROM polls_polls',
'time': '0.002'}]
```

connection.queries is only available if DEBUG is True.
It's a list of dictionaries in order of query execution.
Each dictionary has the following:

```
sql -- The raw SQL statement
time -- How long the statement took to execute, in seconds.
```

connection.queries includes all SQL statements - INSERTs, UPDATES, SELECTs, etc.
Each time your app hits the database, the query will be recorded.

If you are using multiple databases, you can use the same interface on each member of the connections dictionary:

```
>>> from django.db import connections
>>> connections['my_db_alias'].queries
```

If you need to clear the query list manually at any point in your functions, 
just call reset_queries(), like this:

```
from django.db import reset_queries
reset_queries()
```
