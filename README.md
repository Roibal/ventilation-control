ventilation-control
===================

This is a software system to realize a ventilation control based on python scripts running on a Raspberry Pi which drives fans based on data from attached sensors or Netatmo modules .
The primary goal is to bring down the humidity of a room using fans driving them based on indoor and outdoor temperature and humidity values.
The system mainly consists of two components. The meteorologist and control.

Meteorologist
=============

The meteorologist.py script fetches temperature and humidity data from configured sensors assigned to a room and computes a recommendation if ventilation should happen. All the data is saved in a sqlite database. 
Sensors can be components attached directly to the Raspberry Pi for example a DHT231 temperature/humidity sensor. Sensors can also wireless modules from Netatmo.

Control
=======

The control.py script starts and stops fans attached to a relay board attached to the Raspberry Pi based on the data in the sqlite database.

TODO
====
