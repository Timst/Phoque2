"""Phoque display entry point."""

import asyncio
import websockets
import json
from phoque_display.sound import Sound

SERVER_URL = "ws://192.168.1.1:8000/display"

sound = Sound()

async def display_handler():
    """Handle display updates from server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                # TODO: Update LED matrix display with data
                print(f"Display update: {data}")
    except Exception as e:
        print(f"Display connection error: {e}")

def main():
    """Run the Phoque display client."""
    asyncio.run(display_handler())

if __name__ == "__main__":
    main()