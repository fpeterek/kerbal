import math
import tkinter
from PIL import ImageTk, Image

import settings
from engine import Engine
from gravity_point import GravityPoint


class Rocket:

    base_tilt_up = 90.0
    base_tilt_left = 235.0
    base_tilt_right = 305.0
    air_res = 360.0
    terminal_velocity = 500
    g = 500
    max_horizontal_velocity = 360.0
    max_v_to_land = 100

    def __init__(self, x, y, width, height):
        self.angle = 0.0
        self.center = GravityPoint(x, y)
        self.width = width
        self.height = height
        self.up = GravityPoint(x, y - height*0.66)
        self.left = GravityPoint(x - width*0.5, y + height*0.33)
        self.right = GravityPoint(x + width*0.5, y + height*0.33)
        self.wind_velocity = 0
        self.wind_effect = 0
        self.force_x = 0
        self.force_y = 0
        self.force_r = 0
        self.affected_by_forces = True

        img = Image.open('resources/kerbal.png')
        img = img.resize((self.width, self.height), Image.NONE)
        self.sprite = ImageTk.PhotoImage(img)

        self.left_engine = Engine.side_engine()
        self.right_engine = Engine.side_engine()
        self.bottom_engine = Engine.bottom_engine()

        self.ud_dist = \
            ((self.left.x - self.up.x) ** 2 + (self.left.y - self.up.y) ** 2) ** 0.5
        self.lc_dist = (
                               (self.left.x - self.center.x) ** 2 +
                               (self.left.y - self.center.y) ** 2
                       ) ** 0.5

        l_offset_x = math.cos(math.radians(Rocket.base_tilt_left)) * self.lc_dist
        self.left.x = self.center.x + l_offset_x
        self.right.x = self.center.x - l_offset_x

        l_offset_y = math.sin(math.radians(Rocket.base_tilt_left)) * self.lc_dist
        self.left.y = self.center.y - l_offset_y
        self.left.y = self.center.y - l_offset_y

    def draw(self, canvas: tkinter.Canvas):
        if settings.rocket_display_points:
            self.up.draw(canvas)
            self.left.draw(canvas)
            self.right.draw(canvas)
            self.center.draw(canvas)
        canvas.create_image(self.left.x, self.up.y, image=self.sprite, anchor=tkinter.NW)

    def bound_forces(self):
        self.force_x = max(self.force_x, -Rocket.max_horizontal_velocity)
        self.force_x = min(self.force_x, Rocket.max_horizontal_velocity)

        self.force_y = min(self.force_y, Rocket.terminal_velocity)
        self.force_y = max(self.force_y, -Rocket.terminal_velocity)

    def calc_forces(self, dt):
        if not self.affected_by_forces:
            return
        self.calc_wind_effect(dt)
        self.force_x += self.calc_dfx(dt)
        self.force_y += self.calc_dfy(dt)
        self.bound_forces()

    def calc_wind_effect(self, dt):
        self.wind_effect += self.wind_velocity * 10 * dt
        fun = min
        if self.wind_velocity < 0:
            fun = max
        self.wind_effect = fun(self.wind_effect, self.wind_velocity * 10)

    def calc_air_resistance(self, dt) -> float:
        dec = Rocket.air_res * dt * (1 if self.force_x < 0 else -1)
        if abs(dec) > abs(self.force_x):
            dec = self.force_x * -1
        return dec

    def calc_dfx(self, dt) -> float:
        dec = self.calc_air_resistance(dt)
        left = self.left_engine.calc_thrust(dt)
        right = self.right_engine.calc_thrust(dt) * -1
        return left + right + dec

    def calc_dfy(self, dt) -> float:
        gravity = Rocket.g * dt
        engine = self.bottom_engine.calc_thrust(dt) * -1
        return gravity + engine

    def move_x(self, dx):
        self.center.x += dx
        self.up.x += dx
        self.left.x += dx
        self.right.x += dx

    def move_y(self, dy):
        self.center.y += dy
        self.up.y += dy
        self.left.y += dy
        self.right.y += dy

    def move(self, dx, dy):
        self.move_x(dx)
        self.move_y(dy)

    def disable_forces(self):
        self.force_x = 0
        self.force_y = 0
        self.force_r = 0
        self.affected_by_forces = False

    @property
    def forces(self) -> tuple:
        return self.force_x, self.force_y

    def set_wind(self, wind):
        self.wind_velocity = wind

    def tick(self, timedelta):
        if not timedelta:
            return
        self.calc_forces(timedelta)
        # self.move_x(timedelta)
        # self.move_y(timedelta)
        self.tick_engines(timedelta)

    def tick_engines(self, timedelta):
        self.left_engine.tick(timedelta)
        self.right_engine.tick(timedelta)
        self.bottom_engine.tick(timedelta)

    def enable_engine(self, engine: str):
        if engine == 'left':
            self.left_engine.turn_on()
        elif engine == 'right':
            self.right_engine.turn_on()
        elif engine == 'bottom':
            self.bottom_engine.turn_on()

    @property
    def up_angle(self):
        return math.radians(Rocket.base_tilt_up + self.angle)

    @property
    def left_angle(self):
        return math.radians(Rocket.base_tilt_left + self.angle)

    @property
    def right_angle(self):
        return math.radians(Rocket.base_tilt_right + self.angle)

    def tilt(self, time_delta, direction='left'):
        self.angle += time_delta * 2 * (-1 + (direction == 'left') * 2)
        self.up.x = self.center.x + self.height * 0.66 * math.cos(self.up_angle)
        self.up.y = self.center.y - self.height * 0.66 * math.sin(self.up_angle)

        self.left.x = self.center.x + self.lc_dist * math.cos(self.left_angle)
        self.left.y = self.center.y - self.lc_dist * math.sin(self.left_angle)

        self.right.x = self.center.x + self.lc_dist * math.cos(self.right_angle)
        self.right.y = self.center.y - self.lc_dist * math.sin(self.right_angle)

