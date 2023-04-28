import pygame
import math

from client.gameplay.game_settings import *

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, player_id, pos, facing_angle, image):
        super().__init__()
        self.pos = pos
        self.player_id = player_id
        self.image = image
        self.basic_image = self.image

        self.hitbox_rect = self.basic_image.get_rect(center=self.pos)
        self.hitbox_rect.centerx -= 10
        self.hitbox_rect.width *= PLAYER_HITBOX_FACTOR
        self.hitbox_rect.height *= PLAYER_HITBOX_FACTOR
        self.rect = self.hitbox_rect.copy()

        self.speed = pygame.math.Vector2(0, 0)
        self.facing_direction = pygame.math.Vector2(1, 0)
        self.facing_angle = facing_angle
        self.is_accelerating = False

        self.gun_offset = GUN_OFFSET
        self.is_shooting = False
        self.shoot_cooldown = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.facing_angle += ROTATION_SPEED
            self.facing_angle %= 360
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.facing_angle -= ROTATION_SPEED
            self.facing_angle %= 360
        if keys[pygame.K_DOWN]:
            pass

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.is_accelerating = True
        else:
            self.is_accelerating = False

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.is_shooting = True
        else:
            self.is_shooting = False

    def update_shoot_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def rotate(self):
        self.image = pygame.transform.rotate(self.basic_image, -self.facing_angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)
        self.facing_direction = pygame.math.Vector2(math.cos(math.radians(self.facing_angle)),
                                                    math.sin(math.radians(self.facing_angle)))

    def update_speed(self):
        if self.is_accelerating and self.speed.magnitude() < MAX_SPEED:
            self.speed += ACCELERATION * self.facing_direction
        if self.speed.magnitude() > 0:
            passive_speed_decrease = self.speed * PASSIVE_SPEED_DECREASE_FACTOR
            self.speed -= passive_speed_decrease
        if self.speed.magnitude() < MIN_SPEED:
            self.speed = pygame.math.Vector2((0, 0))

    def update(self):
        self.rotate()
        self.update_speed()
        self.update_shoot_cooldown()
