__author__ = 'luishoracio'

import socket

UDP_IP = "riego.chi.itesm.mx"
# UDP_IP = "localhost"
UDP_PORT = 4580
MESSAGE = "!20000000043861312400,1-1#"
#MESSAGE ="!50000101289600679420718-106.0925920028.6701220,0#"
#MESSAGE = "!10000100173516851+34568,#!10000200173516851+34568,#!20002100043861312400,85#!40003100173+5168518755688102,#"
#MESSAGE = "!50000101289600679420719-106.0771050028.67532814/06/12,16:27:40#!10000100173516851+34568,#!10000200173516851+34568,#!20002100043861312400,85#!40003100173+5168518755688102,#"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sen
o(MESSAGE, (UDP_IP, UDP_PORT))