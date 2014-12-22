#!/usr/local/bin/python
# coding: ascii

import ConfigParser
import argparse
import sys

sys.path.insert(0, './lnetatmo')
import lnetatmo

# globals
natatmoAuthorization = None
netatmoDevList = None

class Sensor:
    def getHumidity(self):
        raise NotImplementedError( "Should have implemented this" )
    def getTemperature(self):
        raise NotImplementedError( "Should have implemented this" )

class NetatmoSensor(Sensor):
    def __init__(self, netatmoName):
        self.netatmoName = netatmoName

    def getHumidity(self):
        #print("Trying to get Humidity from %s" % self.netatmoName)
        return netatmoDevList.lastData()[self.netatmoName]['Humidity']

    def getTemperature(self):
        #print("Trying to get Temperature from %s" % self.netatmoName)
        return netatmoDevList.lastData()[self.netatmoName]['Temperature']


def getSensorByName(config, sensorName):
    sensorType = config.get(sensorName, "Type")

    sensor = None

    if sensorType == "Netatmo":
        netatmoName = config.get(sensorName, "NetatmoName")
        sensor = NetatmoSensor(netatmoName)

    return sensor


def configureRoom(config, roomName):
    # create indoor sensor
    # create outdoor sensor
    # create room

    section = "Room_" + roomName

    insideSensorName = config.get(section, "InsideSensor")
    outsideSensorName = config.get(section, "OutsideSensor")
    minInsideTemp = config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")

    insideSensor = getSensorByName(config, insideSensorName)

    print ("Room %s, Sensor %s: Temperature %s C, Humidity %s %%" %
            (
                roomName,
                insideSensor.netatmoName,
                insideSensor.getTemperature(),
                insideSensor.getHumidity()
            )
          )

def main(args):

    global natatmoAuthorization
    #print ("%s %s %s %s" % (args.clientid, args.clientsecret, args.username, args.password))
    natatmoAuthorization = lnetatmo.ClientAuth( clientId = args.clientid,
                                         clientSecret = args.clientsecret,
                                         username = args.username,
                                         password = args.password
                                       )
    
    global netatmoDevList
    netatmoDevList = lnetatmo.DeviceList(natatmoAuthorization)

    config = ConfigParser.ConfigParser()
    config.read("ventilation.cfg")
    
    # configure every room with its sensors
    sections = config.sections()
    for section in sections:
        sectionParts = section.split("_")

        sectionType = sectionParts[0]
        if sectionType == "Room":
            roomName = sectionParts[1]
            configureRoom(config, roomName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
    parser.add_argument('--clientid', type=str, required=True, help='Netatmo CLIENT_ID')
    parser.add_argument('--clientsecret', type=str, required=True, help='Netatmo CLIENT_SECRET')
    parser.add_argument('--username', type=str, required=True, help='Netatmo USERNAME')
    parser.add_argument('--password', type=str, required=True, help='Netatmo PASSWORD')
    args = parser.parse_args()
    main(args)
