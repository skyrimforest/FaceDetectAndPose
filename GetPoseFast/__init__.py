
# This Module is mainly designed for Pose Estimation.
# It takes raw images and anchor boxes as input,
# and get the pose estimation (in detail, yaw, pitch, roll) as output.
# What's more, it will receive it's input from RabbitMQ,
# then send it's output to another RabbitMQ queue.
from .service_angle import *
__all__=[]