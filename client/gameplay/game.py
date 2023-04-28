import pygame

from client.gameplay.map_settings import *
from client.gameplay.game_settings import *
from client.gameplay.tile import Tile
from client.gameplay.player import Player
from client.gameplay.bullet import Bullet

from client.network import network

from server.server_game import Message
from server.server_game import ServerPlayer
from server.server_game import ServerBullet

pygame.init()


class Game:
    def __init__(self, surface, level_data, game_id, player_id):
        self.display_surface = surface
        self.game_id = game_id
        self.player_id = player_id

        self.bullets = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup_images()
        self.setup_map(self.normalize_level_data(level_data))

        self.players_dict = {self.player_id: self.player}
        self.bullets_dict = {self.player_id: self.bullets}

    def normalize_level_data(self, level_data):
        normalized_level_data = []
        for row in level_data:
            normalized_row = [column for column_index, column in enumerate(row) if column_index % 2 == 0]
            normalized_level_data.append(normalized_row)
        return normalized_level_data

    def setup_images(self):
        self.player_images = {}
        self.player_images[0] = pygame.transform.smoothscale(
            pygame.image.load("gameplay/images/player_0.png").convert_alpha(), PLAYER_SIZE)
        self.player_images[1] = pygame.transform.smoothscale(
            pygame.image.load("gameplay/images/player_1.png").convert_alpha(), PLAYER_SIZE)
        self.player_images[2] = pygame.transform.smoothscale(
            pygame.image.load("gameplay/images/player_2.png").convert_alpha(), PLAYER_SIZE)
        self.player_images[3] = pygame.transform.smoothscale(
            pygame.image.load("gameplay/images/player_3.png").convert_alpha(), PLAYER_SIZE)

        self.bullet_image = pygame.transform.smoothscale(
            pygame.image.load("gameplay/images/bullet.png").convert_alpha(), BULLET_SIZE)

    def setup_map(self, layout):
        self.tiles = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == 'X':
                    tile = Tile((x, y), TILE_SIZE)
                    self.tiles.add(tile)
                if cell == str(self.player_id):
                    player_sprite = Player(self.player_id, pygame.math.Vector2(x, y), FACING_ANGLE_DICT[self.player_id],
                                           self.player_images[self.player_id])
                    self.player.add(player_sprite)

    def horizontal_movement_and_collision(self):
        player = self.player.sprite
        player.pos.x += player.speed.x
        player.hitbox_rect.centerx = player.pos.x
        player.rect.centerx = player.hitbox_rect.centerx

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox_rect):
                if player.speed.x < 0:
                    player.hitbox_rect.left = tile.rect.right
                    player.pos.x = player.hitbox_rect.centerx
                    player.speed.x = 0
                elif player.speed.x > 0:
                    player.hitbox_rect.right = tile.rect.left
                    player.pos.x = player.hitbox_rect.centerx
                    player.speed.x = 0

    def vertical_movement_and_collision(self):
        player = self.player.sprite
        player.pos.y += player.speed.y
        player.hitbox_rect.centery = player.pos.y
        player.rect.centery = player.hitbox_rect.centery

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.hitbox_rect):
                if player.speed.y > 0:
                    player.hitbox_rect.bottom = tile.rect.top
                    player.pos.y = player.hitbox_rect.centery
                    player.speed.y = 0
                elif player.speed.y < 0:
                    player.hitbox_rect.top = tile.rect.bottom
                    player.pos.y = player.hitbox_rect.centery
                    player.speed.y = 0

    def bullet_collision(self):
        for bullet in self.bullets.sprites():
            for tile in self.tiles.sprites():
                if bullet.rect.colliderect(tile.rect):
                    bullet.kill()

    def shoot(self):
        player = self.player.sprite
        if player.shoot_cooldown == 0 and player.is_shooting:
            player.shoot_cooldown = SHOOT_COOLDOWN
            bullet_spawn_pos = player.pos + player.facing_direction * player.gun_offset
            bullet = Bullet(self.player_id, bullet_spawn_pos, player.facing_direction, self.bullet_image)
            self.bullets.add(bullet)

    def convert_server_to_client(self, server_players_dict, server_bullets_dict):
        self.players_dict.clear()
        for key, server_player in server_players_dict.items():
            if server_player:
                player_sprite = Player(key, server_player.pos, server_player.facing_angle, self.player_images[key])
                self.players_dict[key] = pygame.sprite.GroupSingle()
                self.players_dict[key].add(player_sprite)

        self.bullets_dict.clear()
        for key, server_bullets in server_bullets_dict.items():
            if server_bullets:
                for bullet in server_bullets:
                    bullet_sprite = Bullet(bullet.player_id, bullet.pos, bullet.direction, self.bullet_image)
                    self.bullets_dict[key] = pygame.sprite.Group()
                    self.bullets_dict[key].add(bullet_sprite)

        print(f"[DECODED] Decoded data into {self.players_dict}, {self.bullets_dict}")

    def convert_client_to_server(self):

        print(f"[ENCODING] Encoding data {self.player}, {self.bullets}")

        player = self.player.sprite
        server_player = ServerPlayer(player.player_id, player.pos, player.facing_angle)

        server_bullets = set()
        for bullet in self.bullets:
            server_bullet = ServerBullet(bullet.player_id, bullet.pos, bullet.direction)
            server_bullets.add(server_bullet)

        return server_player, server_bullets

    def update_players_and_bullets(self):
        message = Message("update_game", (self.game_id, self.convert_client_to_server()))
        network.send_data(message)

        print(f"[SENT] Sent data {message.content}")

        reply = network.receive_data()
        status = reply.status
        server_players_dict = reply.content[0]
        server_bullets_dict = reply.content[1]

        print(f"[RECEIVED] Received data {server_players_dict}, {server_bullets_dict}")

        self.convert_server_to_client(server_players_dict, server_bullets_dict)

        self.players_dict[self.player_id] = self.player
        self.bullets_dict[self.player_id] = self.bullets

    def update(self):
        self.horizontal_movement_and_collision()
        self.vertical_movement_and_collision()
        self.bullet_collision()
        self.shoot()

        self.update_players_and_bullets()

        self.player.sprite.get_input()

        for player in self.players_dict.values():
            player.update()
        for bullets in self.bullets_dict.values():
            bullets.update()

    def draw(self):
        for player in self.players_dict.values():
            player.draw(self.display_surface)
        for bullets in self.bullets_dict.values():
            bullets.draw(self.display_surface)
        self.tiles.draw(self.display_surface)

    def debug(self):
        player = self.player.sprite
        pygame.draw.rect(self.display_surface, "red", player.hitbox_rect, width=2)
        pygame.draw.rect(self.display_surface, "yellow", player.rect, width=2)

        for bullet in self.bullets.sprites():
            pygame.draw.rect(self.display_surface, "orange", bullet.rect, width=2)

        debug_font = pygame.font.SysFont('Georgia', 20, bold=True)
        speed = debug_font.render('speed' + str(player.speed), True, 'red')
        pos = debug_font.render('pos' + str(player.pos), True, 'red')
        self.display_surface.blit(speed, (0, 0))
        self.display_surface.blit(pos, (0, 30))

    def run(self):
        self.update()
        self.draw()
        self.debug()
