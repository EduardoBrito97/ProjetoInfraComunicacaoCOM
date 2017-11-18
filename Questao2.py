# -*- coding: utf-8 -*-
import socket

class Package():
	ControlBit = 0
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
def GetControlBit():
	return str(_control)

def GetUserName():
	return _delimiter + _username

def GetAcknowledge():
	return   _delimiter + '555'

def GetSequenceNumber():
	return _delimiter + '222'

def GetChecksum(message):
	return _delimiter + CalculateCheckSum(message)

def GetMessage(message):
	return _delimiter + message

def CreateMessage(message):
	return GetControlBit() + GetUserName() + GetAcknowledge() + GetSequenceNumber() + GetChecksum(message) + GetMessage(message)

def CreatePackage (rcvdMessage):
	rcvdPackage = Package()
	recvPackage.ControlBit, rcvdPackage.UserName, rcvdPackage.Acknowledge, rcvdPackage.SequenceNumber, rcvdPackage.CheckSum, rcvdPackage.Message  = rcvdMessage.split(_delimiter)
	return rcvdPackage

def SendPackage (client):
	message = raw_input('Your message: ')
	_socket.sendto(CreateMessage(message), client)

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
	if ord(rcvdPackage.ControlBit):
		_senders.append(client)
	print  rcvdPackage.UserName, " says: ", rcvdPackage.Message

def ReceiveMessage():
	rcvdDatagram, client = _socket.recvfrom(1024)
	PrintMessage(rcvdDatagram, client)
	return client

def CallServer():
	_senders = []
	while 1:
		print "Typing..."
		client = ReceiveMessage()
		if client not in _senders:
			_control = 1
			for contact in _senders:
				if contact != client:
					_socket.sendto(CreateMessage(client), contact)
					_socket.sendto(CreateMessage(contact),client)
			_control = 0
		else:
			_control = 0
		for i in _senders:
			SendPackage(i)

def CallClient():
	_senders = ['172.20.18.20']
	#client = (_senders, _port)      
	while 1:
		for i in _senders:		
			SendPackage()
			ReceiveMessage()

def AmIServer():
	try:
		_socket.bind(('172.20.18.20', _port))
		return 1

	except Exception:
		return 0

#Program:
_username = raw_input("What's your name? ")
_port = 12000
_control = 0
_senders = []
_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
_delimiter = '@#!@!#!@!$!#!#@#!!'
_ERROR = 'SYSTEM' + GetAcknowledge() + GetSequenceNumber() + GetChecksum('Something went wrong.') + GetMessage('Something went wrong.')

if AmIServer():
	CallServer()
else:
	CallClient()

