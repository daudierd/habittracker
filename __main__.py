#HabitTracker
#Tracking tool for use with Habitica http://habitica.com
#Author: Dorian Daudier <ddaudier@outlook.com>
#Version 1.0
#License: GNU GPL v3 <www.gnu.org/licenses/gpl.html>

"""
KeybrTracker (HabitTracker)

Automation tool designed to track user activities and score habitica tasks.
The current tool track touch typing training time with Keybr website.
"""

import argparse

from .habitica.api import HabiticaApi
from .keybr.api import KeybrApi
from .tracker.keybr_tracker import KeybrTracker

# Create parser for command-line arguments
parser = argparse.ArgumentParser(
    description='Score Keybr typing sessions on Habitica.')

# Use 2 positional arguments for standard program run
parser.add_argument('taskID', metavar='TID', nargs='?',
                    help="task ID associated with the Keybr Tracker")
parser.add_argument('time', metavar='T', type=int, nargs='?',
                    help="training session time (in minutes)")

# Configuration flag can be specified.
# In this case, 3 arguments are expected.
parser.add_argument('-c', '--configure', action='store_true',
                    help="configure the program")
parser.add_argument('ha_user', nargs='?',
                    help="Habitica user ID.")
parser.add_argument('ha_key', nargs='?',
                    help="Habitica API key.")
parser.add_argument('keybr', nargs='?',
                    help="Keybr login key.")

habitica_api = HabiticaApi()
keybr_api = KeybrApi()
args = parser.parse_args()

if args.configure:
    habitica_api.login(args.ha_user, args.ha_key, auto_login=True)
    keybr_api.login(args.keybr, auto_login=True)
    print("KeybrTracker successfully configured")
else:
    # We assume the program is already configured
    kt = KeybrTracker(args.taskID, args.time, habitica_api, keybr_api)
    print("Starting training for " + str(args.time) + " minutes...")
    kt.start()
    print("Keybr training ended.")

input("Press Enter to exit...")
