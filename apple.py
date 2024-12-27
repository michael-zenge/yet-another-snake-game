# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e

import pygame
import random

class Apple():

    def __init__(self):
        self.apple = pygame.Surface((10, 10))
        self.apple.fill((255, 0,0 ))
        self.position = (0, 0)
    
    def set_random_position(self, screen_size):
        self.position = (random.randrange(0, screen_size-10, 10), random.randrange(0, screen_size-10, 10))
        print(self.position)

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
