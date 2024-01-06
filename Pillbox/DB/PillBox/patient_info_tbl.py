import pymysql

#DB연결
conn = pymysql.connect(host='localhost', port=3306, user='root', password='11223344', db='PillBox')
curs = conn.cursor(pymysql.cursors.DictCursor)


clear = 'drop table if exists patient_info'
curs.execute(clear)

#P_ID = 환자 ID
#P_NAME = 환자 이름
#P_BIRTHDATE = 환자 생년월일
mk_table = 'create table if not exists patient_info (P_ID VARCHAR(50) PRIMARY KEY, P_NAME text, P_BIRTHDATE text)'
curs.execute(mk_table)

insert1 = "INSERT INTO patient_info VALUES('1234' ,'엄태현', '000807')"
curs.execute(insert1)
insert2 = "INSERT INTO patient_info VALUES('1313', '신짱구', '111111')"
curs.execute(insert2)

conn.commit()

#종료
curs.close()
conn.close()
