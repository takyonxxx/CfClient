#!/usr/bin/env python

import logging
import time
from threading import Thread

import imutils
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.uic.uiparser import QtCore
from imutils import video

import cfclient
from cfclient.ui.tab import Tab
from imutils.video import FileVideoStream
from imutils.video import FPS
import cv2

from cfclient.ui.tabs import GoProCamera, constants

GOPRO_IP = '10.5.5.9'
GOPRO_MAC = '064169dfa33e'

__author__ = 'Turkay TB'
__all__ = ['GoProTab']

logger = logging.getLogger(__name__)

gopro_tab_class = uic.loadUiType(cfclient.module_path + "/ui/tabs/goproTab.ui")[0]


class GoProTab(Tab, gopro_tab_class):
    """Tab for plotting logging data"""

    _connected_signal = pyqtSignal(str)
    _disconnected_signal = pyqtSignal(str)
    _log_data_signal = pyqtSignal(int, object, object)
    _log_error_signal = pyqtSignal(object, str)
    _param_updated_signal = pyqtSignal(str, str)

    def __init__(self, tabWidget, helper, *args):
        super(GoProTab, self).__init__(*args)
        self.setupUi(self)

        self.tabName = "GoPro"
        self.menuName = "GoPro Tab"
        self.tabWidget = tabWidget
        self.goproCamera = None
        self.stopped = False

        self._helper = helper

        # Always wrap callbacks from Crazyflie API though QT Signal/Slots
        # to avoid manipulating the UI when rendering it
        self._connected_signal.connect(self._connected)
        self._disconnected_signal.connect(self._disconnected)
        self._log_data_signal.connect(self._log_data_received)
        self._param_updated_signal.connect(self._param_updated)

        # Connect the Crazyflie API callbacks to the signals
        self._helper.cf.connected.add_callback(
            self._connected_signal.emit)

        self._helper.cf.disconnected.add_callback(
            self._disconnected_signal.emit)

        self.textConsole.setStyleSheet("font: 10pt; color: #00cccc; background-color: #001a1a;")
        self._gopro_connect_btn.setStyleSheet("font-size: 10pt;  color: white;background-color: #074666;")
        self._gopro_connect_btn.clicked.connect(self._gopro_connect)
        self.stream_start_thread = Thread(target=self.start_stream, args=())
        self.stream_stop_thread = Thread(target=self.stop_stream, args=())
        self.stream_play_thread = Thread(target=self.play_stream, args=())
        self.fvs = None
        self.fps = None
        self.stop = False

    def start_stream(self):
        self.goproCamera.livestream("stop")
        self.goproCamera.stream("udp://@127.0.0.1:10000", quality="high")

    def stop_stream(self):
        # stop the timer and display FPS information
        self.goproCamera.livestream("stop")
        self.stream_start_thread.join()
        self.goproCamera = None
        self.textConsole.setText(str(""))

    def play_stream(self):

        self.fvs = FileVideoStream('udp://@127.0.0.1:10000').start()
        time.sleep(1.0)
        # start the FPS timer
        self.fps = FPS().start()

        while self.fvs.running():

            frame = self.fvs.read()
            frame = imutils.resize(frame, width=self.video_window.width())
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytesPerLine = 3 * width
            convertToQtFormat = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

            pixmap = QPixmap(convertToQtFormat)
            QApplication.processEvents()
            self.video_window.setPixmap(pixmap)
            self.textConsole.setText("Queue Size: {}".format(self.fvs.Q.qsize()))

            if self.stop:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if self.fvs.Q.qsize() < 2:  # If we are low on frames, give time to producer
                time.sleep(0.001)  # Ensures producer runs now, so 2 is sufficient
            self.fps.update()

        self.fps.stop()
        self.fvs.stop()
        cv2.destroyAllWindows()

    def _gopro_connect(self):

        if not self.goproCamera:
            self.goproCamera = GoProCamera.GoPro(constants.gpcontrol)

        if self._gopro_connect_btn.text() == "Connect":
            self._gopro_connect_btn.setText("Disconnect")
            self.stop = False
            self.textConsole.setText(str(self.goproCamera.infoCamera()))

            self.stream_start_thread.start()
            self.play_stream()

        else:
            self.stop = True
            self._gopro_connect_btn.setText("Connect")
            self.stream_stop_thread.start()

    def _connected(self, link_uri):
        """Callback when the Crazyflie has been connected"""

        logger.debug("Crazyflie connected to {}".format(link_uri))

    def _disconnected(self, link_uri):
        """Callback for when the Crazyflie has been disconnected"""

        logger.debug("Crazyflie disconnected from {}".format(link_uri))

    def _param_updated(self, name, value):
        """Callback when the registered parameter get's updated"""

        logger.debug("Updated {0} to {1}".format(name, value))

    def _log_data_received(self, timestamp, data, log_conf):
        """Callback when the log layer receives new data"""

        logger.debug("{0}:{1}:{2}".format(timestamp, log_conf.name, data))

    def _logging_error(self, log_conf, msg):
        """Callback from the log layer when an error occurs"""

        QMessageBox.about(self, "Example error",
                          "Error when using log config"
                          " [{0}]: {1}".format(log_conf.name, msg))
