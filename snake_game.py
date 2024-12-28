# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e
#
# Re-factoring following the Pygame tutorial:
#   https://pygame.readthedocs.io/en/latest/index.html

import pygame

from snake import *
from apple import *

class SnakeApp:
    """Create a single-window Snake app"""
    
    def __init__(self, size, speed):
        """Initialize pygame and the application"""
        pygame.init()

        # Set private attributes
        self.__screen = pygame.display.set_mode(size)
        self.__speed = speed # framerate in fps
             
        self.__snake = Snake()
        self.__apple = Apple()
        self.__apple.reset(self.__screen.get_size())

        self.__is_running = True # MZE: Why define as an attribute here?
    
    def run(self):
        """Run the main event loop."""
        while self.__is_running:
            pygame.time.Clock().tick(self.__speed) # framerate in fps
            self.__snake.crawl()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_running = False
                if event.type == pygame.KEYDOWN:
                    self.__snake.direction = event.key
                    if event.key == pygame.K_UP:
                        print("UP")                        
                    elif event.key == pygame.K_LEFT:
                        print("LEFT")                        
                    elif event.key == pygame.K_DOWN:
                        print("DOWN")                        
                    elif event.key == pygame.K_RIGHT:
                        print("RIGHT")                        
    
            if self.__snake.wall_collision(400) or self.__snake.self_collision():
                self.__is_running  = False

            if self.__snake.snake_eat_apple(self.__apple.position):
                self.__apple.reset(self.__screen.get_size())
                self.__snake.snake_bigger()
                self.__speed += 0.5
    
            self.__screen.fill((0,0,0))
            for snake_pos in self.__snake.snake[0:-1]:
                self.__screen.blit(self.__snake.skin, snake_pos)
            self.__screen.blit(self.__snake.head, self.__snake.snake[-1])
            self.__screen.blit(self.__apple.image, self.__apple.position)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    SnakeApp((400, 400), 10).run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
