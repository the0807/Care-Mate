from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2
import pymysql
import os
import serial

#DB연결
conn1 = pymysql.connect(host='localhost', port=3306, user='root', password='11223344', db='Patient')
curs1 = conn1.cursor(pymysql.cursors.DictCursor)

conn2 = pymysql.connect(host='localhost', port=3306, user='root', password='11223344', db='PillBox')
curs2 = conn2.cursor(pymysql.cursors.DictCursor)

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

print("[INFO] starting video stream...")

# USB 웹캠 카메라 사용시
vs = VideoStream(src=0).start()

# 파이 카메라 사용시
# vs = VideoStream(usePiCamera=True).start()

port = '/dev/ttyUSB0'
baudrate = 9600

arduino = serial.Serial(port, baudrate)
time.sleep(0.5)
print("\n")

# 지금까지 찾은 바코드 세트 초기화
found = set()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

	# 프레임에서 바코드를 찾고, 각 바코드들 마다 디코드
    barcodes = pyzbar.decode(frame)

    try:
        for barcode in barcodes:
			# 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다. 
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	
			# 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # 현재 바코드 텍스트가 CSV 파일안에 없을경우, barcode를 작성하고 업데이트
            if barcodeData not in found:
				# 터미널을 통해 바코드 유형과 데이터를 출력
                print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

                name = barcodeData.split()[0]
                birthdate = barcodeData.split()[1]
                #print("이름: " + name)
                #print("생년월일: " + birthdate)

                sql1 = f"select * from patient_info where P_NAME='{name}' and P_BIRTHDATE='{birthdate}'"
                result1 = curs1.execute(sql1)
                conn1.commit()

                if result1 == 1:
                    print("환자가 맞습니다!")
                    
                    sql2 = f"select * from patient_info where P_NAME='{name}' and P_BIRTHDATE='{birthdate}'"
                    a = curs2.execute(sql2)
                    conn2.commit()
                    
                    if a == 1:
                        result2 = curs2.fetchall()
                        for record in result2:
                            p_id = record['P_ID']
                        
                        sql3 = f"select * from patient_pillbox where P_ID='{p_id}'"
                        aa = curs2.execute(sql3)
                        conn2.commit()
                        
                        if aa == 1:
                            result3 = curs2.fetchall()
                            for record in result3:
                                b_id = record['B_ID']
                        
                            sql4 = f"select * from pillbox_no where B_ID='{b_id}'"
                            curs2.execute(sql4)
                            conn2.commit()
                            result4 = curs2.fetchall()
                            for record in result4:
                                b_name = record['B_NAME']
                                print("지정된 약통: " + b_name)
                                if b_name == "약통1":
                                    value = 1
                                    arduino.write(str(value).encode())
                                    print('값 전송 완료:', value)
                                    os.system('espeak -s 170 -p 40 -v ko "약통,1이, 열렸습니다."')
                                elif b_name == "약통2":
                                    value = 2
                                    arduino.write(str(value).encode())
                                    print('값 전송 완료:', value)
                                    os.system('espeak -s 170 -p 40 -v ko "약통,2가, 열렸습니다."')
                            #arduino.write(str(value).encode())
                            #print('값 전송 완료:', value)
                        
                        elif aa == 0:
                            print("복용할 약이 없습니다!")
                            os.system('espeak -s 170 -p 40 -v ko "복용할, 약이, 없습니다."')

                    elif a == 0:
                        print("복용할 약이 없습니다!")
                        os.system('espeak -s 170 -p 40 -v ko "복용할, 약이, 없습니다."')
                        
                elif result1 == 0:
                    print("환자가 아닙니다!")
                    os.system('espeak -s 170 -p 40 -v ko "환자,가, 아닙니다."')
	
                found.add(barcodeData)
                print("-----------------------------------------")
	
		# show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        # q를 누르면 loop를 break함
        if key == ord("q"):
            break

    except KeyboardInterrupt:
        break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
curs1.close()
conn1.close()
curs2.close()
conn2.close()
arduino.close()
cv2.destroyAllWindows()
vs.stop()