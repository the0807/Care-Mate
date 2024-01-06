import pymysql

#DB연결
conn = pymysql.connect(host='localhost', port=3306, user='root', password='11223344', db='PillBox')
curs = conn.cursor(pymysql.cursors.DictCursor)


clear = 'drop table if exists patient_pillbox'
curs.execute(clear)

#P_ID = 환자 ID
#B_ID = 약통 ID
mk_table = "create table if not exists patient_pillbox (B_ID VARCHAR(50), P_ID VARCHAR(50), FOREIGN KEY (B_ID) REFERENCES pillbox_no (B_ID), FOREIGN KEY (P_ID) REFERENCES patient_info (P_ID))"
curs.execute(mk_table)

insert1 = "INSERT INTO patient_pillbox VALUES('PB_1', '1234')"
curs.execute(insert1)
insert2 = "INSERT INTO patient_pillbox VALUES('PB_2', '1313')"
curs.execute(insert2)

conn.commit()

#종료
curs.close()
conn.close()
