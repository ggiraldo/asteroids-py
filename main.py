# Asteroids game
# Entry routine for window-based playing

import pygame

import asteroids


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()

def main():
    pygame.init()

    game = asteroids.game.AsteroidsGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()

    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                game.on_key_press(event.key)
            if event.type == pygame.KEYUP:
                game.on_key_release(event.key)

        game.update()
        game.render()
        
        clock.tick(60)


if __name__ == "__main__":
    main()
