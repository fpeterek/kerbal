from PIL import Image, ImageTk
import tkinter


class Explosion:

    width = 300
    height = 300
    sprites = 12
    period = 0.1

    sheet = None

    @property
    def keepalive(self) -> bool:
        return self.phase < Explosion.sprites

    @staticmethod
    def load_spritesheet():
        img: Image.Image = Image.open('resources/explosion.png')
        img = img.resize((Explosion.width * Explosion.sprites, Explosion.height), Image.NONE)
        count = Explosion.sprites
        sheet = [
            img.crop((i * Explosion.width, 0, Explosion.width * (i + 1), Explosion.height)) for i in range(0, count)
        ]
        Explosion.sheet = list(map(lambda image: ImageTk.PhotoImage(image), sheet))

    def __init__(self, x, y):
        if not Explosion.sheet:
            Explosion.load_spritesheet()

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
            canvas.create_image(self.x, self.y, image=Explosion.sheet[self.phase], anchor=tkinter.NW)
