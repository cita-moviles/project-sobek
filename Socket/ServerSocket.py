__author__ = 'luishoracio'

import socket
import threading
import struct
import string
from models import MessageProcessor
from socket import error as SocketError
import errno


class clientThread(threading.Thread):
    def __init__(self, serv):
        threading.Thread.__init__(self)
        self.server = serv
        self.clientList = []
        self.running = True
        print("Client thread created. . .")

    def run(self):
        print("Beginning client thread loop. . .")
        while self.running:
            for client in self.clientList:
                try:
                    message = client.sock.recv(self.server.BUFFSIZE)
                    if message != None and message != "":
                        #respond to messages
                        client.update(message)
                except SocketError as e:
                    print "ERROR " + str(e.errno)
                    if e.errno != errno.ECONNRESET:
                        raise  # Not error we are looking for
                    pass


class clientObject(object):
    def __init__(self, clientInfo):
        self.sock = clientInfo[0]
        self.address = clientInfo[1]
        self.timeout = 900

    def update(self, message):
        self.sock.send("OK")
        MessageProcessor.process_message(message)



class Server(object):
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 4580
        self.BUFFSIZE = 1024
        self.ADDRESS = (self.HOST, self.PORT)
        self.clientList = []
        self.running = True
        self.serverSock = socket.socket()
        self.serverSock.bind(self.ADDRESS)
        self.serverSock.listen(2)
        self.clientThread = clientThread(self)
        print("Starting client thread. . .")
        self.clientThread.start()
        print("Awaiting connections. . .")
        while self.running:
            clientInfo = self.serverSock.accept()
            print("Client connected from {}.".format(clientInfo[1]))
            self.clientThread.clientList.append(clientObject(clientInfo))

        self.serverSock.close()
        print("- end -")


serv = Server()