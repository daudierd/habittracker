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

from .habitica.api import HabiticaApi
from .keybr.api import KeybrApi
from .tracker.keybr_tracker import KeybrTracker

# Please configure the following values before running the script
task_id = ''
habitica_user = ''
habitica_key = ''
keybr_key = ''

ha = HabiticaApi()
ha.login(habitica_user, habitica_key)

print("\nKEYBR TRACKER:")
if not task_id:
    print("Please enter the ID of the task you would like to score with " \
          "Keybr tracker.\nIf you don't want to enter it every time, you can " \
          "edit the __main__.py file.")
    task_id =  input("Task ID: ")

keybr_api = KeybrApi()
keybr_api.login(keybr_key)
kt = KeybrTracker(task_id, ha, keybr_api=keybr_api)

print("Starting training...")
kt.start()

input("Keybr tracking ended.\nPress Enter to exit...")
