#HabitTracker
#Tracking tool for use with Habitica http://habitica.com
#Author: Dorian Daudier <dorian.daudier@gmail.com>
#Version 1.0
#License: GNU GPL v3 <www.gnu.org/licenses/gpl.html>

"""
KeybrTracker (HabitTracker)

Automation tool designed to track user activities and score habitica tasks.
The current tool track touch typing training time with Keybr website.
"""

from .habitica.api import HabiticaApi
from .tracker.keybr_tracker import KeybrTracker

# Task ID for keybr tracking
task_id = ''

ha = HabiticaApi()
print("\nKEYBR TRACKER:")
if not task_id:
    print("Please enter the ID of the task you would like to score with " \
          "Keybr tracker.\nIf you don't want to enter it every time, you can " \
          "edit the __main__.py file.")
    task_id =  input("Task ID: ")
kt = KeybrTracker(task_id, ha)
print("Starting training...")
kt.start()

input("Keybr tracking ended.\nPress Enter to exit...")
