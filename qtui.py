#!/usr/bin/env python3

import sys
from PyQt4 import QtGui, QtCore, uic
import logging
import zmq


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
            self.message.emit("test")


class ThermostatApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.thread = QtCore.QThread()

        self.ui = uic.loadUi('thermostat.ui')
        self.ui.show()

        self.connect(self.ui.forceButton, QtCore.SIGNAL("clicked()"), self.boiler_force)
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.check_boiler)
        self.timer.start(1000)

        self.listener = BoilerStatusListener()
        self.listener.moveToThread(self.thread)
        self.thread.started.connect(self.listener.loop)
        self.listener.message.connect(self.signal_received)
        self.signal_received("test")

        QtCore.QTimer.singleShot(0, self.thread.start)
        # self.ui.forceButton.setEnabled(True)

    def boiler_force(self):
        logging.debug("Force boiler to on")

    def check_boiler(self):
        logging.debug("Check if boiler can be enabled")

    def timer(self):
        logging.debug("timer called")

    def signal_received(self, message):
        logging.debug("Message: %s" % message)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QtGui.QApplication(sys.argv)
    win = ThermostatApp()
    sys.exit(app.exec_())


