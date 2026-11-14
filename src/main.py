import pygame as pg

from .constants import BORDER_WALL_THICKNESS
from .sprites.player import Player
from .sprites.wall import Wall

pg.init()


class Game:
    FPS = 60

    WIDTH = 1280
    HEIGHT = 720

    BG_COLOR = (255, 255, 255)

    def __init__(self, *, allow_debug: bool = False):
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.frames = 0

        pg.display.set_caption('Hackclub Haven')

        self.running = True
        self.allow_debug = allow_debug
        self.debug_active = False

        self.sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # Sprites
        self.player = Player(self.walls, (64, 64), self.sprites)

        # Level
        self.place_border_walls()

    def place_border_walls(self):
        # Ceiling
        Wall(
            (0, 0),
            (self.WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls
        )

        # Floor
        Wall(
            (0, self.HEIGHT - BORDER_WALL_THICKNESS),
            (self.WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls
        )

        # Left Wall
        Wall(
            (0, 0),
            (BORDER_WALL_THICKNESS, self.HEIGHT),
            self.sprites, self.walls
        )
        # Right Wall
        Wall(
            (self.WIDTH - BORDER_WALL_THICKNESS, 0),
            (BORDER_WALL_THICKNESS, self.HEIGHT),
            self.sprites, self.walls
        )

    def update(self):
        self.sprites.update()
        self.sprites.draw(self.window)

    def debug_update(self):
        print(
            f'\n'
            f'Frame {self.frames} ({self.clock.get_fps():.2f}/{self.FPS} fps)\n'
            f'Player: pos{round(self.player.pos, 2)} vel{round(self.player.vel, 2)}\n'
            f'Walls num: {len(self.walls)}'
        )

    def mainloop(self):
        self.window.fill((255, 255, 255))

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_0:
                    self.debug_active = (not self.debug_active) and self.allow_debug

        self.update()
        self.debug_update()

        pg.display.update()
        self.clock.tick(self.FPS)

        self.frames += 1
