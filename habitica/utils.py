import unicodedata
import os

from win10toast import ToastNotifier

# Path to the resource folder
res_path = os.path.join(os.path.dirname(__file__), 'res')

def emoji2text(s):
	"""converts any existing emoji code into its Github format"""
	buff=''
	for c in s:
		if(unicodedata.category(c) == 'So'):
			buff += (':' + unicodedata.name(c).lower().replace(' ', '_') + ':')
		else:
			buff += c
	return buff

def notify(message):
	toaster = ToastNotifier()
	toaster.show_toast(
		'Habitica API Notification',
		message,
		icon_path=(os.path.join(res_path, 'habitica.ico'))
		)
