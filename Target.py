class Target():
    class Pos():
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class Vel():
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    class Acc():
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    def __init__(self, tid, tType, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ, action):
        self.tid = tid
        self.tType = tType
        self.pos = self.Pos(posX, posY, posZ)
        self.vel = self.Vel(velX, velY, velZ)
        self.acc = self.Acc(accX, accY, accZ)
        self.action = action

    def __str__(self):
        return (
        "tid: {}; posX: {}; posY: {}; posZ: {}; velX: {}; velY: {}; velZ: {}; accX: {}; accY: {}; accZ: {}".format(
            self.tid, self.pos.x, self.pos.y, self.pos.z, self.vel.x, self.vel.y, self.vel.z, self.acc.x, self.acc.y,
            self.acc.z))
