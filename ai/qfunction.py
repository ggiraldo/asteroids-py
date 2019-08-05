# Asteoroids game AI
# CNN model for Q function

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Activation, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import RMSprop


class Qfunction():
    """ Class with Convolutional Neural Network to model Q function of Asteroids Game """
    def __init__(self):
        """ Costructor """
        self.buildModel()

    def buildModel(self):
        """ Define NN structure """
        self.model = keras.Sequential()

        # Input image
        self.model.add(Input(shape=(600, 600, 3)))

        # Convolutional layers
        self.model.add(Conv2D(15, 3, activation='relu'))
        self.model.add(MaxPooling2D(2))
        
        self.model.add(Conv2D(30, 3, activation='relu'))
        self.model.add(MaxPooling2D(2))

        # Flatten
        self.model.add(Flatten())

        # Dense layers
        self.model.add(Dense(60, activation='relu'))
        self.model.add(Dense(60, activation='relu'))

        # Output with linear activation
        self.model.add(Dense(5, activation='linear'))

        # Compile model
        self.model.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])

        # Print summary
        print(self.model.summary())
