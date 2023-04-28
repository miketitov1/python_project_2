import pygame

pygame.init()


class Button(pygame.sprite.Sprite):

    def __init__(self, pos, unpressed_button_image, pressed_button_image, handle_event=None):
        super().__init__()
        self.pos = pos
        self.unpressed_button_image = unpressed_button_image
        self.pressed_button_image = pressed_button_image
        self.image = self.unpressed_button_image

        self.rect = self.image.get_rect(center=self.pos)
        self.handle_event = handle_event

    def mouse_button_collision(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos_x, mouse_pos_y)

    def update(self):
        self.update_image()

    def update_image(self):
        if self.mouse_button_collision():
            self.image = self.pressed_button_image
        else:
            self.image = self.unpressed_button_image
