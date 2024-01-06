import pymysql

#DB연결
conn = pymysql.connect(host='localhost', port=3306, user='root', password='11223344', db='PillBox')
curs = conn.cursor(pymysql.cursors.DictCursor)


clear = 'drop table if exists pillbox_no'
curs.execute(clear)

#B_ID = 약통 ID
#B_NAME = 약통 이름
mk_table = 'create table if not exists pillbox_no (B_ID VARCHAR(50) PRIMARY KEY, B_NAME text)'
curs.execute(mk_table)

insert1 = "INSERT INTO pillbox_no VALUES('PB_1', '약통1')"
curs.execute(insert1)
insert2 = "INSERT INTO pillbox_no VALUES('PB_2', '약통2')"
curs.execute(insert2)

conn.commit()

#종료
curs.close()
conn.close()
