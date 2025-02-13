import redis
import json
from app.config import settings

class RedisService:
    def __init__(self):
        self.redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    def store_message(self, user_id: str, message: str):
        self.redis.rpush(f"chat:{user_id}", message)

    def get_messages(self, user_id: str):
        cached_messages = self.redis.lrange(f"chat:{user_id}", 0, -1)
        return [json.loads(msg) for msg in cached_messages] if cached_messages else []
