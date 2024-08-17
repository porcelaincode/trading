import pika
from config import env

rabbitmq_host = env.RABBITMQ_HOST
rabbitmq_pass = env.RABBITMQ_PASS
rabbitmq_user = env.RABBITMQ_USER

credentials = pika.PlainCredentials(username=rabbitmq_user, password=rabbitmq_pass)
parameters = pika.ConnectionParameters(host=rabbitmq_host, port=5672, virtual_host='/', credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

queue = connection.channel()

queue.queue_declare(queue='app')
queue.queue_declare(queue='auth')

def publish_message(queue: str, message: str):
    queue.basic_publish(exchange='', routing_key=queue,
                        body=message)
    pass