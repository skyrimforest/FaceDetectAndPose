import pickle

from GetFaceFast.service_face import FaceDetection
import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np
# def draw_boxes(image, boxes, labels, probs):
#     for i,box in enumerate(boxes):
#         cv2.rectangle(image, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 0, 255),thickness=2)
#     cv2.imshow('image', image)
#
# args = {
#     'net_type': 'mb_tiny_RFB_fd',
#     'input_size': 480,
#     'threshold': 0.7,
#     'candidate_size': 1500,
#     'device': 'cuda:0',
# }
# face_detection = FaceDetection(args)
# image_root_path = BaseConfig.ROOT_DIR + "/inputpics/test"
# file_path = image_root_path + '/' + "family.jpg"
# image = cv2.imread(file_path)
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# boxes, labels, probs = face_detection(image)
# boxes=np.array(boxes,dtype=int)
# image_info = {
#     'image_name': file_path.split('/')[-1],
#     'boxes': boxes.tolist(),
#     'labels': labels.tolist(),
#     'probs': probs.tolist()
# }
# print(image_info)
with open("beforenms2.pkl","rb") as f1:
    with open("afternms2.pkl","rb") as f2:
        beforeNms = pickle.load(f1)
        afterNms = pickle.load(f2)
        print(beforeNms)
        print(afterNms)
        beforeNms=np.array(beforeNms,dtype=int)
        afterNms=np.array(afterNms,dtype=int)
        print(beforeNms)
        print(afterNms)
        # plt.imshow(image_rgb)

        image_root_path = BaseConfig.ROOT_DIR + "/inputpics/test"
        file_path = image_root_path + '/' + "family.jpg"
        image1 = cv2.imread(file_path)
        image_rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image2 = cv2.imread(file_path)
        image_rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        for i, box in enumerate(beforeNms):
            cv2.rectangle(image_rgb1, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)

        for i, box in enumerate(afterNms):
            cv2.rectangle(image_rgb2, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)


        fig = plt.figure(figsize=(8, 4))
        fig.suptitle(
            f'comparison between before NMS and after NMS'
        )
        gs = gridspec.GridSpec(1, 2, figure=fig)
        before = plt.subplot(gs[0,0:1])
        after = plt.subplot(gs[0,1:2])

        before.imshow(image_rgb1)
        before.set_title("before NMS")
        after.imshow(image_rgb2)
        after.set_title("after NMS")
        fig.show()


        # for i, box in enumerate(boxes):
        #     cv2.rectangle(image, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)
        # cv2.imshow('image', image)
        # cv2.waitKey(0)


