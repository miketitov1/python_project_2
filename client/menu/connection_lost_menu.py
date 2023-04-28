import pygame

from client.menu.button import Button
from client.settings import *

pygame.init()


class ConnectionLostMenu:
    def __init__(self, display_surface, create_main_menu):
        self.display_surface = display_surface
        self.buttons = pygame.sprite.Group()

        self.create_main_menu = create_main_menu

        self.setup_buttons()

    def setup_buttons(self):
        unpressed = pygame.transform.smoothscale(pygame.image.load("menu/images/unpressed.png").convert_alpha(),
                                                 (209, 99))
        pressed = pygame.transform.smoothscale(pygame.image.load("menu/images/pressed.png").convert_alpha(),
                                               (209, 99))

        self.main_menu_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10), unpressed, pressed)
        self.buttons.add(self.main_menu_button)

    def get_input(self):
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.main_menu_button.mouse_button_collision():
                self.create_main_menu()

    def update(self):
        self.get_input()
        self.buttons.update()

    def draw(self):
        self.buttons.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
