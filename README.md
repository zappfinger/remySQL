# remySQL
Remote MySQL tool. Requires pymysql. Python3.4+

You might ask:why is this needed? MySQL allows one to connect remotely.
Yes, but not in all cases...

(make sure you have install pymysql via pip)
1> Install remySQLSrv.py and DBClassMySQL.py on the machine where MySQL resides
2> Modify DBClassMySQL.py (database name, login and password) and enter the IP address of the client machine
3> on the client machine install remySQLClient.py, enter the IP address of the MySQL server and run it
4> Enter a SQL command in the format 'SQL@select * from table'
