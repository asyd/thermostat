#!/usr/bin/env python3

import sys
from PyQt4 import QtGui, QtCore, uic
import logging


class Boiler(object):
    def __init__(self):
        #
        self.state = False
        logging.debug("New Boiler class created")

    def force(self):
        logging.debug("Force boiler to on")

    def ping(self):
        logging.debug("boiler: ping")


class ThermostatApp(QtGui.QMainWindow):
    def __init__(self, boiler):
        self.boiler = boiler
        QtGui.QMainWindow.__init__(self)

        self.ui = uic.loadUi('thermostat.ui')
        self.ui.show()

        self.connect(self.ui.forceButton, QtCore.SIGNAL("clicked()"), self.boiler.ping)
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.boiler.ping)
        self.timer.start(1000)

    def boiler_force(self):
        self.boiler.force()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    boiler = Boiler()
    app = QtGui.QApplication(sys.argv)
    win = ThermostatApp(boiler)
    sys.exit(app.exec_())


