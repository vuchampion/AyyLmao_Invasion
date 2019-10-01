import pygame

from button import Button

class Menu:
    def __init__(self):
        self.HEIGHT = 800
        self.WIDTH = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def menu_play(self):
        self.play_button = Button(self, "Bepis", 200, 200)
        self.play_button.draw_button()

        self.play_button = Button(self, "Poontang", 200, 0)
        self.play_button.draw_button()

        self.play_button = Button(self, "sudo rm", 200, 500)
        self.play_button.draw_button()
