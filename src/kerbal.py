from explosion import Explosion
from rocket import Rocket
from sea import Sea, SeaBackground
from wind import Wind
from window import Window

import random
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
        self.rocket = self.rand_rocket
        self.wind_v = self.wind.tick(0)
        self.explosion = None
        self.last_time = Kerbal.millis()
        self.win.add_handler('j', lambda x: self.wind.dec_wind())
        self.win.add_handler('k', lambda x: self.wind.inc_wind())
        self.win.add_handler('<space>', lambda x: self.die())
        self.win.add_handler('r', lambda x: self.reset())

    def rand_explosion(self):
        self.explosion = Explosion(self.rocket.center.x, self.rocket.center.y)

    def left(self):
        if self.rocket:
            self.rocket.enable_engine('right')
        # self.rocket.tilt(1, 'left')

    def right(self):
        if self.rocket:
            self.rocket.enable_engine('left')
        # self.rocket.tilt(1, 'right')

    def up(self):
        if self.rocket:
            self.rocket.enable_engine('bottom')

    @property
    def rand_rocket(self) -> Rocket:
        return Rocket(x=random.randint(100, 1450), y=100, width=75, height=150)

    def reset(self):
        self.wind = Wind(1600, 900)
        self.rocket = self.rand_rocket
        self.wind_v = self.wind.tick(0)
        self.explosion = None
        self.last_time = Kerbal.millis()

    def die(self):
        self.explosion = Explosion(self.rocket.center.x, self.rocket.center.y)
        self.rocket = None

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

    def move_rocket(self, dt):
        fx, fy = self.rocket.forces
        dx = fx * dt
        dy = fy * dt
        self.rocket.move(dx, dy)
        self.rocket_bounds()

    def rocket_bounds(self):
        if self.rocket.left.y > self.sea.y:
            self.rocket.move_y(self.sea.y - self.rocket.left.y)
            self.die()

    def tick(self, timedelta: float):
        self.wind_v = self.wind.tick(timedelta)
        if self.rocket:
            self.rocket.set_wind(self.wind_v)
            self.rocket.tick(timedelta)
            self.move_rocket(timedelta)
        if self.explosion:
            self.explosion.tick(timedelta)
            if not self.explosion.keepalive:
                self.explosion = None
        self.draw()

    def draw(self):
        self.win.clear()
        self.win.draw(self.wind)
        self.win.draw(self.sea_background)
        if self.rocket:
            self.win.draw(self.rocket)
        self.win.draw(self.sea)
        if self.explosion:
            self.win.draw(self.explosion)
        self.win.update()


def main():
    kerbal = Kerbal()
    kerbal.run()


if __name__ == '__main__':
    main()
