import pygame
import sys
import socket

from menu.button import Button
from network import network

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

HOST_GAME_BUTTON_SIZE = (429, 99)
JOIN_GAME_BUTTON_SIZE = (451, 99)
EXIT_BUTTON_SIZE = (209, 99)

GAME_LOGO_SIZE = (450, 262)


class MainMenu:
    def __init__(self, display_surface, resize_screen, create_host_menu, create_join_menu, create_connection_lost_menu):
        self.display_surface = display_surface
        self.resize_screen = resize_screen
        self.resize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.create_host_menu = create_host_menu
        self.create_join_menu = create_join_menu
        self.create_connection_lost_menu = create_connection_lost_menu

        self.logo = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/game_logo.png").convert_alpha(), GAME_LOGO_SIZE)
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.background = pygame.transform.smoothscale(pygame.image.load("menu/images/backgrounds/main_menu_background.png").convert_alpha(),
                                                       (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.setup_buttons()

    def connect(self):
        if not network.connected:
            try:
                network.connect()
            except socket.error as error:
                self.create_connection_lost_menu()
                print(str(error))

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        self.host_game_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), "host_game", HOST_GAME_BUTTON_SIZE)
        self.buttons.add(self.host_game_button)

        self.join_game_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.46), "join_game", JOIN_GAME_BUTTON_SIZE)
        self.buttons.add(self.join_game_button)

        self.exit_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.15), "exit", EXIT_BUTTON_SIZE)
        self.buttons.add(self.exit_button)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.mouse_button_collision():
                    pygame.quit()
                    sys.exit()
                elif self.host_game_button.mouse_button_collision():
                    self.connect()
                    if network.connected:
                        self.create_host_menu(player_id=1, game_id=-1, invite_code=-1, hosting=True)
                elif self.join_game_button.mouse_button_collision():
                    self.connect()
                    if network.connected:
                        self.create_join_menu()

    def update(self):
        self.get_input()
        self.buttons.update()

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.logo, self.logo_rect.topleft)
        self.buttons.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
