import argparse
import sys
sys.path.append('..')
from .config.fd_config import define_img_size
# from vision.ssd.mb_tiny_fd import create_mb_tiny_fd, create_mb_tiny_fd_predictor
from .mb_tiny_RFB_fd import create_Mb_Tiny_RFB_fd, create_Mb_Tiny_RFB_fd_predictor
import BaseConfig

class FaceDetection:

    def __init__(self, args):

        define_img_size(args['input_size'])  # must put define_img_size() before 'import create_mb_tiny_fd, create_mb_tiny_fd_predictor'
        # label = 'Models/voc-model-labels.txt'

        label = BaseConfig.ROOT_DIR+'/Models/voc-model-labels.txt'
        class_names = [name.strip() for name in open(label).readlines()]

        # if args['net_type'] == 'mb_tiny_fd':
        #     model_path = 'models/pretrained/Mb_Tiny_FD_train_input_320.pth'
        #     net = create_mb_tiny_fd(len(class_names), is_test=True, device=args['device'])
        #     self.__predictor = create_mb_tiny_fd_predictor(net, candidate_size=args['candidate_size'], device=args['device'])
        # elif
        if args['net_type'] == 'mb_tiny_RFB_fd':
            model_path =  BaseConfig.ROOT_DIR+'/Models/Mb_Tiny_RFB_FD_train_input_640.pth'
            # model_path = "models/pretrained/Mb_Tiny_RFB_FD_train_input_640.pth"
            net = create_Mb_Tiny_RFB_fd(len(class_names), is_test=True, device=args['device'])
            self.__predictor = create_Mb_Tiny_RFB_fd_predictor(net, candidate_size=args['candidate_size'], device=args['device'])
        else:
            print('[{}] The net type is wrong!'.format(__name__))
            sys.exit(1)

        self.__args = args
        net.load(model_path)

    def __call__(self, image):
        boxes, labels, probs = self.__predictor.predict(image, self.__args['candidate_size'] / 2, self.__args['threshold'])
        return boxes, labels, probs
