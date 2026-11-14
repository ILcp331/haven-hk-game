from typing import Literal

import pygame as pg

from ..utils.keybind import Keybind

pg.init()


class Player(pg.sprite.Sprite):
    WIDTH = 32
    HEIGHT = 32
    COLOR = (0, 0, 0)

    KEYBINDS = Keybind(
        move_left  = pg.K_LEFT,
        move_right = pg.K_RIGHT,
        bounce     = pg.K_SPACE
    )

    ACCELERATION = 1
    FRICTION = 0.875
    GRAVITY = 1
    TERMINAL_VELOCITY = 24

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

        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update_image(self):
        self.rect.x, self.rect.y = self.pos

    def resolve_collision(
        self,
        wall_rect: pg.Rect,
        direction: Literal['x', 'y']
    ) -> pg.Vector2:
        new_pos = self.pos.copy()

        if direction == 'x':
            # Was moving right
            if self.vel.x > 0:
                new_pos.x = wall_rect.left - self.WIDTH

            # Was moving left
            else:
                new_pos.x = wall_rect.right

            self.vel.x = 0

        elif direction == 'y':
            # Was moving down
            if self.vel.y > 0:
                new_pos.y = wall_rect.top - self.HEIGHT

            # Was moving up
            else:
                new_pos.y = wall_rect.bottom

            self.vel.y = 0

        else:
            raise ValueError(f'direction argument must be either "x" or "y". Got {direction}')

        return new_pos

    def handle_collisions(self):
        collided = {'x': False, 'y': False}

        # Horizontal movement
        player_xvel_rect = pg.Rect(
            self.pos.x + self.vel.x, self.pos.y,
            self.WIDTH, self.HEIGHT
        )

        # Vertical movement
        player_yvel_rect = pg.Rect(
            self.pos.x, self.pos.y + self.vel.y,
            self.WIDTH, self.HEIGHT
        )

        for wall in self.walls:
            wall_rect = pg.Rect(wall.pos.x, wall.pos.y, wall.size[0], wall.size[1])

            if player_xvel_rect.colliderect(wall_rect):
                collided['x'] = True
                self.pos = self.resolve_collision(wall_rect, 'x')

            if player_yvel_rect.colliderect(wall_rect):
                collided['y'] = True
                self.pos = self.resolve_collision(wall_rect, 'y')

        return collided

    def move(self):
        self.keys_pressed = pg.key.get_just_pressed()
        self.keys_down = pg.key.get_pressed()

        if self.keys_down[self.KEYBINDS.move_left]:
            self.vel.x -= self.ACCELERATION

        if self.keys_down[self.KEYBINDS.move_right]:
            self.vel.x += self.ACCELERATION

        self.vel.x *= self.FRICTION
        self.vel.y += self.GRAVITY
        self.vel.y = min(self.vel.y, self.TERMINAL_VELOCITY)

        # Tests for collisions at a new position based on velocity, each axis tested independently
        # If a collision is made, player snaps to colliding wall
        # If a collision is not made, velocity is applied to pos later
        collided_by_dir = self.handle_collisions()

        # Apply velocity for axes where a collision was not detected
        if not collided_by_dir['x']:
            self.pos.x += self.vel.x

        if not collided_by_dir['y']:
            self.pos.y += self.vel.y

    def update(self):
        self.move()
        self.update_image()
