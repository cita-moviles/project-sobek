__author__ = 'enriqueramirez'

from models import MessageProcessor
from Utils import FileWriter
from time import strftime
import os

def writeToFile (dataToWrite):
     if os.path.exists (os.path.abspath ('dataLog.txt')):
          with open ('dataLog.txt', 'a+') as file:
               file.write (strftime ("%Y-%m-%d %H:%M") + "," + dataToWrite + '\n')
     else:
          print('Log file created')
          with open ("dataLog.txt", 'w') as file:
               file.write (strftime ("%Y-%m-%d %H:%M") + "," + dataToWrite + '\n')

     print("Data written successfully")

msg = "!200001010123401234#"

MessageProcessor.process_message(msg)
FileWriter.writeToFile(msg)