#!/usr/bin/env python3

#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server


if __name__ == '__main__':
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")

    # Subsribe to 'boiler' topic
    socket.setsockopt_string(zmq.SUBSCRIBE, 'boiler')

    while True:
        json = socket.recv_string()
        print(json)
