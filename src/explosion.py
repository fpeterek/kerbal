from PIL import Image, ImageTk
import tkinter


class Explosion:

    width = 300
    height = 300
    sprites = 12
    period = 0.1

    @property
    def keepalive(self) -> bool:
        return self.phase < Explosion.sprites

    def __init__(self, x, y):
        img: Image.Image = Image.open('resources/explosion.png')
        img = img.resize((Explosion.width*Explosion.sprites, Explosion.height), Image.NONE)
        count = Explosion.sprites
        self.sprites = [
            img.crop((i*Explosion.width, 0, Explosion.width*(i+1), Explosion.height)) for i in range(0, count)
        ]
        self.sprites = list(map(lambda image: ImageTk.PhotoImage(image), self.sprites))
        self.phase = 0
        self.counter = 0.0
        self.x = x - Explosion.width // 2
        self.y = y - Explosion.height // 2

    def tick(self, dt: float):
        self.counter += dt
        if self.counter > Explosion.period:
            self.phase = int(self.counter // Explosion.period)

    def draw(self, canvas: tkinter.Canvas):
        if self.keepalive:
            canvas.create_image(self.x, self.y, image=self.sprites[self.phase], anchor=tkinter.NW)
