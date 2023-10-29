import pygame
import sys

from menu.button import Button

RESUME_BUTTON_SIZE = (261, 81)
EXIT_BUTTON_SIZE = (171, 81)


class PauseMenu:
    def __init__(self, display_surface, close_pause_menu, create_main_menu, unpause_game, leave_game, game_id,
                 player_id):
        self.display_surface = display_surface
        self.display_surface_width, self.display_surface_height = self.display_surface.get_size()
        self.pause_menu_width, self.pause_menu_height = 310, 250
        self.pause_menu_thickness = 13

        self.close_pause_menu = close_pause_menu
        self.create_main_menu = create_main_menu
        self.unpause_game = unpause_game
        self.leave_game = leave_game

        self.game_id = game_id
        self.player_id = player_id

        self.setup_buttons()

    def setup_buttons(self):
        self.buttons = pygame.sprite.Group()

        self.resume_button = Button(
            (self.display_surface_width // 2, self.display_surface_height // 2 - 2 * RESUME_BUTTON_SIZE[1] // 3),
            "resume", RESUME_BUTTON_SIZE)
        self.buttons.add(self.resume_button)

        self.exit_button = Button(
            (self.display_surface_width // 2, self.display_surface_height // 2 + EXIT_BUTTON_SIZE[1] // 1.5), "exit",
            EXIT_BUTTON_SIZE)
        self.buttons.add(self.exit_button)

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.resume_button.mouse_button_collision():
                    self.close_pause_menu()
                    self.unpause_game()
                elif self.exit_button.mouse_button_collision():
                    self.leave_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close_pause_menu()
                    self.unpause_game()

    def update(self):
        self.get_input()
        self.buttons.update()

    def draw(self):
        pygame.draw.rect(self.display_surface, (255, 255, 255),
                         pygame.Rect((self.display_surface_width - self.pause_menu_width) // 2,
                                     (self.display_surface_height - self.pause_menu_height) // 2, self.pause_menu_width,
                                     self.pause_menu_height), self.pause_menu_thickness)
        pygame.draw.rect(self.display_surface, "black",
                         pygame.Rect(
                             (self.display_surface_width - self.pause_menu_width) // 2 + self.pause_menu_thickness,
                             (self.display_surface_height - self.pause_menu_height) // 2 + self.pause_menu_thickness,
                             self.pause_menu_width - self.pause_menu_thickness * 2,
                             self.pause_menu_height - self.pause_menu_thickness * 2))
        self.buttons.draw(self.display_surface)

    def run(self):
        self.update()
        self.draw()
