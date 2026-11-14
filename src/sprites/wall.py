import pygame as pg

pg.init()


class Wall(pg.sprite.Sprite):
    COLOR = pg.Color(128, 128, 128)

    def __init__(
        self,
        pos: tuple[float, float],
        size: tuple[float, float],
        *groups
    ):
        super().__init__(*groups)

        self.pos = pg.Vector2(pos)
        self.size = size

        self.image = pg.Surface(size)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update_image(self):
        pass

    def update(self):
        self.update_image()
