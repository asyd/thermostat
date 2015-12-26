#!/usr/bin/env python3

import sys
import logging
import zmq
import json
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class BoilerStatusListener(QtCore.QObject):
    message = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QObject.__init__(self)

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://localhost:5555')

        # Connect to boiler topic
        self.socket.setsockopt_string(zmq.SUBSCRIBE, 'boiler')
        self.running = True

    def loop(self):
        while self.running:
            string = self.socket.recv_string()
            logging.debug("Receive message %s from 0mq" % string)
            # Remove topic
            string = string.replace('boiler ', '', 1)
            # self.message.emit(string)


class ThermostatApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.thread = QtCore.QThread()
        self.test = False

        self.ui = uic.loadUi('thermostat.ui')
        self.ui.show()

        self.ui.forceButton.clicked.connect(self.boiler_force)
        # self.connect(self.ui.forceButton, QtCore.SIGNAL("clicked()"), self.boiler_force)
        #
        # self.listener = BoilerStatusListener()
        # self.listener.moveToThread(self.thread)
        # self.thread.started.connect(self.listener.loop)
        # self.listener.message.connect(self.signal_received)
        #
        # QtCore.QTimer.singleShot(0, self.thread.start)
        # # Disable the force button by default
        # self.ui.forceButton.setEnabled(False)

    def boiler_force(self):
        logging.debug("Force boiler to on")

    def timer(self):
        logging.debug("timer called")

    def signal_received(self, message):
        logging.debug("signal_received: %s" % message)
        # try:
        boiler = json.loads(message)
        if boiler['status'] == 0:
            self.ui.forceButton.setEnabled(True)
            self.ui.forceButton.setFocus()
            self.ui.forceButton.repaint()
        # except Exception as e:
        #     logging.critical("Exception in signal_received: %s" % e.__str__())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)
    win = ThermostatApp()
    sys.exit(app.exec_())


