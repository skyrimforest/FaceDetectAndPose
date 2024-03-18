import pickle
import time

from GetFaceFast.service_face import FaceDetection
import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np


# 128: [128, 128],
# 160: [160, 160],
# 320: [320, 240],
# 480: [480, 320],
# 640: [640, 480],
# 1280: [1280, 640]

reso=[
    (128,96),
    (160,120),
    (320,240),
    (480,360),
    (640,480),
    (1280,960)
]
# args = {
#     'net_type': 'mb_tiny_RFB_fd',
#     'input_size': 480,
#     'threshold': 0.7,
#     'candidate_size': 1500,
#     'device': 'cuda:0',
# }
# face_detection = FaceDetection(args)
image_root_path = BaseConfig.INPUT_PATH + "/handshaking"

# 第一步测基准
# start=time.time()
# for root, dirs, files in os.walk(image_root_path):
#     for file in files:
#         file_name=file.split('.')[0]
#         print(f"file name:{file_name}")
#         file_path = BaseConfig.INPUT_PATH + '/handshaking' +'/'+ file
#         image = cv2.imread(file_path)
#         boxes, labels, probs = face_detection(image) #经过nms操作的最终结果,可以认为是ground truth
#         with open(BaseConfig.GROUND_TRUTH_PATH+'/'+file_name+".txt",'w',) as f:
#             for i,box in enumerate(boxes):
#                 box = np.array(box, dtype=int)
#                 print(box)
#                 f.write(f"person {box[0]} {box[1]} {box[2]} {box[3]}\n")
# end_time = time.time()


args = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 480,
    'threshold': 0.7,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
# 第二步测试分辨率
for res in reso:
    args['input_size'] = res[0]
    face_detection = FaceDetection(args)
    start=time.time()
    for root, dirs, files in os.walk(image_root_path):
        for file in files:
            file_name=file.split('.')[0]
            print(f"file name:{file_name}")
            file_path = BaseConfig.INPUT_PATH + '/handshaking' +'/'+ file
            image = cv2.imread(file_path)
            image_resize=cv2.resize(image,res)
            boxes, labels, probs = face_detection(image_resize) #经过nms操作的最终结果,可以认为是ground truth
            with open(BaseConfig.DETECTION_RESULT+f"/{res[0]}"+'/'+file_name+".txt",'w',) as f:
                for i,box in enumerate(boxes):
                    box_int = np.array(box, dtype=int)
                    # print(box)
                    f.write(f"person {probs[i]} {box_int[0]} {box_int[1]} {box_int[2]} {box_int[3]}\n")
    end_time = time.time()
    print(end_time-start)
    with open(BaseConfig.INPUT_PATH+'/'+"time_cost.txt",'a') as f:
        f.write(f"{end_time-start}\n")




# for i,box in enumerate(boxes):
#     print(f"{i} {box} {probs[i]}")
#
# for i, box in enumerate(boxes):
#     box=np.array(box,dtype=int)
#     cv2.rectangle(image, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)
#
# cv2.imshow('image',image)
# cv2.waitKey(0)
