import pickle

from GetPoseFast import FaceAlignmentCNN,draw_axis
from GetFaceFast.service_face import FaceDetection

import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec

args = {
    'lite_version': False,
    'model': 'hopenet',
    'batch_size': 1,
    'device': 'cuda:0',
}
args1 = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 480,
    'threshold': 0.7,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
face_detection = FaceDetection(args1)
image_root_path = BaseConfig.ROOT_DIR + "/inputpics/test"

face_alignment = FaceAlignmentCNN(args)
file_path = image_root_path + '/' + "shaking.jpg"
image1 = cv2.imread(file_path)
image_rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
boxes, labels, probs = face_detection(image1)
print(boxes)
head_pose = face_alignment(image1, boxes)

axis=[]
for yaw, pitch, roll, tdx, tdy, size in head_pose:
    ax = draw_axis(image1, yaw, pitch, roll, tdx=tdx, tdy=tdy,size=size)
    axis.append(ax)

for ax in axis:
    cv2.line(image1, (int(ax[0]), int(ax[1])), (int(ax[2]), int(ax[3])),
             (0, 0, 255), 3)
    cv2.line(image1, (int(ax[0]), int(ax[1])), (int(ax[4]), int(ax[5])),
             (0, 255, 0), 3)
    cv2.line(image1, (int(ax[0]), int(ax[1])), (int(ax[6]), int(ax[7])),
             (0, 255, 255), 2)

# image_name='test'
cv2.imwrite(BaseConfig.OUTPUT_PATH+'/'+"shaking.jpg", image1)

