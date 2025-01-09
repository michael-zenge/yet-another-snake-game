# Yet Another Snake Game feat. Q-Learning by Michael Zenge
#
# Run unit tests in project directory with "python -m tests.test_apple"
#

import unittest
import pygame

from apple import Apple

class test_apple(unittest.TestCase):        
    def setUp(self):        
        self._sprite_size = (16,16)
        self._screen_size = (20*self._sprite_size[0], 16*self._sprite_size[1])        
        self._screen = pygame.display.set_mode(self._screen_size)

        self._random_seed = 1000
        self._default_color = 'red'
        self._ref_position = (240,192) # position if initialized with random seed = 1000 
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()

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
        """Test whether position of apple is updated"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        
        apple.draw()        
        success = apple.update()

        # Function always returns 'True'
        self.assertTrue(success)
        # Position shall match reference position, no update
        self.assertEqual(apple.position, self._ref_position)
        
        self._screen.set_at(apple.position, 'black')
        success = apple.update()

        # Function always returns 'True'
        self.assertTrue(success)
        # New position shall differ from reference position
        self.assertNotEqual(apple.position, self._ref_position)

    def test_reset(self):
        """Test whether position is properly reset"""
        apple = Apple(self._sprite_size, self._default_color, self._random_seed)
        apple.reset()
        self.assertNotEqual(apple.position, self._ref_position)

if __name__ == "__main__":
    unittest.main()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
