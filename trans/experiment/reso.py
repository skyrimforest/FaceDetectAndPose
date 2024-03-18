import cv2
import BaseConfig

image_root_path = BaseConfig.ROOT_DIR + "/inputpics/test"
file_path = image_root_path + '/' + "family.jpg"
image = cv2.imread(file_path)
resized_image=cv2.resize(image, (640,480))
cv2.imshow("original", image)
cv2.imshow("resized_image", resized_image)
cv2.waitKey(0)
