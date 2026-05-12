from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from cachetools import cached, TTLCache

from data import Database
from shared.types import Init, OpenState, Template, TicketState

from datetime import datetime

app = FastAPI()
data = Database()
state = OpenState.OPEN

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
    new_number = data.get_latest_ticket_number() + 1
    data.insert(new_number)
    return new_number

@app.post("/serve")
def serve():
    return data.call()

@app.websocket("/display")
async def display(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json(data.get_latest_ticket_number())
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@cached(cache=TTLCache(maxsize=1024, ttl=1))
def get_stats(self):
    '''Return various data on the state of the queue'''
    current = data.get_latest_called_ticket()
    top = data.get_latest_ticket_number()

    if current is None:
        current = 0

    depth = top - current

    samples = data.get_called_tickets_sample()

    time_per_crepe = None
    wait = None

    if samples is not None:
        earliest_ticket = samples[len(samples) - 1]
        latest_ticket = samples[0]

        total_time = latest_ticket.TIMESTAMP_CALLED - earliest_ticket.TIMESTAMP_CALLED
        time_per_crepe = total_time / len(samples)
        wait = time_per_crepe * depth

    return TicketState(
        current = current,
        top = top,
        depth = depth,
        time_per_crepe = time_per_crepe,
        wait = wait,
        remaining = self.end_of_shift - datetime.now(),
        state = state)