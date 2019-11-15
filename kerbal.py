from rocket import Rocket
from window import Window
import time


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
    spots = [Spot(100, 100, 40), Spot(200, 300, 80), Spot(600, 600, 120)]
    rocket = Rocket(x=120, y=300, width=50, height=100)
    while win.open:
        win.draw(rocket)
        for spot in spots:
            spot.x += 1 if spot.x + spot.rad < win.width else 0
            spot.y += 1 if spot.y + spot.rad < win.height else 0
            win.draw(spot)
        win.update()
        time.sleep(0.02)
        win.clear()

