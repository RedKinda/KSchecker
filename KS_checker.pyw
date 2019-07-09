import urllib.request
#from win10toast import ToastNotifier
import win_notif
import os
import sys
import time
import webbrowser
#import ahk
import win32gui
import win32api
import win32con
import unidecode
import unicodedata
import xml.etree.ElementTree as ET
seminare_list = []
seminare_adresa = []


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

from ahk import AHK
ahk = AHK(executable_path = "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe")



def naklik():
	#global y
	#global seminare_adresa
	print("OPENING")
	time.sleep(2)
	#mozilla.disable()
	#mozilla.to_top()
	#mozilla.activate()
	win32api.SendMessage(mozilla, win32con.WM_ACTIVATE)
	win32gui.BringWindowToTop(mozilla)
	#win32gui.SetForegroundWindow(mozilla) 
	webbrowser.open_new_tab(seminare_adresa[y])

def first_run():
	fr = True
	try:
		os.mkdir('data')
	except:
		pass

	name = input("Dobre rano, prve spustenie. Zadajte svoje meno ako je vo vysledkovkach pls (bez diakritiky): ")
	#xmlko = open("KSchecker.xml", "r").read()
	#ako_text = ET.fromstring(xmlko)
	fajl =  ET.parse("format.xml")
	koren = fajl.getroot()
	#print(xmlko)
	elm = koren.find(".//Command")
	elm.text = sys.executable[:-4]+"w"+ sys.executable[-4:]
	print("executable:", elm.text)
	elm = koren.find(".//Arguments")
	elm.text = os.path.abspath(os.path.dirname(__file__)) + "\\KS_checker.pyw" + " " + name
	print("arguments:", elm.text)
	elm = koren.find(".//WorkingDirectory")
	elm.text = os.path.abspath(os.path.dirname(__file__)) + "\\data"
	print("WD:", elm.text)

	
	koren.set("version", "1.2")
	koren.set("xmlns", "http://schemas.microsoft.com/windows/2004/02/mit/task")


	fajl.write("scheduler_import.xml", xml_declaration = True, encoding = "utf-16")
	#tostr = ET.tostring(koren, "utf-8")
	print("running command...")
	os.system('schtasks /create /xml "' + os.path.abspath(os.path.dirname(__file__)) + '\\scheduler_import.xml" /tn "KSchecker for ' + name + '"')
	print("...end of command")


	os.chdir("data")
	return name


fr = False #determines if this is first run on machine
try:
	name = unidecode.unidecode(sys.argv[1]+ " " + sys.argv[2])
except:
	name = first_run()




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
	pocet_uloh_seminaru = 15;
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
						oznamenie=win_notif.ToastNotifier()
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