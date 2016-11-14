import cx_Oracle
username = 'cis550project'

cis550project.cksgc6f8zhlj.us-east-1.rds.amazonaws.com:1521
#host = 'cis550project.cc4zli6er8qm.us-west-2.rds.amazonaws.com'
host = 'cis550project.cksgc6f8zhlj.us-east-1.rds.amazonaws.com'
port = '1521'
sid = 'ORCL'

dsn = cx_Oracle.makedsn(host, port, sid)
db = cx_Oracle.connect(username, password,dsn)
c = db.cursor()
#c.execute('select * from Person')
val = c.execute('select * from Person')
val.fetchall()

sqlplus 'cis550project@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=cis550project.cksgc6f8zhlj.us-east-1.rds.amazonaws.com)(PORT=1521))(CONNECT_DATA=(SID=ORCL)))'