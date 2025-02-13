from celery import Celery
from app.services.redis_service import RedisService

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

redis_service = RedisService()

@celery.task
def process_message(user_id: str, message: str):
    redis_service.store_message(user_id, message)
    return {"user": user_id, "message": message}
