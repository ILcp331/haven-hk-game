import pygame as pg

pg.init()


class Wall(pg.sprite.Sprite):
    COLOR = pg.Color(128, 128, 128)

    wall_index = 0

    def __init__(
        self,
        pos: tuple[float, float],
        size: tuple[float, float],
        *groups,
        **kwargs
    ):
        super().__init__(*groups)

        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = f'wall_{self.wall_index}'
            self.wall_index += 1

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
