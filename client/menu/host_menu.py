import pygame
import socket
import sys

from menu.button import Button
from menu.selectbox import SelectBox
from network import *

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

START_BUTTON_SIZE = (253, 99)
EXIT_BUTTON_SIZE = (209, 99)
YOU_IMAGE_SIZE = (88, 40)

MAP_SELECTBOX_SIZE = (253, 99)
ROUND_SELECTBOX_SIZE = (374, 99)

HOST_MENU_LOGO_SIZE = (624, 80)

GAMEMODE_DEATHMATCH = "deathmatch"
GAMEMODE_TEAM_DEATHMATCH = "team deathmatch"


class HostMenu:
    def __init__(self, display_surface, resize_screen, create_main_menu, create_connection_lost_menu, create_game,
                 player_id, game_id, invite_code, hosting):
        self.player_id = player_id
        self.game_id = game_id
        self.invite_code = invite_code

        self.display_surface = display_surface
        self.resize_screen = resize_screen
        self.resize_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.create_main_menu = create_main_menu
        self.create_connection_lost_menu = create_connection_lost_menu
        self.create_game = create_game

        self.map_id = 1
        self.rounds_number = 1
        self.selection_changed = False

        if hosting:
            self.ask_server_to_create_game()

        self.font = pygame.font.Font('menu/fonts/PixelMaster.ttf', 70)
        self.game_id_surface = self.font.render(f"Game id: {self.game_id}", False, "white")
        self.invite_code_surface = self.font.render(f"Invite code: {self.invite_code}", False, "white")

        self.you_image = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/you_image.png").convert_alpha(),
            YOU_IMAGE_SIZE)
        self.logo = pygame.transform.smoothscale(
            pygame.image.load("menu/images/logos/host_menu_logo.png").convert_alpha(), HOST_MENU_LOGO_SIZE)
        self.logo_rect = self.logo.get_rect(center=(SCREEN_WIDTH // 2, 60))

        self.background = pygame.transform.smoothscale(
            pygame.image.load("menu/images/backgrounds/host_menu_background.jpeg").convert_alpha(),
            (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.players = {}

        self.setup_buttons()
        self.setup_selectboxes()

    def ask_server_to_create_game(self):
        try:
            message = Message(CREATE_GAME_MESSAGE, None)
            network.send_data(message)

            reply = network.receive_data()
            self.game_id, self.invite_code = reply.content
        except socket.error as error:
            print(str(error))

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        self.start_button = Button((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 1.35), "start", START_BUTTON_SIZE)
        self.buttons.add(self.start_button)

        self.exit_button = Button((SCREEN_WIDTH // 4, SCREEN_HEIGHT // 1.1), "exit", EXIT_BUTTON_SIZE)
        self.buttons.add(self.exit_button)

    def setup_selectboxes(self):
        self.selectboxes = pygame.sprite.Group()

        self.map_selectbox = SelectBox((SCREEN_WIDTH // 1.4, SCREEN_HEIGHT // 1.35), "map", 5, MAP_SELECTBOX_SIZE)
        self.selectboxes.add(self.map_selectbox)

        self.round_selectbox = SelectBox((SCREEN_WIDTH // 1.4, SCREEN_HEIGHT // 1.1), "number_of_rounds", 5, ROUND_SELECTBOX_SIZE)
        self.selectboxes.add(self.round_selectbox)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for selectbox in self.selectboxes.sprites():
                selectbox.update_selection(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.mouse_button_collision():
                    message = Message(START_GAME_MESSAGE, self.game_id)
                    network.send_data(message)
                elif self.exit_button.mouse_button_collision():
                    message = Message(LEAVE_MESSAGE, (self.game_id, self.player_id))
                    network.send_data(message)
                    self.create_main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    message = Message(LEAVE_MESSAGE, (self.game_id, self.player_id))
                    network.send_data(message)
                    self.create_main_menu()


    def communication_with_server(self):
        map_id = None
        rounds_number = None
        if self.selection_changed:
            self.selection_changed = False
            map_id = self.map_id
            rounds_number = self.rounds_number

        request = Message(UPDATE_HOST_MENU_MESSAGE, (self.game_id, map_id, rounds_number))
        network.send_data(request)

        reply = network.receive_data()
        self.players, self.map_id, self.rounds_number = reply.content
        if reply.status == "in progress":
            self.create_game(self.game_id, self.player_id, self.invite_code, self.map_id, self.rounds_number, 1)

    def update_starting_parameters(self):
        if self.map_selectbox.selected_index != self.map_id or self.round_selectbox.selected_index != self.rounds_number:
            self.map_id = self.map_selectbox.selected_index
            self.rounds_number = self.round_selectbox.selected_index
            self.selection_changed = True

    def update_selection_from_server(self):
        self.map_selectbox.selected_index = self.map_id
        self.round_selectbox.selected_index = self.rounds_number

    def update(self):
        self.update_starting_parameters()
        self.communication_with_server()
        self.update_selection_from_server()
        self.get_input()
        self.buttons.update()
        self.selectboxes.update()

    def draw_players(self):
        for key in range(1, 5):
            if key in self.players.keys():
                color = "green"
            else:
                color = "red"
            rect_width = 100
            if key == self.player_id:
                self.display_surface.blit(self.you_image, (key * SCREEN_WIDTH // 5 - self.you_image.get_width() // 2,
                                                           SCREEN_HEIGHT // 2 + rect_width // 2))
            pygame.draw.rect(self.display_surface, color,
                             pygame.Rect(key * SCREEN_WIDTH // 5 - rect_width // 2, SCREEN_HEIGHT / 2 - 90, rect_width,
                                         rect_width))

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
        self.buttons.draw(self.display_surface)
        self.selectboxes.draw(self.display_surface)
        self.draw_players()
        self.display_surface.blit(self.game_id_surface, (10, 110))
        self.display_surface.blit(self.invite_code_surface, (10, 180))
        self.display_surface.blit(self.logo, self.logo_rect.topleft)

    def run(self):
        self.update()
        self.draw()
