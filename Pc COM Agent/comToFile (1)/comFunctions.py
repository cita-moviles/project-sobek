__author__ = 'Miguel'

import serial
import datetime

comInSystem = []
moistureLog = {"area_id": "",
               "height1": "", "moistureHB1": "", "moistureLB1": "",
               "height2": "", "moistureHB2": "", "moistureLB2": "",
               "height3": "", "moistureHB3": "", "moistureLB3": "",
               "timeout": "", "min": "", "max": "", "date": "","soh":"","eot":""}
#weatherData = {"area_id":"", "temperature":"", "solar_intensity":"", "windspeed":"", "humidity":"", "air_pressure":"",
#               "ET":"", "date":""}

# Get a list of available COM ports in the system ------------------
def getAvailablePorts():
    for i in range(0, 255):
        try:
            avPort = serial.Serial(i)
            comInSystem.append("COM" + str(i+1))
            avPort.close()
        except serial.SerialException:
            pass

    return comInSystem
#-------------------------------------------------------------------

# Format received string -------------------------------------------
def formatMoistureData(dataIn):
    #Get SOH
    moistureLog["soh"] = str(dataIn[15])

    # Get area_id
    moistureLog["area_id"] = str(dataIn[16])

    # Get height_id 1
    moistureLog["height1"] = str(dataIn[17])

    # Get moisture higher byte, "xx.__"
    moistureLog["moistureHB1"] = str(dataIn[18])

    # Get moisture lower byte, "__.xx"
    moistureLog["moistureLB1"] = str(dataIn[19])

    # Get height_id 2
    moistureLog["height2"] = str(dataIn[20])

    # Get moisture higher byte, "xx.__"
    moistureLog["moistureHB2"] = str(dataIn[21])

    # Get moisture lower byte, "__.xx"
    moistureLog["moistureLB2"] = str(dataIn[22])

    # Get height_id 3
    moistureLog["height3"] = str(dataIn[23])

    # Get moisture higher byte, "xx.__"
    moistureLog["moistureHB3"] = str(dataIn[24])

    # Get moisture lower byte, "__.xx"
    moistureLog["moistureLB3"] = str(dataIn[25])

    # Get the timeout
    moistureLog["timeout"] = int(dataIn[27])

    #Get the eol
    moistureLog["eot"] = str(dataIn[29])

    # Get min moisture value
    moistureLog["min"] = 20

    # Get max moisture value
    moistureLog["max"] = 30

    # Get date value
    date = datetime.datetime.now()
    moistureLog["date"] = str(date)

    if moistureLog["timeout"] == "1":
        formattedData = "Timeout received,%s" % ([moistureLog["date"]])
        return formattedData
    elif moistureLog["soh"] != "1" or moistureLog["eot"] != "4":
        formattedData = ["Message corrupted"]
        return formattedData
    else:
        dataHeight1 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height1"], moistureLog["moistureHB1"], moistureLog["moistureLB1"],
                                                     moistureLog["min"], moistureLog["max"], moistureLog["date"])
        dataHeight2 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height2"], moistureLog["moistureHB2"], moistureLog["moistureLB2"],
                                                     moistureLog["min"], moistureLog["max"], moistureLog["date"])
        dataHeight3 = "%s,%s,%s.%s,%s,%s,%s" % (moistureLog["area_id"], moistureLog["height3"], moistureLog["moistureHB3"], moistureLog["moistureLB3"],
                                                     moistureLog["min"], moistureLog["max"], moistureLog["date"])

        formattedData = [dataHeight1, dataHeight2, dataHeight3]

        return formattedData
#-------------------------------------------------------------------