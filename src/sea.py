import tkinter


class Sea:

    color = '#072aab'

    def __init__(self, width, height):
        self.win_width = width
        self.win_height = height
        self.width = width
        self.height = height / 10
        self.x = 0
        self.y = height - self.height

    def draw(self, canvas: tkinter.Canvas):
        canvas.create_rectangle(self.x, self.y, self.width, self.y + self.height, fill=Sea.color, outline=Sea.color)


class SeaBackground(Sea):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.height *= 1.5
        self.y = height - self.height