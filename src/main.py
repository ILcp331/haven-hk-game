import pygame as pg

from .constants import FPS, WIDTH, HEIGHT, BORDER_WALL_THICKNESS
from .sprites.player import Player
from .sprites.wall import Wall

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
            (WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls
        )

        # Floor
        Wall(
            (0, HEIGHT - BORDER_WALL_THICKNESS),
            (WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls
        )

        # Left Wall
        Wall(
            (0, 0),
            (BORDER_WALL_THICKNESS, HEIGHT),
            self.sprites, self.walls
        )
        # Right Wall
        Wall(
            (WIDTH - BORDER_WALL_THICKNESS, 0),
            (BORDER_WALL_THICKNESS, HEIGHT),
            self.sprites, self.walls
        )

    def update(self):
        self.sprites.update()
        self.sprites.draw(self.window)

    def debug_update(self):
        print(
            f'(FPS: {self.clock.get_fps():.2f}) '
            f'Player: pos{round(self.player.pos, 2)} vel{round(self.player.vel, 2)}; '
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
        self.clock.tick(FPS)

        self.frames += 1
