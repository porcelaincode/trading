# module imports
import os
from dotenv import load_dotenv

load_dotenv()

# server variables
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

# database variables
DATABASE_URL = os.getenv("DATABASE_URL")

# broker creds
# CONSUMER_KEY = os.getenv("NEO_PROD_CONSUMER_KEY")
# CONSUMER_SECRET = os.getenv("NEO_PROD_CONSUMER_SECRET")
# NEO_FIN_KEY = os.getenv("NEO_FIN_KEY")
# NEO_MOBILE_NUMBER = os.getenv("NEO_MOBILE_NUMBER")
# NEO_PASSWORD = os.getenv("NEO_PASSWORD")
# ENVIRONMENT = os.getenv("ENVIRONMENT")

FYERS_WEBHOOK_SECRET = os.getenv('FYERS_WEBHOOK_SECRET')

ICICI_API_KEY = os.getenv("ICICI_API_KEY")
ICICI_API_SECRET = os.getenv("ICICI_API_SECRET")
ICICI_API_USER_ID = os.getenv("ICICI_API_USER_ID")

# database variables
WEBSOCKET_HOST = os.getenv("WEBSOCKET_HOST")
WEBSOCKET_PORT = os.getenv("WEBSOCKET_PORT")

# twitter variables
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_BASE_URL = os.getenv('TWITTER_BASE_URL')

# backup base
MONGODB_URL = os.getenv('MONGODB_URL')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')

# local database
SQLITE_DATABASE = os.getenv('SQLITE_DATABASE')
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH')

# cache database
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# messaging broker
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')
