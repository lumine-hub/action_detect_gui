from queue import Queue
import time
from threading import Event
from DataAcquisitionThread import DataAcquisitionThread
from TargetsDrawerThread import TargetsDrawerThread
from LogOutputThread import LogOutputThread
import globalCfg
import numpy as np

if __name__ == '__main__':

    track_data = []

    # height = input("请输入当前雷达的高度")
    # elevation = input("请输入当前雷达的俯仰角")
    # wid = input("横向(y/n)")
    # cfgSerial = input("Enhanced串口号：")
    # dataSerial = input("Standard串口号：")
    # cfgSerial = 'COM' + cfgSerial
    # dataSerial = 'COM' + dataSerial
    cfgSerial = globalCfg.cfgSerial
    dataSerial = globalCfg.dataSerial
    stopEvent = Event()
    stopEvent.clear()
    targetsQueue = Queue()
    dataAcquisitionThread = DataAcquisitionThread(targetsQueue, stopEvent, track_data, cfgSerial, dataSerial)
    dataAcquisitionThread.start()
    targetsDrawerThread = TargetsDrawerThread(stopEvent)
    targetsDrawerThread.start()
    start_time = time.time()

    logOutputThread = None
    if globalCfg.outputLog:
        logOutputThread = LogOutputThread(stopEvent)
        logOutputThread.start()

    while not stopEvent.isSet():
        time.sleep(0.001)

        while not targetsQueue.empty():
            data = targetsQueue.get()
            targetsDrawerThread.dataQueue.put(data)
            if globalCfg.outputLog:
                logOutputThread.dataQueue.put(data)

    end_time = time.time()
    # np.save("TrackLog_{hei}m_{elev}d_{widthwise}".format(hei=height, elev=elevation, widthwise=wid), track_data)
    print("正常运行的秒数(手动关闭)：", end_time - start_time)
