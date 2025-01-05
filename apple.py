# Yet Another Snake Game
import pygame
import random

class Apple:
    def __init__(self, sprite_size, apple_color):
        self._sprite_size = sprite_size
        self._apple_color = pygame.color.Color(apple_color)

        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        # Create sprite object
        self._image = pygame.Surface(self._sprite_size)
        self._image.fill(self._apple_color)

        self._position = (0,0)
        self.reset()

    @property
    def color(self):
        return self._apple_color

    @property
    def position(self):
        return self._position

    def do(self, event_key):
        pass

    def draw(self):
        self._screen.blit(self._image, self._position)

    def update(self):
        # Reset position if eaten by snake
        if self._screen.get_at(self._position) != self._apple_color:
            self.reset()
        return True
        
    def reset(self):
        pos_x = random.randrange(2*self._sprite_size[0], self._screen_size[0]-2*self._sprite_size[0], self._sprite_size[0])
        pos_y = random.randrange(2*self._sprite_size[1], self._screen_size[1]-2*self._sprite_size[1], self._sprite_size[1])
        self._position = (pos_x, pos_y)

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
