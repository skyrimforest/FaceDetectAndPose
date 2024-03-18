import pickle

from GetFaceFast.service_face import FaceDetection
import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

args = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 480,
    'threshold': 0.7,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
face_detection = FaceDetection(args)
image_root_path = BaseConfig.ROOT_DIR + "/inputpics/test"
file_path = image_root_path + '/' + "family.jpg"
image = cv2.imread(file_path)

boxes, labels, probs = face_detection(image)
print(labels)

for i,box in enumerate(boxes):
    print(f"{i} {box} {probs[i]}")

for i, box in enumerate(boxes):
    box=np.array(box,dtype=int)
    cv2.rectangle(image, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)

cv2.imshow('image',image)
cv2.waitKey(0)


# boxes=np.array(boxes,dtype=int)
# image_info = {
#     'image_name': file_path.split('/')[-1],
#     'boxes': boxes.tolist(),
#     'labels': labels.tolist(),
#     'probs': probs.tolist()
# }
# print(image_info)