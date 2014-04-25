__author__ = 'admin'
 
# Echo client program
import socket
import sys
import time
 
HOST = 'localhost'#10.32.70.126'  # The remote host
PORT = 4580  # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except socket.error as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print 'could not open socket'
    sys.exit(1)
message_list = ["!200001010123401234#", "!100 002 020 530 540 60-170#"]

time.sleep(1    )

for message in message_list:
    print message
    s.sendall(message)
 
data = s.recv(1024)
s.close()
print 'Received', repr(data)