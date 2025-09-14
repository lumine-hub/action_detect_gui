import threading
import time
from queue import Queue


class LogOutputThread(threading.Thread):
    dataQueue = Queue()
    __actionIndex = ['empty', 'stand', 'walk', 'sit', 'fall', 'real fall', 'out']

    def __init__(self, stopEvent):
        threading.Thread.__init__(self)
        fileName = time.strftime(".//log//Log   %Y-%m-%d-%H-%M-%S.txt", time.localtime())
        self.file = open(fileName, 'w')
        self.stopEvent = stopEvent

    def run(self):
        while (not self.stopEvent.isSet()):
            time.sleep(0.001)
            while not self.dataQueue.empty():
                data = self.dataQueue.get()
                frameId = data['frameId']
                targets = data['targetsInfo']
                frameLog = '#\nframeNum: ' + str(frameId) + '\ntrack targets:\n'
                for target in targets:
                    targetLog = "tid: {}; action: {}; posX: {}; posY: {}; posZ: {}; velX: {}; velY: {}; velZ: {}; accX: {}; accY: {}; accZ: {}\n".format(
                        target.tid, self.__actionIndex[int(target.action)], round(target.pos.x, 3),
                        round(target.pos.y, 3), round(target.pos.z, 3), round(target.vel.x, 3), round(target.vel.y, 3),
                        round(target.vel.z, 3), round(target.acc.x, 3), round(target.acc.y, 3), round(target.acc.z, 3))
                    frameLog += targetLog

                self.file.write(frameLog)
        self.file.close()
