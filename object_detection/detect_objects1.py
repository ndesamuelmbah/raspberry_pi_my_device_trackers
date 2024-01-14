import cv2
import time, sys
from datetime import datetime

from get_detected_objects import get_detected_objects

#thres = 0.45 # Threshold to detect object
camera_index = 0
args = sys.argv
if len(args) != 2:
    print("You are running in with default camera index 0. If you want to use a different camera, please provide the camera index as an argument to this script.")
else:
    assert args[1].isdigit(), "Please provide a valid camera index."
    camera_index = int(args[1])

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

print(f'{datetime.now()}: Starting to set video camera index ...')
cap = cv2.VideoCapture(camera_index)
print(f'{datetime.now()}: Set camera to camera index {camera_index}.')
cap.set(3,640)
print(f'{datetime.now()}: Set camera width to 640.')
#cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS, 15)
print(f'{datetime.now()}: Set camera frame rate to 15.')
# Set up video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
print(f'{datetime.now()}: Set up video writer for xvid with fourcc.')
time_now = datetime.now()
output_file = f"{time_now.strftime('%Y-%m-%d-%H-%M-%S-%f')}.avi"
out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
print(f'{datetime.now()}: Set up video writer for output file {output_file}.')
#cap.set(4,480)
#cap.set(10,70)


while True:
    start = datetime.now()
    print(f'{datetime.now()}: Starting to read from camera ...')
    success, img = cap.read()
    print(f'{datetime.now()}: Read from camera.')
    result, object_info = get_detected_objects(img,0.45,0.2, net, supported_object_names, objects=[])
    print(f'{datetime.now()}: Got detected objects.')
    #print(object_info)
    #cv2.imshow("Output",img)
    end = datetime.now()
    out.write(img)
    print(f'{datetime.now()}: Wrote frame to video file.')
    print(f'Completed in {(end - start).total_seconds()} seconds.')
    #time.sleep(1)
    cv2.waitKey(1)
