from pygame import sprite, image, event
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, USEREVENT
)
from constants.C_SCREEN import HEIGHT_SIZE, WEIGHT_SIZE, FRAME_PER_SEC
from constants.C_EVENTS import BULLET_EVENT
from components.Bullet import Bullet
import math
from os import path


class Player(sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surface = image.load(path.join('images', 'space-shooter.png'))
        self.rect = self.surface.get_rect()
        self.pixels = 64
        self.speed = 1
        self.initX = round(HEIGHT_SIZE * 0.1)
        self.initY = round(HEIGHT_SIZE / 2 - self.pixels / 2)
        self.rect.move_ip(self.initX, self.initY)  # init position of the ship
        self.maxBullets = 1
        self.bulletsAmount = self.maxBullets
        self.shootDelay = FRAME_PER_SEC / 3
        self.lastShoot = 0

    def action(self, pressed_keys, munition, state):
        if pressed_keys[K_SPACE]:
            self.shoot(munition, state)
        if pressed_keys[K_RIGHT]:
            self.move_right()
        elif pressed_keys[K_LEFT]:
            self.move_left()
        elif pressed_keys[K_DOWN]:
            self.move_down()
        elif pressed_keys[K_UP]:
            self.move_up()

    def move_right(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= WEIGHT_SIZE:
            self.rect.right = WEIGHT_SIZE

    def move_left(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_down(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= HEIGHT_SIZE:
            self.rect.bottom = HEIGHT_SIZE

    def move_up(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top <= 0:
            self.rect.top = 0

    def shoot(self, munition, state):
        if munition.__len__() == 0:
            self.bulletsAmount = self.maxBullets
        if self.bulletsAmount > 0 and math.fabs(state - self.lastShoot) > self.shootDelay:
            self.lastShoot = state
            bullet = Bullet()
            bullet.available = 0
            bullet.rect[1] = self.rect[1] + 16
            bullet.rect[0] = self.rect[0]
            self.bulletsAmount = self.bulletsAmount - 1
            e = event.Event(USEREVENT + BULLET_EVENT, content=bullet)
            event.post(e)
