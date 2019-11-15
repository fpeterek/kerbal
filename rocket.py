import math

from gravity_point import GravityPoint


class Rocket:

    def __init__(self, x, y, width, height):
        self.angle = 90.0
        self.center = GravityPoint(x, y)
        self.width = width
        self.height = height
        self.up = GravityPoint(x, y - height*0.66)
        self.left = GravityPoint(x - width*0.5, y + height*0.33)
        self.right = GravityPoint(x + width*0.5, y + height*0.33)

        self.ud_dist = \
            ((self.left.x - self.up.x) ** 2 + (self.left.y - self.up.y) ** 2) ** 0.5
        print(self.ud_dist)
        self.lr_dist = width
        print(self.lr_dist)

    @property
    def angle_rad(self):
        return self.angle / 180 * math.pi

    def draw(self, canvas):
        self.up.draw(canvas)
        self.left.draw(canvas)
        self.right.draw(canvas)
        self.center.draw(canvas)

    def tilt(self, time_delta, direction='left'):
        self.up.x = self.center.x + self.height * 0.66 * math.cos(self.angle_rad)
        self.up.y = self.center.y + self.height * 0.66 * math.sin(self.angle_rad)

        self.left.x += self.center.x + self.height * 0.66 * math.cos(self.angle_rad)
        self.left.y += self.center.y + self.height * 0.66 * math.sin(self.angle_rad)
