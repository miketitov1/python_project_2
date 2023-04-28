import pygame
import sys
import socket

from client.menu.button import Button
from client.settings import *
from client.network import network

pygame.init()


class MainMenu:

    def __init__(self, display_surface, create_host_menu, create_join_menu, create_connection_lost_menu):
        self.display_surface = display_surface
        self.buttons = pygame.sprite.Group()

        self.create_host_menu = create_host_menu
        self.create_join_menu = create_join_menu
        self.create_connection_lost_menu = create_connection_lost_menu

        self.setup_buttons()

    def connect(self):
        if not network.is_connected:
            try:
                network.connect()
            except socket.error as error:
                self.create_connection_lost_menu()
                print(str(error))


    def setup_buttons(self):
        unpressed = pygame.transform.smoothscale(pygame.image.load("menu/images/unpressed.png").convert_alpha(),
                                                 (209, 99))
        pressed = pygame.transform.smoothscale(pygame.image.load("menu/images/pressed.png").convert_alpha(),
                                               (209, 99))

        self.host_menu_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), unpressed, pressed)
        self.buttons.add(self.host_menu_button)

        self.join_menu_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.46), unpressed, pressed)
        self.buttons.add(self.join_menu_button)

        self.exit_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.15), unpressed, pressed)
        self.buttons.add(self.exit_button)

    def get_input(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.exit_button.mouse_button_collision():
                pygame.quit()
                sys.exit()
            elif self.host_menu_button.mouse_button_collision():
                self.connect()
                if network.is_connected:
                    self.create_host_menu(0, -1, is_hosting=True)
            elif self.join_menu_button.mouse_button_collision():
                self.connect()
                if network.is_connected:
                    self.create_join_menu()

    def update(self):
        self.get_input()
        self.buttons.update()

    def draw(self):
        self.buttons.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
