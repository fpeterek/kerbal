import tkinter


class Window:

    def __init__(self, win_size):
        self.window_size = win_size
        self.__is_open = False

        self.master = tkinter.Tk()
        self.master.title('Playground')
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.close())
        self.master.bind('<Escape>', lambda e: self.close())

        self.canvas = tkinter.Canvas(self.master, width=win_size[0],
                                     height=win_size[1], background='light blue')
        self.canvas.pack(fill=tkinter.BOTH, expand=1)
        self.__is_open = True

    def close(self):
        self.master.destroy()
        self.__is_open = False

    def add_handler(self, key, handler):
        self.master.bind(key, handler)

    @property
    def width(self):
        return self.master.winfo_width()

    @property
    def height(self):
        return self.master.winfo_height()

    @property
    def open(self):
        return self.__is_open

    def update(self):
        self.master.update()

    def draw(self, drawable):
        drawable.draw(self.canvas)

    def clear(self):
        self.canvas.delete('all')

    def get_window_size(self):
        return self.master.winfo_width(), self.master.winfo_height()
