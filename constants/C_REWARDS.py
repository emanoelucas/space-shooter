from os import path
BULLET_REWARD_TYPE = 1
SPEED_REWARD_TYPE = 2

MAX_BULLET_REWARD = 3
MAX_SPEED_REWARD = 2

REWARDS = [
    [path.join('images', 'asteroid.png'), 0, 0],
    [path.join('images', 'bullet9064.png'), BULLET_REWARD_TYPE, 1],
    [path.join('images', 'speed.png'), SPEED_REWARD_TYPE, 1],
]
