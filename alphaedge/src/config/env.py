# module imports
import os
from dotenv import load_dotenv

load_dotenv()

# server variables
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

# cache database
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# messaging broker
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

# local database
DATABASE_URL = os.getenv('DATABASE_URL')