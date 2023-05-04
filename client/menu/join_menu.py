import pygame
import sys

from menu.button import Button
from menu.inputbox import InputBox
from network import *

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

JOIN_BUTTON_SIZE = (231, 99)
EXIT_BUTTON_SIZE = (209, 99)

JOIN_GAME_LOGO_SIZE = (680, 300)


class JoinMenu:
    def __init__(self, display_surface, resize_screen, create_main_menu, create_connection_lost_menu, create_host_menu):
        self.display_surface = display_surface
        self.resize_screen = resize_screen
        self.resize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.create_host_menu = create_host_menu
        self.create_main_menu = create_main_menu
        self.create_connection_lost_menu = create_connection_lost_menu

        self.game_id = "-1"
        self.invite_code = "-1"

        self.logo = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/join_menu_logo.png").convert_alpha(), JOIN_GAME_LOGO_SIZE)
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.background = pygame.transform.smoothscale(
            pygame.image.load("menu/images/backgrounds/join_menu_background.jpeg").convert_alpha(),
            (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.font = pygame.font.Font('menu/fonts/PixelMaster.ttf', 70)

        self.display_wrong_game_id_warning = False
        self.display_full_game_warning = False
        self.display_game_already_started_warning = False
        self.warning_status = "no warning"

        self.setup_buttons()
        self.setup_inputboxes()

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        self.join_button = Button((SCREEN_WIDTH // 4, 4 * SCREEN_HEIGHT // 5), "join", JOIN_BUTTON_SIZE)
        self.buttons.add(self.join_button)

        self.exit_button = Button((2.8 * SCREEN_WIDTH // 4, 4 * SCREEN_HEIGHT // 5), "exit", EXIT_BUTTON_SIZE)
        self.buttons.add(self.exit_button)

    def setup_inputboxes(self):
        self.inputboxes = []

        self.game_id_inputbox = InputBox((SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 5), width=240, default_text="game id")
        self.inputboxes.append(self.game_id_inputbox)

        self.invite_code_inputbox = InputBox((2.8 * SCREEN_WIDTH // 4, 3 * SCREEN_HEIGHT // 5), width=340,
                                             default_text="invite code")
        self.inputboxes.append(self.invite_code_inputbox)

    def communicate_with_server(self):
        if not self.game_id.isnumeric() or not self.invite_code.isnumeric():
            self.warning_status = "display_wrong_game_id_warning"
        else:
            message = Message(JOIN_GAME_MESSAGE, (int(self.game_id), int(self.invite_code)))
            network.send_data(message)
            reply = network.receive_data()
            if reply.status == "wrong_game_id":
                self.warning_status = "display_wrong_game_id_warning"
            elif reply.status == "game_is_full":
                self.warning_status = "display_game_is_full_warning"
            elif reply.status == "game_already_started":
                self.warning_status = "display_game_already_started_warning"
            else:
                self.game_id = int(self.game_id)
                self.invite_code = int(self.invite_code)
                player_id = reply.content
                self.create_host_menu(player_id, self.game_id, self.invite_code, hosting=False)

    def get_input(self):
        for event in pygame.event.get():
            for inputbox in self.inputboxes:
                inputbox.update_text(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.join_button.mouse_button_collision():
                    self.communicate_with_server()
                elif self.exit_button.mouse_button_collision():
                    self.create_main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.create_main_menu()

    def update_user_input(self):
        self.game_id = self.game_id_inputbox.text
        self.invite_code = self.invite_code_inputbox.text

    def update(self):
        self.get_input()
        self.update_user_input()
        self.buttons.update()
        for inputbox in self.inputboxes:
            inputbox.update()

    def display_warning(self):
        warning = ""
        if self.warning_status == "display_wrong_game_id_warning":
            warning = 'Wrong game id or invite code'
        elif self.warning_status == "display_game_is_full_warning":
            warning = 'Game is full'
        elif self.warning_status == "display_game_already_started_warning":
            warning = 'Game already started'
        warning_surface = self.font.render(warning, False, "red")
        self.display_surface.blit(warning_surface, (
            (SCREEN_WIDTH - warning_surface.get_width()) // 2, (SCREEN_HEIGHT - 3 * warning_surface.get_height()) // 2))

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.logo, self.logo_rect.topleft)
        if self.warning_status != "no warning":
            self.display_warning()
        self.buttons.draw(self.display_surface)
        for inputbox in self.inputboxes:
            inputbox.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
