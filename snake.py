# Yet Another Snake Game
import pygame

class Snake:
    def __init__(self, sprite_size, head_color, body_color, bkgrd_color):
        self.__sprite_size = sprite_size
        self.__bkgrd_color = pygame.color.Color(bkgrd_color)
       
        self.__screen = pygame.display.get_surface()
        self.__sprite_screensize = self.__screen.get_size()

        self.__speed = 10 # framerate in fps
        self.__speed_inc = 0.5 # speed increment
        self.__direction = pygame.K_RIGHT

        # Create sprite object
        self.snake = []
        for ii in range (0,5):
            self.snake.append((int(self.__sprite_screensize[0]/2 + ii*self.__sprite_size[0]), int(self.__sprite_screensize[1]/2)))
                          
        self.head = pygame.Surface(self.__sprite_size)
        self.head.fill(pygame.color.Color(head_color))
        
        self.body = pygame.Surface(self.__sprite_size)
        self.body.fill(pygame.color.Color(body_color))
        
    @property
    def direction(self):
        """Get the current direction."""
        return self.__direction
        
    @direction.setter
    def direction(self, new_direction):
        """Set a new direction."""
        if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
            self.__direction = new_direction
        elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
            self.__direction = new_direction
        elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
            self.__direction = new_direction
        elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
            self.__direction = new_direction
                
    def do(self, event_key):
        if event_key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
            self.direction = event_key

    def update(self):
        # Move snake
        self.move()
               
        # Check collisions
        if self.snake[-1] in self.snake[0:-1]:
            return False
        
        if self.snake[-1][0] < 0 or self.snake[-1][0] >= self.__sprite_screensize[0]:
            return False
        
        if self.snake[-1][1] >= self.__sprite_screensize[1] or self.snake[-1][1] < 0:
            return False
        
        # Eat apple        
        if self.__screen.get_at(self.snake[-1]) != self.__bkgrd_color:
            self.snake.insert(0, (self.snake[0])) # grow snake
            self.__screen.set_at(self.snake[-1], self.__bkgrd_color) # take a bite
            self.__speed += self.__speed_inc

        # Update speed
        pygame.time.Clock().tick(self.__speed) # framerate in fps
     
        return True

    def draw(self):
        for pos in self.snake[0:-1]:
            self.__screen.blit(self.body, pos)
        self.__screen.blit(self.head, self.snake[-1])

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
