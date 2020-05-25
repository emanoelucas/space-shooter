from pygame import sprite, image
from constants.C_SCREEN import WEIGHT_SIZE
from os import path


# Bullet class
class Bullet(sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surface = image.load(path.join('images', 'bullet.png'))
        self.rect = self.surface.get_rect()
        self.pixels = 64
        self.speed = 4
        self.available = 1

    def update(self):
        if not self.available:  # The bullet is flying
            self.rect.move_ip(self.speed, 0)
            if self.rect.right >= WEIGHT_SIZE:
                self.kill()
