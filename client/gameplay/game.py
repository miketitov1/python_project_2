import pygame
import sys

from gameplay.map import *
from gameplay.game_settings import *
from gameplay.tile import Tile
from gameplay.player import Player
from gameplay.bullet import Bullet

from network import *

pygame.init()

GAME_STARTING_LOGO_SIZE = (567, 45)
NUMBER_SIZE = (84, 147)


class Game:
    def __init__(self, display_surface, resize_screen, create_pause_menu, create_main_menu, create_host_menu,
                 create_game, game_id, player_id, invite_code, map_id,
                 rounds_number, current_round):
        self.map = map_dict[map_id]
        self.screen_width = len(self.map.level_data) * self.map.tile_size
        self.screen_height = len(self.map.level_data) * self.map.tile_size

        self.display_surface = display_surface
        self.resize_screen = resize_screen
        self.resize_screen(self.screen_width, self.screen_height)
        self.create_pause_menu = create_pause_menu
        self.create_main_menu = create_main_menu
        self.create_host_menu = create_host_menu
        self.create_game = create_game

        self.game_id = game_id
        self.player_id = player_id
        self.invite_code = invite_code
        self.map_id = map_id
        self.rounds_number = rounds_number
        self.current_round = current_round
        self.status = GAME_STARTING_STATUS
        self.debug_font = pygame.font.SysFont('Georgia', 20, bold=True)
        self.debug_mode = False

        self.background = pygame.transform.smoothscale(
            pygame.image.load("menu/images/backgrounds/game_background.jpeg").convert_alpha(),
            (self.screen_width, self.screen_height))

        self.bullets = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.player_images = {}
        self.bullet_image = {}
        self.tiles = pygame.sprite.Group()
        self.setup_map(self.normalize_level_data(self.map.level_data))

        self.other_players_dict = {}
        self.other_bullets_dict = {}

        self.setup_starting_images()
        self.starting_countdown = 360
        self.finishing_countdown = 360
        self.start_game()

    @staticmethod
    def normalize_level_data(level_data):
        normalized_level_data = []
        for row in level_data:
            normalized_row = [column for column_index, column in enumerate(row) if column_index % 2 == 0]
            normalized_level_data.append(normalized_row)
        return normalized_level_data

    def setup_map(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * self.map.tile_size
                y = row_index * self.map.tile_size
                if cell == 'X':
                    tile = Tile((x, y), self.map.tile_size)
                    self.tiles.add(tile)
                if cell == str(self.player_id):
                    player_sprite = Player(self.player_id, pygame.math.Vector2(x, y),
                                           self.map.facing_angle_dict[self.player_id])

                    self.player.add(player_sprite)

    def setup_starting_images(self):
        self.logo = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/game_starting_logo.png").convert_alpha(), GAME_STARTING_LOGO_SIZE)
        self.logo_rect = self.logo.get_rect(center=(self.screen_width // 2, 190))

        self.starting_images = {}
        for i in range(1, 4):
            self.starting_images[i] = pygame.transform.smoothscale(
                pygame.image.load(f"menu/images/logos/image_{i}.png").convert_alpha(), NUMBER_SIZE)

    def start_game(self):
        if self.starting_countdown == 0:
            self.status = GAME_IN_PROGRESS_STATUS
        else:
            if self.starting_countdown > 240:
                image = self.starting_images[3]
            elif self.starting_countdown > 120:
                image = self.starting_images[2]
            else:
                image = self.starting_images[1]
            self.display_surface.blit(self.logo, self.logo_rect.topleft)
            self.display_surface.blit(image, (
                (self.screen_width - image.get_width()) // 2, (self.screen_height - image.get_height()) // 2))

            self.starting_countdown -= 1

    def finish_game(self):
        if self.finishing_countdown == 0:
            print(self.current_round, self.rounds_number)
            if self.current_round == self.rounds_number:
                self.create_host_menu(player_id=self.player_id, game_id=self.game_id, invite_code=self.invite_code,
                                      hosting=False)
            else:
                self.create_game(self.game_id, self.player_id, self.invite_code, self.map_id, self.rounds_number,
                                 self.current_round + 1)
        else:
            self.finishing_countdown -= 1

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

        for other_player_group in self.other_players_dict.values():
            other_player = other_player_group.sprite
            if other_player.hitbox_rect.colliderect(player.hitbox_rect):
                if player.speed.x < 0:
                    player.hitbox_rect.left = other_player.hitbox_rect.right
                    player.pos.x = player.hitbox_rect.centerx
                    player.speed.x = 0
                elif player.speed.x > 0:
                    player.hitbox_rect.right = other_player.hitbox_rect.left
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

        for other_player_group in self.other_players_dict.values():
            other_player = other_player_group.sprite
            if other_player.hitbox_rect.colliderect(player.hitbox_rect):
                if player.speed.y > 0:
                    player.hitbox_rect.bottom = other_player.hitbox_rect.top
                    player.pos.y = player.hitbox_rect.centery
                    player.speed.y = 0
                elif player.speed.y < 0:
                    player.hitbox_rect.top = other_player.hitbox_rect.bottom
                    player.pos.y = player.hitbox_rect.centery
                    player.speed.y = 0

    def bullets_tiles_collision(self):
        for bullet in self.bullets.sprites():
            for tile in self.tiles.sprites():
                if bullet.rect.colliderect(tile.rect):
                    bullet.kill()

    def bullets_player_collision(self):
        for other_bullets in self.other_bullets_dict.values():
            for other_bullet in other_bullets.sprites():
                if other_bullet.rect.colliderect(self.player.sprite.hitbox_rect):
                    other_bullet.kill()
                    self.destroy_player()

    def destroy_player(self):
        self.player.sprite.status = PLAYER_DESTROYED_STATUS

    def shoot(self):
        player = self.player.sprite
        if player.shoot_cooldown == 0 and player.is_shooting:
            player.shoot_cooldown = SHOOT_COOLDOWN
            bullet_spawn_pos = player.pos + player.facing_direction * player.gun_offset
            bullet = Bullet(self.player_id, bullet_spawn_pos, player.facing_direction)
            self.bullets.add(bullet)

    def encode_data(self):
        if self.debug_mode:
            print(f"[ENCODING] Encoding data {self.player}, {self.bullets}")

        player = self.player.sprite
        server_player = ServerPlayer(player.player_id, player.pos, player.facing_angle, player.status)

        server_bullets = set()
        for bullet in self.bullets:
            server_bullet = ServerBullet(bullet.player_id, bullet.pos, bullet.direction)
            server_bullets.add(server_bullet)

        return server_player, server_bullets

    def decode_data(self, other_players_dict, other_bullets_dict):
        self.other_players_dict.clear()
        for key, other_player in other_players_dict.items():
            if other_player:
                other_player_sprite = Player(key, other_player.pos, other_player.facing_angle)
                other_player_sprite.hitbox_rect.center = other_player_sprite.pos
                other_player_sprite.rect.center = other_player_sprite.hitbox_rect.center
                self.other_players_dict[key] = pygame.sprite.GroupSingle()
                self.other_players_dict[key].add(other_player_sprite)

        self.other_bullets_dict.clear()
        for key, other_bullets in other_bullets_dict.items():
            if other_bullets:
                for other_bullet in other_bullets:
                    other_bullet_sprite = Bullet(other_bullet.player_id, other_bullet.pos, other_bullet.direction)
                    other_bullet_sprite.rect.center = other_bullet_sprite.pos
                    self.other_bullets_dict[key] = pygame.sprite.Group()
                    self.other_bullets_dict[key].add(other_bullet_sprite)
        if self.debug_mode:
            print(f"[DECODED] Decoded data into {self.other_players_dict}, {self.other_bullets_dict}")

    def communication_with_server(self):
        if self.status != LEAVE_GAME_STATUS:
            message = Message(UPDATE_GAME_MESSAGE, (self.game_id, self.encode_data()))
            network.send_data(message)

            if self.debug_mode:
                print(f"[SENT] Sent data {message.content}")

            reply = network.receive_data()
            status = reply.status
            server_players_dict = reply.content[0]
            server_bullets_dict = reply.content[1]

            if self.debug_mode:
                print(f"[RECEIVED] Received data {server_players_dict}, {server_bullets_dict}")

            self.decode_data(server_players_dict, server_bullets_dict)
        elif self.status == LEAVE_GAME_STATUS:
            message = Message(LEAVE_MESSAGE, (self.game_id, self.player_id))
            network.send_data(message)
            self.create_main_menu()

    def unpause_game(self):
        self.status = GAME_IN_PROGRESS_STATUS

    def leave_game(self):
        self.status = LEAVE_GAME_STATUS

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.status == GAME_IN_PROGRESS_STATUS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.debug_mode = not self.debug_mode
                    if event.key == pygame.K_ESCAPE:
                        self.status = GAME_PAUSED_STATUS
                        self.create_pause_menu(self.unpause_game, self.leave_game, self.game_id, self.player_id)
        if self.status == GAME_IN_PROGRESS_STATUS or self.status == GAME_FINISHING_STATUS:
            self.player.sprite.get_input()

    def check_if_finish(self):
        if not len(self.other_players_dict) == 0:
            if self.status == GAME_IN_PROGRESS_STATUS:
                other_players_alive_counter = 0
                for player in self.other_players_dict.values():
                    if player.sprite.status == PLAYER_ALIVE_STATUS:
                        other_players_alive_counter += 1

                if other_players_alive_counter == 0 or (
                        self.player.sprite.status == PLAYER_DESTROYED_STATUS and other_players_alive_counter == 1):
                    self.status = GAME_FINISHING_STATUS

    def update(self):
        if self.player.sprite.status == PLAYER_ALIVE_STATUS:
            self.horizontal_movement_and_collision()
            self.vertical_movement_and_collision()
            self.bullets_tiles_collision()
            self.bullets_player_collision()
            self.shoot()

            self.player.update()
            self.bullets.update()

        if self.status != GAME_PAUSED_STATUS:
            self.get_input()

        self.communication_with_server()

        for other_player in self.other_players_dict.values():
            other_player.update()
        for other_bullets in self.other_bullets_dict.values():
            other_bullets.update()

        self.check_if_finish()

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        if self.player.sprite.status == PLAYER_ALIVE_STATUS:
            self.player.draw(self.display_surface)
            self.bullets.draw(self.display_surface)

        for other_player in self.other_players_dict.values():
            other_player.draw(self.display_surface)
        for other_bullets in self.other_bullets_dict.values():
            other_bullets.draw(self.display_surface)

        self.tiles.draw(self.display_surface)

    def debug(self):
        if self.debug_mode:
            for player_id, player_group in (self.other_players_dict | {self.player_id: self.player}).items():
                player = player_group.sprite
                if player.status == PLAYER_ALIVE_STATUS:
                    pygame.draw.rect(self.display_surface, "red", player.hitbox_rect, width=2)
                    pygame.draw.rect(self.display_surface, "yellow", player.rect, width=2)

                    speed = self.debug_font.render(f"Player {player_id} speed: {player.speed}", True, 'red')
                    pos = self.debug_font.render(f"Player {player_id} pos: {player.pos}", True, 'red')
                    center = self.debug_font.render(f"Player {player_id} center: {player.rect.center}", True, 'red')

                    self.display_surface.blit(speed, (0, (player_id - 1) * 90))
                    self.display_surface.blit(pos, (0, (player_id - 1) * 90 + 30))
                    self.display_surface.blit(center, (0, (player_id - 1) * 90 + 60))

            for bullets in (self.other_bullets_dict | {self.player_id: self.bullets}).values():
                for bullet in bullets:
                    pygame.draw.rect(self.display_surface, "orange", bullet.rect, width=2)

    def run(self):
        self.update()
        self.draw()
        self.debug()

        if self.status == GAME_STARTING_STATUS:
            self.start_game()
        elif self.status == GAME_FINISHING_STATUS:
            self.finish_game()
