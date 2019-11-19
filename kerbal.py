from rocket import Rocket
from wind import Wind
from window import Window
import time


class Kerbal:

    @staticmethod
    def millis():
        return time.time_ns() // 1_000_000

    def __init__(self):
        self.win = Window((1600, 900))
        self.wind = Wind()
        self.rocket = Rocket(x=120, y=300, width=50, height=100)
        self.wind_v = self.wind.tick(0)
        self.last_time = Kerbal.millis()
        self.win.add_handler('a', lambda x: self.left())
        self.win.add_handler('d', lambda x: self.right())

    def left(self):
        self.rocket.tilt(1, 'left')

    def right(self):
        self.rocket.tilt(1, 'right')

    def up(self):
        pass

    def run(self):
        while self.win.open:
            c_time = Kerbal.millis()
            delta = (self.last_time - c_time) / 1000
            self.tick(delta)
            self.last_time = c_time

    def tick(self, timedelta: float):
        self.wind_v = self.wind.tick(timedelta)
        self.draw()

    def draw(self):
        self.win.clear()
        self.win.draw(self.rocket)
        self.win.update()


if __name__ == '__main__':
    kerbal = Kerbal()
    kerbal.run()

