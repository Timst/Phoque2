'''Compute values for the Admin panel'''

import logging
from datetime import datetime, date, time

from cachetools import cached, TTLCache

from data import Database
from shared.types import CallType, OpenState, TicketState

class Admin:
    database: Database
    end_of_shift = datetime.combine(date.today(), time(23, 00, 00))

    resetting: bool
    switching: bool

    stats: TicketState
    state: OpenState

    def __init__(self, database: Database):
        self.database = database

        self.resetting = False
        self.switching = False
        self.state = OpenState.OPEN

    @cached(cache=TTLCache(maxsize=1024, ttl=1))
    def get_stats(self) -> TicketState:
        '''Return various data on the state of the queue'''
        current = self.database.get_latest_called_ticket()
        top = self.database.get_latest_ticket_number()

        if current is None:
            current = 0

        depth = top - current

        samples = self.database.get_called_tickets_sample()

        time_per_crepe = None
        wait = None

        if samples is not None:
            earliest_ticket = samples[len(samples) - 1]
            latest_ticket = samples[0]

            total_time = latest_ticket.TIMESTAMP_CALLED - earliest_ticket.TIMESTAMP_CALLED
            time_per_crepe = total_time / len(samples)
            wait = time_per_crepe * depth

        return TicketState(
            current = current,
            top = top,
            depth = depth,
            time_per_crepe = time_per_crepe,
            wait = wait,
            remaining = self.end_of_shift - datetime.now(),
            state = self.state)

    def add(self):
        '''Add a ticket to the queue (if open)'''
        top = self.database.get_latest_ticket_number()

        if self.state in (OpenState.OPEN, OpenState.LAST_CALL):
            new_number = top + 1
            self.database.insert(new_number)
            return new_number
        else:
            logging.warning(f"Can't add ticket, system is in {self.state.name()} state")
            return None

    def call(self, call_type: CallType):
        '''Make a voice announcement (if calling or reminding) and update called ticket (if calling or skipping)'''

        if self.state != OpenState.CLOSED:
            if call_type == CallType.REMIND:
                self.database.get_latest_called_ticket()
            else:
                self.database.call()

    def set_switching(self, switch):
        '''Indicate that we're mid switching states'''
        self.switching = switch

    def set_resetting(self, reset):
        '''Indicate that we're mid-reset'''
        self.resetting = reset

    def reset(self):
        '''Switch to a new session'''
        logging.info("Resetting the counts")
        self.database.reset()

    def switch(self):
        '''Switch to the next mode'''
        next_state = self.state.next()

        logging.info(f"Switching from {self.state.name} to {next_state.name}")

        self.state = next_state