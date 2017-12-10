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
	#print str(_control)
	return str(_control)

def GetUserName(username):
	return _delimiter + username

def GetAcknowledge(ack):
	return  _delimiter + str(ack)

def GetSequenceNumber():
	return _delimiter + '222'

def GetChecksum(message):
	return _delimiter + CalculateCheckSum(message)

def GetMessage(message):
	return _delimiter + message

def CreateMessage(message, user, ack):
	return GetControlBit() + GetUserName(user) + GetAcknowledge(ack) + GetSequenceNumber() + GetChecksum(message) + GetMessage(message)

def CreatePackage (rcvdMessage):
	rcvdPackage = Package()
	controlBit = ''
	ack = ''
	seq = ''
	check = ''
	controlBit, rcvdPackage.UserName, ack, seq, check, rcvdPackage.Message = rcvdMessage.split(_delimiter)
	rcvdPackage.ControlBit = controlBit
	rcvdPackage.Acknowledge = ack
	rcvdPackage.SequenceNumber = seq
	rcvdPackage.CheckSum = check
	return rcvdPackage

def GetMSGwfError():
	return GetControlBit() + GetUserName('sYSERrORmSG') + GetAcknowledge(_myacknum) + GetSequenceNumber() + GetChecksum('SmetHing uet Wrromng.') + GetMessage('Something went wrong.')

def SendMSGwfError(client):
	_socket.sendto(GetMSGwfError(), client)

def SendPackage (message, client, ack, user):
	_socket.sendto(CreateMessage(message, user, ack), client)

def isCorrupt(rcvdPackage):
	return rcvdPackage.CheckSum != CalculateCheckSum(rcvdPackage.Message)

def TryAgain (client, ack):
	#_socket.sendto(_ERROR, client)
	SendPackage('Something went wrong.', client, ack, 'SYSERRORMSG')
	
def DecodifyMessage(rcvdMessage, client):
	global _lastMessage
	rcvdPackage = CreatePackage(rcvdMessage)
	if isCorrupt(rcvdPackage):
		TryAgain (client, rcvdPackage.Acknowledge)
		
	if (rcvdPackage.UserName == 'SYSERRORMSG'):
		SendPackage(_lastMessage[len(_lastMessage)-1], client, _myacknum, _username)
		#e reinicializa temporizador
		

	#if (rcvdPackage.UserName == 'SYSACKMSG'):
		#para temporizador


	return rcvdPackage

def PrintMessage(rcvdDatagram, client):
	global _senders
	global _control
	global _socket
	rcvdPackage = DecodifyMessage(rcvdDatagram, client)
	if (rcvdPackage.UserName != 'SYSACKMSG'):
		if (rcvdPackage.UserName != 'SYSERRORMSG'):
			if (rcvdPackage.UserName != 'sYSERrORmSG'):
				SendPackage('Acknowledge message ok.', client, rcvdPackage.Acknowledge, 'SYSACKMSG')
				if (rcvdPackage.ControlBit == '1'):
					aux, aux2 = rcvdPackage.Message.split(',')
					aux = aux[2:len(aux)-1]
					aux2 = int(aux2[:len(aux2)-1])
					_senders.append((aux,aux2))
				if client not in _senders:
						_control = 1
						_senders.append(client)
						for contact in _senders:
							if contact != client:
								_socket.sendto(CreateMessage(str(client), _username, _myacknum), contact)
								_socket.sendto(CreateMessage(str(contact), _username, _myacknum), client)
						_control = 0
				print  rcvdPackage.UserName, " says: ", rcvdPackage.Message

def ReceiveMessage(name,s):
	while True:
		rcvdDatagram, client = s.recvfrom(1024)
		PrintMessage(rcvdDatagram, client)

def CallServer():
	global _senders
	global _lastMessage
	global _myacknum
	global conversation
	while 1:
		if (conversation == 'error'):
			for z in _senders:
				SendMSGwfError(z)
			conversation = raw_input('conversation error again?')

		else:
			message = raw_input()
			_lastMessage.append(message)
			_myacknum = _myacknum + 1
			#print str(len(_senders))
			for i in _senders:
				SendPackage(message, i, _myacknum, _username)


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
_lastMessage = []
_lastMessage.append('olar')
_myacknum = 0
_username = raw_input("What's your name? ")
_port = 12000
_control = 0
_senders = []
_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
_delimiter = '@#!@!#!@!$!#!#@#!!'
#_ERROR = GetControlBit() + GetUserName('sYSERrORmSG') + GetAcknowledge(_myacknum) + GetSequenceNumber() + GetChecksum('SmetHing uet Wrromng.') + GetMessage('Something went wrong.')
new_cont = 0
conversation = raw_input("Do you want start a conversation(y/n)")
for u in range(5):
	threading.Thread(target=ReceiveMessage, args=("rec",_socket)).start()

AmIServer()
CallServer()


