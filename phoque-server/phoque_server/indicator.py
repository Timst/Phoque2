'''File to manage the APA102C status indicator board'''

from enum import Enum

from qwiic_led_stick import QwiicLEDStick

class Status(Enum):
    READY = 1
    LOADING = 2
    ERROR = 3

class Device(Enum):
    SERVER = 1
    BACKOFFICE = 2
    DISPLAY = 3
    BUTTON = 4

class IndicatorBoard:
    READY = (0,255,0)
    LOADING = (255,190,0)
    ERROR = (255,0,0)

    board: QwiicLEDStick
    def __init__(self):
        self.board = QwiicLEDStick()
        self.board.begin()
        self.board.set_all_LED_brightness(100)
        self.board.set_all_LED_color(*self.LOADING)
        self.board.set_single_LED_color(0, *self.READY)

    def switch_indicator(self, device: Device, status: Status):
        self.board.set_single_LED_color(device.value, *(self.ERROR if status == Status.ERROR else self.READY if status == Status.READY else self.LOADING))
