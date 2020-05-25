from pygame import sprite, draw
from constants.C_SCREEN import HEIGHT_SIZE, WEIGHT_SIZE
import random


# Star class
class Star(sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        self.xPos = random.randint(0, WEIGHT_SIZE)
        self.yPos = random.randint(0, HEIGHT_SIZE)
        self.speed = 1

    def show(self, screen):
        draw.ellipse(screen, (255, 255, 255), (self.xPos, self.yPos, 1, 1))

    def update(self):
        self.xPos = self.xPos - self.speed
        if self.xPos <= 0:
            self.xPos = random.randint(0, WEIGHT_SIZE)