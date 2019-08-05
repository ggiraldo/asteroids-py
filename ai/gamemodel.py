# Asteoroids game AI
# Helper functions for game interactions

import numpy as np
import pygame


# Game parameters
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
POSSIBLE_ACTIONS = 5


def getState(game):
    """ Extract pixel image from game """
    pixels = pygame.surfarray.array3d(game.screen)[:]
    pixels = np.array([pixels], dtype=float)

    # Here we will preprocess the pixel data
    bitsize = game.screen.get_bitsize() / 4
    pixels *= 1 / 2**bitsize # Normalize to [0..1]

    return pixels


def randomAction():
    """ Return randomly chosen action """
    return np.random.randint(0, POSSIBLE_ACTIONS)


def makeMove(game, action):
    """  Take action on given game sate """
    key = 0
    if action == 0:
        # Press D
        key = pygame.K_d
    elif action == 1:
        # Press A
        key = pygame.K_a
    elif action == 2:
        # Press W
        key = pygame.K_w
    elif action == 3:
        # Press S
        key = pygame.K_s
    elif action == 4:
        # Press SPACE
        key = pygame.K_SPACE
    else:
        # Should not happen
        raise('Invalid Action')

    game.on_key_press(key)
    game.on_key_release(key)

    # Forward game more than one frame
    for _ in range(10):
        game.update()
        game.render()


def getReward(game):
    """ Get reward from given state """
    reward = 0

    # Reward +10 if destroys asteroid
    if game.gameLevel.asteroidDestroyed():
        reward += 10

    # Reward +20 if level cleared
    if game.gameLevel.levelCleared:
        reward += 20

    # Reward -10 if hits asteroid
    if game.gameLevel.gameOver:
        reward -= 10
    
    # Reward -1 if a second passes
    # ToDo: implement timeout in gameLevel

    return reward
