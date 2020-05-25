from pygame import sprite, image, event
import random
from constants.C_SCREEN import HEIGHT_SIZE, WEIGHT_SIZE
from constants.C_SCREEN import FRAME_PER_SEC


# Reward Class
class Reward(sprite.Sprite):
    def __init__(self, img_path, reward_type, value):
        super(Reward, self).__init__()
        self.surface = image.load(img_path)
        self.reward_type = reward_type
        self.value = value
        self.rect = self.surface.get_rect()
        self.speed = 1
        self.pixels = 64
        self.initX = random.randint(WEIGHT_SIZE, WEIGHT_SIZE + self.pixels)
        self.initY = random.randint(0, HEIGHT_SIZE-self.pixels)
        self.rect.move_ip(self.initX, self.initY)  # init position of the alien
        self.delay = FRAME_PER_SEC * 2
        self.last = 0

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.left <= 0:
            self.kill()
