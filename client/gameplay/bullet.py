import pygame

from gameplay.game_settings import *

pygame.init()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_id, pos, direction):
        super().__init__()
        self.player_id = player_id
        self.pos = pos.copy()
        self.image = pygame.transform.smoothscale(pygame.image.load("gameplay/images/bullet.png").convert_alpha(), BULLET_SIZE)
        self.rect = self.image.get_rect(center=self.pos)
        self.direction = direction

    def move(self):
        self.pos += self.direction * BULLET_SPEED
        self.rect.center = self.pos

    def update(self):
        self.move()
