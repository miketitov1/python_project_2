import pygame

from client.menu.button import Button
from client.network import network
from client.settings import *

from server.server_game import Message

pygame.init()


class JoinMenu:
    def __init__(self, display_surface, create_main_menu, create_connection_lost_menu, create_host_menu):
        self.display_surface = display_surface
        self.buttons = pygame.sprite.Group()

        self.create_host_menu = create_host_menu
        self.create_main_menu = create_main_menu
        self.create_connection_lost_menu = create_connection_lost_menu

        self.font = pygame.font.SysFont('Georgia', 40, bold=True)

        self.display_wrong_game_id_warning = False
        self.display_full_game_warning = False
        self.display_game_already_started_warning = False
        self.warning_status = "no warning"

        self.setup_buttons()


    def setup_buttons(self):
        unpressed = pygame.transform.smoothscale(pygame.image.load("menu/images/unpressed.png").convert_alpha(),
                                                 (209, 99))
        pressed = pygame.transform.smoothscale(pygame.image.load("menu/images/pressed.png").convert_alpha(),
                                               (209, 99))

        self.join_game_button = Button((SCREEN_WIDTH / 1.5, SCREEN_HEIGHT / 3), unpressed, pressed)
        self.buttons.add(self.join_game_button)

        self.main_menu_button = Button((SCREEN_WIDTH / 1.5, SCREEN_HEIGHT / 2), unpressed, pressed)
        self.buttons.add(self.main_menu_button)

    def get_input(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.join_game_button.mouse_button_collision():
                game_id = int(input())
                message = Message("join_game", game_id)
                network.send_data(message)
                reply = network.receive_data()
                if reply.status == "wrong_game_id":
                    self.warning_status = "display_wrong_game_id_warning"
                elif reply.status == "game_is_full":
                    self.warning_status = "display_game_is_full_warning"
                elif reply.status == "game_already_started":
                    self.warning_status = "display_game_already_started_warning"
                else:
                    player_id = reply.content
                    self.create_host_menu(player_id, game_id, is_hosting=False)
            elif self.main_menu_button.mouse_button_collision():
                self.create_main_menu()

    def update(self):
        self.get_input()
        self.buttons.update()

    def display_warning(self):
        if self.warning_status == "display_wrong_game_id_warning":
            self.display_surface.blit(self.font.render('Wrong game id', True, "red"), (SCREEN_WIDTH / 3, 0))
        elif self.warning_status == "display_game_is_full_warning":
            self.display_surface.blit(self.font.render('Game is full', True, "red"), (SCREEN_WIDTH / 3, 0))
        elif self.warning_status == "display_game_already_started_warning":
            self.display_surface.blit(self.font.render('Game already started', True, "red"), (SCREEN_WIDTH / 3, 0))

    def draw(self):
        if self.warning_status != "no warning":
            self.display_warning()
        self.buttons.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
