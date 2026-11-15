from math import sqrt
from enum import Enum, auto
from dataclasses import dataclass

from typing import Literal

import pygame as pg

pg.init()


@dataclass
class Keybind:
    """Dataclass for storing pygame keycodes for various actions.
    """
    move_left: int
    move_right: int
    bounce: int


@dataclass
class PlayerAction:
    """Dataclass for tracking what actions must the player take according to the user.
    """
    move_left: bool = False
    move_right: bool = False
    bounce: bool = False

    def clear(self):
        self.move_left = False
        self.move_right = False
        self.bounce = False


class PlayerState(Enum):
    """Placeholder at the moment.
    """
    IDLE = auto()


class Player(pg.sprite.Sprite):
    # Image
    WIDTH = 32
    HEIGHT = 32

    # For the color indicator of stored bounce height
    COLOR_DEFAULT = pg.Color(0, 0, 0)
    COLOR_GRAD_S = 100
    COLOR_GRAD_L = 60
    COLOR_GRAD_H_RANGE = (0, 120)
    COLOR_GRAD_VEL_RANGE = (-10, -30)

    # Physics
    ACCELERATION = 1
    FRICTION = 0.875
    GRAVITY = 1
    TERMINAL_VELOCITY = 9999
    BOUNCE_ENERGY_LOSS = 0

    KEYBINDS = Keybind(
        move_left  = pg.K_LEFT,
        move_right = pg.K_RIGHT,
        bounce     = pg.K_UP
    )

    def __init__(
        self,
        walls: pg.sprite.Group,
        pos: tuple[float, float],
        *groups
    ):
        super().__init__(*groups)
        self.walls = walls  # Reference to the level walls for collisions

        # Core
        self.pos = pg.Vector2(pos)
        self.vel = pg.Vector2(0, 0)
        self.bounce_compensate_amount = 0
        self.fall_dist = 0
        self.fell_from_y = self.pos.y
        self.last_yvel = self.vel.y

        self.last_pos = self.pos.copy()
        self.delta_pos = self.last_pos - self.pos  # Used for external access

        # Status
        self.is_grounded = False
        self.was_grounded = False
        self.actions = PlayerAction()
        self.state = PlayerState.IDLE

        # Image
        self.color = self.COLOR_DEFAULT
        self.image = pg.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos

    def update_color(self):
        # Only update the color indicator when it is relevant (on ground)
        if not self.is_grounded:
            return

        hue_change = self.COLOR_GRAD_H_RANGE[1] - self.COLOR_GRAD_H_RANGE[0]
        vel_change = self.COLOR_GRAD_VEL_RANGE[1] - self.COLOR_GRAD_VEL_RANGE[0]

        # Multiplier from 0.0 to 1.0
        # vel_factor = (self.fall_dist - self.COLOR_GRAD_VEL_RANGE[0]) / vel_change TODO:
        vel_factor = 1

        lower_cap = max(0, self.COLOR_GRAD_H_RANGE[0])
        upper_cap = min(self.COLOR_GRAD_H_RANGE[1], 360)

        hue = vel_factor * hue_change + self.COLOR_GRAD_H_RANGE[0]
        hue = max(lower_cap, hue)
        hue = min(hue, upper_cap)

        self.color = pg.Color.from_hsla(hue, self.COLOR_GRAD_S, self.COLOR_GRAD_L, 0)

    def update_image(self):
        self.update_color()
        self.image.fill(self.color)
        self.rect.x, self.rect.y = self.pos

    def resolve_collision(
        self,
        player_rect: pg.FRect,
        wall_rect: pg.FRect,
        direction: Literal['x', 'y']
    ) -> pg.Vector2:
        new_rect = player_rect.copy()
        delta = pg.Vector2(0, 0)  # Using an object due to scope limitations

        if direction == 'x':
            if self.vel.x > 0:
                delta.x = wall_rect.left - new_rect.right

            elif self.vel.x < 0:
                delta.x = wall_rect.right - new_rect.left

            new_rect.x += delta.x
            self.vel.x = 0

            print(f'resolved by moving {delta.x} in the x dir (now {new_rect.x})')

        elif direction == 'y':
            if self.vel.y > 0:
                delta.y = wall_rect.top - new_rect.bottom

                self.is_grounded = True
                if self.just_grounded():
                    new_y = new_rect.y + delta.y

                    self.fall_dist += new_y - self.fell_from_y
                    self.fell_from_y = new_y

            elif self.vel.y < 0:
                delta.y = wall_rect.bottom - new_rect.top

            new_rect.y += delta.y
            self.vel.y = 0

            print(f'resolved by moving {delta.y} in the y dir (now {new_rect.y})')

        else:
            raise ValueError(f'direction argument must be either "x" or "y". Got {direction}')

        self.pos.x, self.pos.y = new_rect.x, new_rect.y

        return delta

    def handle_collisions(self) -> dict[Literal['x', 'y'], bool]:
        collided = {'x': False, 'y': False}

        # For testing horizontal movement
        player_xvel_rect = pg.FRect(
            self.pos.x + self.vel.x,
            self.pos.y,
            self.WIDTH,
            self.HEIGHT
        )

        # For testing vertical movement
        player_yvel_rect = pg.FRect(
            self.pos.x,
            self.pos.y + self.vel.y,
            self.WIDTH,
            self.HEIGHT
        )

        for wall in self.walls:
            wall_rect = pg.FRect(wall.pos.x, wall.pos.y, wall.size[0], wall.size[1])

            if player_xvel_rect.colliderect(wall_rect):
                print('[X AXIS] COLLISION DETECTED:')
                print(f'with "{wall.id}": {wall_rect}')
                print(f'player: {player_xvel_rect} (after x+{self.vel.x})')
                print()

                collided['x'] = True
                dx, _ = self.resolve_collision(player_xvel_rect, wall_rect, 'x')

                # Currently no need to compensate for collision dx in any way

            if player_yvel_rect.colliderect(wall_rect):
                print('[Y AXIS] COLLISION DETECTED:')
                print(f'with "{wall.id}": {wall_rect}')
                print(f'player: {player_yvel_rect} (after y+{self.vel.y})')
                print()

                collided['y'] = True
                _, dy = self.resolve_collision(player_yvel_rect, wall_rect, 'y')

                # We need to compensate in the opposite direction of collision dy
                self.bounce_compensate_amount += -dy
                # Only account for gravity if are on the ground (but not just landed as we need to
                # include gravity when storing velocity) so compensation doesn't rack up while we're
                # resting on the ground
                if self.is_grounded and not self.just_grounded():
                    self.bounce_compensate_amount -= self.GRAVITY

        return collided

    def update_actions(self):
        self.keys_pressed = pg.key.get_just_pressed()
        self.keys_down = pg.key.get_pressed()

        self.actions.move_left = self.keys_down[self.KEYBINDS.move_left]
        self.actions.move_right = self.keys_down[self.KEYBINDS.move_right]
        self.actions.bounce = self.keys_pressed[self.KEYBINDS.bounce]

    def perform_actions(self):
        if self.actions.move_left:
            self.vel.x -= self.ACCELERATION

        if self.actions.move_right:
            self.vel.x += self.ACCELERATION

        if self.actions.bounce:
            if self.is_grounded:
                self.bounce()

    def calc_bounce_vel(self, height_px: float) -> float:
        return -sqrt(2 * self.GRAVITY * height_px)

    def bounce(self, extra_height: float = 0):
        self.vel.y = self.calc_bounce_vel(self.fall_dist + extra_height)

        self.fall_dist = 0

    def update_physics(self) -> pg.Vector2:
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
            self.is_grounded = False
            self.pos.y += self.vel.y

        if self.just_started_falling():
            self.fell_from_y = self.pos.y

        # Apply compensation for any y offsets due to collisions if we are about to bounce or fall
        # if self.actions.bounce or self.just_left_ground(): TODO:
        #     print(f'applied {self.bounce_compensate_amount} ({self.pos.y} -> {self.pos.y + self.bounce_compensate_amount})')

        #     self.pos.y += self.bounce_compensate_amount
        #     self.bounce_compensate_amount = 0

        return self.get_pos_change(self.pos)

    def update_state(self):
        raise NotImplementedError

    def just_grounded(self):
        return (not self.was_grounded) and self.is_grounded

    def just_left_ground(self):
        return self.was_grounded and (not self.is_grounded)

    def just_started_falling(self):
        return (self.last_yvel < 0) and (self.vel.y >= 0)

    def get_pos_change(self, new_pos: pg.Vector2) -> pg.Vector2:
        return new_pos - self.last_pos

    def update(self):
        print(f'pos {self.pos.y - 32 - 256}, vel {self.vel.y}')
        self.actions.clear()

        self.update_actions()
        self.perform_actions()
        self.delta_pos = self.update_physics()

        self.update_image()

        print(f'\nfell from: {self.fell_from_y}; fall dist: {self.fall_dist}\n')

        self.was_grounded = self.is_grounded
        self.last_pos = self.pos.copy()
        self.last_yvel = self.vel.y
