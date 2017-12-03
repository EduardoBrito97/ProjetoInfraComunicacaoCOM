# -*- coding: utf-8 -*-
import socket
import threading
import time

class Package():
	ControlBit = ''
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
	global _control
	print str(_control)
	return str(_control)

def GetUserName():
	return _delimiter + _username

def GetAcknowledge():
	return  _delimiter + '555'

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
	controlBit = ''
	ack = ''
	seq = ''
	check = ''
	controlBit, rcvdPackage.UserName, ack, sqe, check, rcvdPackage.Message = rcvdMessage.split(_delimiter)
	rcvdPackage.ControlBit = controlBit
	rcvdPackage.Acknowledge = ack
	rcvdPackage.SequenceNumber = seq
	rcvdPackage.CheckSum = check
	return rcvdPackage

def SendPackage (message,client):
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
	global _senders
	global _control
	global _socket
	rcvdPackage = DecodifyMessage(rcvdDatagram, client)
	if rcvdPackage.ControlBit == '1':
		aux, aux2 = rcvdPackage.Message.split(',')
		aux = aux[2:len(aux)-1]
		aux2 = int(aux2[:len(aux2)-1])
		_senders.append((aux,aux2))
	if client not in _senders:
			_control = 1
			_senders.append(client)
			for contact in _senders:
				if contact != client:
					_socket.sendto(CreateMessage(str(client)), contact)
					_socket.sendto(CreateMessage(str(contact)), client)
			_control = 0
	print  rcvdPackage.UserName, " says: ", rcvdPackage.Message

def ReceiveMessage(name,s):
	while True:
		rcvdDatagram, client = s.recvfrom(1024)
		PrintMessage(rcvdDatagram, client)

def CallServer():
	global _senders
	while 1:
		message = raw_input()
		print str(len(_senders))
		for i in _senders:
			SendPackage(message,i)


def AmIServer():
	global _socket
	global _senders
	try:
		_socket.bind(('172.20.18.20', _port))
		return 1

	except Exception:

		_senders = [('172.20.18.20',_port)]
		return 0

#Program:
_username = raw_input("What's your name? ")
_port = 12000
_control = 0
_senders = []
_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
_delimiter = '@#!@!#!@!$!#!#@#!!'
_ERROR = 'SYSTEM' + GetAcknowledge() + GetSequenceNumber() + GetChecksum('Something went wrong.') + GetMessage('Something went wrong.')
new_cont = 0
conversation = raw_input("Do you want start a conversation(y/n)")

threading.Thread(target=ReceiveMessage, args=("rec",_socket)).start()

AmIServer()
CallServer()

