import pygame

from button import Button

class Menu:
    def __init__(self):
        self.HEIGHT = 800
        self.WIDTH = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def play_button(self, xcor, ycor):
        self.play_button = Button(self, "Bepis", xcor, ycor)
        self.play_button.draw_button()

    def scores_button(self, xcor, ycor):
        self.play_button = Button(self, "Scores", xcor, ycor)
        self.play_button.draw_button()

    def exit_button(self, xcor, ycor):
        self.play_button = Button(self, "Exit", xcor, ycor)
        self.play_button.draw_button()
