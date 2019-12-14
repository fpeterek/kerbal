import tkinter


class Platform:

    color = '#807d75'
    width = 150
    height = 10

    def __init__(self, x, y):
        self.x = x - Platform.width//2
        self.y = y - Platform.height
        self.width = Platform.width
        self.height = Platform.height

    def draw(self, canvas: tkinter.Canvas):
        lx = self.x
        ly = self.y
        rx = self.x + self.width
        ry = self.y + self.height
        canvas.create_rectangle(lx, ly, rx, ry, fill=Platform.color, outline=Platform.color)
