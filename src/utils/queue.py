import pika
from config import env

rabbitmq_user = env.RABBITMQ_USER
rabbitmq_host = env.RABBITMQ_HOST
rabbitmq_pass = env.RABBITMQ_PASS

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
parameters = pika.ConnectionParameters(rabbitmq_host, 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)

queue = connection.channel()


queue.queue_declare(queue='signals')
queue.queue_declare(queue='orders')
queue.queue_declare(queue='positions')


def publish_message(queue: str, message: str):
    queue.basic_publish(exchange='', routing_key=queue,
                        body=message)
    pass
