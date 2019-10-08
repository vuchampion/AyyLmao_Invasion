import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game, image_file):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.alien_points = 1

        if image_file == 'images/alien.png':
            self.alien_points = 50
        if image_file == 'images/alien3.png':
            self.alien_points = 75
        if image_file == 'images/alien5.png':
            self.alien_points = 125
        # Clock
        self.watch = pygame.time.Clock()

        # Load the alien image and set its rect attribute.
        #self.image = pygame.image.load('images/alien.png')
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()

        # Animating sprites
        self.sprites = [pygame.image.load('images/alien.png'), pygame.image.load('images/alien2.png')]
        self.frame = 0

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
