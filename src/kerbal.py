from explosion import Explosion
from rocket_platform import Platform
from rocket import Rocket
from sea import Sea, SeaBackground
from wind import Wind
from window import Window

import random
import time
import keyboard


class Kerbal:

    win_width = 1450
    win_height = 800

    @staticmethod
    def millis():
        return time.time_ns() // 1_000_000

    def __init__(self):
        self.win = Window((Kerbal.win_width, Kerbal.win_height))
        self.wind = Wind(Kerbal.win_width, Kerbal.win_height)
        self.sea_background = SeaBackground(Kerbal.win_width, Kerbal.win_height)
        self.sea = Sea(Kerbal.win_width, Kerbal.win_height)
        self.platform = Platform(self.sea.width // 2, self.sea.y)
        self.rocket = self.rand_rocket
        self.wind_v = self.wind.tick(0)
        self.explosion = None
        self.last_time = Kerbal.millis()
        self.controls_enables = True
        self.win.add_handler('j', lambda x: self.wind.dec_wind())
        self.win.add_handler('k', lambda x: self.wind.inc_wind())
        self.win.add_handler('<space>', lambda x: self.die())
        self.win.add_handler('r', lambda x: self.reset())

    def rand_explosion(self):
        self.explosion = Explosion(self.rocket.center.x, self.rocket.center.y)

    def left(self):
        if self.controls_enables and self.rocket:
            self.rocket.enable_engine('right')

    def right(self):
        if self.controls_enables and self.rocket:
            self.rocket.enable_engine('left')

    def up(self):
        if self.controls_enables and self.rocket:
            self.rocket.enable_engine('bottom')

    @property
    def rand_rocket(self) -> Rocket:
        x = random.randint(75, Kerbal.win_width-75)
        return Rocket(x=x, y=100, width=75, height=150)

    def reset(self):
        self.wind = Wind(Kerbal.win_width, Kerbal.win_height)
        self.rocket = self.rand_rocket
        self.wind_v = self.wind.tick(0)
        self.explosion = None
        self.last_time = Kerbal.millis()
        self.controls_enables = True

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
        platform_intersect = self.rocket.left.y > self.platform.y
        platform_intersect = platform_intersect and self.rocket.right.x > self.platform.x
        platform_intersect = platform_intersect and self.rocket.left.x < self.platform.x + self.platform.width
        if platform_intersect:
            fx, fy = self.rocket.forces
            if abs(fy) <= Rocket.max_v_to_land:
                return self.land()
            else:
                return self.die()
        if self.rocket.left.y > self.sea.y:
            self.rocket.move_y(self.sea.y - self.rocket.left.y)
            self.die()

    def land(self):
        self.controls_enables = False
        self.rocket.disable_forces()

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
        self.win.draw(self.platform)
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
