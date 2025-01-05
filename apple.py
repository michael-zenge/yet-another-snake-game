# Yet Another Snake Game
import pygame
import random

class Apple:
    def __init__(self, sprite_size, apple_color):
        self.__sprite_size = sprite_size
        self.__apple_color = pygame.color.Color(apple_color)

        self.__screen = pygame.display.get_surface()
        self.__screen_size = self.__screen.get_size()

        # Create sprite object
        self.__image = pygame.Surface(self.__sprite_size)
        self.__image.fill(self.__apple_color)

        self.__position = (0,0)
        self.reset()

    @property
    def color(self):
        return self.__apple_color

    @property
    def position(self):
        return self.__position

    def do(self, event_key):
        pass

    def draw(self):
        self.__screen.blit(self.__image, self.__position)

    def update(self):
        # Reset position if eaten by snake
        if self.__screen.get_at(self.__position) != self.__apple_color:
            self.reset()
        return True
        
    def reset(self):
        pos_x = random.randrange(2*self.__sprite_size[0], self.__screen_size[0]-2*self.__sprite_size[0], self.__sprite_size[0])
        pos_y = random.randrange(2*self.__sprite_size[1], self.__screen_size[1]-2*self.__sprite_size[1], self.__sprite_size[1])
        self.__position = (pos_x, pos_y)

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
