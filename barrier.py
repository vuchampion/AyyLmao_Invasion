import pygame

from pygame.sprite import Sprite

class Barrier(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/barrier.png')
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)

    def update(self):
        pass

    def blitme(self):
        self.screen.blit(self.imgae, self.rect)
