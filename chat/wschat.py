from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from producer import publish

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.active_by_id = dict()

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.active_by_id[client_id] = websocket

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, str(client_id))
    try:
        while True:
            data = await websocket.receive_json()
            await publish(data)
            if data['receiver']:
                await manager.send_personal_message(f"You wrote to {data['receiver']}: {data['msg']}", websocket)
                await manager.send_personal_message(f"Client #{client_id} says: {data['msg']}",
                                                    manager.active_by_id[data['receiver']])
            else:
                await manager.broadcast(f"Client #{client_id} says: {data['msg']}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
