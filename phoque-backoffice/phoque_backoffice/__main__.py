import asyncio
from time import sleep
import requests
from signal import pause

from radio import Radio
from browser import Browser
from input import Input

SERVER_URL = "http://192.168.1.1:8000"

async def emit_heartbeat():
    while True:
        requests.get(SERVER_URL + "/heartbeat/", timeout=3)

        await asyncio.sleep(5)

def main():
    """Run the Phoque backoffice client."""
    asyncio.create_task(emit_heartbeat())

    radio = Radio(SERVER_URL)
    radio.listen()

    input_handler = Input(SERVER_URL)
    input_handler.start()

    # Wait for system to finish initializing
    sleep(10)

    browser = Browser()
    browser.launch_browser_windows()

    pause()

if __name__ == "__main__":
    main()