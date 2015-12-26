#!/usr/bin/env python3


#
# This is the main (and the only one) process that manage the boiler.
#


import time
import datetime
import zmq
import logging
import threading
import json


PUB_INTERVAL = 10


class Boiler(object):
    STATE_ENABLED = 1
    STATE_DISABLED = 0
    STATE_CAN_BE_CHANGED = 1

    def __init__(self):
        logging.debug("New Boiler class created, ensure everything is disabled")
        self.current_state = self.STATE_DISABLED
        self.current_temp = 'NA'
        self.last_state = self.STATE_DISABLED
        self.last_event = datetime.datetime.now()
        self.switchoff()

    def switchon(self):
        logging.debug("Boiler switch to on")

    def switchoff(self):
        logging.debug("Boiler switch to off")

    def json_status(self):
        return json.dumps({'status': self.current_state, 'temperature': 'NA'})


def status_publisher():
    # Send boiler current status to subscribers, every 10s, in the topic 'boiler'
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    boiler = Boiler()

    while True:
        socket.send_string('boiler ' + str(boiler.json_status()))
        time.sleep(PUB_INTERVAL)


def command_puller():
    # Received command
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")
    while True:
        buffer = socket.recv_string()
        print("command received: %s" % buffer)
        socket.send_string("OK")


if __name__ == "__main__":
    t = threading.Thread(target=status_publisher)
    t.daemon = True
    t.start()

    command_puller()
