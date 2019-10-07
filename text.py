import pygame.font

class Text:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.font_size = 60
        self.font = pygame.font.SysFont(None, self.font_size)

    def message(self, msg, color, locationx, locationy):
        text = self.font.render(str(msg), True, color)
        self.screen.blit(text, (locationx, locationy))
