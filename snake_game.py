# Yet Another Snake Game by Michael Zenge
import pygame

from snake import *
from apple import *

class SnakeApp:
    """Create a single-window Snake app"""
    
    def __init__(self):
        """Initialize pygame and the application"""
        pygame.init()
        pygame.display.set_caption("Yet Another Snake Game")
        
        # Set private attributes
        self.__sprite_size = (16,16)
        self.__screen_size = (40*self.__sprite_size[0], 30*self.__sprite_size[1])
        
        self.__screen = pygame.display.set_mode(self.__screen_size)
        self.__bkgrd_color = pygame.color.Color('lemonchiffon')
                
        self.__sprites = []
        self.__sprites.append(Apple(self.__sprite_size, 'red')) # add apple first to avoid drawing over snake
        self.__sprites.append(Snake(self.__sprite_size, 'darkgreen', 'green', self.__bkgrd_color))
    
        self.__running = True
        self.__updating = True
    
    def run(self):
        """Run the main event loop."""
        while self.__running:
            for event in pygame.event.get():
                self.do(event)
            self.update()
            self.draw()
        pygame.quit() # does not exit the program, safe to call more than once

    def do(self, event):
        match event.type:
            case pygame.QUIT:
                  self.__running = False
                  pygame.quit() # does not exit the program, safe to call more than once
            case pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__updating = not self.__updating
                else:
                    for sprite in self.__sprites:
                        sprite.do(event.key)

    def update(self):
        if self.__running and self.__updating:
            for sprite in self.__sprites:
                success = sprite.update()                    
                if not success:
                    self.__running = False
                    pygame.quit() # does not exit the program, safe to call more than once
                    break

    def draw(self):
        if self.__running and self.__updating:
            self.__screen.fill(self.__bkgrd_color)
            for sprite in self.__sprites:
                sprite.draw()          
            pygame.display.update()

if __name__ == '__main__':
    SnakeApp().run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
