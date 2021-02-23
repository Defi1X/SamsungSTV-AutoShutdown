import uuid
import socket 
import base64
import re

# All the settings down below
remoteIP = "192.168.0.114"
runningDeviceMac = '-'.join(re.findall('..', '%012x' % uuid.getnode()))
runningDeviceIp = socket.gethostbyname(socket.gethostname())
tvModel = "UE40EH5307" # in my case
pretendAs = "iphone..iapp.samsung"
shownName = "Deflix Automatic Shutdown"

generalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
generalSocket.connect((remoteIP, 55000))
baseShownName = base64.b64encode(shownName.encode("utf-8"))
baseMac = base64.b64encode(runningDeviceMac.encode("utf-8"))
baseIp = base64.b64encode(runningDeviceIp.encode("utf-8"))

connectionMessage = chr(0x64) + chr(0x00) + chr(len(baseIp)) + chr(0x00) + str(baseIp) + chr(len(baseMac)) \
	+ chr(0x00) + str(baseMac) + chr(len(baseShownName)) + chr(0x00) + str(baseShownName)

connectionMessageWithHeader	= chr(0x00) + chr(len(pretendAs)) + chr(0x00) + pretendAs + chr(len(connectionMessage)) + chr(0x00) + connectionMessage;

twoCoolBytesMessage = chr(0xc8) + chr(0x00)
twoCoolBytesMessageWithHeader = chr(0x00) + chr(len(pretendAs)) + chr(0x00) + pretendAs + chr(len(twoCoolBytesMessage)) + chr(0x00) + twoCoolBytesMessage;

generalSocket.send(connectionMessageWithHeader)
generalSocket.send(twoCoolBytesMessageWithHeader)

generalSocket.close()