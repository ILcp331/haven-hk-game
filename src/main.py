import pygame as pg

from .constants import BORDER_WALL_THICKNESS
from .utils.text import draw_lines
from .sprites.player import Player
from .sprites.wall import Wall

pg.init()


class Game:
    SPEED = 1
    FPS = 60 if SPEED <= 1 else round(60 * SPEED)

    WIDTH = 1280
    HEIGHT = 720

    BG_COLOR = pg.Color(255, 255, 255)
    DEBUG_TEXT_COLOR = pg.Color(96, 255, 96)
    DEBUG_BG_COLOR = pg.Color(0, 0, 0, 160)

    DEBUG_FONT = pg.font.SysFont('Consolas', 16)

    def __init__(self, *, allow_debug: bool = False):
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.frames = 0

        pg.display.set_caption('Hackclub Haven')

        self.running = True
        self.allow_debug = allow_debug
        self.debug_active = allow_debug
        self.debug_lines = []

        self.sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()

        # Sprites
        self.player = Player(
            self.walls,
            (self.WIDTH / 2 - Player.WIDTH / 2, BORDER_WALL_THICKNESS + Player.HEIGHT),
            self.sprites
        )

        # Level
        self.place_border_walls()
        Wall(
            (0, self.HEIGHT - 256),
            (500, BORDER_WALL_THICKNESS),
            self.sprites, self.walls
        )

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
        if self.frames % round(1 / self.SPEED) == 0:
            self.sprites.update()

        self.sprites.draw(self.window)

    def debug_update(self):
        vel_change = self.player.COLOR_GRAD_VEL_RANGE[1] - self.player.COLOR_GRAD_VEL_RANGE[0]
        vel_factor = (self.player.stored_yvel - self.player.COLOR_GRAD_VEL_RANGE[0]) / vel_change

        self.debug_lines = [
            f'Frame {self.frames} ({self.clock.get_fps():.2f}/{self.FPS} fps)',
            f'Sprites: {len(self.sprites)} | Walls: {len(self.walls)}',
            f'Player: pos {round(self.player.pos, 2)}',
            f'        vel {round(self.player.vel, 2)}',
            f'        delta {round(self.player.delta_pos, 2)} (comp: {self.player.bounce_compensate_amount})',
            f'        grounded: {self.player.is_grounded}',
            f'        stored: {self.player.stored_yvel} ({vel_factor * 100:.2f}%)',
            f'        hue: {self.player.color.hsla[0]:.2f}/{Player.COLOR_GRAD_H_RANGE[1]}'
        ]

        draw_lines(
            self.window,
            (8, 8),
            self.DEBUG_FONT,
            self.debug_lines,
            self.DEBUG_TEXT_COLOR,
            background=self.DEBUG_BG_COLOR,
            alignment='left',
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

        if self.debug_active:
            self.debug_update()

        pg.display.update()
        self.clock.tick(self.FPS)

        self.frames += 1
