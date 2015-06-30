__author__ = 'luishoracio'
from socket import socket, AF_INET, SOCK_DGRAM
from models import MessageProcessor
from Utils import FileWriter
import sys
import time



PORT = 4580


def sobek_server(address):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str (msg[0]) + ' Message ' + msg[1]
        sys.exit()

    sock.bind (address)
    print('Connected to port ' + str (PORT))
    while True:
        print('Waiting for data')
        msg, addr = sock.recvfrom (1024)

        if not msg:
            print('No data received')
            break
        start_time = time.time()
        print('Got message from', addr)

        FileWriter.writeToFile(msg)
        return_value = MessageProcessor.process_message(msg)

        print return_value
        print("--- %s seconds ---" % (time.time() - start_time))
        sock.sendto(return_value, addr)


if __name__ == '__main__':
    sobek_server (('', PORT))
