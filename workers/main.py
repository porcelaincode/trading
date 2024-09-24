import pika
import requests as req
import json
import os
from dotenv import load_dotenv

load_dotenv()
rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')
fastapi_host = os.getenv("HOST")
fastapi_port = int(os.getenv("PORT"))

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

queue = connection.channel()


def handleSignals(body):
    # req.post(f'http://{fastapi_host}:{fastapi_port}/api/signals')
    print('handleSignals: ', body)


def handleOrders(body):
    # req.post(f'http://{fastapi_host}:{fastapi_port}/api/orders')
    print('handleOrders: ', body)


def handlePositions(body):
    print('positionReq: ', body)


def handleAppEvents(body):
    # req.post(f'http://{fastapi_host}:{fastapi_port}/api/events')
    print('appEvent: ', body)


queue_handlers = {
    'orders': handleOrders,
    'positions': handlePositions,
    'signals': handleSignals,
    'app': handleAppEvents
}


def callback(ch, method, properties, body):
    queue_name = method.routing_key
    handler = queue_handlers.get(queue_name)
    if handler:
        handler(json.loads(body))
    else:
        print(f"No handler found for queue: {queue_name}")


for queue_name in queue_handlers.keys():
    queue.queue_declare(queue=queue_name)
    queue.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
queue.start_consuming()