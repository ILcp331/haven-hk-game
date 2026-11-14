import pygame as pg

from ..utils.keybind import Keybind

pg.init()


class Player(pg.sprite.Sprite):
    SIZE = 32
    COLOR = (0, 0, 0)

    KEYBINDS = Keybind(
        move_left  = pg.K_LEFT,
        move_right = pg.K_RIGHT,
        bounce     = pg.K_SPACE
    )

    ACCELERATION = 1
    FRICTION = 0.9
    GRAVITY = 1

    def __init__(
        self,
        walls: pg.sprite.Group,
        pos: tuple[float, float],
        *groups
    ):
        super().__init__(*groups)
        self.walls = walls  # Reference to the level walls for collisions

        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0, 0)

        self.image = pg.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update_image(self):
        self.rect.x, self.rect.y = self.pos

    def move(self):
        self.keys_pressed = pg.key.get_just_pressed()
        self.keys_down = pg.key.get_pressed()

        if self.keys_down[self.KEYBINDS.move_left]:
            self.vel.x -= self.ACCELERATION

        if self.keys_down[self.KEYBINDS.move_right]:
            self.vel.x += self.ACCELERATION

        self.vel.x *= self.FRICTION
        self.vel.y += self.GRAVITY

        self.pos += self.vel

    def update(self):
        self.move()
        self.update_image()
