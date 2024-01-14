import cv2
import time
from datetime import datetime

from get_detected_objects import get_detected_objects

#thres = 0.45 # Threshold to detect object

supported_object_names = []
supported_object_names_files = "coco.names"
with open(supported_object_names_files,"rt") as f:
    supported_object_names = f.read().rstrip("\n").split("\n")

model_config_file_path = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
model_weights_file_path = "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(model_weights_file_path,model_config_file_path)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# def get_detected_objects(img, thres, nms, draw=True, objects=[]):
#     class_ids, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
#     #print(class_ids,bbox)
#     if len(objects) == 0: objects = supported_object_names
#     object_info =[]
#     if len(class_ids) != 0:
#         for object_id, confidence,box in zip(class_ids.flatten(),confs.flatten(),bbox):
#             object_name = supported_object_names[object_id - 1]
#             if object_name in objects:
#                 object_info.append([box,object_name])
#                 if (draw):
#                     cv2.rectangle(img,box,color=(0,255,0),thickness=2)
#                     cv2.putText(img,supported_object_names[object_id-1].upper(),(box[0]+10,box[1]+30),
#                     cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
#                     cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
#                     cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

#     return img,object_info


cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(cv2.CAP_PROP_FPS, 15)
# Set up video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
#cap.set(4,480)
#cap.set(10,70)


while True:
    start = datetime.now()
    success, img = cap.read()
    result, object_info = get_detected_objects(img,0.45,0.2, net, supported_object_names, objects=[])
    #print(object_info)
    cv2.imshow("Output",img)
    end = datetime.now()
    out.write(img)
    print(f'Completed in {(end - start).total_seconds()} seconds.')
    #time.sleep(1)
    cv2.waitKey(1)
