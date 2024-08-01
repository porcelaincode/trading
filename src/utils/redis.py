import redis
from config import env

redis_host = env.REDIS_HOST
redis_port = int(env.REDIS_PORT) or 6379

redis_client = redis.Redis(host=redis_host, port=redis_port)
