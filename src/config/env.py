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
MARKETDATA_APP_KEY = os.getenv('MARKETDATA_APP_KEY')
MARKETDATA_SECRET_KEY = os.getenv('MARKETDATA_SECRET_KEY')
MARKETDATA_SESSION_TOKEN = os.getenv('MARKETDATA_SESSION_TOKEN')

# trading keys
TRADING_CONSUMER_KEY = os.getenv('TRADING_CONSUMER_KEY')
TRADING_CONSUMER_SECRET = os.getenv('TRADING_CONSUMER_SECRET')
TRADING_FIN_KEY = os.getenv('TRADING_FIN_KEY')
TRADING_MOBILE_NUMBER = os.getenv('TRADING_MOBILE_NUMBER')
TRADING_PASSWORD = os.getenv('TRADING_PASSWORD')

# twitter keys
X_API_KEY=os.getenv('X_API_KEY')
X_API_SECRET_KEY=os.getenv('X_API_SECRET_KEY')
X_BEARER_TOKEN=os.getenv('X_BEARER_TOKEN')
X_ACCESS_TOKEN=os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET=os.getenv('X_ACCESS_TOKEN_SECRET')
X_CLIENT_ID=os.getenv('X_CLIENT_ID')
X_CLIENT_SECRET=os.getenv('X_CLIENT_SECRET')