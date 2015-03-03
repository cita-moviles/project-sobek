__author__ = 'citacita'

from socket import socket, AF_INET, SOCK_DGRAM
import sys

PORT = 4582

def test_server(address):
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str (msg[0]) + ' Message ' + msg[1]
        sys.exit()

    sock.bind(address)
    print('Connected to port ' + str (PORT))
    while True:
        print('Waiting for data')
        msg, addr = sock.recvfrom (1024)

        if not msg:
            print('No data received')
            break

        print('Got message from', addr)

        return_value = 'ROK'


        sock.sendto(return_value, addr)
        print 'RESPONSE: ' + return_value

if __name__ == '__main__':
    test_server(('', PORT))