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
    
    def __init__(self):
        """Initialize pygame and the application"""
        pygame.init()

        # Set private attributes
        self.__sprite_size = (16,16)
        self.__sceen_size = (40*self.__sprite_size[0], 20*self.__sprite_size[1])
        self.__speed = 10 # framerate in fps

        self.__screen = pygame.display.set_mode(self.__sceen_size)
                     
        self.__snake = Snake(self.__sprite_size, self.__sceen_size)
        self.__apple = Apple(self.__sprite_size, self.__sceen_size)
        self.__apple.reset()
        
        self.__running = True
        self.__updating = True
    
    def run(self):
        """Run the main event loop."""
        while self.__running:
            for event in pygame.event.get():
                self.do(event)
            self.update()
            self.draw()
        pygame.quit()

    def do(self, event):
        match event.type:
            case pygame.QUIT:
                  self.__running = False
                  pygame.quit()
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__updating = not self.__updating
                else:
                    self.__snake.direction = event.key

    def update(self):
        if self.__updating:
            pygame.time.Clock().tick(self.__speed) # framerate in fps
            self.__snake.crawl()
    
            if self.__snake.wall_collision() or self.__snake.self_collision():
                self.__running  = False

            if self.__snake.snake_eat_apple(self.__apple.position):
                self.__apple.reset()
                self.__snake.snake_bigger()
                self.__speed += 0.5

    def draw(self):
        if self.__updating:
            self.__screen.fill((0,0,0))
            for snake_pos in self.__snake.snake[0:-1]:
                self.__screen.blit(self.__snake.skin, snake_pos)
            self.__screen.blit(self.__snake.head, self.__snake.snake[-1])
            self.__screen.blit(self.__apple.image, self.__apple.position)

        pygame.display.update()

if __name__ == '__main__':
    SnakeApp().run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
