import re
import serial
import time
import struct
import globalCfg


class CalterahReader():
    '''
    加特兰数据读取器
    '''

    __magicWords = b'\x01\x02\x03\x04\x05\x06\x07\x08'

    def __init__(self, cfgSerial, cfgFile, data_serial):
        self.cfgSerial = cfgSerial
        self.cfgFile = cfgFile

        self.dataSerial = serial.Serial(data_serial, globalCfg.dataBaudRate, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=globalCfg.timeout)
        # buffer用于获得帧数据时存储被截断的帧
        self.dataBuffer = bytes()

    # def setSerial(self, serial):
    #     '''
    #     设置串口（serial.Serial）
    #     :param serial: 串口
    #     '''
    #     self.serial = serial

    def startReceive(self):
        '''
        开始接收数据
        '''

        try:
            for echo in self.cfgSerial.readlines():
                print(echo)
            print("========================")

            with open(self.cfgFile, 'rb') as f:
                for line in f.readlines():
                    if not b'\r\n' in line:
                        line = line + b'\r\n'
                    self.cfgSerial.write(line)
                    time.sleep(0.05)
                    for echo in self.cfgSerial.readlines():
                        print(echo)
            print('Configuration file write complete\n')
        except Exception as e:
            print('Configuration file write failed')
            print(e)

        self.clearBuffer()

    # def stopReceive(self):
    #     '''
    #     停止接收数据
    #     '''
    #     cmd = 'scan stop\r\n'.encode()
    #     self.cfgSerial.write(cmd)

    def clearBuffer(self):
        '''
        清除buffer
        '''
        self.dataBuffer = bytes()

    def getFrameData(self):
        '''
        获取一帧的原始字符串
        :return: 帧字符串framesData
        '''

        # 获取缓存数据量
        cachedDataAmount = self.dataSerial.inWaiting()

        # 读取缓存数据并与buffer中数据拼接
        dataString = self.dataSerial.read(cachedDataAmount)
        dataString = self.dataBuffer + dataString
        framesData = []
        # magicWords数量，n个magicWords确定n-1个完整帧
        magicWordsNum = dataString.count(self.__magicWords)

        # 正则表达式匹配所有magicWords
        magicWordsPattern = re.compile(self.__magicWords)
        iter = magicWordsPattern.finditer(dataString)
        # 遍历所有magicWords并获取完整帧数据
        for i in range(magicWordsNum - 1):
            frameStartIndex = next(iter).start()
            frameLength = struct.unpack("<1i", dataString[(frameStartIndex + 28):(frameStartIndex + 32)])[0]
            frameXOR = struct.unpack("<1c",
                                     dataString[(frameStartIndex + frameLength - 1):(frameStartIndex + frameLength)])
            if frameXOR[0] == b'\x00':
                framesData.append(dataString[frameStartIndex:frameStartIndex + frameLength])

        # 存储剩余不完整帧数据
        incompleteDataIndex = 0 if magicWordsNum <= 1 else next(iter).start()
        self.dataBuffer = dataString[incompleteDataIndex:]

        if framesData:
            print("--- Raw Frame Data ---")
            for frame in framesData:
                print(frame)
            print("----------------------")

        return framesData
