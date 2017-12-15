# -*- coding: utf-8 -*-
import socket
import os
import time
import shutil
import threading

#Client functions
def InputUsernameAndPass():
	global _username, _password
	_username = raw_input('Username:')
	_password = raw_input('Password:')
	return _username + _delimiter + _password, _username, _password

def TryToReg(_socket):
	global _delimiter
	message = 'Register' + _delimiter
	SendMessage(message, _socket)
	time.sleep(0.1)
	message, _username, _password = InputUsernameAndPass()
	SendMessage(message, _socket)
	resultMessage = ReceiveMessage (_socket)
	print(resultMessage)
	return resultMessage, _username, _password

def TryToLog (_socket):
	message, _username, _password = InputUsernameAndPass()
	SendMessage(message, _socket)
	resultMessage = ReceiveMessage(_socket)
	print(resultMessage)
	return resultMessage, _username, _password

def Login(_socket, _username, _password, _delimiter, _folder):
	rcvMessage = 'User already registered.'
	while rcvMessage != 'You are logged in.':
		wantReg = raw_input ('Send 1 if you want to Register or 2 if you want to log in. ')
		if(wantReg == '1'):
			rcvMessage, _username, _password = TryToReg(_socket)
		else:
			rcvMessage, _username, _password = TryToLog(_socket)
	_folder = _username
	return _username, _password, _folder


def PrintMenu():
	options = ["File Options", "Folder Options", "Connection and User Options"]
	data = ([
			["1 - Upload"  , "6  - Add"              , "11 - Acess Another User's File"],
     		["2 - Download", "7  - Remove"           , "12 - End Connection"           ],
         	["3 - Rename"  , "8  - Share This Folder", ""                              ],
         	["4 - Remove"  , "9  - Open a Folder"    , ""                              ],
         	["5 - Move"    , "10 - List The Files"  , ""                               ]
         	])
	print('|%-23s|%-23s|%-23s' % (options[0], options[1], options[2]))
	for option in data:
		print('|%-23s|%-23s|%-23s' % (option[0], option[1], option[2]))


def ClientCommandActionsAndString(command, _stillConnected, _socket, _folder, _delimiter, _displayReport, _username):
	_displayReport = 1
	if (command ==  '1'):
		realCommand = 'addFile'
		SendMessage(realCommand, _socket)
		fileName = raw_input ('What is the file name? (Write the whole address) ')
		SendMessage(fileName, _socket)
		rcvMessage = ReceiveMessage(_socket)
		_displayReport = 0
		if (rcvMessage != "You are not authorized to do this. "):
			time.sleep(0.2)
			UploadFile(fileName, _socket, "")
		os.system('clear')
		print(rcvMessage)

	
	elif (command ==  '2'):
		realCommand ='downloadFile'
		SendMessage(realCommand, _socket)
		downloadFile = raw_input('Which file you want to download from this folder? ')
		SendMessage(downloadFile, _socket)
		rcvMessage = ReceiveMessage(_socket)
		_displayReport = 0
		if (rcvMessage != "You are not authorized to do this. "):
			ReceiveFile(downloadFile, _socket, "downloads/")
		os.system('clear')
		print(rcvMessage)

	elif (command ==  '3'):
		realCommand ='editFile'
		SendMessage(realCommand, _socket)
		oldFile = raw_input('Which file you want to rename? ')
		SendMessage(oldFile, _socket)
		newFile = raw_input('What is the new name?' )
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
		message = folder
		os.system('clear')
		SendMessage(message, _socket)

	elif (command ==  '7'):
		realCommand = 'removeFolder'
		SendMessage(realCommand, _socket)
		folder = raw_input('What folder you want to remove? ')
		message = folder
		os.system('clear')
		SendMessage(message, _socket)

	elif (command ==  '8'):
		realCommand = 'shareFolder'
		SendMessage(realCommand, _socket)
		user = raw_input('Who you want to share with? ')
		message = user
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
			_displayReport = 0
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
		user = raw_input('Which users folder you want to access? (Leave blank to go to your root) ')
		if(user == ''):
			user = _username
		SendMessage(user, _socket)

	elif (command ==  '12'):
		_stillConnected = 0
		_displayReport = 0
		realCommand = 'endConnection'
		os.system('clear')
		SendMessage(realCommand, _socket)

	else:
		os.system('clear')
		print('Invalid Command')
		_displayReport = 0

	return _displayReport, _stillConnected

def GetPortAndConnect():
	_port, _client, _socket, _connectionSocket = SetSocket(12000)
	_client = ('172.20.4.194', _port)
	_socket.connect(_client)
	_port = int(ReceiveMessage(_socket))
	_port, _client, _socket, _connectionSocket = SetSocket(_port)
	_client = ('172.20.4.194', _port)
	time.sleep(0.2)
	_socket.connect(_client)
	return _socket

def CallClient(_socket):
	global _delimiter
	print('You are the client')
	_stillConnected = 1
	_username = ''
	_password = ''
	_folder = ''
	_displayReport = 1
	_socket = GetPortAndConnect()
	_username, _password, _folder = Login(_socket, _username, _password, _delimiter, _folder)
	while _stillConnected:
		PrintMenu()
		command = raw_input('Tell us your command:')
		_displayReport, _stillConnected = ClientCommandActionsAndString(command, 1, _socket, _folder, _delimiter, _displayReport, _username)
		if (_displayReport == 1):
			report = ReceiveMessage(_socket)
			print(report)
		_displayReport = 1
	EndConnection(_socket)



#Server functions
def AuthorizeFolder(_username, _folder):
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

def AddFile(_connectionSocket, _folder, _username):
	fileName = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder(_username, _folder)):
		SendMessage('Everything went well. ', _connectionSocket)
		ReceiveFile(fileName, _connectionSocket, _folder + "/")
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)

	return _folder

def DownloadFile(_connectionSocket, _folder, _username):
	fileName = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder(_username, _folder)):
		SendMessage('Everything went well. ', _connectionSocket)
		time.sleep(0.1)
		UploadFile(fileName, _connectionSocket, _folder + '/')
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder

def EditFile(_username, _connectionSocket, _folder, _delimiter):
	oldFile = ReceiveMessage(_connectionSocket)
	newFile = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder(_username, _folder)):
		os.rename(_folder + '/' + oldFile, _folder + '/' + newFile)
		print(_username + ' renamed ' + oldFile + ' to ' + newFile)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder

def RemoveFile(_username, _connectionSocket, _folder, _delimiter):
	removedFile = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder(_username, _folder)):
		os.remove(_folder + '/' + removedFile)
		print(_username + ' removed a file named ' + removedFile)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder

def MoveFile(_username, _connectionSocket, _folder, _delimiter):
	fileName = ReceiveMessage(_connectionSocket)
	newFolder = ReceiveMessage(_connectionSocket)
	if(AuthorizeFolder(_username, _folder)):
		os.rename(_folder + '/' + fileName, _folder + '/' + newFolder + '/' + fileName)
		print(_username + ' moved ' + fileName + ' to ' + newFolder)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)		
	return _folder

def AddFolder(_username, _connectionSocket, _folder, _delimiter):
	createFolder = ReceiveMessage(_connectionSocket)
	if (AuthorizeFolder(_username, _folder)):
		os.makedirs(_folder + '/' + createFolder)
		print(_username + ' added ' + createFolder + ' folder')
		file = open(_folder + '/' + createFolder +  "/acc.txt", "a")
		file.write(_username + "\n")
		file.close()
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder

def RemoveFolder(_username, _connectionSocket, _folder, _delimiter):
	removeFolder = ReceiveMessage(_connectionSocket)
	if (AuthorizeFolder(_username, _folder)):
		shutil.rmtree(_folder + '/' + removeFolder, ignore_errors=True)
		print(_username + ' removed ' + removeFolder + ' folder')
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder

def ShareFolder(_username, _connectionSocket, _folder):
	newUser = ReceiveMessage(_connectionSocket)
	if (AuthorizeFolder(_username, _folder)):
		AddUserToAcc(newUser, _folder)
		print(_username + ' shared ' + _folder + ' with ' + newUser)
		SendMessage('Everything went well. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder;

def OpenFolder(_folder, _connectionSocket, _username):
	if(AuthorizeFolder(_username, _folder)):
		folder = ReceiveMessage(_connectionSocket)
		if (os.path.exists(_folder + '/' + folder)):
			_folder = _folder + '/' + folder
			SendMessage('Everything went well. ', _connectionSocket)
		else:
			SendMessage('There is no such folder. ', _connectionSocket)
	else:
		SendMessage('You are not authorized to do this. ', _connectionSocket)
	return _folder;

def ListFolder(_folder, _connectionSocket, _username):
	if(AuthorizeFolder(_username, _folder)):
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
	return _folder;

def AccessAnotherUserFolder(_folder, _connectionSocket):
	userFolder = ReceiveMessage(_connectionSocket)
	if (os.path.exists(userFolder)):
		_folder = userFolder
		SendMessage('Everything went well.', _connectionSocket)
	else:
		SendMessage('There is no such user.', _connectionSocket)
	return _folder

def ExecuteCommand(command, _connectionSocket, _username, _password, _folder):
	global _delimiter
	_stillConnected = 1
	if (command == 'addFile'):
		_folder = AddFile(_connectionSocket, _folder, _username)
	elif (command == 'editFile'):
		_folder = EditFile(_username, _connectionSocket, _folder, _delimiter)
	elif (command == 'downloadFile'): 
		_folder = DownloadFile(_connectionSocket, _folder, _username)
	elif (command == 'removeFile'):
		_folder = RemoveFile(_username, _connectionSocket, _folder, _delimiter)
	elif (command == 'moveFile'):
		_folder = MoveFile(_username, _connectionSocket, _folder, _delimiter)
	elif (command == 'addFolder'):
		_folder = AddFolder(_username, _connectionSocket, _folder, _delimiter)
	elif (command == 'removeFolder'):
		_folder = RemoveFolder(_username, _connectionSocket, _folder, _delimiter)
	elif (command ==  'shareFolder'):
		_folder = ShareFolder(_username, _connectionSocket, _folder)
	elif (command == 'openFolder'):
		_folder = OpenFolder(_folder, _connectionSocket, _username)
	elif (command == 'listFolder'):
		_folder = ListFolder(_folder, _connectionSocket, _username)
	elif (command == 'endConnection'):
		_stillConnected = 0
	elif(command == 'accessAnotherUser'):
		_folder = AccessAnotherUserFolder(_folder, _connectionSocket)
	else:
		SendMessage('Not a valid command', _connectionSocket)
	return _folder, _stillConnected

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

def WriteUserAndPassInAcc(_username, _password):
	file = open("acc.txt", "a")
	file.write(_username + "\n")
	file.write(_password + "\n")
	file.close

def AddUserToAcc(username, _folder):
	file = open(_folder + "/acc.txt", "a")
	file.write(username + "\n")
	file.close()

def Register(_username, _password, _connectionSocket, _folder):
	message = ReceiveMessage(_connectionSocket)
	_username, _password = GetUsernameAndPassword(message)

	if (not os.path.exists(_username)):
		WriteUserAndPassInAcc(_username, _password)
		_folder = _username
		os.makedirs(_folder)
		AddUserToAcc(_username, _folder)
		print(_username + " registered and logged in.")
		return 1, _username, _password, _folder
	else:
		return 0, _username, _password, _folder

def Authorize(_connectionSocket, _username, _password, _delimiter, _folder):

	while (IsTheUserAuthorized(_username, _password) == 0):
		message = ReceiveMessage(_connectionSocket)
		if (message == 'Register'+ _delimiter):
			Reg, _username, _password, _folder = Register(_username, _password, _connectionSocket, _folder)
			if (Reg == 0):
				SendMessage('User already registered.', _connectionSocket)
				_username = ''
			else:
				SendMessage('You are logged in.', _connectionSocket)
				return _username, _folder, 1, _password 
		else:
			_username, _password = GetUsernameAndPassword(message)
			if (IsTheUserAuthorized(_username, _password) == 0):
				SendMessage('Wrong username or password.', _connectionSocket)

	print(_username + ' has just logged in.')
	_folder = _username
	SendMessage('You are logged in.', _connectionSocket)
	return _username, _folder, 1, _password

def GetUsernameAndPassword (message):
	global _delimiter
	return message.split(_delimiter)

def SendMessage (message, socket):
	socket.send(message)

def ReceiveMessage(socket):
	return socket.recv(1024)

def CreateNewPortAndSend(actualPort, _socket):
	_connectionSocket, _client = _socket.accept()
	SendMessage(str(actualPort), _connectionSocket)
	time.sleep(0.1)
	_port, _client, _socket, _connectionSocket = SetSocket(actualPort)
	_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
	_socket.bind(('', _port))
	_socket.listen(10)
	_connectionSocket, _client = _socket.accept()
	return _connectionSocket

def ServerThread(_connectionSocket):
	global numbOfThreads
	autorizar = 0
	_username = ''
	_password = '' 
	_folder = '' 
	_stillConnected = 1
	while (autorizar == 0):
		time.sleep(0.1)
		_username, _folder, autorizar, _password = Authorize(_connectionSocket, _username, _password, _delimiter, _folder)
	while _stillConnected:
		time.sleep(0.1)
		command = ReceiveMessage(_connectionSocket)
		_folder, _stillConnected = ExecuteCommand(command, _connectionSocket, _username, _password, _folder)
	print(_username + ' logged out.')
	numbOfThreads = numbOfThreads - 1


def CallServer(_socket):
	global _delimiter, numbOfThreads
	print('You are the server')
	ActualPort = 40000
	numbOfThreads = 0
	while 1:
		time.sleep(0.3)
		ActualPort = ActualPort + 1000
		_connectionSocket = CreateNewPortAndSend(ActualPort, _socket)
		threads = []
		t = threading.Thread(target=ServerThread, args=(_connectionSocket, ))
		threads.append(t)
		t.start()


#Neutral functions
def AmIServer(_socket):
	try:
		_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
		_socket.bind(('172.20.4.194', _port))
		_socket.listen(10)
		return _socket, 1

	except Exception:
		return _socket, 0

def SetSocket(_port):
	_client = ('172.20.4.194', _port)
	_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	_connectionSocket = socket.socket()
	return _port, _client, _socket, _connectionSocket

def EndConnection(_socket):
	_stillConnected = 0
	_socket.close()

def UploadFile(fileName, SendSocket, folder):
	global uploadPort, uploadHost, uploadSocket, uploadConnectionSocket
	skt = socket.socket()
	uploadHost = socket.gethostbyname("172.20.4.194")
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
	uploadHost = socket.gethostbyname("172.20.4.194")
	uploadPort = 15500
	skt.bind((uploadHost, uploadPort))
	file = open(folder + fileName, 'wb')
	skt.listen(50)

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
_displayReport = 1
_stillConnected = 1
_username = ''
_password = ''
_delimiter = '@#!@!#!@!$!#!#@#!!'
_folder = ' '
_port, _client, _socket, _connectionSocket = SetSocket(12000)
_socket, amIServer = AmIServer(_socket)
if amIServer:
	CallServer(_socket)
else:
	CallClient(_socket)
