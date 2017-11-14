# -*- coding: utf-8 -*-
import socket

class Package():
	UserName = ''
	Message = ''
	Acknowledge = 0
	SequenceNumber = 0
	CheckSum = 0

def CalculateCheckSum(message):
	CheckSum = 0
	for char in message:
		CheckSum = CheckSum + ord(char)
	return str(CheckSum)

def GetUserName():
	return _username

def GetAcknowledge():
	return   _delimiter + '555'

def GetSequenceNumber():
	return _delimiter + '222'

def GetChecksum(message):
	return _delimiter + CalculateCheckSum(message)

def GetMessage(message):
	return _delimiter + message

def CreateMessage():
	message = raw_input('Your message: ')
	return GetUserName() + GetAcknowledge() + GetSequenceNumber() + GetChecksum(message) + GetMessage(message)

def CreatePackage (rcvdMessage):
	rcvdPackage = Package()
	rcvdPackage.UserName, rcvdPackage.Acknowledge, rcvdPackage.SequenceNumber, rcvdPackage.CheckSum, rcvdPackage.Message  = rcvdMessage.split(_delimiter)
	return rcvdPackage

def SendPackage (client):
	_socket.sendto(CreateMessage(), client)

def isCorrupt(rcvdPackage):
	return rcvdPackage.CheckSum != CalculateCheckSum(rcvdPackage.Message)

def TryAgain (client):
	_socket.sendto(_ERROR, client)
	return DecodifyMessage(ReceiveMessage())

def DecodifyMessage(rcvdMessage, client):
	rcvdPackage = CreatePackage(rcvdMessage)

	if isCorrupt(rcvdPackage):
		rcvdPackage = TryAgain (client)

	return rcvdPackage

def PrintMessage(rcvdDatagram, client):
	rcvdPackage = DecodifyMessage(rcvdDatagram, client)
	print  rcvdPackage.UserName, " says: ", rcvdPackage.Message

def ReceiveMessage():
	rcvdDatagram, client = _socket.recvfrom(1024)
	PrintMessage(rcvdDatagram, client)
	return client

def CallServer():
	while 1:
		print "Typing..."
		client = ReceiveMessage()
		SendPackage(client)

def CallClient():
	client = ('', _port)      
	while 1:		
		SendPackage(client)
		ReceiveMessage()

def AmIServer():
	try:
		_socket.bind(('', _port))
		return 1

	except Exception:
		return 0

#Program:
_username = raw_input("What's your name? ")
_port = 12000
_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
_delimiter = '@#!@!#!@!$!#!#@#!!'
_ERROR = 'SYSTEM' + GetAcknowledge() + GetSequenceNumber() + GetChecksum('Something went wrong.') + GetMessage('Something went wrong.')

if AmIServer():
	CallServer()
else:
	CallClient()




