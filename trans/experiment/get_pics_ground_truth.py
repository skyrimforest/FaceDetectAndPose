import BaseConfig
import os
from GetFaceFast.service_face import FaceDetection
import cv2
import numpy as np

image_root_path = BaseConfig.INPUT_PATH + "/handshaking"
image_detect_path = BaseConfig.INPUT_PATH + "/person_per_pics"
show_detect_path = BaseConfig.INPUT_PATH + "/show_pics"

args = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 1280,
    'threshold': 0.9,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
face_detection = FaceDetection(args)

reso=(1280,960)


for root, dirs, files in os.walk(image_root_path):
    for file in files:
        file_name = file.split('.')[0]
        print(f"file name:{file_name}")
        file_path = BaseConfig.INPUT_PATH + '/handshaking' + '/' + file
        image = cv2.imread(file_path)
        origin =image.shape
        image=cv2.resize(image,reso)
        boxes, labels, probs = face_detection(image)  # 经过nms操作的最终结果,可以认为是ground truth
        with open(f"{image_detect_path}" + '/' + file_name + ".txt", 'w', ) as f:
            for i, box in enumerate(boxes):
                box = np.array(box, dtype=int)
                f.write(f"person {probs[i]} {box[0]} {box[1]} {box[2]} {box[3]}\n")
                cv2.rectangle(image, pt1=(box[0], box[1]), pt2=(box[2], box[3]), color=(0, 255, 255), thickness=2)
                cv2.imwrite("after_"+file_name+".jpg",image)


