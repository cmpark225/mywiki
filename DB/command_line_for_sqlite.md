```
$sqlite3
sqlite > .open mydatabase

sqlite > .tables // show tables
auth_user
auth_group

sqlite > select * from auth_user;
1|admin|||test@test.com|sha1$c717b$faea855493006307477311f9a3ff3efc102d167c|1|1|1|2020-09-22 21:19:00.728980|2020-09-22 01:29:25

sqlite > .headers on // Add column Header

sqlite > select * from auth_user;
id|username|first_name|last_name|email|password|is_staff|is_active|is_superuser|last_login|date_joined
1|admin|||test@test.com|sha1$c717b$faea855493006307477311f9a3ff3efc102d167c|1|1|1|2020-09-22 21:19:00.728980|2020-09-22 01:29:25

```
