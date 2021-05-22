# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np
import argparse
from random import choice
from uuid import uuid4 
import cvlib 
from cvlib.object_detection import draw_bbox



BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

def color():
    cor = list(range(255))
    return choice(cor)

cor = color()

def pose_estimation(IMAGE,flag):
  print(IMAGE)
  thr = 0.1
  inWidth = 368
  inHeight = 368
  net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
  cap = cv.VideoCapture(IMAGE)
  cor = color()
  font = cv.FONT_HERSHEY_SCRIPT_SIMPLEX 
  frame = None
  status = {'pose':0}  
    
  while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        try:
            face, conf = cvlib.detect_face(frame)
            padding = 20
            for f in face:
                    (startX,startY) = max(0, f[0]-padding), max(0, f[1]-padding)
                    (endX,endY) = min(frame.shape[1]-1, f[2]+padding), min(frame.shape[0]-1, f[3]+padding)
                    cv.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
                    (label, confidence) = cvlib.detect_gender(np.copy(frame[startY:endY, startX:endX]))
                    idx = np.argmax(confidence)
                    label = label[idx]
                    conf = confidence[idx] * 100
                    if conf > 90:
                       cv.putText(frame, "{}: {:.2f}%".format(label, conf), (startX, startY - 10 if startY - 10 > 10 else startY + 10),  cv.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 255, 0), 2)
                       if label=='male' and flag == True:
                            status['pose'] = 'aprovado'
                       else:
                            status['pose'] = 'reprovado' 
                            
                    else:
                        print("...")

        except TypeError:
            pass

        if not hasFrame:
            cv.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]  
        assert(len(BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(BODY_PARTS)):
            heatMap = out[0, i, :, :]
            _, conf, _, point = cv.minMaxLoc(heatMap)
            points.append((int((frameWidth * point[0]) / out.shape[3]), int((frameHeight * point[1]) / out.shape[2])) if conf > thr else None)

        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:
                cv.line(frame, points[idFrom], points[idTo], (cor,cor ,cor), 3)
                print(idFrom,idTo,points[idFrom], points[idTo])
                cv.ellipse(frame, points[idFrom], (4, 4), 0, 0, 360, (cor,cor ,cor), cv.FILLED)
                cv.ellipse(frame, points[idTo], (4, 4), 0, 0, 360, (cor,cor ,cor), cv.FILLED)

        t, _ = net.getPerfProfile()
        freq = cv.getTickFrequency() / 1000
        cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        #cv.imshow('OpenPose using OpenCV', frame)
        name = "output_"+str(uuid4())+IMAGE

        cv.imwrite(name,frame)         
  return status  

#print(pose_estimation("einstein.jpg",True)) 
url ="https://to-vivo-app.s3.amazonaws.com/users/usr_54fbb7f880214222958ce92aef0f22f2/renato_corpo_inteiro.jpg"


print(pose_estimation(url,True)) 