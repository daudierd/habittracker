import os
import json
import logging
import time
import threading

class Tracker(threading.Thread):
    """Generic class that defines the methods for tracking user activity and
    record it to Habitica."""
    def __init__(self, name, task_id, habitica_api):
        threading.Thread.__init__(self)
        self.habitica_api = habitica_api
        self.task_id = task_id
        self.name = name

    def run(self):
        """Main function that regularily checks the conditions required to
        trigger a task update"""
        pass

    def task_update(self):
        """Triggers a task update throuh the Habitica API"""
        pass
