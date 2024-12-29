# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e

import pygame
import random

class Apple:

    def __init__(self, sprite_size, screen_size):
        self.__sprite_size = sprite_size
        self.__screen_size = screen_size
                
        self.image = pygame.Surface(self.__sprite_size)
        self.image.fill((255, 0,0 ))

        self.position = (0,0)
        
        
    def reset(self):
        pos_x = random.randrange(0, self.__screen_size[0]-self.__sprite_size[0], self.__sprite_size[0])
        pos_y = random.randrange(0, self.__screen_size[1]-self.__sprite_size[1], self.__sprite_size[1])
        self.position = (pos_x, pos_y)
        print(self.position)

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
