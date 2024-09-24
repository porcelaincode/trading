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

# mongo connection string
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

# marketdata envs
MARKETDATA_CLIENT_ID = os.getenv('MARKETDATA_CLIENT_ID')
MARKETDATA_API_KEY = os.getenv('MARKETDATA_API_KEY')
MARKETDATA_SECRET_KEY = os.getenv('MARKETDATA_SECRET_KEY')
MARKETDATA_SESSION_TOKEN = os.getenv('MARKETDATA_SESSION_TOKEN')
