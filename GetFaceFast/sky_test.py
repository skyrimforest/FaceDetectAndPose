from FaceDetection import FaceDetection
import cv2
import requests
if __name__ == '__main__':
    requests.post('http://192.168.0.107:8000/face/start')
    # requests.post('http://192.168.0.107:8000/')
    # requests.get('http://192.168.0.107:8000/')
    # args = {
    #     'net_type': 'mb_tiny_RFB_fd',
    #     'input_size': 480,
    #     'threshold': 0.7,
    #     'candidate_size': 1500,
    #     'device': 'cuda:0',
    # }
    # face_detection = FaceDetection(args)
    # image=cv2.imread('../inputpics/xuezhang.jpg')
    # boxes, labels, probs = face_detection(image)
    # print(boxes)
    # print(labels)
    # print(probs)