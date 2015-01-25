#!/usr/local/bin/python
# coding: utf-8

import ConfigParser
from sensors import *
from actors import *

class Room:
    name = "Room-with-no-name"
    insideSensor = None
    outsideSensor = None
    actor = None
    minInsideTemp = 0.0
    minHumidDiff = 0.0
    ventilationDuration = 0.0
    ventilationQuietTime = 0.0

    def __str__(self):
        result = "No data available"

        if self.insideSensor.data_available() and self.outsideSensor.data_available():

            result = "Room: " + self.name + "\n" + \
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

        return result


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
    elif sensorType == "AM2302":
        pin = config.get(sensorName, "Pin")
        sensor = AM2302Sensor(pin)

    return sensor

def getActorByName(config, actorName):
    actorType = config.get(actorName, "Type")

    actor = None

    if actorType == "Demo":
        actor = DemoActor(actorName)
    elif actorType == "RaspberryPi":
        pin = config.get(actorName, "Pin")
        actor = RaspberrypiActor(actorName, pin)

    return actor

def createRoom(config, roomName):
    section = "Room_" + roomName
    insideSensorName = config.get(section, "InsideSensor")
    outsideSensorName = config.get(section, "OutsideSensor")
    actorName = config.get(section, "Actor")

    room = Room()
    room.name = roomName
    room.insideSensor = getSensorByName(config, insideSensorName)
    room.outsideSensor = getSensorByName(config, outsideSensorName)
    room.actor = getActorByName(config, actorName)
    room.minInsideTemp = config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")
    room.minHumidDiff = config.getfloat(section, "MinimumHumidityDifference")
    room.ventilationDuration = config.getfloat(section, "VentilationDurationInMinutes")
    room.ventilationQuietTime = config.getfloat(section, "QuietTimeBetweenVentilationInMinutes")

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
            #print ("%s" % room)

    return rooms



