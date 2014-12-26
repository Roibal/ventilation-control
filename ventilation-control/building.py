#!/usr/local/bin/python
# coding: utf-8

import ConfigParser
import sys

sys.path.insert(0, '../lnetatmo')
import lnetatmo

natatmoAuthorization = None
netatmoDevList = None
args = None

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
        #print("DEMO: getHumidity() %s" % self.humidity)
        return self.humidity

    def getTemperature(self):
        #print("DEMO: getTemperature() %s" % self.temperature)
        return self.temperature

class Room:
    name = "Room-with-no-name"
    insideSensor = None
    outsideSensor = None
    minInsideTemp = 0.0
    minHumidDiff = 0.0

    def __str__(self):
        return "Room: " + self.name + "\n" + \
            "  Temperature(in/out): " + \
            str(self.insideSensor.getTemperature()) + " / " + \
            str(self.outsideSensor.getTemperature()) + \
            "\n" + \
            "  Humidity(in/out): " + \
            str(self.insideSensor.getHumidity()) + " / " + \
            str(self.outsideSensor.getHumidity()) + \
            "\n" + \
            "  Minimum inside temperatur: " + str(self.minInsideTemp) + \
            "\n" + \
            "  Minimum Humidity difference: " + str(self.minHumidDiff)

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
    section = "Room_" + roomName
    insideSensorName = config.get(section, "InsideSensor")
    outsideSensorName = config.get(section, "OutsideSensor")

    room = Room()
    room.name = roomName
    room.insideSensor = getSensorByName(config, insideSensorName)
    room.outsideSensor = getSensorByName(config, outsideSensorName)
    room.minInsideTemp = config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")
    room.minHumidDiff = config.getfloat(section, "MinimumHumidityDifference")

    return room


def getRooms():
    config = ConfigParser.ConfigParser()
    config.read("ventilation.cfg")

    rooms = []
    
    # create every configured room with its sensors
    sections = config.sections()
    for section in sections:
        sectionParts = section.split("_")

        sectionType = sectionParts[0]
        if sectionType == "Room":
            roomName = sectionParts[1]
            room = createRoom(config, roomName)
            rooms.append(room)
            print ("%s" % room)

    return rooms



