from fastapi import WebSocket

from singleton import Singleton


class ConnectionManager(Singleton):
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    @classmethod
    def instance(cls):
        return cls()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_json(message)
