import pygame
import sys

from settings import *
from client.menu.main_menu import MainMenu
from client.menu.host_menu import HostMenu
from client.menu.join_menu import JoinMenu
from client.menu.connection_lost_menu import ConnectionLostMenu
from client.gameplay.game import Game


pygame.init()


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Battle")
        self.clock = pygame.time.Clock()

        self.status = "main_menu"
        self.main_menu = MainMenu(self.screen, self.create_host_menu, self.create_join_menu, self.create_connection_lost_menu)

    def resize_screen(self, width, height):
        self.screen = pygame.display.set_mode((width, height))

    def create_main_menu(self):
        del self.main_menu
        self.main_menu = MainMenu(self.screen, self.create_host_menu, self.create_join_menu, self.create_connection_lost_menu)
        self.status = "main_menu"

        print("[NEW MENU]: Creating main menu")

    def create_host_menu(self, player_id, game_id, is_hosting):
        self.host_menu = HostMenu(self.screen, self.create_main_menu, self.create_connection_lost_menu, self.create_game, player_id, game_id, is_hosting)
        self.status = "host_menu"

        print("[NEW MENU]: Creating host menu")

    def create_join_menu(self):
        self.join_menu = JoinMenu(self.screen, self.create_main_menu, self.create_connection_lost_menu, self.create_host_menu)
        self.status = "join_menu"

        print("[NEW MENU]: Creating join menu")

    def create_connection_lost_menu(self):
        self.connection_lost_menu = ConnectionLostMenu(self.screen, self.create_main_menu)
        self.status = "connection_lost"

        print("[NEW MENU]: Creating connection lost menu")

    def create_game(self, level_data, game_id, player_id):
        self.game = Game(self.screen, level_data, game_id, player_id)
        self.status = "game"

        print("[NEW GAME]: Creating game")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')

            if self.status == "main_menu":
                self.main_menu.run()
            elif self.status == "host_menu":
                self.host_menu.run()
            elif self.status == "join_menu":
                self.join_menu.run()
            elif self.status == "connection_lost":
                self.connection_lost_menu.run()
            elif self.status == "game":
                self.game.run()

            pygame.display.update()
            self.clock.tick(FPS)


main = Main()
main.run()
