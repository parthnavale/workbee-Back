from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, List
import json
import logging

router = APIRouter()

# Configure logging
logger = logging.getLogger(__name__)

# In-memory store for connected clients: worker_id -> list of WebSocket connections
active_connections: Dict[int, List[WebSocket]] = {}

@router.websocket("/ws/notifications/{worker_id}")
async def websocket_endpoint(websocket: WebSocket, worker_id: int):
    await websocket.accept()
    logger.info(f"WebSocket connection established for worker {worker_id}")
    
    if worker_id not in active_connections:
        active_connections[worker_id] = []
    active_connections[worker_id].append(websocket)
    
    logger.info(f"Active connections for worker {worker_id}: {len(active_connections[worker_id])}")
    
    try:
        while True:
            # Receive messages and broadcast them to all connections for this worker
            message = await websocket.receive_text()
            logger.info(f"Received message from worker {worker_id}: {message}")
            
            # Broadcast the message to all other connections for this worker
            for other_ws in active_connections[worker_id]:
                if other_ws != websocket:  # Don't send back to sender
                    try:
                        await other_ws.send_text(message)
                        logger.info(f"Broadcasted message to worker {worker_id}")
                    except Exception as e:
                        logger.error(f"Failed to broadcast message: {e}")
                        
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for worker {worker_id}")
        active_connections[worker_id].remove(websocket)
        if not active_connections[worker_id]:
            del active_connections[worker_id]

# HTTP endpoint to send notifications to workers
@router.post("/send-notification/{worker_id}")
async def send_notification_to_worker(worker_id: int, notification: dict):
    """
    Send a notification to a specific worker via WebSocket
    """
    try:
        if worker_id not in active_connections:
            logger.warning(f"No active connections for worker {worker_id}")
            raise HTTPException(status_code=404, detail=f"No active connections for worker {worker_id}")
        
        message = json.dumps(notification)
        sent_count = 0
        
        for ws in active_connections[worker_id]:
            try:
                await ws.send_text(message)
                sent_count += 1
                logger.info(f"Notification sent to worker {worker_id}: {notification.get('title', 'Unknown')}")
            except Exception as e:
                logger.error(f"Failed to send notification to worker {worker_id}: {e}")
        
        return {
            "success": True,
            "message": f"Notification sent to {sent_count} connection(s) for worker {worker_id}",
            "notification": notification
        }
        
    except Exception as e:
        logger.error(f"Error sending notification to worker {worker_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

# Utility function to send a notification to a worker (for internal use)
async def send_notification_to_worker_internal(worker_id: int, message: str):
    if worker_id in active_connections:
        for ws in active_connections[worker_id]:
            try:
                await ws.send_text(message)
                logger.info(f"Internal notification sent to worker {worker_id}")
            except Exception as e:
                logger.error(f"Failed to send internal notification to worker {worker_id}: {e}")

# Get active connections info
@router.get("/active-connections")
async def get_active_connections():
    """
    Get information about active WebSocket connections
    """
    return {
        "active_workers": list(active_connections.keys()),
        "total_connections": sum(len(connections) for connections in active_connections.values()),
        "connections_per_worker": {str(worker_id): len(connections) for worker_id, connections in active_connections.items()}
    } 