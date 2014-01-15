__author__ = 'Miguel'
import datetime

# Make file of data received ---------------------------------------
date = None

def setDate(exactTime):
   global date
   date = exactTime

def getDate():
    global date
    return date



def writeToFile(dataToWrite):
    with open("dataLog%s.txt" % (str(getDate())), 'w') as file:
        for dataLineToWrite in dataToWrite:
            file.write(str(dataLineToWrite) + "\n")

    print("Data written successfully")
#-------------------------------------------------------------------