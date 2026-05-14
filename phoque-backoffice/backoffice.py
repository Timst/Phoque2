import asyncio

import requests
from gpiozero import Button
from signal import pause

SERVER_URL = "http://192.168.1.1:8000"
GPIO_PIN = 18

call_button = Button(GPIO_PIN, pull_up=True, bounce_time=0.1)

async def emit_heartbeat():
    while True:
        requests.get(SERVER_URL + "/heartbeat/", timeout=3)

        await asyncio.sleep(5)

def call_next_number():
    try:
        response = requests.get(SERVER_URL + "/serve", timeout=3)

        if response.status_code == 200:
            print(f"Success: Called ticket {response.text}")
        else:
            print(f"Server error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

call_button.when_pressed = call_next_number

emit_heartbeat()

pause()