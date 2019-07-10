def first_run():

	import sys
	import os
	import xml.etree.ElementTree as ET
	import unidecode
	import unicodedata
	
	
	os.system("wmic useraccount where name='%username%' get sid > sid.txt")
	sid = open("sid.txt", "rb").read().decode("utf-16")[4:]
	sid = sid[:-1]
	
	try:
		import win32gui
		import win32api
		import win32con
		import webbrowser
		import unidecode
	except:
		input("hej, chybaju ti moduly. Mozem ich instalovat? Ak ano, stlac enter, ak nie, zavri program a nebudes ho mat proste")
		os.system("pip install webbrowser")
		os.system("pip install unidecode")
		os.system("pip install pywin32")

		os.execl(sys.executable, 'python', __file__, *sys.argv[1:])

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

	elm = koren.find(".//UserId")
	elm.text = sid
	print("UserID:", elm.text)
	
	koren.set("version", "1.2")
	koren.set("xmlns", "http://schemas.microsoft.com/windows/2004/02/mit/task")


	fajl.write("scheduler_import.xml", xml_declaration = True, encoding = "utf-16")
	#tostr = ET.tostring(koren, "utf-8")
	print("running command...")
	os.system('schtasks /create /xml "' + os.path.abspath(os.path.dirname(__file__)) + '\\scheduler_import.xml" /tn "KSchecker for ' + name + '"')
	print("...end of command")


	os.chdir("data")
	input("want to continue?")
	return name

if __name__ == '__main__':
	first_run()
