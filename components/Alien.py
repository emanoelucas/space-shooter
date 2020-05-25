from constants.C_SCREEN import HEIGHT_SIZE, WEIGHT_SIZE
from pygame import sprite, image
import random
from os import path


# Alien
class Alien(sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        self.surface = image.load(path.join('images','alien.png'))
        self.rect = self.surface.get_rect()
        self.pixels = 64
        self.speed = random.randint(2, 3)
        self.initX = random.randint(WEIGHT_SIZE, WEIGHT_SIZE + self.pixels)
        self.initY = random.randint(0, HEIGHT_SIZE-self.pixels)
        self.rect.move_ip(self.initX, self.initY)  # init position of the alien

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left <= 0:
            self.kill()
