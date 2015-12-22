#!/usr/bin/env python3

import sys
from PyQt4 import QtGui, QtCore, uic
import logging
from datetime import datetime


class Boiler(QtCore.QThread):
    STATE_ENABLED = 1
    STATE_DISABLED = 0
    STATE_CAN_BE_CHANGED = 1

    def __init__(self):
        logging.debug("New Boiler class created, ensure everything is disabled")
        self.current_state = self.STATE_DISABLED
        self.last_state = self.STATE_DISABLED
        self.last_event = datetime.now()
        self.switchoff()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.switchavailable)
        self.timer.start(1000)

    def force(self):
        logging.debug("Force boiler to on")

    def switchon(self):
        logging.debug("Boiler switch to on")

    def switchoff(self):
        logging.debug("Boiler switch to off")

    def switchavailable(self):
        logging.debug("Switchavailable called")
        if (not self.current_state and not self.last_state):
            return True
        else:
            return False


class ThermostatApp(QtGui.QMainWindow):
    def __init__(self, boiler):
        self.boiler = boiler
        QtGui.QMainWindow.__init__(self)

        self.ui = uic.loadUi('thermostat.ui')
        self.ui.show()

        self.connect(self.ui.forceButton, QtCore.SIGNAL("clicked()"), self.boiler_force)
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.check_boiler)
        self.timer.start(1000)

    def boiler_force(self):
        self.boiler.switchon()

    def check_boiler(self):
        logging.debug("Check if boiler can be enabled")
        if self.boiler.switchavailable():
            self.ui.forceButton.setEnabled(True)
        else:
            self.ui.forceButton.setEnabled(False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    boiler = Boiler()
    app = QtGui.QApplication(sys.argv)
    win = ThermostatApp(boiler)
    sys.exit(app.exec_())


