import os
import json
import logging
import time

from .tracker import Tracker
from ..keybr.api import KeybrApi
from ..keybr.common.exceptions import TimeoutException

# converts a 'hh:mm:ss' string into an int representing the number of seconds
def _str2seconds(string):
    time = string.split(':')
    return (int(time[0]) * 60 + int(time[1])) * 60 + int(time[2])

class KeybrTracker(Tracker):
    """
    Class implementing a method to regularily check keybr training time using
    Keybr API and trigger a task update with Habitica API.

    Arguments:
        task_id: ID of the Habitica task that is updated by the tracker
        habitica_api: A reference to the Habitica API
        keybr_api : A reference to the Keybr API
    """
    def __init__(self, task_id, habitica_api, keybr_api):
        super().__init__(task_id, habitica_api)
        self.keybr_api = keybr_api
        # Set a training deadline triggering task update
        deadline = input("Please indicate a training time in hh:mm:ss format: ")
        self.deadline = _str2seconds(deadline)
        logging.info("Keybr tracker successfully loaded")

    def sync(self):
        """Synchronize the data stored in the program with data online.
        The time until next sync is updated in 'wait_time' attribute"""
        updated = False
        timeout = 10
        while not updated:
            try:
                self.indicators = self.keybr_api.get_indicators(timeout=timeout)
                updated = True
            except TimeoutException as e:
                logging.warning(e)
                timeout = min(timeout * 2, 60)
                continue

    def condition(self):
        """Returns 'True' when a certain condition is met (deadline reached).
        This is used as a trigger to score a task"""
        cond = _str2seconds(self.indicators['today']['time']) >= self.deadline
        return (cond)

    def start(self):
        """Regularily syncs and triggers task score when condition is reached"""
        # indicators and remaining time initialized to avoid unnecessary loops
        logging.info("Tracking started")
        self.sync()
        while not self.condition():
            t = self.deadline - _str2seconds(self.indicators['today']['time'])
            logging.info("Keybr tracker: " + str(t) + " sec remaining...")
            time.sleep(t)
            self.sync()
        self.task_update()

    def task_update(self):
        self.habitica_api.score(
            self.task_id,
            'Your have reached your target training time for today')
