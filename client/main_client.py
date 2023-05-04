import pygame
import sys

from menu.main_menu import MainMenu
from menu.host_menu import HostMenu
from menu.join_menu import JoinMenu
from menu.cannot_connect_menu import CannotConnectMenu
from gameplay.game import Game
from menu.pause_menu import PauseMenu

sys.path.append('../server')

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GAME_NAME = "Space Battle"
FPS = 120

MAIN_MENU_STATUS = "main menu"
HOST_MENU_STATUS = "host menu"
JOIN_MENU_STATUS = "join_menu"
CANNOT_CONNECT_STATUS = "cannot connect"
GAME_STATUS = "game"
GAME_PAUSED_STATUS = "game paused"


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        self.status = MAIN_MENU_STATUS
        self.main_menu = MainMenu(self.screen, self.resize_screen, self.create_host_menu, self.create_join_menu,
                                  self.create_cannot_connect_menu)

    def resize_screen(self, width, height):
        del self.screen
        self.screen = pygame.display.set_mode((width, height))

    def create_main_menu(self):
        del self.main_menu
        self.main_menu = MainMenu(self.screen, self.resize_screen, self.create_host_menu, self.create_join_menu,
                                  self.create_cannot_connect_menu)
        self.status = MAIN_MENU_STATUS

        print("[NEW MENU]: Creating main menu")

    def create_host_menu(self, player_id, game_id, invite_code, hosting):
        self.host_menu = HostMenu(self.screen, self.resize_screen, self.create_main_menu,
                                  self.create_cannot_connect_menu,
                                  self.create_game, player_id, game_id, invite_code, hosting)
        self.status = HOST_MENU_STATUS

        print("[NEW MENU]: Creating host menu")

    def create_join_menu(self):
        self.join_menu = JoinMenu(self.screen, self.resize_screen, self.create_main_menu,
                                  self.create_cannot_connect_menu,
                                  self.create_host_menu)
        self.status = JOIN_MENU_STATUS

        print("[NEW MENU]: Creating join menu")

    def create_cannot_connect_menu(self):
        self.cannot_connect_menu = CannotConnectMenu(self.screen, self.resize_screen, self.create_main_menu)
        self.status = CANNOT_CONNECT_STATUS

        print("[NEW MENU]: Creating connection lost menu")

    def create_game(self, game_id, player_id, invite_code, map_id, rounds_number, current_round):
        self.game = Game(self.screen, self.resize_screen, self.create_pause_menu, self.create_main_menu, self.create_host_menu, self.create_game, game_id, player_id, invite_code, map_id, rounds_number, current_round)
        self.status = GAME_STATUS
        print(f"[NEW GAME]: Creating game {game_id}")

    def create_pause_menu(self, unpause_game, leave_game, game_id, player_id):
        self.pause_menu = PauseMenu(self.screen, self.close_pause_menu, self.create_main_menu, unpause_game, leave_game, game_id, player_id)
        self.status = GAME_PAUSED_STATUS
        print(f"[NEW MENU]: Creating pause menu")

    def close_pause_menu(self):
        self.status = GAME_STATUS

        print(f"[CLOSING MENU]: Closing pause menu")

    def run(self):
        while True:
            self.screen.fill('black')

            if self.status == MAIN_MENU_STATUS:
                self.main_menu.run()
            elif self.status == HOST_MENU_STATUS:
                self.host_menu.run()
            elif self.status == JOIN_MENU_STATUS:
                self.join_menu.run()
            elif self.status == CANNOT_CONNECT_STATUS:
                self.cannot_connect_menu.run()
            elif self.status == GAME_STATUS:
                self.game.run()
            elif self.status == GAME_PAUSED_STATUS:
                self.game.run()
                self.pause_menu.run()

            pygame.display.update()
            self.clock.tick(FPS)


main = Main()
main.run()
