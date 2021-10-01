import cv2
import numpy as np
import os

# Hyper-Parameters



# image formats supported by OpenCv
image_format = ["bmp", "pbm", "pgm", "ppm", "jpeg", "jpg", "jpe", "png", "sr", "ras", "jp2", "tiff", "tif"]
# video formats supported by OpenCv
video_format = ["avi", "mp4"]
# for Images


nmsthreshold=0.2  # non max suppresion 

confThreshold =0.3 # confidence threshold
whT=416
classFile='Yolo/obj.names'
modelConfiguration='Yolo/yolov4-obj.cfg'

modelWeights='Yolo/yolov4-obj_last.weights'



classNames=[]
with open(classFile,'rt') as f:
    classNames=f.read().rstrip('\n').split('\n')

net= cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

#setting preferences
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)  
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def data(cap):
    all_boxes=[]
    blob=cv2.dnn.blobFromImage(cap,1/255,(whT,whT),[0,0,0],1,crop=False)
    net.setInput(blob)                                         # blob conversion
    layerNames = net.getLayerNames()
    
    
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
   
    outputs = net.forward(outputNames) # getting the outputs
  
    hT,wT,cT=cap.shape
    bbox=[]
    box=[]
    classIds=[]
    confs=[]
    for output in outputs:
        for det in output:
            scores=det[5:]
            classId=np.argmax(scores)
            confidence=scores[classId]
            if confidence> confThreshold:
                w,h=int(det[2]*wT),int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2),int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices= cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsthreshold)  
    
   
    for j in indices:
        j=j[0]
        box=bbox[j]
        x,y,w,h=box[0],box[1],box[2],box[3]   
        a = (classIds[j], x + w/2, y + h/2, w, h) # class, x_center, y_center, height,width
        all_boxes.append(a)
        
              #getting the imgs and box coordinates
   
    return all_boxes


def get_image_coordinates(path):
    for i in os.listdir(path):
        if i.split('.')[-1] in image_format:
            cap = cv2.imread(path+i)
            
            return data(cap)
        # #elif i.split('.')[-1] in video_format:
        #     cap = cv2.VideoCapture('capture.mp4')
        #     while(cap.isOpened()):
        #         ret, frame = cap.read()
        #         if ret == True:
        #             return data(cap)




