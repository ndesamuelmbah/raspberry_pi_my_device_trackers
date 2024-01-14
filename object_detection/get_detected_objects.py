import cv2

def get_detected_objects(img, thres, nms, net, supported_object_names, draw=True, objects=[]):
    class_ids, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(class_ids,bbox)
    if len(objects) == 0: objects = supported_object_names
    object_info =[]
    if len(class_ids) != 0:
        print(f"Found {len(class_ids)} objects in the image {img.shape}, class_ids: {class_ids}, confs: {confs}, bbox: {bbox}")
        for object_id, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
            object_name = supported_object_names[object_id - 1]
            if object_name in objects:
                object_info.append([box,object_name])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,supported_object_names[object_id-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,object_info