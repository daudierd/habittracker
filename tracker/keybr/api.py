import os
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from .common.exceptions import TimeoutException as KeybrTimeoutException

root_dir = os.path.split(os.path.split(
                os.path.split(os.path.abspath(__file__))[0])[0])[0]
phantomjs_path = os.path.join(
                    os.path.join(root_dir, 'browser'),
                    'phantomjs.exe')
# load the configuration file
config_file = os.path.join(os.path.dirname(__file__), 'keybr.conf')

class KeybrApi():
    """Class providing methods for logging and fetching typing data on Keybr"""
    browser = webdriver.PhantomJS(executable_path=phantomjs_path)
    def __init__(self):
        #Load configuration from file. If failure, create a new configuration
        self.timeout = 10
        self.indicators = None
        if not self.load_config():
            self.configure()

    def configure(self):
        """Creates a new configuration file from user input and loads it"""
        # Request information to create the new configuration file
        key = input("Please enter your login key (last part of sign-in link " \
                    "https://www.keybr.com/login/[key]): ")
        # Load the configuration
        self.login(key)
        # Write the configuration in the corresponding file
        config = {'key' : key}
        try:
            with open(config_file, 'w') as f:
                f.write(json.dumps(config))
        except:
            logging.error("Configuration file could not be created")

    def load_config(self):
        """Retrieves the configuration file in json format.
        If the configuration file cannot be found, 'False' is returned."""
        try:
            with open(config_file, 'r') as f:
                config = f.read()
                config = json.loads(config)
        except:
            logging.warning("Configuration file could't be loaded")

        if 'key' in config:
            self.login(config['key'])
            return True
        return False

    def login(self, key):
        """Logs a user on keybr with the key provided in the sign-in link"""
        loginURL = 'https://www.keybr.com/login/' + key
        self.browser.get(loginURL)

    def get_indicators(self):
        """Loads and returns a dictionary containting the data of the indicators
        displayed on the website's 'profile' page. If the function fails, the
        old indicators values are retained."""
        self.browser.get('https://www.keybr.com/profile/')
        try:
            WebDriverWait(self.browser, self.timeout).until(
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
