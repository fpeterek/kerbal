import math

from gravity_point import GravityPoint


class Rocket:

    base_tilt_up = 90.0
    base_tilt_left = 235.0
    base_tilt_right = 305.0

    force_x = 0
    force_y = 0
    force_r = 0

    def __init__(self, x, y, width, height):
        self.angle = 0.0
        self.center = GravityPoint(x, y)
        self.width = width
        self.height = height
        self.up = GravityPoint(x, y - height*0.66)
        self.left = GravityPoint(x - width*0.5, y + height*0.33)
        self.right = GravityPoint(x + width*0.5, y + height*0.33)

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

    def draw(self, canvas):
        self.up.draw(canvas)
        self.left.draw(canvas)
        self.right.draw(canvas)
        self.center.draw(canvas)

    def move_x(self, timedelta):
        dx = self.force_x * timedelta
        self.center.x += dx
        self.up.x += dx
        self.left.x += dx
        self.right.x += dx

    def move_y(self, timedelta):
        dy = self.force_y * timedelta
        self.center.y += dy
        self.up.y += dy
        self.left.y += dy
        self.right.y += dy

    def tick(self, timedelta):
        self.move_x(timedelta)
        self.move_y(timedelta)

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

