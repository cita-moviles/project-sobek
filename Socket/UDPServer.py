__author__ = 'luishoracio'
from socket import socket, AF_INET, SOCK_DGRAM
from models import MessageProcessor
from Utils import FileWriter
import sys
import time

PORT = 4580

def sobek_server(address):
    
    msg_processor = MessageProcessor()
    try:
        sock = socket(AF_INET, SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str (msg[0]) + ' Message ' + msg[1]
        sys.exit()

    h_f1, h_f2, h_f3 = "", "", ""
    received_gok = False
    sock.bind (address)
    print('Connected to port ' + str (PORT))
    while True:
        print('Waiting for data')
        msg, addr = sock.recvfrom (1024)

        #In case there's no message from GPRS
        if not msg:
            print('No data received')
            break
        start_time = time.time()
        print('Got message from', addr)

        if msg == 'GOK':
            received_gok = True

        FileWriter.writeToFile(msg)
        return_value = msg_processor.process_message(msg)

        if msg_processor.changed_f1 == True and received_gok == False:
            msg_processor.changed_f1 = False
            h_f1 = return_value
        elif msg_processor.changed_f2 == True and received_gok == False:
            msg_processor.changed_f2 = False
            h_f2 = return_value
        elif msg_processor.changed_f3 == True and received_gok == False:
            msg_processor.changed_f3 = False
            h_f3 = return_value

        print "***LOGGING***"
        print "H_F1 "+ h_f1 
        print "H_F2 " + h_f2 
        print "H_F3 " +h_f3
        print "Received -> ", received_gok

        if len(h_f1) > 0 and received_gok == False:
            print "Response: " + h_f1
            sock.sendto(h_f1, addr)
        elif len(h_f1) > 0 and received_gok == True:
            h_f1 = ""
            print "Response: ROK"
            received_gok = False
            sock.sendto('ROK', addr)
        elif len(h_f2) > 0 and received_gok == False:
            print "Response: " + h_f2
            sock.sendto(h_f2, addr)
        elif len(h_f2) > 0 and received_gok == True:
            print "Response: ROK"
            received_gok = False
            h_f2 = ""
            sock.sendto('ROK', addr)
        elif len(h_f3) > 0 and received_gok == False:
            print "Response: " + h_f3
            sock.sendto(h_f3, addr)
        elif len(h_f3) > 0 and received_gok == True:
            received_gok = False
            print "Response: ROK"
            h_f3 = ""
            sock.sendto('ROK', addr)
        else:
            print "Response: ROK"
            sock.sendto('ROK', addr)

        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    sobek_server (('', PORT))