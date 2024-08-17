from time import sleep
import redis
from config import env

redis_host = env.REDIS_HOST
redis_port = int(env.REDIS_PORT) or 6379


class RedisClient:
    def __init__(self, prefix, max_retries=20):
        self.prefix = prefix
        self.max_retries = max_retries
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port
        )
        self._connect()

    def _connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client.ping()
                print("Connected to Redis!!!")
                return
            except redis.ConnectionError:
                retries += 1
                print(f"Attempt {retries} to reconnect...")
                sleep(retries * 0.5)
        raise Exception("Too many retries.")

    def _generate_key(self, key):
        return f"{self.prefix}:{key}"

redis_client = RedisClient(prefix='alphaedge')


class Store:
  pass

store = Store()