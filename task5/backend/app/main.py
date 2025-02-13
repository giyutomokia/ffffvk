from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from app.routes import chat
from app.config import settings
from app.monitoring import metrics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WebSocket Chat API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include WebSocket routes
app.include_router(chat.router)

# Add monitoring endpoint
app.add_route("/metrics", metrics)
