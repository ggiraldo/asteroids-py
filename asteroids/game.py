# Asteroids Game
# Main game window class

import pygame

from . import gameLevel


class AsteroidsGame():
    """ Main game application class """

    def __init__(self, width, height, offScreen=False):
        """ Class constructor """
        self.width = width
        self.height = height
        self.offScreen = offScreen

        if self.offScreen:
            # Draw off-screen for learning routines
            self.screen = pygame.Surface((width, height))
        else:
            # Draw window for normal game-play
            self.screen = pygame.display.set_mode((width, height))

    def setup(self):
        """ Initalize game """
        self.level = 1
        self.score = 0

        self.gameLevel = gameLevel.GameLevel(self.level, self.width, self.height)

        print('GAME STARTED')

    def render(self):
        """ Rendering routine """
        self.screen.fill((0, 0, 0))

        self.gameLevel.render(self.screen)

        if not self.offScreen:
            self.gameLevel.renderHUD(self.screen)
            pygame.display.flip()

    def on_key_press(self, key):
        """ Handle key presses """
        self.gameLevel.keyPressed(key)

        if(self.gameLevel.gameOver and key == pygame.K_SPACE):
            self.level = 0
            self.score = 0
            self.gameLevel = gameLevel.GameLevel(self.level, self.width, self.height)

    def on_key_release(self, key):
        """ Handle key releases """
        self.gameLevel.keyReleased()

    def update(self):
        """ Game logic update """
        if(not self.gameLevel.gameOver and not self.gameLevel.levelCleared):
            self.gameLevel.update()

        if(self.gameLevel.levelCleared):
            self.score += self.gameLevel.score
            self.level += 1
            self.gameLevel = gameLevel.GameLevel(self.level, self.width, self.height)
            self.gameLevel.score = self.score
