from socket import *
import os
import sys
import model_firebase
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

for i in range(0, 30):
    # Use a service account
    #cred = credentials.Certificate('./mykey.json')
    #firebase_admin.initialize_app(cred)

    db = firestore.client()

    doc_ref = db.collection('socket').document('trigger')
    switch = doc_ref.get().to_dict()['switch']
    # print(switch)
    time.sleep(3)
    
    if switch == 1:
        clientSock = socket(AF_INET, SOCK_STREAM)
        clientSock.connect(('localhost', 8080))

        print('연결에 성공했습니다.')
        filename = 'image.jpg'
        clientSock.sendall(filename.encode('utf-8'))

        data = clientSock.recv(1024)
        data_transferred = 0

        if not data:
            print('파일 %s 가 서버에 존재하지 않음' %filename)
            sys.exit()

        nowdir = '/home/ubuntu/ros/photo'
        with open(nowdir + "//" + 'test5.jpg', 'wb') as f: #현재dir에 filename으로 파일을 받는다
            try:
                while data: #데이터가 있을 때까지
                    f.write(data) #1024바이트 쓴다
                    data_transferred += len(data)
                    data = clientSock.recv(1024) #1024바이트를 받아 온다
            except Exception as ex:
                print(ex)
        print('파일 %s 받기 완료. 전송량 %d' %(filename, data_transferred))

        time.sleep(2)

        doc_ref.update({
            'switch': 0
        })
        
        print(model_firebase.run_seg('/home/ubuntu/ros/photo/test5.jpg'))

