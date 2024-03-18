import os

from fastapi import APIRouter
from .FaceDetection import FaceDetection
from RMQ import rmq_send
import BaseConfig
import cv2
from SkyLogger import get_logger

logger=get_logger('face_detection')

router = APIRouter(
    prefix="/face",
    tags=["face"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.post("/start")
def start_service():
    logger.info('start detection service')
    args = {
        'net_type': 'mb_tiny_RFB_fd',
        'input_size': 480,
        'threshold': 0.7,
        'candidate_size': 1500,
        'device': 'cuda:0',
    }
    face_detection = FaceDetection(args)
    image_root_path=BaseConfig.ROOT_DIR+"/inputpics"
    for root,dirs,files in os.walk(image_root_path):
        for file in files:
            file_path=image_root_path+'/'+file
            image=cv2.imread(file_path)
            boxes, labels, probs = face_detection(image)
            image_info={
                'image_name':file,
                'image_mat':image.tolist(),
                'boxes': boxes.tolist(),
            }
            rmq_send(image_info)
            logger.info(file_path+' have sent!')
    logger.info('end of detection service')
