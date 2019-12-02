import math
import random
import tkinter


class Wind:
    max_wind = 10
    wind_change_threshold = 300.0
    wind_min_duration = 3.0

    def __init__(self, width, height):
        self.counter = 0.0
        self.wind = random.randint(-Wind.max_wind, Wind.max_wind)
        self.wind_indicator = WindIndicator(width, height)

        self.change_fun = self.change_enabled
        self.inc_wind = self.inc_wind_and_disable_auto
        self.dec_wind = self.dec_wind_and_disable_auto

    @staticmethod
    def change_disabled():
        return False

    def change_enabled(self):
        return random.randint(0, int(Wind.wind_change_threshold)) + Wind.wind_min_duration < self.counter

    @property
    def should_change(self):
        return self.change_fun()

    def tick(self, timedelta: float):
        self.counter += timedelta
        if self.should_change:
            self.change_wind()
        self.wind_indicator.tick(timedelta, self.wind)
        return self.wind

    def change_wind(self):
        delta = 4 - math.ceil(random.randint(1, 9) ** 0.5)
        self.wind += random.choice([-1, 1]) * delta
        self.wind = max(self.wind, -Wind.max_wind)
        self.wind = min(self.wind, Wind.max_wind)
        self.counter = 0.0

    def disable_auto(self):
        self.change_fun = self.change_disabled
        self.inc_wind = self.inc_fun
        self.dec_wind = self.dec_fun

    def inc_wind_and_disable_auto(self):
        self.disable_auto()
        self.inc_wind()

    def dec_wind_and_disable_auto(self):
        self.disable_auto()
        self.dec_wind()

    def inc_fun(self):
        self.wind = min(self.wind + 1, 10)

    def dec_fun(self):
        self.wind = max(self.wind - 1, -10)

    def draw(self, canvas: tkinter.Canvas):
        canvas.create_text(canvas.winfo_width() - 40, 10, text=f'Wind={self.wind}')
        self.wind_indicator.draw(canvas)


class WindIndicator:

    def __init__(self, width, height):
        self.particles = []
        self.width = width
        self.height = height

        step = height * 2 / 3 / 4

        for i in range(1, 4):
            self.create_row(width, i * step)

    def create_row(self, width, y):
        first = random.randint(0, width / 4)
        dist = width / 4 + WindRect.width / 4
        for i in range(0, 4):
            self.particles.append(WindRect(first + dist * i, y))

    def tick(self, timedelta, v):
        for particle in self.particles:
            particle.x += timedelta * v**3
            if particle.x > self.width:
                particle.x -= self.width + particle.width
            if particle.x + particle.width < 0:
                particle.x += self.width + particle.width

    def draw(self, canvas: tkinter.Canvas):
        for particle in self.particles:
            particle.draw(canvas)


class WindRect:

    width = 100
    height = 5
    color = '#cae2e8'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas: tkinter.Canvas):
        canvas.create_rectangle(self.x, self.y, self.x + WindRect.width, self.y + WindRect.height,
                                fill=WindRect.color, outline=WindRect.color)
