# -*- coding: utf-8 -*-
import socket
import threading
import thread
import time

class Package():
	ControlBit = ''
	UserName = ''
	Message = ''
	Acknowledge = 0
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
	global setAck
	return  _delimiter + setAck

def GetChecksum(message):
	return _delimiter + CalculateCheckSum(message)

def GetMessage(message):
	return _delimiter + message

def CreateMessage(message):
	return GetControlBit() + GetUserName() + GetAcknowledge() + GetChecksum(message) + GetMessage(message)

def CreatePackage (rcvdMessage):
	rcvdPackage = Package()
	controlBit, rcvdPackage.UserName, ack, check, rcvdPackage.Message = rcvdMessage.split(_delimiter)
	rcvdPackage.ControlBit = controlBit
	rcvdPackage.Acknowledge = ack
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

def PrintMessage(rcvdDatagram, client, lock):
	global messages
	global _senders
	global _control
	global _socket
	global setAck
	rcvdPackage = DecodifyMessage(rcvdDatagram, client)
	if rcvdPackage.ControlBit == '1':
		ip, portR = rcvdPackage.Message.split(',')
		ip = ip[2:len(ip)-1]
		portR = int(portR[:len(portR)-1])
		_senders.append((ip,portR))

	elif client not in _senders:
			_control = 1
			_senders.append(client)
			for contact in _senders:
				if contact != client:
					_socket.sendto(CreateMessage(str(client)), contact)
					_socket.sendto(CreateMessage(str(contact)), client)
			_control = 0
	else:
		print rcvdPackage.UserName, " says: ", rcvdPackage.Message

	if rcvdPackage.Acknowledge == '0':
		print "recebi"
		setAck = '1'
		SendPackage(rcvdPackage.Message,client)
	elif rcvdPackage.Acknowledge == '1':
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		lock.acquire()
		setAck = '0'
		for aux in messages:
			if aux[1] == client:
				print "removeu"
				messages.remove(aux)
		lock.release()

def temporizador(lock, s):
	global messages
	global setAck
	i = 0
	while True:
		lock.acquire()
		if len(messages) > 0 and i < len(messages):
			tupla = messages[i]
			msg_timer = tupla[0]
			timer = msg_timer[1]
			atual = time.clock()
			if (atual - timer) > 0.5:
				print "estourou"
				setAck = '0'				
				SendPackage(msg_timer[0], tupla[1])
				msg_timer = (msg_timer[0],atual)
				tupla = (msg_timer, tupla[1])
				messages[i] = tupla

			i = i+1		
				
			if i >= len(messages):
				i=0
		lock.release()

def ReceiveMessage(name,s, lock):
	while True:
		rcvdDatagram, client = s.recvfrom(2048)
		PrintMessage(rcvdDatagram, client, lock)

def CallServer(lock):
	global messages
	global _senders
	global timer
	global setAck
	while 1:
		message = raw_input()
		print str(len(_senders))
		for i in _senders:
			lock.acquire()
			setAck = '0'
			SendPackage(message,i)
			timer = time.clock()
			print 'enviei'
			messages.append(((message, timer), i))
			lock.release()


def AmIServer():
	global _socket
	global _senders
	try:
		_socket.bind(('172.20.18.12', _port))
		return 1

	except Exception:
		_socket.bind(('', _port))
		_senders = [('172.20.18.12',_port)]
		return 0

#Program:
setAck = '0'
messages = []
_username = raw_input("What's your name? ")
_port = 12000
_control = 0
_senders = []
_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
_delimiter = '@#!@!#!@!$!#!#@#!!'
_ERROR = 'SYSTEM' + GetAcknowledge() + GetChecksum('Something went wrong.') + GetMessage('Something went wrong.')
new_cont = 0
conversation = raw_input("Do you want start a conversation(y/n)")

#for i in range(5):
lock = thread.allocate_lock()
thread.start_new_thread(ReceiveMessage,("rec",_socket, lock)) 
thread.start_new_thread(temporizador,(lock, "")) 
#threading.Thread(target=ReceiveMessage, args=("rec",_socket)).start()
#threading.Thread(target=temporizador, args=()).start()


AmIServer()
CallServer(lock)