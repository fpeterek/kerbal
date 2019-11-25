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
        self.wind = Wind(1600, 900)
        self.rocket = Rocket(x=120, y=300, width=50, height=100)
        self.wind_v = self.wind.tick(0)
        self.last_time = Kerbal.millis()
        self.win.add_handler('a', lambda x: self.left())
        self.win.add_handler('d', lambda x: self.right())
        self.win.add_handler('w', lambda x: self.up())
        self.win.add_handler('j', lambda x: self.wind.dec_wind())
        self.win.add_handler('k', lambda x: self.wind.inc_wind())
        # self.win.add_handler('<KeyRelease-a>', lambda x: print('A up'))
        # self.win.add_handler('<KeyRelease-d>', lambda x: print('D up'))

    def left(self):
        self.rocket.enable_engine('right')
        # self.rocket.tilt(1, 'left')

    def right(self):
        self.rocket.enable_engine('left')
        # self.rocket.tilt(1, 'right')

    def up(self):
        self.rocket.enable_engine('bottom')

    def run(self):
        while self.win.open:
            c_time = Kerbal.millis()
            delta = (c_time - self.last_time) / 1000
            self.tick(delta)
            self.last_time = c_time

    def tick(self, timedelta: float):
        self.wind_v = self.wind.tick(timedelta)
        self.rocket.set_wind(self.wind_v)
        self.rocket.tick(timedelta)
        self.draw()

    def draw(self):
        self.win.clear()
        self.win.draw(self.wind)
        self.win.draw(self.rocket)
        self.win.update()


if __name__ == '__main__':
    kerbal = Kerbal()
    kerbal.run()

