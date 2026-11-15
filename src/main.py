import pygame as pg

from .constants import WIDTH, HEIGHT, SPEED, FPS, BORDER_WALL_THICKNESS, LEVEL_PATHS
from .utils.text import draw_lines
from .utils.level import LevelLoader, LevelInfo
from .sprites.player import Player

pg.init()


class Game:
    BG_COLOR = pg.Color(255, 255, 255)
    DEBUG_TEXT_COLOR = pg.Color(96, 255, 96)
    DEBUG_BG_COLOR = pg.Color(0, 0, 0, 160)

    DEBUG_FONT = pg.font.SysFont('Consolas', 16)

    def __init__(self, *, allow_debug: bool = False):
        self.window = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.frames = 0

        pg.display.set_caption('Hackclub Haven')

        self.running = True
        self.allow_debug = allow_debug
        self.debug_active = False
        self.debug_lines_left = []
        self.debug_mouse_pinned_pos = []

        self.sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.objects = pg.sprite.Group()
        self.player = None
        self.lvl_info = LevelInfo()

        # Load Level
        self.reset_scene('level1')

    def update(self):
        if self.frames % round(1 / SPEED) == 0:
            self.sprites.update()

        self.sprites.draw(self.window)

    def debug_update(self):
        bheight_change = Player.COLOR_GRAD_BHEIGHT_RANGE[1] - Player.COLOR_GRAD_BHEIGHT_RANGE[0]
        bheight_factor = (self.player.fall_dist -
                          Player.COLOR_GRAD_BHEIGHT_RANGE[0]) / bheight_change

        self.debug_lines_left = [
            f'Frame {self.frames} ({self.clock.get_fps():.2f}/{FPS} fps)',
            f'Sprites: {len(self.sprites)} | Walls: {len(self.walls)}',
            f'Player: pos {round(self.player.pos, 2)}',
            f'        vel {round(self.player.vel, 2)}',
            f'        delta {round(self.player.delta_pos, 2)} (comp: {self.player.bounce_compensate_amount})',
            f'        status: isg {self.player.is_grounded} jsg {self.player.just_grounded()}',
            f'                jsf_colis {self.player.just_left_ground()} jsf_velct {self.player.just_started_falling()}',
            f'        fall_dist: {self.player.fall_dist} (from {self.player.fell_from_y})',
            f'        hue: {self.player.color.hsla[0]:.2f}/{Player.COLOR_GRAD_H_RANGE[1]} ({bheight_factor*100:.2f}%)'
        ]

        self.debug_lines_center = [
            f'[{self.lvl_info.level_name}]',
            '',
            'Mouse position',
            f'{pg.mouse.get_pos()}',
            '===== PINNED =====',
        ]

        if pg.mouse.get_just_pressed()[0]:
            self.debug_mouse_pinned_pos.append(pg.mouse.get_pos())

        for pos in self.debug_mouse_pinned_pos:
            self.debug_lines_center.append(f'{pos}')

        self.debug_lines_right = [
            'Init conditions',
            f'player init at {self.lvl_info.start_pos}',
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
            (WIDTH / 2, 8),
            self.DEBUG_FONT,
            self.debug_lines_center,
            self.DEBUG_TEXT_COLOR,
            background=self.DEBUG_BG_COLOR,
            alignment='centered',
        )

        draw_lines(
            self.window,
            (WIDTH - 8, 8),
            self.DEBUG_FONT,
            self.debug_lines_right,
            self.DEBUG_TEXT_COLOR,
            background=self.DEBUG_BG_COLOR,
            alignment='right',
        )

        # Logs
        print(f'Pinned: {self.debug_mouse_pinned_pos}')

    def load_level(self, level_id: str):
        path = LEVEL_PATHS[level_id]

        loader = LevelLoader(
            path,
            self.lvl_info,
            self.sprites,
            self.walls,
            self.objects
        )
        loader.parse_level()

    def reset_scene(self, level_id: str):
        self.sprites.empty()
        self.walls.empty()
        self.objects.empty()

        self.load_level(level_id)

        self.player = Player(
            self.walls,
            self.objects,
            self.lvl_info.start_pos,
            self.sprites
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

                if e.key == pg.K_BACKSPACE:
                    self.debug_mouse_pinned_pos = []

                if e.key == pg.K_r:
                    self.reset_scene('level1')

        self.update()

        if self.debug_active:
            self.debug_update()

        pg.display.update()
        self.clock.tick(FPS)

        self.frames += 1
