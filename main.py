import sys
import re
from datetime import datetime 
import time as tm
import schedule
import uuid
import socket 
import base64

# All the settings down below
remoteIP = "192.168.0.114"
runningDeviceMac = '-'.join(re.findall('..', '%012x' % uuid.getnode()))
runningDeviceIp = socket.gethostbyname(socket.gethostname())
tvModel = "UE40EH5307" # in my case
pretendAs = "iphone..iapp.samsung"
shownName = "Deflix Automatic Shutdown"
keyCodeStr = "KEY_POWEROFF"

def fullmatch(regex, string, flags=0):
    m = re.match(regex, string, flags=flags)
    if m and m.span()[1] == len(string):
        return m

def turnOffTV():
	generalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	generalSocket.connect((remoteIP, 55000))
	baseShownName = base64.b64encode(shownName.encode("utf-8"))
	baseMac = base64.b64encode(runningDeviceMac.encode("utf-8"))
	baseIp = base64.b64encode(runningDeviceIp.encode("utf-8"))
	keyCode = base64.b64encode(keyCodeStr.encode("utf-8"))

	connectionMessage = chr(0x64) + chr(0x00) + chr(len(baseIp)) + chr(0x00) + str(baseIp) + chr(len(baseMac)) \
		+ chr(0x00) + str(baseMac) + chr(len(baseShownName)) + chr(0x00) + str(baseShownName)

	connectionMessageWithHeader	= chr(0x00) + chr(len(pretendAs)) + chr(0x00) + pretendAs + chr(len(connectionMessage)) + chr(0x00) + connectionMessage;

	twoCoolBytesMessage = chr(0xc8) + chr(0x00)
	twoCoolBytesMessageWithHeader = chr(0x00) + chr(len(pretendAs)) + chr(0x00) + pretendAs + chr(len(twoCoolBytesMessage)) + chr(0x00) + twoCoolBytesMessage;

	generalSocket.send(connectionMessageWithHeader)
	generalSocket.send(twoCoolBytesMessageWithHeader)

	# Sending test key
	turnOffMessage = chr(0x00) + chr(0x00) + chr(0x00) + chr(len(keyCode)) + chr(0x00) + keyCode
	turnOffMessageWithHeader = chr(0x00) + chr(len(pretendAs)) + chr(0x00) + pretendAs + chr(len(turnOffMessage)) + chr(0x00) + turnOffMessage

	generalSocket.send(turnOffMessageWithHeader)

	generalSocket.close()

	print("Key Sended")

def main():
	# Time formats:
	# python main.py 23:30
	# python main.py 2:30 pm

	timeRegEx = "\\d{2}:\\d{2}"
	timeFormat = "%H:%M"
	shutdownTime = ""

	if len(sys.argv) == 3:
		# am\pm format
		time = sys.argv[1]
		amPm = sys.argv[2].upper()

		if not fullmatch(timeRegEx, time):
			print("Wrong time format! Please use HH:MM AM / PM")
			sys.exit(1)

		if not (amPm == "AM" or amPm == "PM"):
			print("Some shit with am / pm") 
			sys.exit(1)

		shutdownTime = str(datetime.strptime(time + " " + amPm, "%I:%M %p"))[11:]

	elif len(sys.argv) == 2:
		# 24-hours format
		time = sys.argv[1]
		if not fullmatch(timeRegEx, time):
			print("Wrong time format! Please use HH:MM AM / PM or HH:MM")
			sys.exit(1)

		shutdownTime = time

	elif len(sys.argv) == 1:
		print("No shut down time provided!")
		sys.exit(2)

	else:
		print("Wtf")
		sys.exit(1)

	if int(shutdownTime[:2]) > 23:
		print("How df you have more than 24 hours?")
		sys.exit(1)

	# Finally its all ok with time

	print("Everyday scheduled shutdown time is " + shutdownTime)
	
	schedule.every().day.at(shutdownTime).do(turnOffTV)
	
	while True:
		print("Checking time...")
		schedule.run_pending()
		tm.sleep(60)

if __name__ == '__main__':	
	main()