'''Handles the GPIO button logic'''

import logging
import time
import requests

from gpiozero import Button as GpioButton

from .composer import Composer

SERVER_URL = "http://192.168.1.1:8000/queue"

class Button:
    composer: Composer

    button: GpioButton

    last_press_timestamp: float

    def __init__(self, composer: Composer):
        self.composer = composer
        self.button = GpioButton(23)
        self.last_press_timestamp = None

    def listen(self):
        '''Listen for button taps'''
        self.button.when_released = self.snap

    def snap(self):
        '''Handle button taps'''
        logging.debug("Snap")

        logging.debug(f"Last timestamp: {self.last_press_timestamp}, " +
                      f"current time: {time.time()}, " +
                      f"diff: {'' if self.last_press_timestamp is None else time.time() - self.last_press_timestamp}")

        if self.last_press_timestamp is not None and time.time() - self.last_press_timestamp < 1:
            logging.warning("Throttling call.")
        else:
            new_ticket =  self.queue()

            if new_ticket is not None:
                self.composer.make_ticket(new_ticket)

        self.last_press_timestamp = time.time()

    def queue(self) -> int | None:
        try:
            response = requests.get(SERVER_URL, timeout=3)

            if response.status_code == 200:
                number = int(response.text())
                print(f"Success: Enqueued ticket {number}")
                return number
            else:
                print(f"Server error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")

        return None