"""Phoque button entry point."""

import asyncio
import logging
from signal import pause

import requests

from camera import Camera
from printer import Printer
from composer import Composer, Mode
from button import PhoqueButton

HEARTBEAT_URL = "http://192.168.1.1:8000/queue"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/phoque_server.log"),
        logging.StreamHandler()
    ]
)

def main():
    with Camera() as camera:
        composer = Composer(camera, Printer(), Mode.TICKET)
        button = PhoqueButton(composer)
        button.listen()

        pause()

async def emit_heartbeat():
    while True:
        requests.get(HEARTBEAT_URL, timeout=3)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.create_task(emit_heartbeat())
    main()