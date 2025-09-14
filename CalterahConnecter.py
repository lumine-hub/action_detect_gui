import serial
import time
import serial.tools.list_ports


class CalterahConnecter():
    '''
    加特兰设备串口连接器
    '''

    def __init__(self):
        pass

    def getSerial(self, baudRate, timeout, port):
        '''
        手动指定串口参数并返回串口对象
        :param baudRate: 波特率
        :param timeout: 读超时
        :param port: 串口号
        :return: 串口对象
        '''
        s = serial.Serial(port, baudRate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                          timeout=timeout)
        return s

    def getSerialAuto(self, baudRate, timeout):
        port = self.__findComInterface(baudRate, timeout)
        s = serial.Serial(port, baudRate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                          timeout=timeout)
        return s

    def __findComInterface(self, baudRate, timeout):
        '''
        自动获取设备连接COM口
        :return: 返回设备连接COM口号
        '''

        # 所有的COM口名称
        portsNameAll = [port.name for port in serial.tools.list_ports.comports()]

        connectedPort = []
        # 对于每个端口测试是否连接设备
        for port in portsNameAll:
            s = serial.Serial(port, baudRate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                              timeout=timeout)
            # 清除输入缓冲区数据
            s.flushInput()
            s.flushOutput()

            # 获取0.1s的数据
            cmd = 'help\r\n'.encode()
            s.write(cmd)
            time.sleep(0.1)

            # 返回接收缓存中的字节数
            cachedDataNum = s.inWaiting()
            str = s.read(cachedDataNum)

            # 如果有输出信息
            if len(str) > 0:
                connectedPort.append(port)

        # 检查是否只获取到一个端口号
        try:
            if len(connectedPort) != 1:
                raise RuntimeError('无法自动获取设备端口号，请检查是否连接或手动指定')

        except Exception as e:
            print(e.args[0])
            exit()

        else:
            print('获得设备端口号' + connectedPort[0])
            return connectedPort[0]
