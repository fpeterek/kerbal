
class GravityPoint:

    rad = 10

    def __init__(self, x, y, color='#f00000'):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, canvas):
        return canvas.create_oval(self.x - GravityPoint.rad, self.y - self.rad,
                                  self.x + GravityPoint.rad, self.y + self.rad,
                                  fill=self.color)

