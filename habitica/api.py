import os
import json
import logging

import urllib.request
from urllib.error import HTTPError

from .utils import emoji2text   #console doesn't support emoji
from .utils import notify
from .common.exceptions import *

config_file = os.path.join(os.path.dirname(__file__), 'habitica.conf')

class HabiticaApi():
    """Class using some services from habitica API for habit tracking"""
    task_types = {"habits", "dailys", "todos", "rewards", "completedTodos"}

    def __init__(self):
        """Initialize the API configuration and log in the API"""
        self.authHeaders = {'x-api-user' : '', 'x-api-key' : ''}
        #Load configuration from file. If failure, create a new configuration
        if not self.load_config():
            self.configure()

    def configure(self):
        """Creates a new configuration file from user input and loads it"""
        # Request information to create the new configuration file
        user = input("Please enter your user ID: ")
        key = input("Please enter your API key: ")
        # Load the configuration
        self.login(user, key)
        # Write the configuration in the corresponding file
        config = {'user' : user, 'key' : key}
        try:
            with open(config_file, 'w') as f:
                f.write(json.dumps(config))
        except:
            logging.error("Configuration file could't be created")

    def load_config(self):
        """Retrieves the configuration file in json format.
        If the configuration file cannot be found, 'False' is returned."""
        try:
            with open(config_file, 'r') as f:
                config = f.read()
                config = json.loads(config)
        except:
            logging.warning("Configuration file could't be loaded")
            return False

        if ('user' in config) and ('key' in config):
            self.login(config['user'], config['key'])
            return True
        else:
            return False

    def login(self, user, key):
        """Creates authentification headers 'authHeaders' used in the API"""
        self.authHeaders['x-api-user'] = user
        self.authHeaders['x-api-key'] = key

    def score(self, task_id, msg="A task has been scored", direction='up'):
        """Scores a task given its ID for the authenticated user"""
        url = 'https://habitica.com/api/v3/tasks/' + task_id + '/score/' + direction
        q = urllib.request.Request(url, headers=self.authHeaders, method='POST')
        try:
            r = urllib.request.urlopen(q).read()
        except HTTPError as e:
            if e.getcode() == 404:    #NotFound
                #TO DO
                raise(Exception)
            elif e.getcode() == 401:  #NotAuthorized
                raise(LoginException)

        out = json.loads(str(r, 'utf-8'))
        if out['success']: notify(msg)

    def get_tasks(self, task_type=""):
        """Returns an array of tasks with the attributes defined in the API.
        Tasks can optionally be filtered by type"""
        url = 'https://habitica.com/api/v3/tasks/user'
        if task_type:
            url = url + '?type=' + task_type

        q = urllib.request.Request(url, headers=self.authHeaders, method='GET')
        try:
            r = urllib.request.urlopen(q).read()
        except HTTPError as e:
            if e.getcode() == 400:    #BadRequest
                raise(ParameterException(
                        msg="Couldn't retrieve tasks.",
                        expected_params=list(self.task_types)))
            elif e.getcode() == 401:  #NotAuthorized
                raise(LoginException)

        out = json.loads(emoji2text(str(r, 'utf-8')))
        return out['data']
