import sys
import time
import random

from PyQt5.QtChart import QChart, QChartView, QScatterSeries, QValueAxis
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QGraphicsTextItem

import globalCfg


class TargetsDrawer2D(QWidget):
    # __actionIndex = ['empty', 'stand', 'walk', 'sit', 'fall', 'real fall', 'out']
    # __actionIndex = ['empty', 'non-fall', 'walk', 'sit', 'fall', 'real fall', 'out']
    __actionIndex = ['empty', '正常', '行走', '坐', '跌倒', '跌倒', '出边界']


    def __init__(self, dataQueue, stopEvent):
        super(TargetsDrawer2D, self).__init__()
        self.dataQueue = dataQueue
        self.stopEvent = stopEvent
        self.__initUI()

    def __initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('状态检测GUI——2D')

        # 初始化散点图
        self.scatter = QScatterSeries()
        self.scatter.setMarkerSize(40)

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.addSeries(self.scatter)

        chartView = QChartView()
        chartView.setChart(self.chart)

        # 设置坐标轴
        axisX = QValueAxis()
        axisX.setMin(globalCfg.xlim2D[0])
        axisX.setMax(globalCfg.xlim2D[1])
        axisX.setTickCount(int((globalCfg.xlim2D[1] - globalCfg.xlim2D[0] + 1) / globalCfg.xScale2D))
        axisX.setLabelFormat("%.1f")
        axisX.setTitleText("X轴")
        axisX.setLabelsFont(QFont("Times", 15, QFont.Bold))
        axisX.setTitleFont(QFont("Times", 18, QFont.Bold))
        self.chart.addAxis(axisX, Qt.AlignBottom)
        self.scatter.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setMin(globalCfg.ylim2D[0])
        axisY.setMax(globalCfg.ylim2D[1])
        axisY.setTickCount(int((globalCfg.ylim2D[1] - globalCfg.ylim2D[0] + 1) / globalCfg.yScale2D))
        axisY.setLabelFormat("%.1f")
        axisY.setTitleText("Y轴")
        axisY.setLabelsFont(QFont("Times", 15, QFont.Bold))
        axisY.setTitleFont(QFont("Times", 18, QFont.Bold))
        self.chart.addAxis(axisY, Qt.AlignLeft)
        self.scatter.attachAxis(axisY)

        vbox = QVBoxLayout()
        vbox.addWidget(chartView)

        self.setLayout(vbox)

        # 设置绘图定时器
        self.drawTimer = QTimer(self)
        self.drawTimer.timeout.connect(self.__draw)
        self.drawTimer.start(10)

        # 设置文本控件列表
        self.textItems = []

    def __draw(self):

        while (not self.dataQueue.empty()):
            self.__clearChart()
            # 获取数据
            data = self.dataQueue.get()
            frameId = data['frameId']
            targets = data['targetsInfo']
            # 绘制数据
            for i, target in enumerate(targets):
                # 状态文本
                text = self.__actionIndex[int(target.action)]

                text += ': \n(x:{}, y:{}, z:{} tType:{} )'.format(round(target.pos.x, 3), round(target.pos.y, 3),
                                                                  round(target.pos.z, 3), target.tType)
                # text = '  (x:{}, y:{}, z:{})'.format(round(target.pos.x, 3), round(target.pos.y, 3),  # 不显示姿态信息
                #                                      round(target.pos.z, 3))
                textItem = QGraphicsTextItem(text, parent=self.chart)
                textItem.setFont(QFont("Times", 30, QFont.Bold))
                self.textItems.append(textItem)
                # 设置目标点
                self.scatter.append(target.pos.x, target.pos.y)
                point = self.scatter.at(i)
                # 设置状态文本位置
                posInChart = self.scatter.chart().mapToPosition(point, self.scatter)
                textItem.setPos(posInChart)

    def __clearChart(self):
        self.scatter.clear()
        for textItem in self.textItems:
            textItem.deleteLater()
        self.textItems = []

    def closeEvent(self, event):
        self.stopEvent.set()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TargetsDrawer2D('test', 'test')
    win.show()
    sys.exit(app.exec_())
