import sys
import threading
from queue import Queue
from PyQt5.QtWidgets import QApplication

from TargetsDrawer2D import TargetsDrawer2D
from TargetsDrawer3D import TargetsDrawer3D
import globalCfg


class TargetsDrawerThread(threading.Thread):
    dataQueue = Queue()

    def __init__(self, stopEvent):
        threading.Thread.__init__(self)
        self.stopEvent = stopEvent

    def run(self):
        app = QApplication(sys.argv)
        if globalCfg.gui3D:
            win = TargetsDrawer3D(self.dataQueue, self.pointQueue, self.stopEvent)
        else:
            win = TargetsDrawer2D(self.dataQueue, self.stopEvent)
        win.show()
        sys.exit(app.exec_())
