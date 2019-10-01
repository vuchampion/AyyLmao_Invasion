import sys, pygame
from pygame.locals import *

from func import Menu

HEIGHT = 800
WIDTH = 600

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WINDOW")

menu = Menu()

while True:
    pygame.display.update()
    window.fill((0, 0, 0))

    menu.menu_play()

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            print("Hello")

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

#menu = Menu()
#menu.menu_play()
