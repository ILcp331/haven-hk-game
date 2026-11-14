import pygame as pg

from .constants import FPS, WIDTH, HEIGHT

pg.init()


class Game:
    def __init__(self, *, allow_debug: bool = False):
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.frames = 0

        pg.display.set_caption('Hackclub Haven')

        self.running = True

        self.allow_debug = allow_debug
        self.debug_active = False

    def update(self):
        pass

    def debug_update(self):
        pass

    def mainloop(self):
        self.window.fill((0, 0, 0))

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_0:
                    self.debug_active = (not self.debug_active) and self.allow_debug

        self.update()
        self.debug_update()

        pg.display.update()
        self.clock.tick(FPS)

        self.frames += 1
