# -*- coding: utf-8 -*-
import socket
import thread
import time

class Buffer():
	timer = 0
	message = ""
	tentativas = 0
	i = ()

class Package():
	ControlBit = ''
	UserName = ''
	Message = ''
	Acknowledge = 0

def GetControlBit():
	global _control
	return str(_control)

def GetUserName():
	return _delimiter + _username

def GetAcknowledge():
	global setAck
	return  _delimiter + setAck

def GetMessage(message):
	return _delimiter + message

def CreateMessage(message):
	return GetControlBit() + GetUserName() + GetAcknowledge() + GetMessage(message)

def CreatePackage (rcvdMessage):
	rcvdPackage = Package()
	controlBit, rcvdPackage.UserName, ack, rcvdPackage.Message = rcvdMessage.split(_delimiter)
	rcvdPackage.ControlBit = controlBit
	rcvdPackage.Acknowledge = ack
	return rcvdPackage

def SendPackage (message,client):
	_socket.sendto(CreateMessage(message), client)

def DecodifyMessage(rcvdMessage, client):
	rcvdPackage = CreatePackage(rcvdMessage)
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

	if rcvdPackage.Acknowledge == '0':
		print rcvdPackage.UserName, " says: ", rcvdPackage.Message
		setAck = '1'
		SendPackage(rcvdPackage.Message,client)
	elif rcvdPackage.Acknowledge == '1':
		lock.acquire()
		setAck = '0'
		for aux in messages:
			if aux.i == client:
				messages.remove(aux)
		lock.release()

def temporizador(lock, s):
	buff = Buffer()
	global messages
	global setAck
	global _senders
	i = 0
	while True:
		lock.acquire()
		if len(messages) > 0 and i < len(messages):
			buff = messages[i]
			atual = time.clock()
			if (atual - buff.timer) > 0.05:
				setAck = '0'				
				SendPackage(buff.message, buff.i)
				buff.timer = atual
				buff.tentativas = buff.tentativas + 1
				messages[i] = buff

			if buff.tentativas == 10:
				print "parei"
				_senders.remove(buff.i)
				messages.remove(buff)

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
	buff = Buffer()
	global _senders
	global timer
	global setAck
	while 1:
		message = raw_input()
		for i in _senders:
			lock.acquire()
			setAck = '0'
			SendPackage(message,i)
			timer = time.clock()
			buff.timer = timer
			buff.message = message
			buff.tentativas = 0
			buff.i = i
			messages.append(buff)
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
_ERROR = 'SYSTEM' + GetAcknowledge() + GetMessage('Something went wrong.')

lock = thread.allocate_lock()
thread.start_new_thread(ReceiveMessage,("rec",_socket, lock)) 
thread.start_new_thread(temporizador,(lock, "")) 

AmIServer()
CallServer(lock)