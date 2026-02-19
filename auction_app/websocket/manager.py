from fastapi import WebSocket
from typing import Dict, List
from uuid import UUID


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, lot_id: UUID):
        await websocket.accept()
        if lot_id not in self.active_connections:
            self.active_connections[lot_id] = []
        self.active_connections[lot_id].append(websocket)

    def disconnect(self, websocket: WebSocket, lot_id: UUID):
        if lot_id in self.active_connections:
            self.active_connections[lot_id].remove(websocket)
            if not self.active_connections[lot_id]:
                del self.active_connections[lot_id]

    async def broadcast(self, lot_id: UUID, message: dict):
        if lot_id in self.active_connections:
            for connection in self.active_connections[lot_id]:
                await connection.send_json(message)


manager = ConnectionManager()

