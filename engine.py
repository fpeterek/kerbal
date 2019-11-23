
class Engine:

    keepalive = 0.05  # 50 ms
    power = 720.0

    def __init__(self):
        self.timer = 0.0

    def turn_on(self):
        self.timer = 0.0

    def tick(self, timedelta):
        self.timer += timedelta

    @property
    def on(self):
        return self.timer < Engine.keepalive
