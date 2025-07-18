from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List

router = APIRouter()

# In-memory store for connected clients: worker_id -> list of WebSocket connections
active_connections: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/notifications/{worker_id}")
async def websocket_endpoint(websocket: WebSocket, worker_id: int):
    await websocket.accept()
    if worker_id not in active_connections:
        active_connections[worker_id] = []
    active_connections[worker_id].append(websocket)
    try:
        while True:
            # Keep the connection alive (no need to receive messages)
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections[worker_id].remove(websocket)
        if not active_connections[worker_id]:
            del active_connections[worker_id]

# Utility function to send a notification to a worker
async def send_notification_to_worker(worker_id: int, message: str):
    if worker_id in active_connections:
        for ws in active_connections[worker_id]:
            await ws.send_text(message) 