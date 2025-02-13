from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.redis_service import RedisService
import json

router = APIRouter()

redis_service = RedisService()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.dumps({"user": user_id, "message": data})
            await redis_service.store_message(user_id, message)
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
