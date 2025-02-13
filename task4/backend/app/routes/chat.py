from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.redis_service import RedisService
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from app.worker import process_message

router = APIRouter()
redis_service = RedisService()
limiter = Limiter(key_func=lambda _: "global")

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_message(self, user_id: str, message: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
@limiter.limit("5/second")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await process_message.delay(user_id, data)  # Async processing
    except WebSocketDisconnect:
        manager.disconnect(user_id)
