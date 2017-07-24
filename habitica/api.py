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
        """Initialize the API configuration"""
        self.authHeaders = {'x-api-user' : '', 'x-api-key' : ''}
        #Load configuration from file. If failure, create a new configuration
        if os.path.exists(config_file):
            self.autologin()

    def login(self, user, key, auto_login=False):
        """Creates authentification headers 'authHeaders' used in the API."""
        if auto_login:
            try:
                with open(config_file, 'w') as f:
                    f.write(json.dumps({'user' : user, 'key' : key}))
            except:
                logging.error("Configuration file could not be created.")
        self.authHeaders['x-api-user'] = user
        self.authHeaders['x-api-key'] = key
        logging.info("User successfully logged in.")

    def autologin(self):
        """Logs a user in Habitica API using the configuration file
        (created when the user specified to be logged in automatically)."""
        try:
            with open(config_file, 'r') as f:
                data = json.loads(f.read())
                self.login(data['user'], data['key'])
        except:
            raise LoginException("Login failed! Try login with a password")

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
