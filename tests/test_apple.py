# Yet Another Snake Game feat. Q-Learning by Michael Zenge
#
# Run unit tests in project directory with "python -m tests.test_apple"
#

import unittest
import pygame

from apple import *

class test_apple(unittest.TestCase):
    def __init__(self, module_name='test_apple'):
        super().__init__(module_name)

        self._random_seed = 1000

        self._sprite_size = (16,16)
        self._screen_size = (20*self._sprite_size[0], 16*self._sprite_size[1])        
        self._screen = pygame.display.set_mode(self._screen_size)

        self._default_color = 'red'
        self._ref_position = (240,192)        

    def test_color(self):
        """Test selection of supported color formats"""        
        # Integer value
        color_int = 0xFFFFFFFF # (255, 255, 255, 255) -> white
        white_apple = Apple(self._sprite_size, color_int)
        self.assertIsInstance(white_apple.color, pygame.color.Color)
        self.assertEqual(white_apple.color, pygame.color.Color(color_int))

        # (r, g, b, [a])
        color_rgb = (255, 0, 0) # red
        red_apple = Apple(self._sprite_size, color_rgb)
        self.assertIsInstance(red_apple.color, pygame.color.Color)
        self.assertEqual(red_apple.color, pygame.color.Color(color_rgb))

        # Named color
        color_str = 'green'
        green_apple = Apple(self._sprite_size, color_str)
        self.assertIsInstance(green_apple.color, pygame.color.Color)
        self.assertEqual(green_apple.color, pygame.color.Color(color_str))

        # HTML color format
        color_str = '#0000FF' # blue
        blue_apple = Apple(self._sprite_size, color_str)
        self.assertIsInstance(blue_apple.color, pygame.color.Color)
        self.assertEqual(blue_apple.color, pygame.color.Color(color_str))
        
    def test_position(self):
        """Test reference position after initialization"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        self.assertEqual(apple.position, self._ref_position)

    def test_do(self):
        """Up to now,'do' function does not do anything at all"""
        apple = Apple(self._sprite_size, self._default_color)
        self.assertIsNone(apple.do(pygame.K_RIGHT))

    def test_draw(self):
        """Test whether apple is drawn at respective position"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        apple.draw()
        self.assertEqual(self._screen.get_at(apple.position), apple.color)

    def test_update(self):
        """Test whether position of apple is updated and function returns true"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        success = apple.update()        
        self.assertEqual(apple.position, self._ref_position)
        self.assertTrue(success)

    def test_reset(self):
        """Test whether position is properly reset"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        apple.reset()
        self.assertEqual(apple.position, self._ref_position)

if __name__ == "__main__":
    unittest.main()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
