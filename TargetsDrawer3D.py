import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from pyqtgraph.opengl import *
import globalCfg
import numpy as np


class TargetsDrawer3D(GLViewWidget):
    __targetColorList = [[(0.5019, 0.5019, 0.5019, 1), (0.6627, 0.6627, 0.6627, 1)],
                         [(1, 0, 0, 1), (0.5451, 0, 0, 1)],
                         [(0.9803, 0.5019, 0.4470, 1), (0.9137, 0.5882, 0.4784, 1)],
                         [(1, 0.6470, 0, 1), (1, 0.5490, 0, 1)],
                         [(1, 0.7529, 0.7961, 1), (1, 0.0784, 0.5764, 1)],
                         [(0, 0.5019, 0, 1), (0, 0.3921, 0, 1)],
                         [(0, 0, 1, 1), (0, 0, 0.5451, 1)],
                         [(0.8549, 0.4392, 0.8392, 1), (0.6, 0.1961, 0.8, 1)]]

    __actionIndex = ['empty', 'stand', 'walk', 'sit', 'fall', 'out']

    def __init__(self, dataQueue, pointQueue, stopEvent):
        super().__init__()
        self.dataQueue = dataQueue
        self.pointQueue = pointQueue
        self.stopEvent = stopEvent
        self.initUI()

    def initUI(self):

        self.opts['distance'] = 20
        self.show()
        self.setWindowTitle('Calterh Mmwave Motion Acquisition System')

        grid = GLGridItem()
        grid.setSize(50, 50, 50)
        self.addItem(grid)

        self.__drawBoundingBox()
        self.__drawSensor()

        # 设置绘图定时器
        self.drawTimer = QTimer(self)
        self.drawTimer.timeout.connect(self.__draw)
        self.drawTimer.start(10)

        # 目标相关item
        self.targetsItem = []
        self.pointsItem = []

    def __drawBoundingBox(self):

        colorsGround = np.array([
            [1, 0.87059, 0.67843, 1],
            [1, 0.87059, 0.67843, 1],
            [1, 0.87059, 0.67843, 1],
            [1, 0.87059, 0.67843, 1],
        ])
        colors = np.array([
            [1, 1, 1, 0.5],
            [1, 1, 1, 0.5],
            [1, 1, 1, 0.5],
            [1, 1, 1, 0.5],
        ])
        print(colors.shape)
        # 绘制两个Z平面
        x = np.array(globalCfg.xlim3D)
        y = np.array(globalCfg.ylim3D)
        z = np.zeros((2, 2))
        boundingBoxSurface1 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colorsGround, shader='shaded')
        boundingBoxSurface1.translate(0, 0, globalCfg.zlim3D[0])
        self.addItem(boundingBoxSurface1)
        boundingBoxSurface2 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colors, shader='shaded')
        boundingBoxSurface2.translate(0, 0, globalCfg.zlim3D[1])
        self.addItem(boundingBoxSurface2)

        # 绘制两个X平面
        x = np.array([0, 0])
        y = np.array(globalCfg.ylim3D)
        z = np.array([
            [globalCfg.zlim3D[0], globalCfg.zlim3D[0]],
            [globalCfg.zlim3D[1], globalCfg.zlim3D[1]]
        ])
        boundingBoxSurface3 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colors, shader='shaded')
        boundingBoxSurface3.translate(globalCfg.xlim3D[0], 0, 0)
        self.addItem(boundingBoxSurface3)
        boundingBoxSurface4 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colors, shader='shaded')
        boundingBoxSurface4.translate(globalCfg.xlim3D[1], 0, 0)
        self.addItem(boundingBoxSurface4)

        # 绘制两个Y平面
        x = np.array(globalCfg.xlim3D)
        y = np.array([0, 0])
        z = np.array([
            [globalCfg.zlim3D[0], globalCfg.zlim3D[1]],
            [globalCfg.zlim3D[0], globalCfg.zlim3D[1]]
        ])
        boundingBoxSurface5 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colors, shader='shaded')
        boundingBoxSurface5.translate(0, globalCfg.ylim3D[0], 0)
        self.addItem(boundingBoxSurface5)
        boundingBoxSurface6 = GLSurfacePlotItem(x=x, y=y, z=z, colors=colors, shader='shaded')
        boundingBoxSurface6.translate(0, globalCfg.ylim3D[1], 0)
        self.addItem(boundingBoxSurface6)

        # 透明显示
        # boundingBoxSurface1.setGLOptions('additive')
        boundingBoxSurface2.setGLOptions('additive')
        boundingBoxSurface3.setGLOptions('additive')
        boundingBoxSurface4.setGLOptions('additive')
        boundingBoxSurface5.setGLOptions('additive')
        boundingBoxSurface6.setGLOptions('additive')

    def __drawSensor(self):

        # 绘制传感器
        sensorPos = np.array([0, 0, globalCfg.sensorHeight3D])
        sensor = GLScatterPlotItem(pos=sensorPos, size=0.5, color=(0, 255, 255, 1), pxMode=False)
        self.addItem(sensor)

    def __draw(self):

        while (not self.dataQueue.empty()):
            # 清空所有目标相关item
            self.__clearTargetsItem()

            data = self.dataQueue.get()
            frameId = data['frameId']
            targets = data['targetsInfo']

            # 绘制所有target
            for target in targets:
                targetsCentroid = []
                # target质心
                targetsCentroid.append([target.pos.x, target.pos.y, target.pos.z])
                # target检测框
                self.__drawTargetBox(target.pos.x, target.pos.y, target.pos.z)

                targetsCentroid = np.array(targetsCentroid)
                targetsCentroidSize = np.ones(targetsCentroid.shape[0]) * 15
                targetsCentroidScatter = GLScatterPlotItem(pos=targetsCentroid, color=
                self.__targetColorList[target.tid % len(self.__targetColorList)][0], size=targetsCentroidSize)

                # 设置状态文本
                font = QFont('SansSerif', 20)
                targetsAction = GLTextItem(
                    pos=np.array([target.pos.x, target.pos.y, target.pos.z + globalCfg.targetBoxRadius[2]]), font=font,
                    text=self.__actionIndex[target.action])

                self.addItem(targetsCentroidScatter)
                self.addItem(targetsAction)
                self.targetsItem.append(targetsCentroidScatter)
                self.targetsItem.append(targetsAction)

        while not self.pointQueue.empty():
            point_data = self.pointQueue.get()
            points = point_data['pointInfo']

            for i, point in enumerate(points):
                pointCloud = []
                pointCloud.append([point.pointX, point.pointY, point.pointX])
                pointCloud = np.array(pointCloud)
                pointCloudScatter = GLScatterPlotItem(pos=pointCloud)

                self.addItem(pointCloudScatter)
                self.pointsItem.append(pointCloudScatter)

    def __clearTargetsItem(self):

        for item in self.targetsItem:
            self.removeItem(item)
        for item in self.pointsItem:
            self.removeItem(item)
        self.targetsItem = []
        self.pointsItem = []

    def __drawTargetBox(self, x, y, z):

        # 生成点
        posXList = [x - globalCfg.targetBoxRadius[0], x + globalCfg.targetBoxRadius[0]]
        posYList = [y - globalCfg.targetBoxRadius[1], y + globalCfg.targetBoxRadius[1]]
        posZList = [z - globalCfg.targetBoxRadius[2], z + globalCfg.targetBoxRadius[2]]
        points = []
        for posX in posXList:
            for posY in posYList:
                for posZ in posZList:
                    points.append([posX, posY, posZ])

        # 生成边
        boxLines = np.array([points[0], points[2]])
        boxLines = np.append(boxLines, np.array([points[2], points[6]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[6], points[4]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[4], points[0]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[1], points[3]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[3], points[7]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[7], points[5]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[5], points[1]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[5], points[4]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[7], points[6]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[3], points[2]]), axis=0)
        boxLines = np.append(boxLines, np.array([points[0], points[1]]), axis=0)

        targetBox = GLLinePlotItem(pos=boxLines, width=1.5, color=(0, 0, 0.80392, 1), antialias=True, mode='lines')
        self.addItem(targetBox)
        self.targetsItem.append(targetBox)

    def closeEvent(self, event):
        self.stopEvent.set()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    targetsDrawer3D = TargetsDrawer3D('test', 'test')
    app.exec_()
