from gpiozero import Button
import requests

class Radio:
    GPIO_PIN = 18
    server_url: str
    call_button: Button

    def __init__(self, url: str):
        self.call_button = Button(self.GPIO_PIN, pull_up=True, bounce_time=0.1)
        self.server_url = url

    def listen(self):
        self.call_button.when_pressed = self.call_next_number

    def call_next_number(self):
        try:
            response = requests.get(self.server_url + "/serve", timeout=3)

            if response.status_code == 200:
                print(f"Success: Called ticket {response.text}")
            else:
                print(f"Server error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")