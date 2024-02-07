import sys
sys.path.append('..')
import cv2
import torch
from torch.autograd import Variable
from torchvision import transforms
import torch.backends.cudnn as cudnn
import torchvision
import torch.nn.functional as F
from PIL import Image
from .hopenet import Hopenet
import BaseConfig

class FaceAlignmentCNN:
    def __init__(self, args):

        cudnn.enabled = True

        self.__gpu = args['device']
        model_path = BaseConfig.ROOT_DIR+'/Models/'+args['model']+'.pkl'

        print('[{}] Loading model from {}...'.format(__name__, model_path))

        self.__model =Hopenet(torchvision.models.resnet.Bottleneck, [3, 4, 6, 3], 66)

        # saved_state_dict = torch.load(model_path)
        saved_state_dict = torch.load(model_path, map_location=torch.device(self.__gpu))
        self.__model.load_state_dict(saved_state_dict)

        # image preprocess
        self.__transformations = transforms.Compose([transforms.Resize(224),
        transforms.CenterCrop(224), transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        self.__model.eval()

        print('[{}] Model loaded.'.format(__name__))

        # Test torchscript model
        idx_tensor = [idx for idx in range(66)]

        self.__idx_tensor = torch.FloatTensor(idx_tensor)
        self.__batch_size = args['batch_size']

    def __call__(self, image, bbox):
        '''
        An implementation of head pose estimation by solvePnP.
        :param image:
        :param box:
        :return: euler angles
        '''
        head_pose = []
        height, width, _ = image.shape
        print('[{}] len(bbox)={}'.format(__name__, len(bbox)))
        for x_min, y_min, x_max, y_max in bbox:

            x_min = int(max(x_min, 0))
            y_min = int(max(y_min, 0))
            x_max = int(min(width, x_max))
            y_max = int(min(height, y_max))

            face = Image.fromarray(image[y_min:y_max, x_min:x_max])
            face = self.__transformations(face)
            face = face.view(1, face.shape[0], face.shape[1], face.shape[2])
            # face = Variable(face).cuda(self.__gpu)
            face = Variable(face)
            yaw, pitch, roll = self.__model(face)
            yaw_predicted = F.softmax(yaw, dim=1)
            pitch_predicted = F.softmax(pitch, dim=1)
            roll_predicted = F.softmax(roll, dim=1)
            yaw_predicted = torch.sum(yaw_predicted.data[0] * self.__idx_tensor) * 3 - 99
            pitch_predicted = torch.sum(pitch_predicted.data[0] * self.__idx_tensor) * 3 - 99
            roll_predicted = torch.sum(roll_predicted.data[0] * self.__idx_tensor) * 3 - 99
            head_pose.append([yaw_predicted, pitch_predicted, roll_predicted, (x_min + x_max) / 2, (y_min + y_max) / 2, (y_max - y_min) / 2])

        return head_pose

    def forward(self, image, bbox):
        '''
        An implementation of head pose estimation by solvePnP.
        :param image:
        :param box:
        :return: euler angles
        '''
        head_pose = []
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image.shape

        i = 0
        while i < len(bbox):
            face_batch = torch.zeros([self.__batch_size, 3, 224, 224], device='cpu')

            j = 0
            face_location = []
            while j < self.__batch_size and i + j < len(bbox):
                x_min, y_min, x_max, y_max = bbox[i + j]
                x_min = int(max(x_min, 0))
                y_min = int(max(y_min, 0))
                x_max = int(min(x_max, width))
                y_max = int(min(y_max, height))
                face_location.append([x_min, y_min, x_max, y_max])
                face = Image.fromarray(image[y_min:y_max, x_min:x_max])
                face = self.__transformations(face)
                face = face.view(1, face.shape[0], face.shape[1], face.shape[2])
                # face = Variable(face).cuda(self.__gpu)
                face = Variable(face)
                face_batch[j] = face
                j += 1

            yaw, pitch, roll = self.__model(face_batch)
            for k, (x_min, y_min, x_max, y_max) in enumerate(face_location):
                yaw_predicted = F.softmax(yaw[k].unsqueeze(0), dim=1)
                pitch_predicted = F.softmax(pitch[k].unsqueeze(0), dim=1)
                roll_predicted = F.softmax(roll[k].unsqueeze(0), dim=1)
                yaw_predicted = torch.sum(yaw_predicted.data[0] * self.__idx_tensor) * 3 - 99
                pitch_predicted = torch.sum(pitch_predicted.data[0] * self.__idx_tensor) * 3 - 99
                roll_predicted = torch.sum(roll_predicted.data[0] * self.__idx_tensor) * 3 - 99
                head_pose.append([yaw_predicted, pitch_predicted, roll_predicted, (x_min + x_max) / 2, (y_min + y_max) / 2, (y_max - y_min) / 2])

            i += j

        return head_pose
