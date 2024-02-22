from fastapi import WebSocket

clientes = set()


async def on_connect(websocket: WebSocket):
    await websocket.accept()
    clientes.add(websocket)


async def on_message(websocket: WebSocket, data: str):
    # Ignorar mensagens do cliente
    pass


async def on_disconnect(websocket: WebSocket, close_code: int):
    clientes.remove(websocket)


async def broadcast_raio(raio):
    for cliente in clientes:
        await cliente.send(raio.json())
