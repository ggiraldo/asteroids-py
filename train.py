# Asteroids game
# AI player training routine
# Method: Q-Learning with Convolutional NN

import numpy as np
import random
import pygame

import asteroids
from ai import qfunction
from ai import gamemodel


epochs = 1 # Number of games to train on to
gamma = 0.9 # (Future reward) Discount factor [0..1]
epsilon = 0.5 # Exploration vs exploitation parameter [0..1]

qf = qfunction.Qfunction()

pygame.init()
game = asteroids.game.AsteroidsGame(gamemodel.SCREEN_WIDTH, gamemodel.SCREEN_HEIGHT, False)

# Training Loop
for i in range(epochs):
    print("Start of Game #", i+1)
    # Create and init new game
    game.setup()
    game.render()

    # Initial state
    state = gamemodel.getState(game)

    # Game session
    print("Start of game session")
    while not game.gameLevel.gameOver:
        # Run Q function on current state
        qvalues = qf.model.predict(state, batch_size=1)
        print("Q values: ", qvalues)

        # Apply epsilon rule
        if random.random() < epsilon :
            # Choose random action
            action = gamemodel.randomAction()
            print("Chosen random action: ", action)
        else:
            # Choose best action based on Q
            action = (np.argmax(qvalues))
            print("Chosen best action: ", action)

        # Implement chosen action and get new state
        gamemodel.makeMove(game, action)
        new_state = gamemodel.getState(game)

        # Observe reward
        reward = gamemodel.getReward(game)
        print("Reward: ", reward)

        # Get maxQ(s',a)
        newQ = qf.model.predict(new_state, batch_size=1)
        maxQ = np.max(newQ)
        print("New Q: ", newQ)
        print("Max Q: ", maxQ)

        # Build training target vector
        y = np.zeros((1, gamemodel.POSSIBLE_ACTIONS))
        y[:] = qvalues[:]
        
        if not game.gameLevel.gameOver:
            # Non-terminal state
            update = reward + gamma * maxQ
        else:
            # Terminal state
            update = reward

        y[0][action] = update
        print("Ytarget: ", y)

        # Fit model
        qf.model.fit(state, y, batch_size=1, epochs=1, verbose=1)

        # Prepare for next epoch
        state = new_state
        prev_score = game.score

        print("\n")
        
    # Update epsilon
    if epsilon > 0.1:
        epsilon -= 1 / epochs

    print("End of Game #", i+1)

pygame.quit()

# Save trained model
# qf.model.save('./ai/model.h5')
