from pathlib import Path
from dataclasses import dataclass

import pygame as pg

from ..constants import WIDTH, HEIGHT, BORDER_WALL_THICKNESS
from ..sprites.wall import Wall
from ..sprites.bouncepad import Bouncepad
from ..sprites.slime import SlimeWall

pg.init()


@dataclass
class LevelInfo:
    level_name: str = 'untitled'
    start_pos: tuple[int, int] = (0, 0)


class LevelLoader:
    HEADER_CHAR = '#'
    HEADER_LVL_NAME = 'name '
    HEADER_PLAYER_POS = 'start '
    HEADER_GENERATE_X = 'gen '

    SPRITE_WALL = 'wall '
    SPRITE_BPAD = 'bpad '
    SPRITE_SLIME = 'slme '

    ARGS_SEP = ','
    SPRITE_SEP = ' '

    def __init__(
        self,
        level_path: Path,
        level_info_ref: LevelInfo,
        sprites_grp_ref: pg.sprite.Group,
        walls_grp_ref: pg.sprite.Group,
        objs_grp_ref: pg.sprite.Group,
    ):
        self.lvlpath = level_path

        self.lvlinfo = level_info_ref
        self.sprites = sprites_grp_ref
        self.walls = walls_grp_ref
        self.objects = objs_grp_ref

    def generate_border_walls(
        self,
        *raw_args,
    ):
        # Parsing raw args
        thickness = BORDER_WALL_THICKNESS
        walls_tblr = [True, True, True, True]

        if len(raw_args) == 1:
            thickness = int(raw_args[0])

        if len(raw_args) == 2:
            thickness = int(raw_args[0])
            tblr = list(raw_args[1])
            walls_tblr = [i == '1' for i in tblr]

        # Placing objects
        Wall(
            (0, 0),
            (WIDTH, thickness),
            self.sprites, self.walls,
            id='ceiling',
        ) if walls_tblr[0] else ...

        Wall(
            (0, HEIGHT - thickness),
            (WIDTH, thickness),
            self.sprites, self.walls,
            id='floor',
        ) if walls_tblr[1] else ...

        Wall(
            (0, 0),
            (thickness, HEIGHT),
            self.sprites, self.walls,
            id='leftw',
        ) if walls_tblr[2] else ...

        Wall(
            (WIDTH - thickness, 0),
            (thickness, HEIGHT),
            self.sprites, self.walls,
            id='rightw',
        ) if walls_tblr[3] else ...

    def generate_x(self, gen_name: str, *raw_args):
        method_map = {
            'border': self.generate_border_walls,
        }

        generate_method = method_map[gen_name]
        generate_method(*raw_args)

    def place_wall(self, *raw_args):
        *configs, wall_id = raw_args
        x, y, w, h = map(float, configs)

        Wall(
            (x, y),
            (w, h),
            self.sprites, self.walls,
            id=wall_id,
        )

    def place_bpad(self, *raw_args):
        *configs, bpad_id = raw_args
        x, y, w, h, strength = map(float, configs)

        Bouncepad(
            (x, y),
            (w, h),
            strength,
            self.sprites, self.objects,
            id=bpad_id,
        )

    def place_slime(self, *raw_args):
        *configs, wall_id = raw_args
        x, y, w, h = map(float, configs)

        SlimeWall(
            (x, y),
            (w, h),
            self.sprites, self.walls,
            id=wall_id,
        )

    def place_x(self, sprite_name: str, *raw_args):
        method_map = {
            'wall': self.place_wall,
            'bpad': self.place_bpad,
            'slme': self.place_slime,
        }

        place_method = method_map[sprite_name]
        place_method(*raw_args)

    def parse_file_line(self, line: str):
        line = line.strip()

        # Handle Headers
        if line.startswith(self.HEADER_CHAR):
            line = line.removeprefix(self.HEADER_CHAR)

            # Set level name
            if line.startswith(self.HEADER_LVL_NAME):
                body = line.removeprefix(self.HEADER_LVL_NAME)

                self.lvlinfo.level_name = body
                return

            # Set player starting position
            if line.startswith(self.HEADER_PLAYER_POS):
                body = line.removeprefix(self.HEADER_PLAYER_POS)

                x, y = body.split(self.ARGS_SEP)
                self.lvlinfo.start_pos = (float(x), float(y))
                return

            # Object placement shortcut
            if line.startswith(self.HEADER_GENERATE_X):
                body = line.removeprefix(self.HEADER_GENERATE_X)

                gen_name, *raw_args = body.split(self.ARGS_SEP)
                self.generate_x(gen_name, *raw_args)
                return

        # Handle Level Placing
        sprite_name, raw_raw_args = line.split(self.SPRITE_SEP)
        raw_args = raw_raw_args.split(self.ARGS_SEP)

        self.place_x(sprite_name, *raw_args)

    def parse_level(self):
        with open(self.lvlpath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                self.parse_file_line(line)
