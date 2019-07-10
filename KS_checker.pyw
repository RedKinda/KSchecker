from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import install

import os
import sys
import time

fr = False #determines if this is first run on machine
try:
	import unidecode
	name = unidecode.unidecode(sys.argv[1]+ " " + sys.argv[2])
except:
	name = install.first_run()










import win32api
import win32con
import win32gui
import urllib.request
import webbrowser
import unidecode

import unicodedata

seminare_list = []
seminare_adresa = []


# ##################################
# ########## Libraries #############
# ##################################
# standard library
import logging
import threading
from os import path
from pkg_resources import Requirement
from pkg_resources import resource_filename
from time import sleep

# 3rd party modules
from win32api import GetModuleHandle
from win32api import PostQuitMessage
from win32con import CW_USEDEFAULT
from win32con import IDI_APPLICATION
from win32con import IMAGE_ICON
from win32con import LR_DEFAULTSIZE
from win32con import LR_LOADFROMFILE
from win32con import WM_USER
from win32con import WS_OVERLAPPED
from win32con import WS_SYSMENU
from win32gui import CreateWindow
from win32gui import DestroyWindow
from win32gui import LoadIcon
from win32gui import LoadImage
from win32gui import NIF_ICON
from win32gui import NIF_INFO
from win32gui import NIF_MESSAGE
from win32gui import NIF_TIP
from win32gui import NIM_ADD
from win32gui import NIM_DELETE
from win32gui import NIM_MODIFY
from win32gui import RegisterClass
from win32gui import UnregisterClass
from win32gui import Shell_NotifyIcon
from win32gui import UpdateWindow
from win32gui import WNDCLASS
from win32gui import PumpMessages

# Magic constants
PARAM_DESTROY = 1028
PARAM_CLICKED = 1029

# ##################################
# ########### Classes ##############
# ##################################
class ToastNotifier(object):
	"""Create a Windows 10  toast notification.

	from: https://github.com/jithurjacob/Windows-10-Toast-Notifications
	"""

	def __init__(self):
		"""Initialize."""
		self._thread = None

	@staticmethod
	def _decorator(func, callback=None):
		"""

		:param func: callable to decorate
		:param callback: callable to run on mouse click within notification window
		:return: callable
		"""
		def inner(*args, **kwargs):
			kwargs.update({'callback': callback})
			func(*args, **kwargs)
		return inner

	def _show_toast(self, title, msg,
					icon_path, duration,
					callback_on_click):
		"""Notification settings.

		:title: notification title
		:msg: notification message
		:icon_path: path to the .ico file to custom notification
		:duration: delay in seconds before notification self-destruction
		"""

		# Register the window class.
		self.wc = WNDCLASS()
		self.hinst = self.wc.hInstance = GetModuleHandle(None)
		self.wc.lpszClassName = str("PythonTaskbar")  # must be a string
		self.wc.lpfnWndProc = self._decorator(self.wnd_proc, callback_on_click)  # could instead specify simple mapping
		#try:
		self.classAtom = RegisterClass(self.wc)
		#except (TypeError, Exception):
		#	pass  # not sure of this
		style = WS_OVERLAPPED | WS_SYSMENU
		self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
								 0, 0, CW_USEDEFAULT,
								 CW_USEDEFAULT,
								 0, 0, self.hinst, None)
		UpdateWindow(self.hwnd)

		# icon
		if icon_path is not None:
			icon_path = path.realpath(icon_path)
		else:
			icon_path = resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
		icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
		try:
			hicon = LoadImage(self.hinst, icon_path,
							  IMAGE_ICON, 0, 0, icon_flags)
		except Exception as e:
			logging.error("Some trouble with the icon ({}): {}"
						  .format(icon_path, e))
			hicon = LoadIcon(0, IDI_APPLICATION)

		# Taskbar icon
		flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
		nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Tooltip")
		Shell_NotifyIcon(NIM_ADD, nid)
		Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
									  WM_USER + 20,
									  hicon, "Balloon Tooltip", msg, 200,
									  title))
		PumpMessages()
		# take a rest then destroy
		sleep(duration)
		DestroyWindow(self.hwnd)
		UnregisterClass(self.wc.lpszClassName, None)
		return None

	def show_toast(self, title="Notification", msg="Here comes the message",
					icon_path=None, duration=5, threaded=False, callback_on_click=None):
		"""Notification settings.

		:title: notification title
		:msg: notification message
		:icon_path: path to the .ico file to custom notification
		:duration: delay in seconds before notification self-destruction
		"""
		if not threaded:
			self._show_toast(title, msg, icon_path, duration, callback_on_click)
		else:
			if self.notification_active():
				# We have an active notification, let is finish so we don't spam them
				return False

			self._thread = threading.Thread(target=self._show_toast, args=(
				title, msg, icon_path, duration, callback_on_click
			))
			self._thread.start()
		return True

	def notification_active(self):
		"""See if we have an active notification showing"""
		if self._thread != None and self._thread.is_alive():
			# We have an active notification, let is finish we don't spam them
			return True
		return False

	def wnd_proc(self, hwnd, msg, wparam, lparam, **kwargs):
		"""Messages handler method"""
		if lparam == PARAM_CLICKED:
			# callback goes here
			if kwargs.get('callback'):
				kwargs.pop('callback')()
			self.on_destroy(hwnd, msg, wparam, lparam)
		elif lparam == PARAM_DESTROY:
			self.on_destroy(hwnd, msg, wparam, lparam)

	def on_destroy(self, hwnd, msg, wparam, lparam):
		"""Clean after notification ended."""
		nid = (self.hwnd, 0)
		Shell_NotifyIcon(NIM_DELETE, nid)
		PostQuitMessage(0)

		return None



#initializing list of seminars, should change later to nicer version
seminare_list.append("kms")
seminare_list.append("ksp")
seminare_list.append("fks")
seminare_list.append("sezam")
seminare_list.append("sezamko")
seminare_adresa.append("https://kms.sk/vysledky/")
seminare_adresa.append("https://ksp.sk/vysledky/")
seminare_adresa.append("https://fks.sk/vysledky/")
seminare_adresa.append("http://primerane.sk/sezam/poradie_sezam.php")
seminare_adresa.append("http://primerane.sk/sezam/poradie_sezamko.php")



#called when notification is clicked
def naklik():
	print("OPENING")
	time.sleep(2)
	win32api.SendMessage(mozilla, win32con.WM_ACTIVATE)
	win32gui.BringWindowToTop(mozilla)
	webbrowser.open_new_tab(seminare_adresa[y])







for y in range (0, len(seminare_list)):
	#stiahne vysledkovku
	response = urllib.request.urlopen(seminare_adresa[y])
	html = str(response.read().decode("utf-8"))
	#da do prec diakritiku
	try:
		html = unicode(html, 'utf-8')
	except (TypeError, NameError): # unicode is a default on python 3 
		pass
	html = unicodedata.normalize('NFD', html)
	html = html.encode('ascii', 'ignore')
	html = str(html.decode("utf-8"))
	
	#check na zmenu
	seminar = seminare_list[y]

	posledne_body=""
	progress = 0
	pocet_uloh_seminaru = 15
	if(seminar=="sezam" or seminar=="sezamko"):
		pocet_uloh_seminaru=8
			
	#opens last state
	if os.path.exists(name + seminar + ".txt"):
#	subor=open(name + seminar + ".txt", "a")
#	subor.close()
		subor=open(name + seminar + ".txt", "r")
		posledne_body=subor.read()
	for x in range (0, pocet_uloh_seminaru-len(posledne_body)):
		posledne_body=posledne_body + "?"

	subor=open(name + seminar + ".txt", "w")

	#searches for name
	for x in range (0, len(html)-1):
		if html[x]==name[progress]:
			progress+=1
		else:
			progress=0
		if progress==len(name):
			#name found
			print("nasiel v " + seminar)
			zaciatok_mena = x
			progress=0
			cislo_ulohy = 0
			body_v_ulohach = []

			dur = 5
			notif =True
			while cislo_ulohy < pocet_uloh_seminaru:
				#searches for numbers, '?' and '.'
				if str.isdigit(html[x]) or html[x]=='?' or html[x]=='.':
					body_v_ulohach.append(html[x])
					if body_v_ulohach[cislo_ulohy]!=(posledne_body[cislo_ulohy]):
						#throws notification on windows
						oznamenie=ToastNotifier()
						#gets window handler for mozilla, used in pushing to top
						mozilla = win32gui.FindWindowEx(0, 0, "MozillaWindowClass", None)
						if notif:
							oznamenie.show_toast("Seminare checker", "Nove body v seminari " + seminare_list[y], duration=dur, threaded=False, callback_on_click = naklik)
							notif = False
					cislo_ulohy+=1

					subor.write(html[x])
				x+=1
			break
	subor.close()
