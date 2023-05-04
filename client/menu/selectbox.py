import pygame

pygame.init()


class SelectBox(pygame.sprite.Sprite):

    def __init__(self, pos, name, images_number, size):
        super().__init__()
        self.pos = pos
        self.active = False

        self.images_pressed = {}
        self.images_unpressed = {}
        for i in range(1, images_number + 1):
            self.images_pressed[i] = pygame.transform.smoothscale(
                pygame.image.load(f"menu/images/selectboxes/{name}_{i}_selectbox_pressed.png").convert_alpha(), size)
            self.images_unpressed[i] = pygame.transform.smoothscale(
                pygame.image.load(f"menu/images/selectboxes/{name}_{i}_selectbox_unpressed.png").convert_alpha(), size)

        self.selected_index = 1
        self.image = self.images_unpressed[self.selected_index]
        self.rect = self.image.get_rect(center=self.pos)

    def update_selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.selected_index == len(self.images_unpressed):
                        self.selected_index = 1
                    else:
                        self.selected_index += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.selected_index == 1:
                        self.selected_index = len(self.images_unpressed)
                    else:
                        self.selected_index -= 1
            self.image = self.images_pressed[self.selected_index]

    def mouse_selectbox_collision(self):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos_x, mouse_pos_y)

    def update_image(self):
        if self.mouse_selectbox_collision():
            self.image = self.images_pressed[self.selected_index]
        elif not self.active:
            self.image = self.images_unpressed[self.selected_index]

    def update(self):
        self.update_image()
