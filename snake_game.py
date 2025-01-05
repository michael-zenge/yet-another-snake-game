# Yet Another Snake Game feat. Q-Learning by Michael Zenge
import pygame

from snake import *
from apple import *

from q_learning import SnakeQLearning

class SnakeApp:
    """Create a single-window Snake app"""
    
    def __init__(self):
        """Initialize pygame and the application"""
        pygame.init()        
        
        # Set private attributes
        self.__sprite_size = (32,32)
        self.__screen_size = (20*self.__sprite_size[0], 16*self.__sprite_size[1])
        
        self.__screen = pygame.display.set_mode(self.__screen_size)
        
        self.__bkgrd_color = pygame.color.Color('lemonchiffon')
        self.__wall_color = pygame.color.Color('dimgrey')
        self.__apple_color = pygame.color.Color('red')
        self.__head_color = pygame.color.Color('darkgreen')
        self.__body_color = pygame.color.Color('green')
                
        self.__sprites = []
        self.__sprites.append(Apple(self.__sprite_size, self.__apple_color)) # add apple first to avoid drawing over snake
        self.__sprites.append(Snake(self.__sprite_size, self.__head_color, self.__body_color, self.__apple_color, self.__wall_color, 5, 0.0))
    
        self.__env = SnakeQLearning(self.__sprites[0], self.__sprites[1])        
        self.__learning = True
        
        self.__running = True
        self.__updating = True        

        if not self.__learning:
            pygame.display.set_caption("Yet Another Snake Game")
        else:
            pygame.display.set_caption("Yet Another Snake Game (Q-Learning)")
            
    def run(self):
        """Run the main event loop."""        
        self.draw()
        while self.__running:
            for event in pygame.event.get():
                self.do(event)
            self.update()            
        pygame.quit() # does not exit the program, safe to call more than once

    def do(self, event):
        match event.type:
            case pygame.QUIT:
                  self.__running = False
                  pygame.quit() # does not exit the program, safe to call more than once
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:                
                        self.__updating = not self.__updating
                    case pygame.K_ESCAPE:
                        self.__running = False
                        pygame.quit() # does not exit the program, safe to call more than once
                    case _:
                        if not self.__learning: # do not accept keyboard input
                            for sprite in self.__sprites:
                                sprite.do(event.key)

    def update(self):
        if self.__running and self.__updating:            
            if self.__learning:
                self.__env.update()
            
            for sprite in self.__sprites:
                success = sprite.update()                    
                if not success and not self.__learning:
                    self.__running = False
                    pygame.quit() # does not exit the program, safe to call more than once
                    break
            
            self.draw()

            if self.__learning:
                self.__env.reward()

    def draw(self):
        if self.__running and self.__updating:
            # Q-learning requires wall thickness = 2 * size of sprite
            bkgrd_coord = (2*self.__sprite_size[0], 2*self.__sprite_size[1])
            bkgrd_size = (self.__screen_size[0]-4*self.__sprite_size[0], self.__screen_size[1]-4*self.__sprite_size[1])

            self.__screen.fill(self.__wall_color)
            screen_bkgrd = pygame.Rect(bkgrd_coord, bkgrd_size)
            pygame.draw.rect(self.__screen, self.__bkgrd_color, screen_bkgrd)

            for sprite in self.__sprites:
                sprite.draw()
               
            pygame.display.update()

if __name__ == '__main__':
    SnakeApp().run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
