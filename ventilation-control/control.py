#!/usr/local/bin/python
# coding: utf-8

def stop_ventilation():


def start_ventilation(room, db):
    # power on actor
    room.actor.setPowerOn(True)

    # save power on time to db
    c = db.cursor()
    c.execute('SELECT rowid, powered_on FROM actor_status WHERE room=?', (room.name, ))
    row = c.fetchone()

    if not row:
        c.execute('INSERT INTO actor_status(room, powered_on) VALUES(?,?)', (room.name, datetime.now()))
        db.commit()
    else:
        c.execute('UPDATE actor_status SET powered_on = ? WHERE rowid = ?', (datetime.now(), row['rowid']))
        db.commit() 


def process_room(room, db):
    # get recommendation
    c = db.cursor()
    c.execute('select ventilation_recommended from weather where room=? order by date desc', (room.name, ))
    row = c.fetchone()

    ventilation_recommended = false
    
    if row not None:
        ventilation_recommended = row['ventilation_recommended']

    # get actor status
    c = db.cursor()
    c.execute('select powered_on from actor_status where room=?', (room.name, ))
    row = c.fetchone()

    if not row:
        # no entry yet for room: power on actor if recommended by weather
        if ventilation_recommended:
            start_ventilation(room, db)
    else:
        # actor was enabled before. Check if it

        # 1. should be on

        # 2. should be of

        # switch on otherwise

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
