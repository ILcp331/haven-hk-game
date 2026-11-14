from dataclasses import dataclass

import pygame as pg

pg.init()


@dataclass
class Keybind:
    """Dataclass for storing pygame keycodes for various actions.
    """

    move_left: int
    move_right: int
    bounce: int
