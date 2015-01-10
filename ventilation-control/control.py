#!/usr/local/bin/python
# coding: utf-8

import building
import database
from datetime import datetime
from datetime import timedelta

def stop_ventilation(room, db):
    # power off actor
    room.actor.setPowerOn(False)

    # save power off time to db
    c = db.cursor()
    c.execute('SELECT rowid FROM actor_status WHERE room=? AND powered_off IS NULL ORDER BY powered_on DESC', (room.name, ))
    row = c.fetchone()

    if row:
        c.execute('UPDATE actor_status SET powered_off = ?  WHERE rowid = ?', (datetime.now(), row[0]))
        db.commit()
    else:
        print("Actor of room %s is OFF based on DB but requested to be switched off again" % (room.name, ))


def start_ventilation(room, db):
    # power on actor
    room.actor.setPowerOn(True)

    # save power on time to db
    c = db.cursor()
    c.execute('SELECT rowid FROM actor_status WHERE room=? AND powered_off IS NULL ORDER BY powered_on DESC', (room.name, ))
    row = c.fetchone()

    if not row:
        c.execute('INSERT INTO actor_status(room, powered_on) VALUES(?,?)', (room.name, datetime.now()))
        db.commit()
    else:
        print("Actor of room %s is ON based on DB but requested to be switched on again" % (room.name, ))


def process_room(room, db):
    # get recommendation
    c = db.cursor()
    c.execute('SELECT ventilation_recommended FROM weather WHERE room=? ORDER BY date DESC', (room.name, ))
    row = c.fetchone()

    ventilation_recommended = False
    
    if row:
        ventilation_recommended = row[0]

    # get actor status
    c.execute('SELECT powered_on FROM actor_status WHERE room = ? AND powered_off IS NULL', (room.name, ))
    row = c.fetchone()

    if not row:
        # no entry yet for room: power on actor if recommended by weather

        # TODO check if we are in the greace periode and are not allowed to switch on !!!!!

        if ventilation_recommended:
            print("New Entry - Start ventilation for %s"% (room.name, ))
            start_ventilation(room, db)
    else:
        # actor was enabled before. Check if it
        powered_on_time = row[0]

        print("powered on %s, powered on until %s, now %s" % (powered_on_time, powered_on_time + timedelta(minutes=room.ventilationDuration), datetime.now()))

        # should actor be on?
        if  powered_on_time + timedelta(minutes=room.ventilationDuration) < datetime.now():
            # should be off
            if room.actor.is_on():
                print("Stop ventilation for %s"% (room.name, ))
                stop_ventilation(room, db)
            else:
                print("Ventilation in %s already stopped"% (room.name, ))

        else:
            # should be on
            if not room.actor.is_on():
                print("Start ventilation for %s again"% (room.name, ))
                start_ventilation(room, db)
            else:
                print("Ventilation in %s already running"% (room.name, ))


def main():

    db = None

    try:
        db = database.connect_db()
        rooms = building.getRooms()

        for room in rooms:
            process_room(room, db)

    finally:
        if db:
            db.close()


if __name__ == '__main__':
    main()
