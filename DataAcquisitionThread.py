import threading
import time
from CalterahConnecter import CalterahConnecter
from CalterahReader import CalterahReader
from FrameParser import FrameParser
import globalCfg


class DataAcquisitionThread(threading.Thread):
    '''
    点云获取线程类
    '''

    def __init__(self, targetsQueue, stopEvent, track_data, cfg_serial, data_serial):
        threading.Thread.__init__(self)
        self.targetsQueue = targetsQueue
        self.stopEvent = stopEvent
        self.track_data = track_data
        self.cfgSerial = cfg_serial
        self.dataSerial = data_serial

    def run(self):
        # 获得串口
        connecter = CalterahConnecter()
        serial = connecter.getSerial(globalCfg.cfgBaudRate, globalCfg.timeout, self.cfgSerial)

        # 初始化读取器
        cfgFile = globalCfg.cfgPath
        reader = CalterahReader(serial, cfgFile, self.dataSerial)
        # 开始收数据
        reader.startReceive()
        print("开始时间", time.asctime())

        start_time = time.time()
        end_time = start_time

        while (not self.stopEvent.isSet()):
            time.sleep(0.001)
            # 获取帧数据
            frameData = reader.getFrameData()
            if frameData:
                end_time = time.time()
            if (not frameData) and ((time.time() - end_time) > 15):
                print("无法读出数据，疑似死机，总共运行时长(s)：", time.time() - start_time)
                exit(20)
            # 提取每一帧
            for fd in frameData:
                parser = FrameParser()
                parser.analyzeSingleFrame(fd)
                targets, target_data = parser.getTargets()
                self.targetsQueue.put(targets)
                self.track_data.append(target_data)
