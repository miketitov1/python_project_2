import pygame

pygame.init()


class Button(pygame.sprite.Sprite):

    def __init__(self, pos, name, size):
        super().__init__()
        self.pos = pos

        self.button_image_pressed = pygame.transform.smoothscale(
            pygame.image.load(f"menu/images/buttons/{name}_button_pressed.png").convert_alpha(), size)
        self.button_image_unpressed = pygame.transform.smoothscale(
            pygame.image.load(f"menu/images/buttons/{name}_button_unpressed.png").convert_alpha(), size)
        self.image = self.button_image_unpressed

        self.rect = self.image.get_rect(center=self.pos)

    def mouse_button_collision(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos_x, mouse_pos_y)

    def update(self):
        self.update_image()

    def update_image(self):
        if self.mouse_button_collision():
            self.image = self.button_image_pressed
        else:
            self.image = self.button_image_unpressed
