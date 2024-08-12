from time import sleep
import json
import redis
from app_config import env

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

    def bulk_hset(self, key, data):
        data_key = self._generate_key(key)
        with self.client.pipeline() as pipe:
            for item_key, item_value in data.items():
                pipe.hset(data_key, item_key, json.dumps(item_value))
            pipe.execute()

    def hget(self, key, field):
        data_key = self._generate_key(key)
        data = self.client.hget(data_key, field)
        return json.loads(data) if data else None

    def hmget(self, key, fields):
        data_key = self._generate_key(key)
        data = self.client.hmget(data_key, fields)
        return [json.loads(item) if item else None for item in data]


redis_client = RedisClient(prefix='alpha')


class Store:
    @staticmethod
    def get_instrument_by_symbol_and_token(key):
        return redis_client.hget('instruments:segment:token', key)

    @staticmethod
    def get_instrument_by_identifier(key):
        return redis_client.hget('instruments:identifiers', key)

    @staticmethod
    def get_sl_positions_by_identifiers(identifier):
        position_ids = redis_client.hget('positions:sl', identifier)
        if not position_ids:
            return []
        return redis_client.hmget('positions', position_ids)


store = Store()
