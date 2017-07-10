import os
import json
import logging
import time

class Tracker():
    """Generic class that defines the methods for tracking user activity and
    record it to Habitica."""
    def __init__(self, task_id, habitica_api):
        self.habitica_api = habitica_api
        self.task_id = task_id

    def start(self):
        """Main function that regularily checks the conditions required to
        trigger a task update"""
        pass

    def task_update(self):
        """Triggers a task update throuh the Habitica API"""
        pass
