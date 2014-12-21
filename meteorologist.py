#!/usr/local/bin/python
# coding: ascii

import ConfigParser
import argparse
import sys

sys.path.insert(0, './lnetatmo')
import lnetatmo

def main(args):

    authorization = lnetatmo.ClientAuth( clientId = args.clientid,
                                         clientSecret = args.clientsecret,
                                         username = args.username,
                                         password = args.password
                                       )
    
    devList = lnetatmo.DeviceList(authorization)


    Config = ConfigParser.ConfigParser()
    Config.read("ventilation.cfg")
    sections = Config.sections()
    for section in sections:
        insideSensorName = Config.get(section, "InsideSensorName")
        outsideSensorName = Config.get(section, "OutsideSensorName")
        minInsideTemp = Config.getfloat(section, "MinimumInsideTemperaturInDegreeCentigrade")

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
    parser.add_argument('--clientid', type=str, required=True, help='Netatmo CLIENT_ID')
    parser.add_argument('--clientsecret', type=str, required=True, help='Netatmo CLIENT_SECRET')
    parser.add_argument('--username', type=str, required=True, help='Netatmo USERNAME')
    parser.add_argument('--password', type=str, required=True, help='Netatmo PASSWORD')
    args = parser.parse_args()
    main(args)
