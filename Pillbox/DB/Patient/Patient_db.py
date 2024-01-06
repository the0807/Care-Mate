import pymysql

#DB연결
conn = pymysql.connect(host='localhost', port=3306, user='root', password='11223344')
curs = conn.cursor(pymysql.cursors.DictCursor)


clear = 'drop database if exists Patient'
curs.execute(clear)

mk_db = "create database if not exists Patient"
curs.execute(mk_db)

conn.commit()

#종료
curs.close()
conn.close()
