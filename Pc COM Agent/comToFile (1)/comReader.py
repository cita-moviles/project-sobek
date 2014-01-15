__author__ = 'Miguel'

import serial
import comFunctions
import writeToFile
from writeToFile import *
import atexit

print("Available ports:\n")

portList = comFunctions.getAvailablePorts()


while 1:
        serialPort = serial.Serial("/dev/tty.usbserial-AH01CRV0")

        #serialPort.write(bytearray("Write data:", 'ascii'))

        while serialPort.inWaiting() < 1:
            pass

        dataIn = serialPort.readline()

        formattedData = comFunctions.formatMoistureData(dataIn)

        for x in range(0, len(dataIn)):
            print(dataIn[x])

        if formattedData == "Timeout received":
            writeToFile(formattedData)
        else:
            writeToFile(formattedData)
            writeToFile.setDate(datetime.datetime.now())

        serialPort.close()