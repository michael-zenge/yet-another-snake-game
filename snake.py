# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e

import pygame

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Snake():

    def __init__(self):
        self.snake = [(200, 200), (210, 200), (220, 200), (230, 200), (240, 200)]
        self.skin = pygame.Surface((10,10))
        self.skin.fill((255, 255, 255))
        self.head = pygame.Surface((10,10))
        self.head.fill((200, 200, 200))
        self.direction = RIGHT

    def crawl(self):
        if self.direction == RIGHT:
            self.snake.append((self.snake[len(self.snake)-1][0] + 10 , self.snake[len(self.snake)-1][1]))
        elif self.direction == UP:
            self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] - 10))
        elif self.direction == DOWN:
            self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] + 10))
        elif self.direction == LEFT:        
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
