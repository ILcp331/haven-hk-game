import pygame as pg

from .wall import Wall

pg.init()


class SlimeWall(Wall):
    COLOR = pg.Color(255, 117, 239)
    ...
