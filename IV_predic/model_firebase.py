
#...............................Imports..................................................................

import os
import sys
# sys.path.append('/home/ubuntu/Vessel_segmentation/')
import torch
import numpy as np
import FCN_NetModel as FCN # The net Class
import CategoryDictionary as CatDic
import cv2
import isEdge
import math
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./mykey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

OutDir='out/' # Folder of output

UseGPU=False # Use GPU or CPU  for prediction (GPU faster but demend nvidia GPU and CUDA installed else set UseGPU to False)
FreezeBatchNormStatistics=False # wether to freeze the batch statics on prediction  setting this true or false might change the prediction mostly False work better
OutEnding="" # Add This to file name
if not os.path.exists(OutDir): os.makedirs(OutDir) # Create folder for trained weight

#-----------------------------------------Location of the pretrain model-----------------------------------------------------------------------------------
# Trained_model_path = '/home/ubuntu/Vessel_segmentation/logs/weight.torch'
Trained_model_path = '/home/ubuntu/ros/weight.torch'
##################################Load net###########################################################################################
#---------------------Create and Initiate net and create optimizer------------------------------------------------------------------------------------
Net=FCN.Net(CatDic.CatNum) # Create net and load pretrained encoder path
if UseGPU==True:
    print("USING GPU")
    Net.load_state_dict(torch.load(Trained_model_path))
else:
    print("USING CPU")
    Net.load_state_dict(torch.load(Trained_model_path, map_location=torch.device('cpu')))
#--------------------------------------------------------------------------------------------------------------------------
# Net.half()
#..................Read and resize image...............................................................................
    
def run_seg(img_path):
    try:
        print(img_path + " :  running - start")
        img_name = img_path[-9:-4]
        InPath = img_path
        Im=cv2.imread(InPath)
        h,w,d=Im.shape
        r=np.max([h,w])
        if r>840: # Image larger then 840X840 are shrinked (this is not essential, but the net results might degrade when using to large images
            fr=840/r
            Im=cv2.resize(Im,(int(w*fr),int(h*fr)))
        Imgs=np.expand_dims(Im,axis=0)
        print(img_path + " :  running - Make Prediction")
    #................................Make Prediction.............................................................................................................
        with torch.autograd.no_grad():
            OutLbDict=Net.forward(Images=Imgs,TrainMode=False,UseGPU=UseGPU, FreezeBatchNormStatistics=FreezeBatchNormStatistics) # Run net inference and get prediction
    #...............................Save prediction on fil
        
        vesselpix = 0
        filledpix = 0
        Ves = []

        print(img_path + " :  running - start reading pixel")
        # print(img_path[-9:-4])
        for nm in OutLbDict:
            if nm != 'Vessel' and nm != 'Filled' : continue
            Lb=OutLbDict[nm].data.cpu().numpy()[0].astype(np.uint8)
            if Lb.mean()<0.001: continue
            if nm=='Ignore': continue
            ImOverlay1 = Im.copy()
            ImOverlay1[:, :, 0][Lb==1] = 255
            ImOverlay1[:, :, 1][Lb==1] = 0
            ImOverlay1[:, :, 2][Lb==1] = 255
            
            FinIm=np.concatenate([Im,ImOverlay1],axis=1)

            #Get Mask RGB
            h,w = Lb.shape
            for hei in range(h):
                for wid in range(w):
                    if Lb[hei, wid] == 1 :
                        if nm == 'Vessel' : vesselpix = vesselpix + 1
                        if nm == 'Filled' : filledpix = filledpix + 1
                        #print(str(hei) + "," + str(wid))
        # print(img_path + " :  running - read all pixels")
        
            #Draw mask only
            Mask = Im.copy()
            Mask[:,:,:] = 0
            Mask[:,:,0][Lb==1] = 255
            Mask[:,:,2][Lb==1] = 255

            #Get Edge
            LbEdge = isEdge.get(Lb)
            lEdge = Mask.copy()
            lEdge[:,:,:] = 0
            lEdge[:,:,0][LbEdge==1] = 255
            lEdge[:,:,2][LbEdge==1] = 255

            MaEd = np.concatenate([Mask,lEdge],axis=1)

            if nm == 'Vessel' : Ves = Mask.copy()
            if nm == 'Filled' : Fill = Lb.copy()

        Ves[:,:,1][Lb==1] = 255
        Ves[:,:,2][Lb==1] = 255
        
        residual = round(float(filledpix)/float(vesselpix), 1)
        #print("Residual -> " + str(residual))
        
        OutPath = OutDir + "//" + img_name + "/"

        if not os.path.exists(OutPath): os.makedirs(OutPath)

        OutName = OutPath+img_name+"_"+"out"+".png"
        cv2.imwrite(OutName,FinIm)
        
        MaskName = OutPath+img_name+"_"+"mask"+".png"
        cv2.imwrite(MaskName,MaEd)

        VesName = OutPath+img_name+"_"+"vess"+".png"
        cv2.imwrite(VesName, Ves)


        #loopend = time.time()
        #print(f"{loopend - looptime: .5f} sec")
        
        doc_ref = db.collection('IV').document('1414')
        doc_ref.update({
            'remain': residual
        })
        return residual

    except ZeroDivisionError : 
          return 0.0
    except Exception as e :
          print(e)
          return "False"





