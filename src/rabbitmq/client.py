import threading
import pika
from ..config import env
from pika.exceptions import AMQPConnectionError, ChannelClosedByBroker, ConnectionWrongStateError
import time
import logging

logging.basicConfig(level=logging.INFO)
rabbitmq_logger = logging.getLogger(__name__)


class RabbitMQClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RabbitMQClient, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.rabbitmq_host = env.RABBITMQ_HOST
        self.rabbitmq_user = env.RABBITMQ_USER
        self.rabbitmq_pass = env.RABBITMQ_PASS

        self.credentials = pika.PlainCredentials(
            username=self.rabbitmq_user,
            password=self.rabbitmq_pass
        )
        self.parameters = pika.ConnectionParameters(
            host=self.rabbitmq_host,
            port=5672,
            virtual_host='/',
            credentials=self.credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        attempt = 0
        while True:
            try:
                rabbitmq_logger.info("Attempting to connect to RabbitMQ...")
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                rabbitmq_logger.info("Connected to RabbitMQ")
                break
            except AMQPConnectionError as e:
                attempt += 1
                rabbitmq_logger.error(
                    f"Connection attempt {attempt} failed: {e}")
                time.sleep(5)  # Wait before retrying

    def declare_queue(self, queue_name: str):
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            rabbitmq_logger.info(
                f"Queue '{queue_name}' declared successfully.")
        except ChannelClosedByBroker as e:
            rabbitmq_logger.error(
                f"Failed to declare queue '{queue_name}': {e}")
            self.reconnect()

    def publish_message(self, queue_name: str, message: str):
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            rabbitmq_logger.info(f"Message sent to '{queue_name}': {message}")
        except (AMQPConnectionError, ConnectionWrongStateError) as e:
            rabbitmq_logger.error(f"Failed to send message: {e}")
            self.reconnect()
            self.publish_message(queue_name, message)

    def reconnect(self):
        rabbitmq_logger.info("Reconnecting to RabbitMQ...")
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            rabbitmq_logger.error(f"Error closing connection: {e}")
        self.connect()

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            rabbitmq_logger.info("RabbitMQ connection closed.")


rabbitmq_client = RabbitMQClient()

rabbitmq_client.declare_queue('app')
rabbitmq_client.declare_queue('auth')
rabbitmq_client.declare_queue('broadcast_signals')
