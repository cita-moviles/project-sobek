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

        #Processes the message received and writes to a Log file
        FileWriter.writeToFile(msg)
        return_value = msg_processor.process_message(msg)
        #Holds the value for future use
        print return_value
        print " *** LOGGING *** "
        print " Received GOK -> ", received_gok
        print " Changed -> ", msg_processor.changed
        #Will send the message processed if there's a config, until there's a GOK reply
        if received_gok == False and msg_processor.changed == True:
            sock.sendto(return_value,addr)
        #Resets all the variables if there is a GOK reply
        elif received_gok == True:
            received_gok = False
            msg_processor.changed = False
            pass
        #If tehre is not a config, send ROK
        else:
            sock.sendto('ROK', addr)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    sobek_server (('', PORT))
