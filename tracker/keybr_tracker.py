import os
import json
import logging
import time
from datetime import datetime

from .tracker import Tracker
from ..keybr.api import KeybrApi
from ..keybr.common.exceptions import TimeoutException

timedate_format = '%Y-%m-%d %H:%M:%S'
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
    def __init__(self, name, task_id, minutes, habitica_api, keybr_api):
        super().__init__(name, task_id, habitica_api)
        self.keybr_api = keybr_api
        # Set a training deadline triggering task update
        self.deadline = minutes * 60
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

    def run(self):
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
        ha = self.habitica_api
        now = datetime.now()
        task_notes = ha.get_task(self.task_id)['notes']
        if task_notes:
            task_notes = json.loads(task_notes)
            if 'last_update' in task_notes:
                # get the last update time and compare it to now
                last_update = task_notes['last_update']
                last_update = datetime.strptime(last_update, timedate_format)
                if (last_update.day == now.day):
                    logging.info("The task was already scored earlier today.")
                    return

        new_notes = json.dumps({
            'last_update': now.strftime('%Y-%m-%d %H:%M:%S'),
            'deadline' : self.deadline})
        ha.update_notes(self.task_id, new_notes)
        ha.score(self.task_id,
            'Your have reached your target training time for today')
