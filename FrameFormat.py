'''
本文件定义了加特兰数据帧原始格式类
MessageHeader：帧头
MessageHeader：目标信息
'''

class FrameHeader():
    def __init__(self):
        self.magicWords = bytes()    #8*1bytes
        self.deviceID = bytes()    #4*4bytes
        self.version = bytes()    #4*1bytes
        self.totalPacketLength = bytes()    #1*4bytes
        self.numTrackObj = bytes()    #1*1bytes
        self.numTrackObjStatic = bytes()    #1*1bytes

    # 重写类print函数
    def __str__(self):
        return ("magicWords: {}; deviceID: {}; version: {}; totalPacketLength: {}; numTrackObj: {}; numTrackObjStatic: {}".format(
            self.magicWords, self.deviceID, self.version, self.totalPacketLength, self.numTrackObj, self.numTrackObjStatic))

class FrameTarget():
    def __init__(self):
        self.tid = bytes()    #1*2bytes
        self.action = bytes()    #1*2bytes
        self.tType = bytes()  # 1*2bytes
        self.pointsNum = bytes()    #1*4bytes
        self.posX = bytes()    #1*4bytes
        self.posY = bytes()    #1*4bytes
        self.posZ = bytes()    #1*4bytes
        self.velX = bytes()    #1*4bytes
        self.velY = bytes()    #1*4bytes
        self.velZ = bytes()    #1*4bytes
        self.accX = bytes()    #1*4bytes
        self.accY = bytes()    #1*4bytes
        self.accZ = bytes()    #1*4bytes

    # 重写类print函数
    def __str__(self):
        return ("tid: {}; action: {}; pointsNum: {}; posX: {}; posY: {}; posZ: {}; velX: {}; velY: {}; velZ: {}; accX: {}; accY: {}; accZ: {}".format(
            self.tid, self.action, self.pointsNum, self.posX, self.posY, self.posZ, self.velX, self.velY, self.velZ, self.accX, self.accY, self.accZ))


