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
        self.create_handlers()

    def create_handlers(self):
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

    def left_point_collision(self):
        return self.check_point_platform(self.rocket.left) or 'left' in self.fixed_points

    def right_point_collision(self):
        return self.check_point_platform(self.rocket.right) or \
               'right' in self.fixed_points

    def fix_points_on_collision(self, left_collides: bool, right_collides: bool):
        if left_collides and right_collides:
            self.fixed_points = ['left', 'right']
        elif left_collides:
            self.fixed_points = ['left']
            self.rocket.move_y(self.platform.y - self.rocket.left.y)
            self.rocket.fix_point('left')
        elif right_collides:
            self.fixed_points = ['right']
            self.rocket.move_y(self.platform.y - self.rocket.right.y)
            self.rocket.fix_point('right')

    def rocket_bounds(self):
        left_coll = self.left_point_collision()
        right_coll = self.right_point_collision()
        fx, fy = self.rocket.forces

        if (left_coll or right_coll) and abs(fy) > Rocket.max_v_to_land:
            return self.die()

        self.fix_points_on_collision(left_coll, right_coll)
        if len(self.fixed_points) == 2:
            self.land()
        self.check_bounds_sea()

    def land(self):
        self.controls_enabled = False
        self.rocket.land()
        self.rocket.move_y(self.platform.y - self.rocket.right.y)

    def update_wind(self, dt: float):
        self.wind_v = self.wind.tick(dt)

    def update_rocket(self, dt: float):
        if not self.rocket:
            return

        self.rocket.set_wind(self.wind_v)
        self.rocket.tick(dt)
        self.move_rocket(dt)

    def update_explosion(self, dt: float):
        if not self.explosion:
            return

        self.explosion.tick(dt)
        if not self.explosion.keepalive:
            self.explosion = None

    def update(self, dt: float):
        self.update_wind(dt)
        self.update_rocket(dt)
        self.update_explosion(dt)

    def tick(self, timedelta: float):
        self.update(timedelta)
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
