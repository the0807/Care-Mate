# import the necessary packages
# 필요한 패키지 임포트
from pyzbar import pyzbar
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help = "path to inpuit image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

# find the barcodes in the image and decode each of the barcodes
# 이미지에서 바코드 찾기
barcodes = pyzbar.decode(image)

# loop over the detected barcodes
for barcode in barcodes:

	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
    # 이미지에서 바코드의 경계 상자부분을 그리고, 바코드의 경계 상자부분(?)을 추출한다. 
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
    # 바코드 데이터는 바이트 객체이므로, 어떤 출력 이미지에 그리려면 가장 먼저 문자열로 변환해야 한다.
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
 
	# draw the barcode data and barcode type on the image
    # 이미지에서 바코드 데이터와 테입(유형)을 그린다
	#text = "{} ({})".format(barcodeData, barcodeType)
	#cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
 
	# print the barcode type and data to the terminal
    # 터미널을 통해 바코드 유형과 데이터를 출력
	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
 
# show the output image
# 이미지 출력을 보여준다.
cv2.imshow("Image", image)
cv2.waitKey(0)