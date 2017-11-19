# -*- coding: utf-8 -*-
import socket
import threading
import time


shutdown = False

def receving(name, sock):
    while not shutdown:
        try:

            while True:
                data, addr = sock.recvfrom(1024)

                print str(data)
        except:
            pass


host = ''
port = 12002

server = ('172.20.18.20',12000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
#s.setblocking(0)

for i in range(5):
    threading.Thread(target=receving, args=("RecvThread",s)).start()


alias = raw_input("Name: ")
message = alias + " se juntou a conversa"
s.sendto(message, server)
while message != 'q':
    message = raw_input()
    if message != '':
        s.sendto(alias + ": " + message, server)


    time.sleep(0.1)

shutdown = True

s.close()