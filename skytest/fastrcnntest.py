import cv2
import torchvision
import torchvision.models.detection.faster_rcnn
model=torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn()
model.eval()
image=cv2.imread('family.jpg')
predictions=model(image)
