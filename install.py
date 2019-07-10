def first_run():
	import sys
	import os
	import subprocess
	import xml.etree.ElementTree as ET

	# platform check
	platform = sys.platform
	if platform == "linux" or platform == "linux2":
		PLATFORM = "Linux"
	elif platform == "darwin":
		PLATFORM = "MacOX"
	elif platform == "win32":
		PLATFORM = "Windows"
	print("Running on platform - " + PLATFORM)


 	# package check
	def check_install(package):
			try:
				__import__(package)
			except ImportError:
				subprocess.run([sys.executable, "-m", "pip", "install", package])
			try:
				__import__(package)
			except ImportError:
				print("Cannot install systemwide - retrying install by local user")
				subprocess.check_output([sys.executable, "-m", "site", "--user-site"]).decode('utf-16')[:-1]
				subprocess.run([sys.executable, "-m", "pip", "install", package, "--user"])
			finally:
				__import__(package)

	def AddSysPath(new_path):
		new_path = os.path.abspath(new_path)
		if PLATFORM == "Windows":
			new_path = new_path.lower()
		do = -1
		if os.path.exists(new_path):
			do = 1
			# check against all paths currently available
			for x in sys.path:
				x = os.path.abspath(x)
				if sys.platform == 'win32':
					x = x.lower()
				if new_path in (x, x + os.sep):
					do = 0
			# add path if we don't already have it
			if do:
				sys.path.append(new_path)
				pass
		return do

	input("hej, chybaju ti moduly. Mozem ich instalovat? Ak ano, stlac enter, ak nie, zavri program a nebudes ho mat proste")
	if PLATFORM == "Windows":
		def pywin_import():
			import win32gui
			import win32api
			import win32con
		try:
			pywin_import()
		except ImportError:
			subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"])
		try:
			pywin_import()
		except ImportError:
			subprocess.run([sys.executable, "-m", "pip", "install", "pywin32", "--user"])
		finally:
			pywin_import()
				
				
	check_install("webbrowser")
	check_install("unidecode")

	fr = True
	# create working dir
	try:
		os.mkdir('data')
	except:
		pass

	name = input("Dobre rano, prve spustenie. Zadajte svoje meno ako je vo vysledkovkach pls (bez diakritiky): ")

	if PLATFORM == "Windows":
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

if __name__ == '__main__':
	first_run()