__author__ = 'luishoracio'

import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 4580
MESSAGE = "!200 001 010 123 401 234#"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))