import cx_Oracle
username = 'cis550project'
password = 'Obstacle123'

host = 'cis550project.cc4zli6er8qm.us-west-2.rds.amazonaws.com'
port = '1521'
sid = 'ORCL'

dsn = cx_Oracle.makedsn(host, port, sid)
db = cx_Oracle.connect(username, password,dsn)
c = db.cursor()
c.execute('select * from Person')
val = c.execute('select * from Person')
val.fetchall()