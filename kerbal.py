from rocket import Rocket
from wind import Wind
from window import Window
import time

def millis():
    return time.time_ns() // 1_000_000

class Spot:

    def __init__(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad

    def draw(self, canvas):
        return canvas.create_oval(self.x - self.rad, self.y - self.rad,
                                  self.x + self.rad, self.y + self.rad,
                                  fill='#000000')


if __name__ == '__main__':
    win = Window((1600, 900))
    wind = Wind()
    win.add_handler('d', lambda r: rocket.tilt(1, 'right'))
    win.add_handler('a', lambda r: rocket.tilt(1, 'left'))
    wind_v = wind.tick(0)

    spots = [Spot(100, 100, 40), Spot(200, 300, 80), Spot(600, 600, 120)]
    rocket = Rocket(x=120, y=300, width=50, height=100)

    last_time = millis()

    while win.open:
        c_time = millis()
        delta = (c_time - last_time) / 1000
        n_wind = wind.tick(delta)
        if n_wind != wind_v:
            print(f'new wind: {wind_v}')

        wind_v = n_wind
        win.draw(rocket)
        win.update()
        time.sleep(0.02)
        win.clear()
        last_time = c_time

