from fastapi import Request
from starlette.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

request_count = Counter("websocket_requests", "Number of WebSocket connections")

async def metrics(request: Request):
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
