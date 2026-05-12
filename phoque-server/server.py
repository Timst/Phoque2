from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from data import Database
from admin import Admin
from shared.types import CallType, Init, OpenState, Template

from datetime import datetime

app = FastAPI()
data = Database()
state = OpenState.OPEN
admin = Admin(data)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.get("/init")
def init() -> Init:
    current_number = data.get_latest_ticket_number()
    return Init(
        current_number = current_number,
        template = Template(
            event = "",
            tagline= ""),
        current_time= datetime.now)

@app.post("/queue")
def queue() -> int:
    return admin.add()

@app.post("/serve")
def serve():
    return admin.call(CallType.CALL)

@app.websocket("/display")
async def display(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json(admin.get_stats())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)