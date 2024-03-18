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
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

boxes, labels, probs = face_detection(image)
boxes=np.array(boxes,dtype=int)
image_info = {
    'image_name': file_path.split('/')[-1],
    'boxes': boxes.tolist(),
    'labels': labels.tolist(),
    'probs': probs.tolist()
}
print(image_info)