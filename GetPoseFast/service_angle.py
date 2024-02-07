import numpy as np
import torch
from fastapi import APIRouter
from .FaceAlignment import FaceAlignmentCNN,draw_axis
from RMQ import rmq_recv
import BaseConfig
import cv2
from SkyLogger import get_logger
import json

logger=get_logger('face_alignment')

router = APIRouter(
    prefix="/pose",
    tags=["pose"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


def align_callback(ch, method, properties, body):
    args = {
        'lite_version': False,
        'model': 'hopenet',
        'batch_size': 1,
        'device': 'cuda:0',
    }

    face_alignment = FaceAlignmentCNN(args)
    body=body.decode()
    body=json.loads(body)
    image=np.array(body['image_mat'],dtype=np.uint8)
    boxes=torch.Tensor(body['boxes'])
    # print(body)
    image_name=body['image_name']
    head_pose = face_alignment(image, boxes)

    axis=[]
    for yaw, pitch, roll, tdx, tdy, size in head_pose:
        ax = draw_axis(image, yaw, pitch, roll, tdx=tdx, tdy=tdy,size=size)
        axis.append(ax)

    for ax in axis:
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[2]), int(ax[3])),
                 (0, 0, 255), 3)
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[4]), int(ax[5])),
                 (0, 255, 0), 3)
        cv2.line(image, (int(ax[0]), int(ax[1])), (int(ax[6]), int(ax[7])),
                 (0, 255, 255), 2)

    # image_name='test'
    cv2.imwrite(BaseConfig.OUTPUT_PATH+'/'+image_name, image)
    logger.info('pic results written!')

    ch.basic_ack(delivery_tag = method.delivery_tag)

    # pass
@router.post("/start")
def start_service():
    # face_alignment = FaceAlignmentCNN(args)
    logger.info('start alignment service')
    rmq_recv(align_callback)

    # head_pose=face_alignment(image,boxes)
    # image_root_path=BaseConfig.ROOT_DIR+"/inputpics"
    # for root,dirs,files in os.walk(image_root_path):
    #     for file in files:
    #         file_path=image_root_path+'/'+file
    #         image=cv2.imread(file_path)
    #         boxes, labels, probs = face_detection(image)
    #         image_info={
    #             'image_mat':image.tolist(),
    #             'boxes': boxes.tolist(),
    #         }
    #         rmq_send(image_info)
    #         logger.info(file_path+' have sent!')
    # logger.info('end of detection service')