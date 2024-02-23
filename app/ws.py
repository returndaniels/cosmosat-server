from fastapi import WebSocket
from singleton import Singleton


class ConnectionManager(Singleton):
    """Gerencia conexões WebSocket ativas, permitindo transmissão de mensagens.

    Atributos:
        active_connections (list[WebSocket]): Lista de conexões WebSocket ativas.
    """

    def __init__(self):
        """Inicializa o gerenciador de conexões."""
        self.active_connections: list[WebSocket] = []

    @classmethod
    def instance(cls):
        """Retorna a instância singleton do gerenciador de conexões."""
        return cls()

    async def connect(self, websocket: WebSocket):
        """Aceita uma nova conexão WebSocket e a adiciona à lista de conexões ativas.

        Args:
            websocket (WebSocket): Conexão WebSocket a ser aceita.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove uma conexão WebSocket da lista de conexões ativas.

        Args:
            websocket (WebSocket): Conexão WebSocket a ser removida.
        """
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        """Envia uma mensagem JSON para todas as conexões WebSocket ativas.

        Args:
            message: Mensagem a ser enviada.
        """
        for connection in self.active_connections:
            await connection.send_json(message)
