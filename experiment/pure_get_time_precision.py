import pickle
import time

from GetFaceFast.service_face import FaceDetection
import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np


# Memory_Sizes=[14,16,18,20,22,23]
CPU_Ratio=80

image_root_path = BaseConfig.INPUT_PATH + "/handshaking"
args = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 480,
    'threshold': 0.7,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
face_detection = FaceDetection(args)

# for Memory_Size in Memory_Sizes:
for idx in range(0,100):
    start=time.time()
    for root, dirs, files in os.walk(image_root_path):
        for file in files:
            file_name=file.split('.')[0]
            # print(f"file name:{file_name}")
            file_path = BaseConfig.INPUT_PATH + '/handshaking' +'/'+ file
            image = cv2.imread(file_path)
            boxes, labels, probs = face_detection(image) #经过nms操作的最终结果,可以认为是ground truth
            if idx==99:
                with open(BaseConfig.INPUT_PATH + '/cpu'+f"/{CPU_Ratio}"+'/'+file_name+".txt",'w',) as f:
                    for i,box in enumerate(boxes):
                        box = np.array(box, dtype=int)
                        # print(box)
                        f.write(f"person {probs[i]} {box[0]} {box[1]} {box[2]} {box[3]}\n")
    end_time = time.time()

    with open(BaseConfig.INPUT_PATH + '/cpu' + "/time_cost.txt", 'a') as f:
        f.write(f"{CPU_Ratio}---{end_time - start}\n")




