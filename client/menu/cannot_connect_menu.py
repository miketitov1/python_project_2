import pygame
import sys

from menu.button import Button

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

EXIT_BUTTON_SIZE = (209, 99)

CANNOT_CONNECT_MENU_LOGO_SIZE = (638, 154)


class CannotConnectMenu:
    def __init__(self, display_surface, resize_screen, create_main_menu):
        self.display_surface = display_surface
        self.resize_screen = resize_screen
        self.resize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.create_main_menu = create_main_menu

        self.logo = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/cannot_connect_menu_logo.png").convert_alpha(), CANNOT_CONNECT_MENU_LOGO_SIZE)
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.background = pygame.transform.smoothscale(
            pygame.image.load("menu/images/backgrounds/cannot_connect_menu_background3.jpeg").convert_alpha(),
            (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.setup_buttons()

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        self.exit_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT - EXIT_BUTTON_SIZE[1]), "exit", EXIT_BUTTON_SIZE)
        self.buttons.add(self.exit_button)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.exit_button.mouse_button_collision():
                    self.create_main_menu()

    def update(self):
        self.get_input()
        self.buttons.update()

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.buttons.draw(self.display_surface)
        self.display_surface.blit(self.logo, self.logo_rect.topleft)

    def run(self):
        self.update()
        self.draw()
