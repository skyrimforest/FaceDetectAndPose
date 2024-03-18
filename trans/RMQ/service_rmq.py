import pika
import BaseConfig
from typing import Dict,Callable
import json
from SkyLogger import get_current_time
import threading
from concurrent.futures import ThreadPoolExecutor

# lock=threading.Lock()
local=threading.local()

credentials = pika.PlainCredentials(BaseConfig.RMQ_USER, BaseConfig.RMQ_PASS)
# conn = pika.BlockingConnection(pika.ConnectionParameters(host=BaseConfig.RMQ_IP, port=BaseConfig.RMQ_PORT, virtual_host="/", credentials=credentials))
# channel = conn.channel()
# channel.queue_declare(queue=BaseConfig.RMQ_QUEUE, durable=True)

def init():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=BaseConfig.RMQ_IP, port=BaseConfig.RMQ_PORT, virtual_host="/",
                                  credentials=credentials))
    channel = conn.channel()
    return channel

def rmq_send(message:Dict[str, str]) -> None:
    # with lock:
    if not hasattr(local,'channel'):
        channel=init()
        thread_id = threading.currentThread().ident
        print(f'线程：{thread_id} 创建 channel')
        local.channel = channel
    message=json.dumps(message)
    local.channel.basic_publish(exchange='',
                          routing_key=BaseConfig.RMQ_QUEUE,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))

def rmq_recv(special_callback) -> None:
    # with lock:
    if not hasattr(local,'channel'):
        channel = init()
        thread_id = threading.currentThread().ident
        print(f'线程：{thread_id} 创建 channel')
        local.channel = channel
    local.channel.basic_qos(prefetch_count=1)
    local.channel.basic_consume(queue=BaseConfig.RMQ_QUEUE, on_message_callback=special_callback)
    local.channel.start_consuming()