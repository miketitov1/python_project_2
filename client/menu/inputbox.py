import pygame

pygame.init()


class InputBox:
    """Класс окна для ввода текста"""
    def __init__(self, pos, width=240, height=99, default_text="sample_text", text_color="grey",
                 active_color="white", inactive_color=(34, 31, 79)):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.rect.center = pos

        self.text = default_text
        self.default_text = default_text
        self.font = pygame.font.Font('menu/fonts/PixelMaster.ttf', 90)
        self.text_color = text_color
        self.text_surface = self.font.render(self.text, True, self.text_color)

        self.color = inactive_color
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.active = False

    def update_text(self, event):
        """Обновление текста в окне ввода текста"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if self.text == self.default_text:
                    self.text = ""
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 6:
                    self.text += event.unicode
            self.text_surface = self.font.render(self.text, True, self.text_color)

    def mouse_inputbox_collision(self):
        """Проверка пересечения курсора мыши и окна ввода текста"""
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos_x, mouse_pos_y)

    def update_inputbox(self):
        """Обновление цвета окна ввода текста"""
        if self.mouse_inputbox_collision():
            self.color = self.active_color
        elif not self.active:
            self.color = self.inactive_color

    def update(self):
        self.update_inputbox()

    def draw(self, display_surface):
        """Отрисовка окна ввода текста"""
        pygame.draw.rect(display_surface, "black", self.rect)
        pygame.draw.rect(display_surface, self.color, self.rect, 10)
        display_surface.blit(self.text_surface, (self.rect.x + 20, self.rect.y))

