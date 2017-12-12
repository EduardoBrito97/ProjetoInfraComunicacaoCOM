# -*- coding: utf-8 -*-
import socket
import os
import time

#Client functions
def InputUsernameAndPass():
	global _username, _password
	_username = raw_input('Username:')
	_password = raw_input('Password:')
	return _username + _delimiter + _password

def TryToReg():
	global _socket, _delimiter
	message = 'Register' + _delimiter
	SendMessage(message, _socket)
	message = InputUsernameAndPass()
	SendMessage(message, _socket)
	resultMessage = ReceiveMessage (_socket)
	print(resultMessage)
	return resultMessage

def TryToLog ():
	global _socket
	SendMessage(InputUsernameAndPass(), _socket)
	resultMessage = ReceiveMessage(_socket)
	print(resultMessage)
	return resultMessage

def Login():
	global _socket, _username, _password, _delimiter, _folder
	rcvMessage = 'User already registered.'
	while rcvMessage != 'You are logged in.':
		wantReg = raw_input ('Send 1 if you want to Register or 2 if you want to log in. ')
		if(wantReg == '1'):
			rcvMessage = TryToReg()
		else:
			rcvMessage = TryToLog()
	_folder = _username
	return 0


def PrintMenu():
	print('Press 1 to Upload a File')
	print('Press 2 to Download a File')
	print('Press 3 to Edit File')
	print('Press 4 to Remove File')
	print('Press 5 to Move File')
	print('Press 6 to Add Folder')
	print('Press 7 to Remove Folder')
	print('Press 8 to Share This Folder')
	print('Press 9 to Open a Folder')
	print('Press 10 to List the Itens in a Folder')
	print('Press 11 to Access Another Users Folder')
	print('Press 12 to End Connection')


def ClientCommandActionsAndString(command):
	global _stillConnected, _socket, _folder, _delimiter, _unauthorized
	if (command ==  '1'):
		realCommand = 'addFile'
		SendMessage(realCommand, _socket)
		fileName = raw_input ('What is the file name? (Write the whole address) ')
		SendMessage(fileName, _socket)
		time.sleep(0.2)
		UploadFile(fileName, _socket, "")
		os.system('clear')
	
	elif (command ==  '2'):
		realCommand ='downloadFile'
		SendMessage(realCommand, _socket)
		downloadFile = raw_input('Which file you want to download from this folder? ')
		SendMessage(downloadFile, _socket)
		ReceiveFile(downloadFile, _socket, "downloads/")
		os.system('clear')


	elif (command ==  '3'):
		realCommand ='editFile'
		SendMessage(realCommand, _socket)
		oldFile = raw_input('Which file you want to rename? ')
		SendMessage(oldFile, _socket)
		newFile = raw_input('What is the new name?')
		os.system('clear')
		SendMessage(newFile, _socket)

	elif (command ==  '4'):
		realCommand ='removeFile'
		SendMessage(realCommand, _socket)
		removeFile = raw_input('Which file you want to remove? ')
		os.system('clear')
		SendMessage(removeFile, _socket)

	elif (command ==  '5'):
		realCommand ='moveFile'
		SendMessage(realCommand, _socket)
		fileName = raw_input('Which file you want to move? ')
		SendMessage(fileName, _socket)
		newFolder = raw_input('Where do you want to move? ')
		os.system('clear')
		SendMessage(newFolder, _socket)

	elif (command ==  '6'):
		realCommand ='addFolder'
		SendMessage(realCommand, _socket)
		folder = raw_input('What is the name of the folder you want to add? ')
		message = folder + _delimiter + _folder
		os.system('clear')
		SendMessage(message, _socket)

	elif (command ==  '7'):
		realCommand = 'removeFolder'
		SendMessage(realCommand, _socket)
		folder = raw_input('What folder you want to remove? ')
		message = folder + _delimiter + _folder
		os.system('clear')
		SendMessage(message, _socket)

	elif (command ==  '8'):
		realCommand = 'shareFolder'
		SendMessage(realCommand, _socket)
		user = raw_input('Who you want to share with? ')
		message = user + _delimiter + _folder
		os.system('clear')
		SendMessage(message, _socket)

	elif (command ==  '9'):
		realCommand = 'openFolder'
		SendMessage(realCommand, _socket)
		folder = raw_input('Which folder you want to open? ')
		SendMessage(folder, _socket)
		os.system('clear')

	elif (command ==  '10'):
		realCommand = 'listFolder'
		os.system('clear')
		SendMessage(realCommand, _socket)
		rcvMessage = ReceiveMessage(_socket)
		if (rcvMessage == "You are not authorized to do this. "):
			_unauthorized = 1
			print(rcvMessage)

		else:
			itens = rcvMessage.split(',')
			print('The files in this folder are: ')
			for item in itens:
				print(item)
		

	elif (command ==  '11'):
		realCommand = 'accessAnotherUser'
		os.system('clear')
		SendMessage(realCommand, _socket)
		user = raw_input('Which users folder you want to access? ')
		SendMessage(user, _socket)

	elif (command ==  '12'):
		_stillConnected = 0
		realCommand = 'endConnection'
		os.system('clear')
		SendMessage(realCommand, _socket)

	return 0

def CallClient():
	global _port, _client, _socket, _stillConnected, report, _unauthorized
	SetSocket()
	print('You are the client')
	_client = ('', _port)
	_socket.connect(_client)
	Login()
	while _stillConnected:
		PrintMenu()
		command = raw_input('Tell us your command:')
		realCommand = ClientCommandActionsAndString(command)
		if (_unauthorized == 0):
			report = ReceiveMessage(_socket)
			print(report)
		_unauthorized = 0


#Server functions
def AuthorizeFolder():
	global _username, _folder
	file = open(_folder + "/acc.txt", "r")
	lines = file.readlines()
	length = len(lines)
	file.close()
	for index in range (0, length):
		if (lines[index] == _username + "\n"):
			return 1

	if (lines[length-1] == _username):
		return 1

	return 0

def AddFile():
	global _connectionSocket, _folder
	fileName = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder()):
		ReceiveFile(fileName, _connectionSocket, _folder + "/")
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)

	return 0

def DownloadFile():
	global _connectionSocket, _folder
	fileName = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder()):
		time.sleep(0.1)
		UploadFile(fileName, _connectionSocket, _folder + '/')
		print('made it here')
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0

def EditFile():
	global _username, _connectionSocket, _folder, _delimiter
	oldFile = ReceiveMessage(_connectionSocket)
	newFile = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder()):
		os.system('mv ' + _folder + '/' + oldFile + ' ' + _folder + '/' + newFile)
		print(_username + ' renamed ' + oldFile + ' to ' + newFile)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0

def RemoveFile():
	global _username, _connectionSocket, _folder, _delimiter
	removedFile = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder()):
		os.system('rm ' + _folder + '/' + removedFile)
		print(_username + ' removed a file named ' + removedFile)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0

def MoveFile():
	global _username, _connectionSocket, _folder, _delimiter
	fileName = ReceiveMessage(_connectionSocket)
	newFolder = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder()):
		os.system('mv ' + _folder + '/' + fileName + ' ' + _folder + '/' + newFolder + '/' + fileName)
		print(_username + ' moved ' + fileName + ' to ' + newFolder)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)		
	return 0

def AddFolder():
	global _username, _connectionSocket, _folder, _delimiter
	createFolder, _folder = ReceiveMessage(_connectionSocket).split(_delimiter)
	if (AuthorizeFolder()):
		os.system('mkdir  ' + _folder + '/' + createFolder)
		print(_username + ' added ' + createFolder + ' folder')
		file = open(_folder + '/' + createFolder +  "/acc.txt", "a")
		file.write(_username + "\n")
		file.close()
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0

def RemoveFolder():
	global _username, _connectionSocket, _folder, _delimiter
	removeFolder, _folder = ReceiveMessage(_connectionSocket).split(_delimiter)
	if (AuthorizeFolder()):
		os.system('rm -rf ' + _folder + '/' + removeFolder)
		print(_username + ' removed ' + removeFolder + ' folder')
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0

def ShareFolder():
	global _username, _connectionSocket, _folder, _delimiter
	newUser, _folder = ReceiveMessage(_connectionSocket).split(_delimiter)
	print(newUser+ 'new ')
	print(_folder+ 'folder ')
	if (AuthorizeFolder()):
		AddUserToAcc(newUser)
		print(_username + ' shared ' + _folder + ' with ' + newUser)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0;

def OpenFolder():
	global _folder, _connectionSocket
	if(AuthorizeFolder()):
		folder = ReceiveMessage(_connectionSocket)
		_folder = _folder + '/' + folder
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0;

def ListFolder():
	global _folder, _connectionSocket, _username
	if(AuthorizeFolder()):
		itens = os.listdir(_folder)
		allItens = ''
		for item in itens:
			allItens = item + ',' + allItens
		SendMessage(allItens, _connectionSocket)
		print(_username + ' listed all files in ' + _folder)
		time.sleep(0.1)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return 0;

def AccessAnotherUserFolder():
	global _folder, _connectionSocket
	userFolder = ReceiveMessage(_connectionSocket)
	if (os.system("cd " + userFolder) == 0):
		_folder = userFolder
		SendMessage('Everything went well.', _connectionSocket)
	else:
		SendMessage('There is no such user.', _connectionSocket)
	return 0

def ExecuteCommand(command):
	global _connectionSocket
	if (command == 'addFile'):
		AddFile()
	elif (command == 'editFile'):
		EditFile()
	elif (command == 'downloadFile'): 
		DownloadFile()
	elif (command == 'removeFile'):
		RemoveFile()
	elif (command == 'moveFile'):
		MoveFile()
	elif (command == 'addFolder'):
		AddFolder()
	elif (command == 'removeFolder'):
		RemoveFolder()
	elif (command ==  'shareFolder'):
		ShareFolder()
	elif (command == 'openFolder'):
		OpenFolder()
	elif (command == 'listFolder'):
		ListFolder()
	elif (command == 'endConnection'):
		EndConnection()
	elif(command == 'accessAnotherUser'):
		AccessAnotherUserFolder()
	else:
		SendMessage('Not a valid command', _connectionSocket)
	return 0

def IsTheUserAuthorized(username, password):
	file = open("acc.txt", "r")
	lines = file.readlines()
	length = len(lines)
	file.close()

	for index in range (0, length):
		if (lines[index] == username + "\n" and lines[index+1] == password + "\n"):
			return 1

	if(len(lines)>1):
		if (lines[length-2] == username + "\n" and lines[length - 1] == password):
			return 1

	return 0

def WriteUserAndPassInAcc():
	global _username, _password
	file = open("acc.txt", "a")
	file.write(_username + "\n")
	file.write(_password + "\n")
	file.close

def AddUserToAcc(username):
	global _folder
	file = open(_folder + "/acc.txt", "a")
	file.write(username + "\n")
	file.close()

def Register():
	global _username, _password, _connectionSocket, _folder
	message = ReceiveMessage(_connectionSocket)
	_username, _password = GetUsernameAndPassword(message)

	if (os.system("cd " + _username)!= 0):
		WriteUserAndPassInAcc()
		_folder = _username
		os.system("mkdir " + _folder)
		AddUserToAcc(_username)
		print(_username + " registered and logged in.")
		return 1
	else:
		return 0

def Authorize():
	global _connectionSocket, _username, _password, _delimiter, _folder

	message = ReceiveMessage(_connectionSocket)
	if (message == 'Register'+ _delimiter):
		if (Register() == 0):
			SendMessage('User already registered.', _connectionSocket)
			return 0

	while (IsTheUserAuthorized(_username, _password) == 0):
			_username, _password = GetUsernameAndPassword(message)
			if (IsTheUserAuthorized(_username, _password) == 0):
				SendMessage('Wrong username or password.', _connectionSocket)
				message = ReceiveMessage(_connectionSocket)

	print(_username + ' has just logged in.')
	_folder = _username
	SendMessage('You are logged in.', _connectionSocket)
	return 1

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
	autorizar = 0
	while (autorizar == 0):
		autorizar = Authorize()
	while _stillConnected:
		command = ReceiveMessage(_connectionSocket)
		ExecuteCommand(command)


#Neutral functions
def AmIServer():
	global _socket
	try:
		_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
		_socket.bind(('', _port))
		_socket.listen(10)
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

def UploadFile(fileName, SendSocket, folder):
	global uploadPort, uploadHost, uploadSocket, uploadConnectionSocket
	skt = socket.socket()
	uploadHost = socket.gethostbyname("")
	uploadPort = 15500

	skt.connect((uploadHost, uploadPort))
	file = open(folder + fileName, 'rb')
	bytes = file.read(1024)
	while (bytes):
	    skt.send(bytes)
	    bytes = file.read(1024)
	file.close()
	skt.close()
	time.sleep(0.1)
	return 0

def ReceiveFile(fileName, ReceiveSocket, folder):
	global uploadPort, uploadHost, uploadSocket, uploadConnectionSocket
	skt = socket.socket()
	uploadHost = socket.gethostbyname("")
	uploadPort = 15500
	skt.bind((uploadHost, uploadPort))
	file = open(folder + fileName, 'wb')
	skt.listen(5)

	while True:
	    c, addr = skt.accept()
	    bytes = c.recv(1024)
	    while (bytes):
	        file.write(bytes)
	        bytes = c.recv(1024)
	    file.close()
	    c.close()
	    break
	return 0

#Program:
global _username, _password, _delimiter, _stillConnected, _folder, _unauthorized
_unauthorized = 0
_stillConnected = 1
_username = ''
_password = ''
_delimiter = '@#!@!#!@!$!#!#@#!!'
_folder = ' '
SetSocket()
if AmIServer():
	CallServer()
else:
	CallClient()

EndConnection()