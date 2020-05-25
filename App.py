import pygame
import random
import math
from os import path
from components.Alien import Alien
from components.Asteroid import Asteroid
from components.Player import Player
from components.Star import Star
from components.Reward import Reward
from constants import C_EVENTS
from constants import C_SCREEN
from constants import C_REWARDS
from constants import C_SCORES


class App:
    def __init__(self):
        self.reward = Reward(C_REWARDS.REWARDS[0][0], C_REWARDS.REWARDS[0][1], C_REWARDS.REWARDS[0][2])
        self.max_speed = C_REWARDS.MAX_SPEED_REWARD
        self.max_bullet = C_REWARDS.MAX_BULLET_REWARD
        self.screen = pygame.display.set_mode((C_SCREEN.WEIGHT_SIZE, C_SCREEN.HEIGHT_SIZE))
        self.aliens = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.components = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.stars = []
        self.player = Player()
        self.running = 1
        self.game_state = 1
        self.score = 0
        self.font = 0

    def set_events(self, alien_time, asteroid_time):
        pygame.time.set_timer(C_EVENTS.ADD_ALIEN, alien_time)
        pygame.time.set_timer(C_EVENTS.ADD_ASTEROID, asteroid_time)

    def init_components(self):
        self.components.add(self.player)
        for i in range(C_SCREEN.STARS):
            self.stars.append(Star())

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0
            if event.type == C_EVENTS.ADD_ALIEN:
                new_alien = Alien()
                self.aliens.add(new_alien)
                self.components.add(new_alien)
            if event.type == C_EVENTS.ADD_ASTEROID:
                new_asteroid = Asteroid()
                self.asteroids.add(new_asteroid)
                self.components.add(new_asteroid)
            if event.type == C_EVENTS.BULLET_EVENT + pygame.USEREVENT:
                self.bullets.add(event.content)
                self.components.add(event.content)
            if event.type == C_EVENTS.DEATH_EVENT + pygame.USEREVENT:
                self.stop_interaction()

    def render_components(self):
        for component in self.components:
            self.screen.blit(component.surface, component.rect)

    def player_action(self, keys, game_state):
        self.player.action(keys, self.bullets, game_state)

    def update_components(self):
        self.aliens.update()
        self.bullets.update()
        self.asteroids.update()
        self.reward.update()
        for star in self.stars:
            star.update()
            star.show(self.screen)

    def components_collide(self):
        hit0 = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        hit1 = pygame.sprite.spritecollideany(self.player, self.aliens)
        hit2 = pygame.sprite.spritecollideany(self.player, self.asteroids)
        hit3 = pygame.sprite.collide_rect(self.player, self.reward)
        if hit0:
            self.score += C_SCORES.KILL
        if hit1 or hit2:
            self.player.kill()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + C_EVENTS.DEATH_EVENT))

        if hit3:
            r_type = self.reward.reward_type
            r_value = self.reward.value
            self.player_upgrade(r_type, r_value)
            self.reward.kill()

    def player_upgrade(self, r_type, r_value):
        if math.fabs(self.game_state - self.reward.last) > self.reward.delay:
            self.score += C_SCORES.REWARD
            self.reward.last = self.game_state
            if r_type == C_REWARDS.BULLET_REWARD_TYPE:
                self.max_bullet = self.max_bullet - 1
                self.player.bulletsAmount = self.player.bulletsAmount + r_value
                self.player.maxBullets = self.player.maxBullets + r_value
            elif r_type == C_REWARDS.SPEED_REWARD_TYPE:
                self.max_speed = self.max_speed - 1
                self.player.speed = self.player.speed + r_value

    def send_reward(self):
        self.reward.kill()
        if self.max_bullet > 0 or self.max_speed > 0:
            num = random.randint(1, 2)
            if num == 1:
                if not self.max_bullet == 0:
                    r = C_REWARDS.REWARDS[num]
                    self.reward = Reward(r[0], r[1], r[2])
                    self.components.add(self.reward)
            elif num == 2:
                if not self.max_speed == 0:
                    r = C_REWARDS.REWARDS[num]
                    self.reward = Reward(r[0], r[1], r[2])
                    self.components.add(self.reward)

    def show_score(self):
        self.screen.blit(self.font.render('Score: ' + str(self.score), True, (255, 255, 255)), (10, 10))

    def info_text(self, state):
        if state == "death":
            size = 64
            font = pygame.font.Font(path.join('fonts', 'BebasNeue-Regular.ttf'), size)
            text = "GAME OVER"
            self.screen.blit(font.render(text, True, (255, 255, 255)), (
                (C_SCREEN.WEIGHT_SIZE/2) - ((text.__len__()-1)*size/2)/2, C_SCREEN.HEIGHT_SIZE/2 - size)
            )
            size = 32
            text = 'Score: ' + str(self.score)
            self.screen.blit(self.font.render(text, True, (255, 255, 255)), (
                (C_SCREEN.WEIGHT_SIZE/2) - ((text.__len__()-1)*(size/2))/2, C_SCREEN.HEIGHT_SIZE/2)
            )
            text = 'Restart'
            initX = (C_SCREEN.WEIGHT_SIZE / 2) - ((text.__len__())*(size/2))/2
            initY = C_SCREEN.HEIGHT_SIZE / 2 + size*2
            finalX = initX + (size/2 * (text.__len__()-1))
            finalY = initY + 32
            self.screen.blit(self.font.render(text, True, (255, 255, 255)), (
                initX, initY)
             )
            self.check_mouse(initX, finalX, initY, finalY)

    def check_mouse(self, init_x, final_x, init_y, final_y):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        if init_x < mouse[0] < final_x and init_y < mouse[1] < final_y:
            if pressed[0]:
                self.restart_interaction()

    def stop_interaction(self):
        self.set_events(0, 0)
        self.game_state = 0
        self.components.empty()
        self.bullets.empty()
        self.asteroids.empty()
        self.aliens.empty()

    def restart_interaction(self):
        self.set_events(C_EVENTS.ALIEN_TIME, C_EVENTS.ASTEROID_TIME)
        self.game_state = 1
        self.player = Player()
        self.score = 0
        self.components.add(self.player)

    def only_stars(self):
        for star in self.stars:
            star.update()
            star.show(self.screen)

    def game_loop(self):
        alien_increase = C_EVENTS.ALIEN_TIME
        asteroid_increase = C_EVENTS.ASTEROID_TIME
        while self.running:
            if self.game_state > 0:
                self.screen.fill((0, 0, 0))

                self.event_loop()
                self.render_components()

                keys = pygame.key.get_pressed()
                self.player_action(keys, self.game_state)

                self.update_components()
                self.components_collide()

                self.show_score()

                pygame.display.flip()

                self.clock.tick(C_SCREEN.FRAME_PER_SEC)

                if self.game_state >= C_SCREEN.REWARD_TIME and self.game_state > 0:
                    self.score += C_SCORES.TIME
                    self.send_reward()
                    if alien_increase > 500:
                        alien_increase = round(alien_increase * 0.90)
                    if asteroid_increase > 750:
                        asteroid_increase = round(asteroid_increase * 0.99)
                    self.set_events(alien_increase, asteroid_increase)
                    self.game_state = 1
                if self.game_state:
                    self.game_state += 1
            else:
                self.screen.fill((0, 0, 0))
                self.event_loop()
                self.only_stars()
                self.info_text('death')
                pygame.display.flip()

    def initialize(self):
        pygame.init()
        self.font = pygame.font.Font(path.join('fonts', 'BebasNeue-Regular.ttf'), 32)
        self.set_events(C_EVENTS.ALIEN_TIME, C_EVENTS.ASTEROID_TIME)
        self.init_components()
        self.game_loop()
        pygame.quit()
