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

    def data_available(self):
        self.temperature = self.t
        self.humidity = self.h
        return True


class AM2302Sensor(Sensor):
    def __init__(self, pin):
        Sensor.__init__(self)
        self.pin = pin

    def data_available(self):
        self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.pin)

        if self.humidity is not None and self.temperature is not None:
            return True
        else:
            return False
