# -*- coding: utf-8 -*-
import socket
import os

def AddFile():
	print('Add File')
	return 0

def EditFile():
	print('Edit File')
	return 0

def RemoveFile():
	print('Remove File')
	return 0

def MoveFile():
	print('Move File')
	return 0

def AddFolder():
	print('Add Folder')
	return 0

def RemoveFolder():
	print('Remove Folder')
	return 0


def ExecuteCommand(command):
	if (command == 'addFile'):
		AddFile()
	elif (command == 'editFile'):
		EditFile()
	elif (command == 'removeFile'):
		RemoveFile()
	elif (command == 'moveFile'):
		MoveFile()
	elif (command == 'addFolder'):
		AddFolder()
	elif (command == 'removeFolder'):
		RemoveFolder()
	elif (command == 'endConnection'):
		EndConnection()
	return 0

def IsTheUserAuthorized(username, password):
	file = open("acc.txt", "r")
	lines = file.readlines()
	length = len(lines)
	file.close()

	for index in range (0, length - 1):
		if (lines[index] == username + "\n" and lines[index+1] == password + "\n"):
			return 1

	if (lines[length-2] == username + "\n" and lines[length - 1] == password):
		return 1

	return 0

def Authorize():
	global _connectionSocket, _username, _password

	while (IsTheUserAuthorized(_username, _password) == 0):
			message = ReceiveMessage(_connectionSocket)
			_username, _password = GetUsernameAndPassword(message)
			if (IsTheUserAuthorized(_username, _password) == 0):
				SendMessage('Wrong username or password.', _connectionSocket)
	SendMessage('You are logged in.', _connectionSocket)

def InputUsernameAndPass():
	_username = raw_input('Username:')
	_password = raw_input('Password:')
	return _username + _delimiter + _password

def Login():
	global _socket, _username, _password, _delimiter
	rcvMessage = 'teste'
	while (rcvMessage != 'You are logged in.'):
		message = InputUsernameAndPass()
		SendMessage(message, _socket)
		rcvMessage = ReceiveMessage(_socket)
		print(rcvMessage)

def GetUsernameAndPassword (message):
	global _delimiter
	return message.split(_delimiter)

def SendMessage (message, socket):
	socket.send(message)

def ReceiveMessage(socket):
	return socket.recv(1024)

def CallServer():
	global _connectionSocket
	print('You are the server')
	_connectionSocket, _client = _socket.accept()  
	while _stillConnected:
		Authorize();
		command = ReceiveMessage(_connectionSocket)
		ExecuteCommand(command)

def PrintMenu():
	print('Press 1 to Add File')
	print('Press 2 to Edit File')
	print('Press 3 to Remove File')
	print('Press 4 to Move File')
	print('Press 5 to Add Folder')
	print('Press 6 to Remove Folder')
	print('Press 7 to End Connection')

def GetCommandString(command):
	global _stillConnected
	if (command ==  '1'):
		return 'addFile'
	elif (command ==  '2'):
		return 'editFile'
	elif (command ==  '3'):
		return 'removeFile'
	elif (command ==  '4'):
		return 'moveFile'
	elif (command ==  '5'):
		return 'addFolder'
	elif (command ==  '6'):
		return'removeFolder'
	elif (command ==  '7'):
		_stillConnected = 0
		return 'endConnection'
	return 0

def CallClient():
	global _port, _client, _socket, _stillConnected
	SetSocket()
	print('You are the client')
	_client = ('', _port)
	_socket.connect(_client)
	Login()
	while _stillConnected:
		PrintMenu()
		command = raw_input('Tell us your command:')
		realCommand = GetCommandString(command)
		SendMessage(realCommand, _socket)
		os.system('clear')

def AmIServer():
	global _socket
	try:
		_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
		_socket.bind(('', _port))
		_socket.listen(1)
		return 1

	except Exception:
		return 0

def SetSocket():
	global _port, _client, _socket, _connectionSocket
	_port = 12000
	_client = ('', _port)
	_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	_connectionSocket = socket.socket()

def EndConnection():
	global _socket, _connectionSocket, _stillConnected
	_stillConnected = 0
	_socket.close()
	_connectionSocket.close()

#Program:
global _username, _password, _delimiter, _stillConnected
_stillConnected = 1
_username = ''
_password = ''
_delimiter = '@#!@!#!@!$!#!#@#!!'
SetSocket()

if AmIServer():
	CallServer()
else:
	CallClient()

EndConnection()