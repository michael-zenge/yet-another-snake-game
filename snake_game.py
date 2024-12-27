# Following this tutorial to implement a snake game:
#   https://medium.com/@robsonsampaio90/snake-game-in-python-with-pygame-291f5206a35e

import pygame

from snake import *
from apple import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    clock = pygame.time.Clock()
    
    snake = Snake()
    apple = Apple()
    apple.set_random_position(400)

    is_running = True
    speed = 10

    while is_running:
        clock.tick(speed)
        snake.crawl()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    print("UP")
                    snake.direction = UP                
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    print("LEFT")
                    snake.direction = LEFT                
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    print("DOWN")
                    snake.direction = DOWN                
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    print("RIGHT")
                    snake.direction = RIGHT
    
        if snake.wall_collision(400) or snake.self_collision():
            is_running  = False

        if snake.snake_eat_apple(apple.position):
            apple.set_random_position(400)
            snake.snake_bigger()
            speed += 0.5
    
        screen.fill((0,0,0))
        for snake_pos in snake.snake[0:-1]:
            screen.blit(snake.skin, snake_pos)
        screen.blit(snake.head, snake.snake[-1])
        screen.blit(apple.apple, apple.position)

        pygame.display.update()

    pygame.quit()

main()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
