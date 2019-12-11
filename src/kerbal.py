from explosion import Explosion
from gravity_point import GravityPoint
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
        self.controls_enabled = True
        self.fixed_points = []
        self.win.add_handler('j', lambda x: self.wind.dec_wind())
        self.win.add_handler('k', lambda x: self.wind.inc_wind())
        self.win.add_handler('<space>', lambda x: self.die())
        self.win.add_handler('r', lambda x: self.reset())

    def rand_explosion(self):
        self.explosion = Explosion(self.rocket.center.x, self.rocket.center.y)

    def left(self):
        if self.controls_enabled and self.rocket:
            self.rocket.enable_engine('right')

    def right(self):
        if self.controls_enabled and self.rocket:
            self.rocket.enable_engine('left')

    def up(self):
        if self.controls_enabled and self.rocket:
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
        self.fixed_points = []
        self.controls_enabled = True

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

    def check_point_platform(self, point: GravityPoint) -> bool:
        return self.platform.x <= point.x <= self.platform.x + self.platform.width and \
               point.y >= self.platform.y

    def check_bounds_sea(self):
        for point in [self.rocket.left, self.rocket.right, self.rocket.up]:
            if point.y > self.sea.y:
                self.rocket.move_y(self.sea.y - point.y - 1)
                self.die()

    def rocket_bounds(self):
        left_coll = self.check_point_platform(self.rocket.left) or \
                    'left' in self.fixed_points
        right_coll = self.check_point_platform(self.rocket.right) or \
                     'right' in self.fixed_points
        fx, fy = self.rocket.forces
        landable_v = abs(fy) <= Rocket.max_v_to_land

        if left_coll and right_coll:
            if landable_v:
                self.fixed_points = ['left', 'right']
            else:
                return self.die()
        elif left_coll:
            if landable_v:
                self.fixed_points = ['left']
                self.rocket.move_y(self.platform.y - self.rocket.left.y)
                self.rocket.fix_point('left')
            else:
                return self.die()
        elif right_coll:
            if landable_v:
                self.fixed_points = ['right']
                self.rocket.move_y(self.platform.y - self.rocket.right.y)
                self.rocket.fix_point('right')
            else:
                return self.die()

        if len(self.fixed_points) == 2:
            self.land()

        self.check_bounds_sea()

    def land(self):
        self.controls_enabled = False
        self.rocket.land()
        self.rocket.move_y(self.platform.y - self.rocket.right.y)

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
