# Yet Another Snake Game
import pygame

class Snake:
    def __init__(self, sprite_size, head_color, body_color, apple_color, wall_color, speed=10, speed_inc=0.5):
        self.__sprite_size = sprite_size
        self.__apple_color = pygame.color.Color(apple_color)
        self.__wall_color = wall_color
        self.__speed = speed # framerate in fps
        self.__speed_inc = speed_inc # speed increment
        
        self.__screen = pygame.display.get_surface()
        self.__screen_size = self.__screen.get_size()
                       
        self.__head_color = pygame.color.Color(head_color)
        self.__head = pygame.Surface(self.__sprite_size)
        self.__head.fill(self.__head_color)
        
        self.__body_color = pygame.color.Color(body_color)
        self.__body = pygame.Surface(self.__sprite_size)
        self.__body.fill(self.__body_color)        

        # Create sprite object
        self.snake = []
        self.reset()

    @property
    def sprite_size(self):
        return self.__sprite_size

    @property
    def body_color(self):
        return self.__body_color
    
    @property
    def wall_color(self):
        return self.__wall_color
    
    @property
    def direction(self):
        """Get the current direction."""
        return self.__direction
        
    @direction.setter
    def direction(self, new_direction, advanced=False):
        """Set a new direction."""
        if advanced:
            if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
                self.__direction = new_direction
                print("UP")
            elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                self.__direction = new_direction
                print("LEFT")        
            elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                self.__direction = new_direction
                print("RIGHT")
            elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
                self.__direction = new_direction        
                print("DOWN")                
        else:
            self.__direction = new_direction

    def reset(self):
        self.snake.clear()
        for ii in range (0,5):
            self.snake.append((int(self.__screen_size[0]/4 + ii*self.__sprite_size[0]), int(self.__screen_size[1]/2)))
        self.__direction = pygame.K_RIGHT

    def do(self, event_key):
        if event_key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
            self.direction = event_key

    def update(self):
        # Move snake
        self.move()

        if self.__screen.get_at(self.snake[-1]) in [self.__body_color, self.__wall_color]:
            return False
                               
        # Eat apple        
        if self.__screen.get_at(self.snake[-1]) == self.__apple_color:
            self.snake.insert(0, (self.snake[0])) # grow snake
            self.__speed += self.__speed_inc

        # Update speed
        pygame.time.Clock().tick(self.__speed) # framerate in fps

        return True

    def draw(self):
        for pos in self.snake[0:-1]:
            self.__screen.blit(self.__body, pos)
        # Do not draw head over apple or wall
        if self.__screen.get_at(self.snake[-1]) not in [self.__body_color, self.__wall_color, self.__apple_color]:
            self.__screen.blit(self.__head, self.snake[-1])

    def move(self):
        if self.direction == pygame.K_RIGHT:
            self.snake.append((self.snake[-1][0] + self.__sprite_size[0] , self.snake[-1][1]))
        elif self.direction == pygame.K_UP:
            self.snake.append((self.snake[-1][0] , self.snake[-1][1] - self.__sprite_size[1]))
        elif self.direction == pygame.K_DOWN:
            self.snake.append((self.snake[-1][0] , self.snake[-1][1] + self.__sprite_size[1]))
        elif self.direction == pygame.K_LEFT:        
            self.snake.append((self.snake[-1][0] - self.__sprite_size[0] , self.snake[-1][1]))
        self.snake.pop(0)
   
# Copyright (c) 2024 michael-zenge, permission granted under MIT license
