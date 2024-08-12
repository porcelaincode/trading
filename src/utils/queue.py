import pika
from app_config import env

rabbitmq_host = env.RABBITMQ_HOST
rabbitmq_pass = env.RABBITMQ_PASS
rabbitmq_user = env.RABBITMQ_USER

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

queue = connection.channel()

queue.queue_declare(queue='app')

queue.queue_declare(queue='signals')
queue.queue_declare(queue='orders')
queue.queue_declare(queue='positions')

queue.queue_declare(queue='manager')
queue.queue_declare(queue='engine')


def publish_message(queue: str, message: str):
    queue.basic_publish(exchange='', routing_key=queue,
                        body=message)
    pass
