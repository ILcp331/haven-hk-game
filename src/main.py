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

    PLAYER_INIT_POS = (
        WIDTH / 2 - Player.WIDTH / 2,
        BORDER_WALL_THICKNESS + 256
    )

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
        self.debug_lines_left = []

        self.sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.objects = pg.sprite.Group()

        # Sprites
        self.player = Player(self.walls, self.objects, self.PLAYER_INIT_POS, self.sprites)

        # Level
        self.place_border_walls()
        Wall(
            (0, self.HEIGHT - 256),
            (600, BORDER_WALL_THICKNESS),
            self.sprites, self.walls,
            id='platform'
        )

    def place_border_walls(self):
        Wall(
            (0, 0),
            (self.WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls,
            id='ceiling',
        )

        Wall(
            (0, self.HEIGHT - BORDER_WALL_THICKNESS),
            (self.WIDTH, BORDER_WALL_THICKNESS),
            self.sprites, self.walls,
            id='floor',
        )

        Wall(
            (0, 0),
            (BORDER_WALL_THICKNESS, self.HEIGHT),
            self.sprites, self.walls,
            id='leftw',
        )

        Wall(
            (self.WIDTH - BORDER_WALL_THICKNESS, 0),
            (BORDER_WALL_THICKNESS, self.HEIGHT),
            self.sprites, self.walls,
            id='rightw',
        )

    def update(self):
        if self.frames % round(1 / self.SPEED) == 0:
            self.sprites.update()

        self.sprites.draw(self.window)

    def debug_update(self):
        bheight_change = Player.COLOR_GRAD_BHEIGHT_RANGE[1] - Player.COLOR_GRAD_BHEIGHT_RANGE[0]
        bheight_factor = (self.player.fall_dist - Player.COLOR_GRAD_BHEIGHT_RANGE[0]) / bheight_change

        self.debug_lines_left = [
            f'Frame {self.frames} ({self.clock.get_fps():.2f}/{self.FPS} fps)',
            f'Sprites: {len(self.sprites)} | Walls: {len(self.walls)}',
            f'Player: pos {round(self.player.pos, 2)}',
            f'        vel {round(self.player.vel, 2)}',
            f'        delta {round(self.player.delta_pos, 2)} (comp: {self.player.bounce_compensate_amount})',
            f'        status: isg {self.player.is_grounded} jsg {self.player.just_grounded()}',
            f'                jsf_colis {self.player.just_left_ground()} jsf_velct {self.player.just_started_falling()}',
            f'        fall_dist: {self.player.fall_dist} (from {self.player.fell_from_y})',
            f'        hue: {self.player.color.hsla[0]:.2f}/{Player.COLOR_GRAD_H_RANGE[1]} ({bheight_factor*100:.2f}%)'
        ]

        self.debug_lines_right = [
            'Init conditions',
            f'player init at {self.PLAYER_INIT_POS}',
            f'player size: {Player.WIDTH}x{Player.HEIGHT}',
            'player physics',
            f'{Player.GRAVITY} = grav',
            f'{Player.FRICTION} = fric',
            f'{Player.TERMINAL_VELOCITY} = maxv',
            f'{Player.BOUNCE_ENERGY_LOSS} = elos',
            f'wall thickness: {BORDER_WALL_THICKNESS}',
        ]

        draw_lines(
            self.window,
            (8, 8),
            self.DEBUG_FONT,
            self.debug_lines_left,
            self.DEBUG_TEXT_COLOR,
            background=self.DEBUG_BG_COLOR,
            alignment='left',
        )

        draw_lines(
            self.window,
            (self.WIDTH - 8, 8),
            self.DEBUG_FONT,
            self.debug_lines_right,
            self.DEBUG_TEXT_COLOR,
            background=self.DEBUG_BG_COLOR,
            alignment='right',
        )

    def mainloop(self):
        print(f'======== FRAME {self.frames} ========')
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
