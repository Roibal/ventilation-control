#!/usr/local/bin/python
# coding: ascii

import ConfigParser
import argparse
import sys

sys.path.insert(0, './lnetatmo')
import lnetatmo

def configureRoom(config, devlist, roomName):
    # create indoor sensor
    # create outdoor sensor
    # create room 

    insideSensorName = config.get(section, "InsideSensorName")
    outsideSensorName = config.get(section, "OutsideSensorName")
    minInsideTemp = config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")

    print ("Current inside temperature/humidity of sensor '%s': %s C / %s %%" %
            (
                insideSensorName,
                devList.lastData()[insideSensorName]['Temperature'],
                devList.lastData()[insideSensorName]['Humidity']
            )
          )
    print ("Current ouside temperature/humidity of sensor '%s': %s C / %s %%" %
            (
                outsideSensorName,
                devList.lastData()[outsideSensorName]['Temperature'],
                devList.lastData()[outsideSensorName]['Humidity']
            )
          )

def main(args):

    authorization = lnetatmo.ClientAuth( clientId = args.clientid,
                                         clientSecret = args.clientsecret,
                                         username = args.username,
                                         password = args.password
                                       )
    
    devList = lnetatmo.DeviceList(authorization)

    config = ConfigParser.ConfigParser()
    config.read("ventilation.cfg")
    
    # configure every room with its sensors
    sections = config.sections()
    for section in sections:
        sectionParts = section.split("_")

        sectionType = sectionParts[0]
        if sectionType == "Room":
            roomName = sectionParts[1]
            configureRoom(config, devlist, roomName)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
    parser.add_argument('--clientid', type=str, required=True, help='Netatmo CLIENT_ID')
    parser.add_argument('--clientsecret', type=str, required=True, help='Netatmo CLIENT_SECRET')
    parser.add_argument('--username', type=str, required=True, help='Netatmo USERNAME')
    parser.add_argument('--password', type=str, required=True, help='Netatmo PASSWORD')
    args = parser.parse_args()
    main(args)
