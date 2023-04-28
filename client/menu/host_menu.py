import pygame
import socket

from client.menu.button import Button
from client.network import network
from client.settings import *
from client.gameplay.map_settings import *

from server.server_game import Message

pygame.init()


class HostMenu:
    def __init__(self, display_surface, create_main_menu, create_connection_lost_menu, create_game, player_id, game_id,
                 is_hosting):
        self.create_main_menu = create_main_menu
        self.create_connection_lost_menu = create_connection_lost_menu
        self.create_game = create_game

        self.player_id = player_id
        self.game_id = game_id
        self.map = map_1

        if is_hosting:
            self.ask_server_to_create_game()

        self.display_surface = display_surface

        self.font = pygame.font.SysFont('Georgia', 40, bold=True)
        self.surface = self.font.render('Your game id:' + str(self.game_id), True, "red")
        self.surface1 = self.font.render('You' + str(self.game_id), True, "blue")

        self.players = {}

        self.setup_buttons()

    def ask_server_to_create_game(self):
        try:
            message = Message("create_new_game", None)
            network.send_data(message)

            reply = network.receive_data()
            self.game_id = reply.content
            print(f"[NEW GAME]: You have created a new game {self.game_id}")
        except socket.error as error:
            print(str(error))

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        unpressed = pygame.transform.smoothscale(pygame.image.load("menu/images/unpressed.png").convert_alpha(),
                                                 (209, 99))
        pressed = pygame.transform.smoothscale(pygame.image.load("menu/images/pressed.png").convert_alpha(),
                                               (209, 99))

        self.game_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3), unpressed, pressed)
        self.buttons.add(self.game_button)

        self.main_menu_button = Button((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), unpressed, pressed)
        self.buttons.add(self.main_menu_button)

    def get_input(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.game_button.mouse_button_collision():
                message = Message("start_game", self.game_id)
                network.send_data(message)
                self.create_game(map_1, self.game_id, self.player_id)
            elif self.main_menu_button.mouse_button_collision():
                message = Message("leaving_game", (self.game_id, self.player_id))
                network.send_data(message)
                self.create_main_menu()

    def update_players_and_status(self):
        request = Message("update_host_menu", self.game_id)
        network.send_data(request)

        reply = network.receive_data()
        self.players = reply.content
        if reply.status == "started":
            self.create_game(map_1, self.game_id, self.player_id)

    def update(self):
        self.update_players_and_status()
        self.get_input()
        self.buttons.update()

    def draw_players(self):
        for key in range(0, 4):
            if key in self.players.keys():
                color = "green"
            else:
                color = "red"
            if key == self.player_id:
                pygame.draw.rect(self.surface1, color,
                                 pygame.Rect(SCREEN_WIDTH * key / 4, SCREEN_HEIGHT / 2, 60, 60))
            pygame.draw.rect(self.display_surface, color,
                             pygame.Rect(SCREEN_WIDTH * key / 4, SCREEN_HEIGHT / 2, 60, 60))

    def draw(self):
        self.buttons.draw(self.display_surface)
        self.draw_players()
        self.display_surface.blit(self.surface, (SCREEN_WIDTH / 2, 0))

    def run(self):
        self.update()
        self.draw()
