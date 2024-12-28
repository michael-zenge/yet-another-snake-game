# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e
#
# See also: https://www.python-kurs.eu/python3_properties.php

import pygame

class Snake:

    def __init__(self):
        self.snake = [(200, 200), (210, 200), (220, 200), (230, 200), (240, 200)]
        self.skin = pygame.Surface((10,10))
        self.skin.fill((255, 255, 255))
        self.head = pygame.Surface((10,10))
        self.head.fill((200, 200, 200))
        self.__direction = pygame.K_RIGHT

    @property
    def direction(self):
        """Get the current direction."""
        return self.__direction
        
    @direction.setter
    def direction(self, new_direction):
        """Set a new direction."""
        if new_direction == pygame.K_UP and self.__direction != pygame.K_DOWN:
            self.__direction = new_direction
        elif new_direction == pygame.K_LEFT and self.__direction != pygame.K_RIGHT:
            self.__direction = new_direction
        elif new_direction == pygame.K_RIGHT and self.__direction != pygame.K_LEFT:
            self.__direction = new_direction
        elif new_direction == pygame.K_DOWN and self.__direction != pygame.K_UP:
            self.__direction = new_direction
                
    def crawl(self):
        if self.direction == pygame.K_RIGHT:
            self.snake.append((self.snake[len(self.snake)-1][0] + 10 , self.snake[len(self.snake)-1][1]))
        elif self.direction == pygame.K_UP:
            self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] - 10))
        elif self.direction == pygame.K_DOWN:
            self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] + 10))
        elif self.direction == pygame.K_LEFT:        
            self.snake.append((self.snake[len(self.snake)-1][0] - 10 , self.snake[len(self.snake)-1][1]))
        self.snake.pop(0)

    def self_collision(self):
        return self.snake[-1] in self.snake[0:-1]
    
    def wall_collision(self, screen_size):
        return self.snake[len(self.snake)-1][0] >= screen_size or self.snake[len(self.snake)-1][0] < 0 or self.snake[len(self.snake)-1][1] >= screen_size or self.snake[len(self.snake)-1][1] < 0

    def snake_eat_apple(self, apple_pos):
        return self.snake[-1] == apple_pos
    
    def snake_bigger(self):
        self.snake.insert(0, (self.snake[0]))

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
