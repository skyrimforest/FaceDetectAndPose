# handshaking 总共121张图片
import pickle

from GetPoseFast import FaceAlignmentCNN,draw_axis
from GetFaceFast.service_face import FaceDetection

import BaseConfig
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib import gridspec
import time
import psutil

def my_draw_axis(image,head_pose,pic_name):
    axis = []
    for yaw, pitch, roll, tdx, tdy, size in head_pose:
        ax = draw_axis(image, yaw, pitch, roll, tdx=tdx, tdy=tdy, size=size)
        axis.append(ax)

    for ax in axis:
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[2]), int(ax[3])),
                 (0, 0, 255), 3)
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[4]), int(ax[5])),
                 (0, 255, 0), 3)
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[6]), int(ax[7])),
                 (0, 255, 255), 2)

    # image_name='test'
    cv2.imwrite(BaseConfig.OUTPUT_PATH + '/' + f"{pic_name}", image)

args1 = {
    'net_type': 'mb_tiny_RFB_fd',
    'input_size': 480,
    'threshold': 0.7,
    'candidate_size': 1500,
    'device': 'cuda:0',
}
args = {
    'lite_version': False,
    'model': 'hopenet',
    'batch_size': 1,
    'device': 'cuda:0',
}

face_detection = FaceDetection(args1)
image_root_path = BaseConfig.ROOT_DIR + "/inputpics/handshaking"

face_alignment = FaceAlignmentCNN(args)

memory_usage0 = psutil.Process().memory_info().rss # 记录字节数
print(f"最初的内存:{memory_usage0} bytes")
p = psutil.Process()
print(f"最初的CPU:{p.cpu_percent(interval=None)}%")

all_file_name=[]
pics=[]
for root, dirs, files in os.walk(image_root_path):
    for file in files:
        file_path = image_root_path + '/' + file
        all_file_name.append(file_path)
        image = cv2.imread(file_path)
        pics.append(image)
        # boxes, labels, probs = face_detection(image)
# print(all_file_name)
memory_usage1 = psutil.Process().memory_info().rss # 记录字节数
print(f"读入图片后的内存:{memory_usage1}")
print(f"读入图片后CPU:{p.cpu_percent(interval=None)}%")

pic_boxes=[]
t1=time.time()
for i,pic in enumerate(pics):
    # image_rgb1 = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    boxes, labels, probs = face_detection(pic)
    pic_boxes.append(boxes)
    # memory_usage2 = psutil.Process().memory_info().rss  # 记录字节数
    # print(f"做检测时的内存:{memory_usage2}")
    # print(f"做检测的CPU:{p.cpu_percent(interval=None)}%")
t2=time.time()

detect_time = t2-t1
memory_usage2 = psutil.Process().memory_info().rss # 记录字节数
print(f"做完检测后的内存:{memory_usage2}")
cpu_usage2=p.cpu_percent(interval=None)
print(f"做完检测后的CPU:{cpu_usage2}%")

print(f"pure detect time needed:{detect_time}")

head_poses=[]
t1=time.time()
for i,pic in enumerate(pics):
    head_pose = face_alignment(pic, pic_boxes[i])
    head_poses.append(head_pose)
t2=time.time()

alignment_time = t2-t1
memory_usage3 = psutil.Process().memory_info().rss # 记录字节数
print(f"做完姿态识别后的内存:{memory_usage3}")
print(f"face alignment time needed:{alignment_time}")
cpu_usage3=p.cpu_percent(interval=None)
print(f"做完姿态识别后的CPU:{cpu_usage3}%")
# image1 = cv2.imread(file_path)
# image_rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
# boxes, labels, probs = face_detection(image1)
# print(boxes)
# head_pose = face_alignment(image1, boxes)

t1=time.time()
for i,head_pose in enumerate(head_poses):
    my_draw_axis(pics[i],head_pose,all_file_name[i].split('/')[-1])
t2=time.time()
write_time=t2-t1
memory_usage4 = psutil.Process().memory_info().rss # 记录字节数
print(f"画完图后的内存:{memory_usage4}")
print(f"written to disk time needed:{write_time}")
cpu_usage4=p.cpu_percent(interval=None)
print(f"画完图后的CPU:{cpu_usage4}%")


detect_labels=['time','memory','cpu']
detect_height=[detect_time,(memory_usage2-memory_usage1)/(2**25),cpu_usage2]

align_labels=['time','memory','cpu']
align_height=[alignment_time,(memory_usage3-memory_usage2)/(2**25),cpu_usage3]

write_labels=['time','memory','cpu']
write_height=[write_time,(memory_usage4-memory_usage3)/(2**25),cpu_usage4]

fig = plt.figure(figsize=(21, 15))
fig.suptitle(
    f'each phase resource usage',
    fontsize=50
)

gs = gridspec.GridSpec(1, 3, figure=fig)
detect = plt.subplot(gs[0, 0:1])
align = plt.subplot(gs[0, 1:2])
w2disk = plt.subplot(gs[0, 2:3])

detect.set_title("face detection phase",fontdict={'size':25})
detect.axis('on')
detect.bar(detect_labels,detect_height,color=['red', 'green', 'blue'])
# detect.set_xlabel('index', fontdict={'size':20})
detect.tick_params(labelsize=20)
detect.set_ylabel('time:seconds; memory:32MB; cpu:percentage %', fontdict={'size':20},)
detect.set_ylim((0, 60))

align.set_title("pose estimation phase",fontdict={'size':25})
align.axis('on')
align.bar(align_labels,align_height,color=['red', 'green', 'blue'])
align.tick_params(labelsize=20)
# align.set_xlabel('index', fontdict={'size':20})
align.set_ylim((0,60))

w2disk.set_title("write to disk phase",fontdict={'size':25})
w2disk.axis('on')
w2disk.bar(write_labels,write_height,color=['red', 'green', 'blue'])
w2disk.tick_params(labelsize=20)
# w2disk.set_xlabel('index', fontdict={'size':20})
w2disk.set_ylim((0,60))

fig.show()





