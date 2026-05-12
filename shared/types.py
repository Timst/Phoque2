import datetime
from pydantic import BaseModel
from enum import Enum
from datetime import timedelta

class Status(BaseModel):
    current_number: int
    top_of_line: int
    remaining_time_s: int
    estimated_wait_min: int

class Template(BaseModel):
    event: str
    tagline: str

class Init(BaseModel):
    start_number: int
    template: Template
    current_time: datetime

class CallType(Enum):
    CALL = 1
    REMIND = 2
    SKIP = 3

class OpenState(Enum):
    OPEN = 1
    LAST_CALL = 2
    FINISHING = 3
    CLOSED = 4

    def next(self):
        '''Get following state'''
        if self.value == 4:
            return OpenState.OPEN
        else:
            return OpenState(self.value + 1)

class TicketState(BaseModel):
    current: int
    top: int
    depth: int
    time_per_crepe: timedelta
    wait: timedelta
    remaining: timedelta
    state: OpenState
