KeybrTracker (HabitTracker)
===========================

KeybrTracker is an automation tool for ![Habitica](https://habitica.com/) that
automatically scores a task when a Keybr user has reached a certain target time.

HabitTracker is the successor of KeybrTracker: A project that aims at providing
a set of tools to monitor various data sources and track for changes to score
Habitica tasks.

#### Who is it intended to?
The current tool is intended to Habitica users that train touch typing with Keybr.
Notifications to the user are triggered in Windows 10.

Requirements
------------

Please install Python 3 or higher and download the packages included in
*requirements.txt* before running the script. It is required to download and
place *phantomjs.exe* in the browser menu in order to run KeybrTracker

Future improvements
-------------------

Here are some of the improvements that will be included in future versions:
* Store an history of the past task scores to avoid scoring tasks several times
when the user quits the tool and runs it again
* Enable multithreading to enable parallel tracking activities
* Provide the possibility for a user to choose whether to store credentials or not
* Secure the credentials stored in configuration files
* Add notifications support for other platforms
