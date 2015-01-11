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
    print("Control is processing room %s -------------" % room.name)
    # get recommendation
    c = db.cursor()
    c.execute('SELECT ventilation_recommended FROM weather WHERE room=? ORDER BY date DESC', (room.name, ))
    row = c.fetchone()

    ventilation_recommended = False
    
    if row:
        ventilation_recommended = row[0]

    # get actor status
    c.execute('SELECT powered_on, powered_off FROM actor_status WHERE room = ? ORDER BY powered_on DESC', (room.name, ))
    row = c.fetchone()

    if not row:
        # no entry yet for room: power on actor if recommended by weather
        if ventilation_recommended:
            print("No entry for room. Starting ventilation.")
            start_ventilation(room, db)
    else:
        # actor was enabled before. Was it switched off again?
        powered_on_time = row[0]
        powered_off_time = row[1]

        if not powered_off_time:
            # was not switched off
            print("Ventilation is ON based on DB")
            # should actor still be on?
            if  powered_on_time + timedelta(minutes=room.ventilationDuration) < datetime.now():
                # should be off now
                if room.actor.is_on():
                    print("Actor status is ON but should be OFF now, stopping...")
                    stop_ventilation(room, db)
                else:
                    print("Actor status is OFF. Should be OFF anyhow, doing nothing.")

            else:
                # should be on
                if not room.actor.is_on():
                    print("Actor status is OFF but should be ON. Starting ventilation again.")
                    start_ventilation(room, db)
                else:
                    print("Actor status is ON and should be ON, doing nothing.")

        else:
            # was switched off
            print("Ventilation was ON and also switched OFF")
            # check if we should switch it on again
            # ventilationQuietTime
            if  powered_off_time + timedelta(minutes=room.ventilationQuietTime) < datetime.now():
                # switch on
                print("Ventilation Quiet time passed")

                if ventilation_recommended:
                    print("Ventilation recommended, starting ventilation")
                    start_ventilation(room, db)

            else:
                print("Ventilation Quiet time in effect. Doing nothing.")




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
