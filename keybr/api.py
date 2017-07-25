import os
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .common.exceptions import LoginException
from .common.exceptions import TimeoutException as KeybrTimeoutException

root_dir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
phantomjs_path = os.path.join(
                    os.path.join(root_dir, 'browser'),
                    'phantomjs.exe')
# load the configuration file
keybr_login = os.path.join(os.path.dirname(__file__), 'keybr.conf')

class KeybrApi():
    """Class providing methods for logging in & fetching typing data on Keybr"""
    browser = webdriver.PhantomJS(executable_path=phantomjs_path)

    def __init__(self):
        self.indicators = None
        # If a file exists for auto-login, log the user in
        if os.path.exists(keybr_login):
            self.autologin()

    def login(self, key, auto_login=False):
        """Logs a user in keybr with the key provided in the sign-in link."""
        if auto_login:
            try:
                with open(keybr_login, 'w') as f:
                    f.write(json.dumps({'key' : key}))
            except:
                logging.error("Configuration file could not be created.")
        loginURL = 'https://www.keybr.com/login/' + key
        self.browser.get(loginURL)
        logging.info("User is logged in." )

    def autologin(self):
        """Logs a user in keybr using the configuration file
        (created when the user specified to be logged in automatically)."""
        try:
            with open(keybr_login, 'r') as f:
                data = json.loads(f.read())
                self.login(data['key'])
        except:
            raise LoginException("Login failed! Try login with a password")

    def get_indicators(self, timeout=10):
        """
        Loads and returns a dictionary containting the data of the indicators
        displayed on the website's 'profile' page. If the function fails, the
        old indicators values are retained.

        Arguments:
            timeout (optional): timeout (in sec) for fetching the indicators.
                If no timeout is specified, the default value of 10sec is used"""
        self.browser.get('https://www.keybr.com/profile/')
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'Indicator-value'))
                )
        except TimeoutException:
            raise(KeybrTimeoutException(
                    "Keybr took too long to reach the database"))
            return self.indicators

        # The indicators are updated only if they can all be found
        ind = self.browser.find_elements_by_class_name('Indicator-value')
        if ind and len(ind) >= 8:
            alltime_ind = {'time': ind[0].text,
                           'samples' : ind[1].text,
                           'top_speed' : ind[2].text,
                           'avg_speed' : ind[3].text}
            today_ind = {'time': ind[4].text,
                         'samples' : ind[5].text,
                         'top_speed' : ind[6].text,
                         'avg_speed' : ind[7].text}
            self.indicators = {'alltime' : alltime_ind, 'today' : today_ind}
        return self.indicators

    def __del__(self):
        self.browser.quit()
