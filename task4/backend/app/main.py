from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.routes import chat
from app.monitoring import metrics

app = FastAPI(title="Optimized Chat API")

# Rate Limiting (5 requests/sec per user)
limiter = Limiter(key_func=get_remote_address, default_limits=["5/second"])

app.state.limiter = limiter

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(chat.router)
app.add_route("/metrics", metrics)
