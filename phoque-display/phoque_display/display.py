from datetime import timedelta
import json

from humanfriendly import format_timespan
import websockets
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from phoque_shared.types import TicketState

class Display:
    canvas: graphics.Canvas
    matrix: RGBMatrix
    white = graphics.Color(255, 255, 255)

    server_uri = "ws://localhost:8000/display"

    def __init__(self):
        options = RGBMatrixOptions()
        options.hardware_mapping = 'adafruit-hat'
        options.drop_privileges = False

        options.rows = 16
        options.cols = 32
        options.chain_length = 4
        options.parallel = 1
        options.multiplexing = 11
        options.pixel_mapper_config = "U-mapper"
        options.gpio_slowdown = 3
        options.pwm_bits = 1
        options.pwm_lsb_nanoseconds = 1000

        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()


    def render(self, number: int, wait_time: timedelta):
        self.canvas.Clear()

        font_large = graphics.Font()
        font_large.LoadFont("fonts/texgyre-27.bdf")
        graphics.DrawText(self.canvas, font_large, 8, 22, self.white, str(number))

        wait_time_formatted = format_timespan(wait_time, detailed=False, max_units=1)
        font_small = graphics.Font()
        font_small.LoadFont("fonts/5x8.bdf")
        graphics.DrawText(self.canvas, font_small, 3, 30, self.white, f"Wait: {wait_time_formatted}")

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    async def display_server_data(self):
        try:
            async with websockets.connect(self.server_uri) as websocket:
                print(f"Connected to {self.server_uri}")

                async for message in websocket:
                    try:
                        data: TicketState = json.loads(message)
                        print(f"Received data: {data}")
                        await self.render(data.current, timedelta(seconds=data.wait))
                    except json.JSONDecodeError:
                        print("Invalid JSON received from server")
        except Exception as e:
            print(f"Websocket connection error: {e}")