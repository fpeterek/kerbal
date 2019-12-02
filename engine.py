
class Engine:

    keepalive = 0.05  # 50 ms
    SIDE_ENGINE_POWER = 500.0
    BOTTOM_ENGINE_POWER = 800.0

    @staticmethod
    def side_engine():
        return Engine(Engine.SIDE_ENGINE_POWER)

    @staticmethod
    def bottom_engine():
        return Engine(Engine.BOTTOM_ENGINE_POWER)

    def __init__(self, power):
        self.timer = 0.0
        self.power = power

    def turn_on(self):
        self.timer = 0.0

    def tick(self, timedelta):
        self.timer += timedelta

    def calc_thrust(self, dt) -> float:
        return self.on * self.power * dt

    @property
    def on(self):
        return self.timer < Engine.keepalive
