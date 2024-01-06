from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

print("[INFO] starting video stream...")

# USB 웹캠 카메라 사용시
vs = VideoStream(src=0).start()

# 파이 카메라 사용시
# vs = VideoStream(usePiCamera=True).start()

time.sleep(2.0)
 
# 작성을 위해 출력된 CSV 파일을 열고, 지금까지 찾은 바코드 세트 초기화
csv = open(args["output"], "w")
found = set()

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
 
    # 프레임에서 바코드를 찾고, 각 바코드들 마다 디코드
	barcodes = pyzbar.decode(frame)

	for barcode in barcodes:
        # 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다. 
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
        # 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
  
        # 현재 바코드 텍스트가 CSV 파일안에 없을경우, barcode를 작성하고 업데이트
		if barcodeData not in found:
			name = barcodeData.split()[0]
			birthdate = barcodeData.split()[1]
			
			#print("이름: " + name)
			#print("생년월일: " + birthdate)
   
			csv.write("{},{}\n".format(name, birthdate))
			csv.flush()
			found.add(barcodeData)
   
			# 터미널을 통해 바코드 유형과 데이터를 출력
			print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

    # show the output frame
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
    # q를 누르면 loop를 break함
	if key == ord("q"):
		break
 
# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()