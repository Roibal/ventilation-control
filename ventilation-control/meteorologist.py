#!/usr/local/bin/python
# coding: utf-8

import sys
import argparse
import weathermath
import building
import database
from datetime import datetime

def processRoom(room, db):
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

    c = db.cursor()
    c.execute('insert into weather (date, room, inside_temperature, inside_humidity, ' +
              'outside_temperature, outside_humidity, ventilation_recommended) values ' +
              '(?, ?, ?, ?, ?, ?, ?)', (datetime.now(), room.name, insideTemp, insideRelHumid, outsideTemp, outsideRelHumid, recommendVentilation))
    db.commit()

def main():

    db = None

    try:
        db = database.connect_db()
        rooms = building.getRooms()

        for room in rooms:
            processRoom(room, db)

    finally:
        if db:
            db.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Meteorologist', version='%(prog)s 0.1')
        parser.add_argument('--clientid', type=str, help='Netatmo CLIENT_ID')
        parser.add_argument('--clientsecret', type=str, help='Netatmo CLIENT_SECRET')
        parser.add_argument('--username', type=str, help='Netatmo USERNAME')
        parser.add_argument('--password', type=str, help='Netatmo PASSWORD')
        building.args = parser.parse_args()
    else:
        print("No arguments given, running in DEMO mode")

    main()
