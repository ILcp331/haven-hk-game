import pygame as pg

pg.init()


class Bouncepad(pg.sprite.Sprite):
    COLOR = pg.Color(255, 195, 49)

    bpad_index = 0

    def __init__(
        self,
        pos: tuple[float, float],
        size: tuple[float, float],
        strength: float,
        *groups,
        **kwargs
    ):
        super().__init__(*groups)

        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = f'bpad{self.bpad_index}'
            self.bpad_index += 1

        self.pos = pg.Vector2(pos)
        self.size = size

        self.strength = strength

        self.image = pg.Surface(size)
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update_image(self):
        pass

    def update(self):
        self.update_image()
