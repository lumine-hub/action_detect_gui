import struct
from FrameFormat import *
from Target import Target
from PointFormat import *


class FrameParser():

    def __init__(self):
        self.frameHeader = FrameHeader()
        self.frameTL = []
        self.pointCL = []
        self.track_data = []

    def analyzeSingleFrame(self, frameData):

        # 解析帧头
        dataCursor = 0
        self.frameHeader.magicWords = struct.unpack("<8s", frameData[dataCursor:dataCursor + 8])[0]
        dataCursor += 8
        self.frameHeader.deviceID = struct.unpack("<16c", frameData[dataCursor:dataCursor + 16])[0]
        dataCursor += 16
        self.frameHeader.version = struct.unpack("<4c", frameData[dataCursor:dataCursor + 4])[0]
        # print("version", struct.unpack("<4c", frameData[dataCursor:dataCursor + 4]))
        dataCursor += 4
        self.frameHeader.totalPacketLength = struct.unpack("<1i", frameData[dataCursor:dataCursor + 4])[0]
        # print("Packet Length:", self.frameHeader.totalPacketLength)
        dataCursor += 4
        self.frameHeader.numTrackObj = struct.unpack("<1B", frameData[dataCursor:dataCursor + 1])[0]
        # print("num of obj:", self.frameHeader.numTrackObj)
        dataCursor += 1
        self.frameHeader.numTrackObjStatic = struct.unpack("<1B", frameData[dataCursor:dataCursor + 1])[0]
        dataCursor += 1

        # 解析帧体
        for i in range(self.frameHeader.numTrackObj):
            frameTarget = FrameTarget()
            # print(frameData[dataCursor + i * 48:dataCursor + (i + 1) * 48])
            frameTarget.tid, frameTarget.action, frameTarget.tType, frameTarget.pointsNum, frameTarget.posX, frameTarget.posY, frameTarget.posZ, frameTarget.velX, frameTarget.velY, frameTarget.velZ, frameTarget.accX, frameTarget.accY, frameTarget.accZ = struct.unpack(
                "<2h2i9f", frameData[dataCursor + i * 48:dataCursor + (i + 1) * 48])
            self.frameTL.append(frameTarget)

    def getTargets(self):

        targetsInfo = []

        for frameTarget in self.frameTL:
            target = Target(frameTarget.tid, frameTarget.tType, frameTarget.posX, frameTarget.posY, frameTarget.posZ,
                            frameTarget.velX,
                            frameTarget.velY, frameTarget.velZ, frameTarget.accX, frameTarget.accY, frameTarget.accZ,
                            frameTarget.action)
            targetsInfo.append(target)
            self.track_data.append([frameTarget.tid, frameTarget.posX, frameTarget.posY])

            print(f"--- Parsed Target ---")
            print(f"  ID: {target.tid}")
            print(f"  Position: ({target.posX:.2f}, {target.posY:.2f}, {target.posZ:.2f})")
            print(f"  Action: {target.action}")
            print(f"---------------------")

        return {'frameId': 0, 'targetsInfo': targetsInfo}, self.track_data
