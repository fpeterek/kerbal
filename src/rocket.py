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

    max_rotation = 50.0
    r_acceleration = 500.0
    gravity_rotation = 300.0
    r_depreciation = 100.0

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
        self.rotation_enabled = True
        self.fixed = ''
        self.cog_center_dist = (self.center.y - self.up.y) - (height // 2)
        image_width = int(max(width, height) * 1.1)

        img = Image.open('resources/kerbal.png').resize((width, height), Image.NONE)
        square = Image.new('RGBA', (image_width, image_width), (0, 0, 0, 0))
        square.paste(img, ((image_width - width) // 2, (image_width - height) // 2))
        self.orig_img = square
        self.sprite = ImageTk.PhotoImage(self.orig_img)

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

        x = self.center.x - round(self.cog_center_dist * math.cos(math.radians(self.angle - 90)))
        y = self.center.y + round(self.cog_center_dist * math.sin(math.radians(self.angle - 90)))
        canvas.create_image(x, y, image=self.sprite, anchor=tkinter.CENTER)

    def bound_force_x(self):
        self.force_x = max(self.force_x, -Rocket.max_horizontal_velocity)
        self.force_x = min(self.force_x, Rocket.max_horizontal_velocity)

    def bound_force_y(self):
        self.force_y = min(self.force_y, Rocket.terminal_velocity)
        self.force_y = max(self.force_y, -Rocket.terminal_velocity)

    def bound_forces(self):
        self.bound_force_x()
        self.bound_force_y()

    def calc_forces(self, dt):
        if self.rotation_enabled:
            self.calc_rotation_force(dt)

        if not self.affected_by_forces:
            return
        self.calc_wind_effect(dt)

        left = self.left_engine.calc_thrust(dt)
        right = self.right_engine.calc_thrust(dt)
        bottom = self.bottom_engine.calc_thrust(dt)

        self.force_x += self.calc_dfx(dt, left, right, bottom)
        self.force_y += self.calc_dfy(dt, left, right, bottom)
        self.bound_forces()

    def calc_wind_effect(self, dt):
        if not self.affected_by_forces:
            return
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

    def calc_dfx(self, dt, left, right, bottom) -> float:
        dec = self.calc_air_resistance(dt)
        l_thrust = left * math.cos(math.radians(self.angle - 180))
        r_thrust = right * math.cos(math.radians(self.angle))
        b_thrust = bottom * math.cos(math.radians(self.angle + 90))
        return l_thrust + r_thrust + b_thrust + dec

    def calc_dfy(self, dt, left, right, bottom) -> float:
        gravity = Rocket.g * dt
        l_thrust = left * math.sin(math.radians(self.angle))
        r_thrust = right * math.sin(math.radians(self.angle - 180))
        b_thrust = bottom * math.sin(math.radians(self.angle + 90))
        return gravity - l_thrust - r_thrust - b_thrust

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
        self.wind_effect = 0
        self.affected_by_forces = False

    def disable_rotation(self):
        self.force_r = 0
        self.rotation_enabled = False

    @property
    def fixed_point(self):
        if self.fixed:
            return self.left if self.fixed == 'left' else self.right

    def landing_correction(self, dt: float):
        fixed = self.fixed_point
        direction = 1 - 2 * (self.center.x >= fixed.x)
        self.force_r += Rocket.gravity_rotation * direction * dt

    def calc_rotation_force(self, dt: float):
        self.force_r += bool(self.left_engine.on) * Rocket.r_acceleration * dt * -1
        self.force_r += bool(self.right_engine.on) * Rocket.r_acceleration * dt
        self.force_r += bool(self.force_r) * Rocket.r_depreciation * dt * (1 if self.force_r < 0 else -1)

        if self.fixed:
            self.landing_correction(dt)
        else:
            self.force_r = max(-Rocket.max_rotation, self.force_r)
            self.force_r = min(Rocket.max_rotation, self.force_r)

    @property
    def forces(self) -> tuple:
        return self.force_x + self.wind_effect, self.force_y

    def set_wind(self, wind):
        self.wind_velocity = wind

    def tick(self, timedelta):
        if not timedelta:
            return
        self.calc_forces(timedelta)
        self.tilt(timedelta)
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

    def fix_point(self, point: str):
        self.fixed = point
        self.disable_forces()

    @property
    def up_angle(self):
        return math.radians(Rocket.base_tilt_up + self.angle)

    @property
    def left_angle(self):
        return math.radians(Rocket.base_tilt_left + self.angle)

    @property
    def right_angle(self):
        return math.radians(Rocket.base_tilt_right + self.angle)

    def land(self):
        self.angle = 0
        self.disable_forces()
        self.disable_rotation()
        self.tilt(0)

    @property
    def fixed_coordinates(self):
        if not self.fixed:
            return None, None
        return self.fixed_point.x, self.fixed_point.y

    def adjust_position(self, orig_pos):
        if not self.fixed:
            return
        ox, oy = orig_pos
        cx, cy = self.fixed_point.x, self.fixed_point.y
        dx = ox - cx
        dy = oy - cy
        self.move(dx, dy)

    def tilt(self, time_delta):
        self.angle += time_delta * self.force_r

        orig_pos = self.fixed_coordinates

        self.up.x = self.center.x + self.height * 0.66 * math.cos(self.up_angle)
        self.up.y = self.center.y - self.height * 0.66 * math.sin(self.up_angle)

        self.left.x = self.center.x + self.lc_dist * math.cos(self.left_angle)
        self.left.y = self.center.y - self.lc_dist * math.sin(self.left_angle)

        self.right.x = self.center.x + self.lc_dist * math.cos(self.right_angle)
        self.right.y = self.center.y - self.lc_dist * math.sin(self.right_angle)

        self.adjust_position(orig_pos)

        self.sprite = ImageTk.PhotoImage(self.orig_img.rotate(self.angle))

