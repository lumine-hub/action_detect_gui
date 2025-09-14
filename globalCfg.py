# ------------------------------------------------
# 串口相关配置
cfgSerial = 'COM11'  # cfg串口号
dataSerial = 'COM12'  # data串口号
cfgBaudRate = 115200  # cfg串口波特率
dataBaudRate = 115200  # data串口波特率
timeout = 0.01

# ------------------------------------------------
# 配置文件路径
cfgPath = './/cfg//RadarConfig.cfg'

# ------------------------------------------------
# gui相关配置
gui3D = False

# 下面是2D显示相关参数
xlim2D = [-4, 4]  # X坐标显示范围
ylim2D = [0, 7]  # Y坐标显示范围
xScale2D = 1  # X坐标显示精度
yScale2D = 1  # Y坐标显示精度

# 下面是3D显示相关参数
xlim3D = [-4, 4]  # X坐标显示范围
ylim3D = [0, 7]  # Y坐标显示范围
zlim3D = [0, 4]  # Z坐标显示范围
sensorHeight3D = 2  # 传感器高度
targetBoxRadius = [1.5 / 2, 1.5 / 2, 2 / 2]  # 目标框三维半径

# ------------------------------------------------
# 日志相关配置
outputLog = True  # 是否输出日志文件
