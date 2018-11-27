# remySQL
Remote MySQL tool. Requires pymysql. Python3.4+

You might ask: hy is this needed? MySQL allows one to connect remotely.
Yes, but not in all cases...

(make sure you have installed pymysql and python-osc via pip)

1> Install remySQLSrv.py and DBClassMySQL.py on the machine where MySQL resides

2> Modify DBClassMySQL.py (db name, login and password) and enter the IP address of the client machine, then run remySQLSrv.py

3> on the client machine install remySQLClient.py, enter the IP address of the MySQL server and run it

4> Enter a SQL command in the format 'SQL@select * from table'

As an alternative, you can import remySQLClient in your program and call its methods...
