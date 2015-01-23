#!/usr/local/bin/python
# coding: utf-8

import ConfigParser
import sys

sys.path.insert(0, '../lnetatmo')
import lnetatmo


try:
    import Adafruit_DHT
except ImportError:
    pass

class Sensor:
    def __init__(self):
        self.humidity = None
        self.temperature = None

    def data_available(self):
        raise NotImplementedError( "Should have implemented this" )

    def getHumidity(self):
        #print("Sensor: getHumidity() %s" % self.humidity)
        assert self.humidity
        return self.humidity

    def getTemperature(self):
        #print("Sensor: getTemperature() %s" % self.temperature)
        assert self.temperature
        return self.temperature

class NetatmoSensor(Sensor):
    def __init__(self, netatmoName):
        Sensor.__init__(self)
        self.netatmoName = netatmoName
        self.natatmoAuthorization = None
        self.netatmoDevList = None

    def data_available(self):
        if not self.netatmoDevList:

            if self.natatmoAuthorization == None:
                config = ConfigParser.ConfigParser()
                config.read("netatmo-auth.cfg")

                if config.get("Netatmo_Auth", "clientsecret") == "":
                    raise RuntimeError('Netatmo authentication information are missing in netatmo-auth.cfg')

                self.natatmoAuthorization = lnetatmo.ClientAuth( clientId = config.get("Netatmo_Auth", "clientid"),
                                                                 clientSecret = config.get("Netatmo_Auth", "clientsecret"),
                                                                 username = config.get("Netatmo_Auth", "username"),
                                                                 password = config.get("Netatmo_Auth", "password") )

                if self.natatmoAuthorization == None:
                    print('Netatmo authentication failed')
                    return False
            
            self.netatmoDevList = lnetatmo.DeviceList(self.natatmoAuthorization)

            if self.netatmoDevList == None:
                print('Could not get Netatmo device list')
                return False

        self.humidity = self.netatmoDevList.lastData()[self.netatmoName]['Humidity']
        self.temperature = self.netatmoDevList.lastData()[self.netatmoName]['Temperature']

        return True

class DemoSensor(Sensor):
    def __init__(self, temperature, humidity):
        Sensor.__init__(self)
        self.t = temperature
        self.h = humidity

    def gather_data(self):
        self.temperature = self.t
        self.humidity = self.h
        return True


class AM2302Sensor(Sensor):
    def __init__(self, pin):
        Sensor.__init__(self)

    def gather_data(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, pin)

        if self.humidity is not None and self.temperature is not None:
            return True
        else:
            return False


class Actor:
    name = "Actor-with-no-name"

    def setPowerOn(self, on):
        raise NotImplementedError( "Should have implemented this" )

    def is_on(self):
        raise NotImplementedError( "Should have implemented this" )        

class DemoActor(Actor):
    def __init__(self, name):
        self.name = name

    def setPowerOn(self, on):
        print( "Switching actor %s to %r" % (self.name, on) )

    def is_on(self):
        return True

class PaspberrypiActor(Actor):
    pin = -1

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def setPowerOn(self, on):
        GPIO.output(self.pin, on)

    def is_on(self):
        return GPIO.input(self.pin)


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
            print ("%s" % room)

    return rooms



