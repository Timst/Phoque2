'''Play audio announcement of numbers'''
import logging
from time import sleep

from playsound3 import playsound
from pyttsx3 import Engine, init as tts_init
from pyttsx3.voice import Voice
from phoque_shared.types import CallType

class Sound:
    engine: Engine
    english: Voice
    french: Voice

    def __init__(self):
        self.engine = tts_init()
        self.engine.setProperty('rate', 130)
        voices = self.engine.getProperty('voices')
        self.english = next(filter(lambda x: x.name == "english-us", voices))
        self.french = next(filter(lambda x: x.name == "french", voices))

    def call(self, number: int, call_type: CallType):
        '''Make a voice announcement (if calling or reminding) and update called ticket (if calling or skipping)'''

        if number is not None and call_type != CallType.SKIP:
            logging.info(f"{'Calling' if call_type == CallType.CALL else 'Pinging'} ticket {number}")

            playsound("assets/sounds/jingle.wav")

            sleep(0.3)

            self.engine.setProperty('voice', self.english.id)
            self.engine.say(f"Number {number}")
            self.engine.runAndWait()

            sleep(0.3)

            self.engine.setProperty('voice', self.french.id)
            self.engine.say(f"Numéro {number}")
            self.engine.runAndWait()