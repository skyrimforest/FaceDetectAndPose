import pika
import BaseConfig
from typing import Dict
import json
from SkyLogger import get_current_time
credentials = pika.PlainCredentials(BaseConfig.RMQ_USER, BaseConfig.RMQ_PASS)
conn = pika.BlockingConnection(pika.ConnectionParameters(host=BaseConfig.RMQ_IP, port=BaseConfig.RMQ_PORT, virtual_host="/", credentials=credentials))
channel = conn.channel()
channel.queue_declare(queue=BaseConfig.RMQ_QUEUE, durable=True)


def rmq_send(message:Dict[str, str]) -> None:
    message=json.dumps(message)
    channel.basic_publish(exchange='',
                          routing_key=BaseConfig.RMQ_QUEUE,
                          body=message,
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))


def callback(ch, method, properties, body):
    print(get_current_time()+f"[x] Received {body.decode()}")
    print("[x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

def rmq_recv():
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=BaseConfig.RMQ_QUEUE, on_message_callback=callback)
    channel.start_consuming()

