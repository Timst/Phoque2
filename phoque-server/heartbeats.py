import asyncio
from datetime import datetime, time
from dataclasses import dataclass

from indicator import Device, IndicatorBoard, Status

@dataclass
class Heartbeats:
    backoffice: float | None = None
    display: float | None = None

class HeartbeatManager():
    board: IndicatorBoard

    TIMEOUT_THRESHOLD_S = 10
    heartbeats = Heartbeats()

    def __init__(self, board: IndicatorBoard):
        self.board = board

    async def start(self):
        while True:
            self.board.switch_indicator(Device.BACKOFFICE, self.client_status(self.heartbeats.backoffice))
            self.board.switch_indicator(Device.DISPLAY, self.client_status(self.heartbeats.display))

            await asyncio.sleep(5)

    def update_heartbeat(self, device: Device, last_seen: time):
        match device:
            case Device.BACKOFFICE:
                self.heartbeats.backoffice = last_seen
            case Device.DISPLAY:
                self.heartbeats.display = last_seen

    def client_status(self, last_seen: time) -> Status:
        now = time()

        if now - last_seen > self.TIMEOUT_THRESHOLD_S:
            if now - last_seen > self.TIMEOUT_THRESHOLD_S * 3:
                return Status.ERROR
            else:
                return Status.LOADING
        else:
            return Status.READY