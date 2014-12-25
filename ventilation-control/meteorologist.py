#!/usr/local/bin/python
# coding: utf-8

import ConfigParser
import argparse
import sys

sys.path.insert(0, '../lnetatmo')
import lnetatmo

import weathermath

# globals
args = None
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
        return getNetatmoDevList().lastData()[self.netatmoName]['Humidity']

    def getTemperature(self):
        #print("Trying to get Temperature from %s" % self.netatmoName)
        return getNetatmoDevList().lastData()[self.netatmoName]['Temperature']

class DemoSensor(Sensor):
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity

    def getHumidity(self):
        return self.humidity

    def getTemperature(self):
        return self.temperature

class Room:
    name = "Room-with-no-name"
    insideSensor = None
    outsideSensor = None
    minInsideTemp = 0.0
    minHumidDiff = 0.0

    def __str__(self):
        return "Room: " + self.name + ", Temperature(in/out): " + str(self.insideSensor.getTemperature()) + " / " + str(self.outsideSensor.getTemperature())



def getSensorByName(config, sensorName):
    sensorType = config.get(sensorName, "Type")

    sensor = None

    if sensorType == "Netatmo":
        netatmoName = config.get(sensorName, "NetatmoName")
        sensor = NetatmoSensor(netatmoName)
    elif sensorType == "Demo":
        temperature = config.getfloat(sensorName, "Temperature")
        humidity = config.getfloat(sensorName, "Humidity")
        sensor = DemoSensor(temperature, humidity)

    return sensor


def createRoom(config, roomName):
    # create indoor sensor
    # create outdoor sensor
    # create room

    section = "Room_" + roomName

    insideSensorName = config.get(section, "InsideSensor")
    outsideSensorName = config.get(section, "OutsideSensor")
    minInsideTemp = config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")
    minHumidDiff = config.getfloat(section, "MinimumHumidityDifference")

    room = Room()
    room.insideSensor = getSensorByName(config, insideSensorName)
    room.outsideSensor = getSensorByName(config, outsideSensorName)

    return room


def getNetatmoDevList():
    global natatmoAuthorization
    global netatmoDevList

    if natatmoAuthorization == None:
        #print ("%s %s %s %s" % (args.clientid, args.clientsecret, args.username, args.password))
        natatmoAuthorization = lnetatmo.ClientAuth( clientId = args.clientid,
                                         clientSecret = args.clientsecret,
                                         username = args.username,
                                         password = args.password
                                       )
    
        netatmoDevList = lnetatmo.DeviceList(natatmoAuthorization)

        return netatmoDevList


def configureRoom(room):
    insideTemp = room.insideSensor.getTemperature()
    insideRelHumid = room.insideSensor.getHumidity()
    insideAbsHumid = weathermath.AF(insideRelHumid, insideTemp)

    outsideTemp = room.outsideSensor.getTemperature()
    outsideRelHumid = room.outsideSensor.getHumidity()
    outsideAbsHumid = weathermath.AF(outsideRelHumid, insideTemp)

    recommendVentilation = False

    if insideAbsHumid - room.minHumidDiff > outsideAbsHumid:
        recommendVentilation = True

    if insideTemp <= room.minInsideTemp:
        recommendVentilation = False


def main():

    rooms = []

    config = ConfigParser.ConfigParser()
    config.read("ventilation.cfg")
    
    # configure every room with its sensors
    sections = config.sections()
    for section in sections:
        sectionParts = section.split("_")

        sectionType = sectionParts[0]
        if sectionType == "Room":
            roomName = sectionParts[1]
            room = createRoom(config, roomName)
            rooms.append(room)
            #print ("%s" % room)

    for room in rooms:
        configureRoom(room)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
        parser.add_argument('--clientid', type=str, help='Netatmo CLIENT_ID')
        parser.add_argument('--clientsecret', type=str, help='Netatmo CLIENT_SECRET')
        parser.add_argument('--username', type=str, help='Netatmo USERNAME')
        parser.add_argument('--password', type=str, help='Netatmo PASSWORD')
        args = parser.parse_args()
    else:
        print("No arguments given, running in DEMO mode")

    main()
