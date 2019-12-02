from rocket import Rocket
from sea import Sea, SeaBackground
from wind import Wind
from window import Window
import time
import keyboard


class Kerbal:

    @staticmethod
    def millis():
        return time.time_ns() // 1_000_000

    def __init__(self):
        self.win = Window((1600, 900))
        self.wind = Wind(1600, 900)
        self.sea_background = SeaBackground(1600, 900)
        self.sea = Sea(1600, 900)
        self.rocket = Rocket(x=120, y=300, width=50, height=100)
        self.wind_v = self.wind.tick(0)
        self.last_time = Kerbal.millis()
        self.win.add_handler('j', lambda x: self.wind.dec_wind())
        self.win.add_handler('k', lambda x: self.wind.inc_wind())

    def left(self):
        self.rocket.enable_engine('right')
        # self.rocket.tilt(1, 'left')

    def right(self):
        self.rocket.enable_engine('left')
        # self.rocket.tilt(1, 'right')

    def up(self):
        self.rocket.enable_engine('bottom')

    def handle_keyboard(self):
        if keyboard.is_pressed('a'):
            self.left()
        if keyboard.is_pressed('d'):
            self.right()
        if keyboard.is_pressed('w'):
            self.up()

    def run(self):
        while self.win.open:
            c_time = Kerbal.millis()
            delta = (c_time - self.last_time) / 1000
            self.handle_keyboard()
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
        self.win.draw(self.sea_background)
        self.win.draw(self.rocket)
        self.win.draw(self.sea)
        self.win.update()


def main():
    kerbal = Kerbal()
    kerbal.run()


if __name__ == '__main__':
    main()
