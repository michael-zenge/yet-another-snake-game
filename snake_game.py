# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e
#
# Re-factoring following the Pygame tutorial:
#   https://pygame.readthedocs.io/en/latest/index.html

import pygame

from snake import *
from apple import *

class SnakeApp():
    """Create a single-window Snake app"""
    
    def __init__(self):
        """Initialize pygame and the application"""
        pygame.init()
        self.screen = pygame.display.set_mode((400,400))
        self.clock = pygame.time.Clock()
    
        self.snake = Snake()
        self.apple = Apple()
        self.apple.set_random_position(400)

        self.is_running = True
        self.speed = 10

    def run(self):
        """Run the main event loop."""
        while self.is_running:
            self.clock.tick(self.speed)
            self.snake.crawl()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != DOWN:
                        print("UP")
                        self.snake.direction = UP                
                    elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                        print("LEFT")
                        self.snake.direction = LEFT                
                    elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                        print("DOWN")
                        self.snake.direction = DOWN                
                    elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                        print("RIGHT")
                        self.snake.direction = RIGHT
    
            if self.snake.wall_collision(400) or self.snake.self_collision():
                self.is_running  = False

            if self.snake.snake_eat_apple(self.apple.position):
                self.apple.set_random_position(400)
                self.snake.snake_bigger()
                self.speed += 0.5
    
            self.screen.fill((0,0,0))
            for snake_pos in self.snake.snake[0:-1]:
                self.screen.blit(self.snake.skin, snake_pos)
            self.screen.blit(self.snake.head, self.snake.snake[-1])
            self.screen.blit(self.apple.apple, self.apple.position)

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    SnakeApp().run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
