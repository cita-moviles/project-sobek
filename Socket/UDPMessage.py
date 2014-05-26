__author__ = 'luishoracio'

import socket

UDP_IP = "riego.chi.itesm.mx"
#UDP_IP = "localhost"
UDP_PORT = 4580
#MESSAGE = "!200001010123401234,#"
MESSAGE = "!10000100173516851+34568,#!10000200173516851+34568,#!20002100043861312400,85#!40003100173+5168518755688102,#"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))