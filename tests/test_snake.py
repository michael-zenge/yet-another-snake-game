# Yet Another Snake Game feat. Q-Learning by Michael Zenge
#
# Run unit tests in project directory with "python -m tests.test_snake"
#

import unittest
import pygame

from tests.color import Color

from snake import Snake


class test_snake(unittest.TestCase):
    def setUp(self):
        self._sprite_size = (16, 16)
        self._screen_size = (20 * self._sprite_size[0], 16 * self._sprite_size[1])
        self._screen = pygame.display.set_mode(self._screen_size)
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_sprite_size(self):
        """Test 'sprite_size' property"""
        snake = Snake(self._sprite_size, "darkgreen", "green", "red", "dimgrey")
        self.assertEqual(snake.sprite_size, self._sprite_size)

    def test_body_color(self):
        """Test selection of supported color formats"""
        # Integer value
        color_int = 0xFFFFFFFF  # (255, 255, 255, 255) -> white
        white_snake = Snake(self._sprite_size, "darkgreen", color_int, "red", "dimgrey")
        self.assertIsInstance(white_snake.body_color, pygame.color.Color)
        self.assertEqual(white_snake.body_color, pygame.color.Color(color_int))

        # (r, g, b, [a])
        color_rgb = (255, 0, 0)  # red
        red_snake = Snake(self._sprite_size, "darkgreen", color_rgb, "red", "dimgrey")
        self.assertIsInstance(red_snake.body_color, pygame.color.Color)
        self.assertEqual(red_snake.body_color, pygame.color.Color(color_rgb))

        # Named color
        color_str = "green"
        green_snake = Snake(self._sprite_size, "darkgreen", color_str, "red", "dimgrey")
        self.assertIsInstance(green_snake.body_color, pygame.color.Color)
        self.assertEqual(green_snake.body_color, pygame.color.Color(color_str))

        # HTML color format
        color_str = "#0000FF"  # blue
        blue_snake = Snake(self._sprite_size, "darkgreen", color_str, "red", "dimgrey")
        self.assertIsInstance(blue_snake.body_color, pygame.color.Color)
        self.assertEqual(blue_snake.body_color, pygame.color.Color(color_str))

    def test_wall_color(self):
        """Test selection of supported color formats"""
        # Integer value
        color_int = 0xFFFFFFFF  # (255, 255, 255, 255) -> white
        wall_color = Snake(
            self._sprite_size, "darkgreen", "green", "red", color_int
        ).wall_color
        self.assertIsInstance(wall_color, pygame.color.Color)
        self.assertEqual(wall_color, pygame.color.Color(color_int))

        # (r, g, b, [a])
        color_rgb = (255, 0, 0)  # red
        wall_color = Snake(
            self._sprite_size, "darkgreen", "green", "red", color_rgb
        ).wall_color
        self.assertIsInstance(wall_color, pygame.color.Color)
        self.assertEqual(wall_color, pygame.color.Color(color_rgb))

        # Named color
        color_str = "green"
        wall_color = Snake(
            self._sprite_size, "darkgreen", "green", "red", color_str
        ).wall_color
        self.assertIsInstance(wall_color, pygame.color.Color)
        self.assertEqual(wall_color, pygame.color.Color(color_str))

        # HTML color format
        color_str = "#0000FF"  # blue
        wall_color = Snake(
            self._sprite_size, "darkgreen", "green", "red", color_str
        ).wall_color
        self.assertIsInstance(wall_color, pygame.color.Color)
        self.assertEqual(wall_color, pygame.color.Color(color_str))

    def test_direction_without_save_update(self):
        """Test 'direction' property without save update"""
        snake = Snake(
            self._sprite_size, "darkgreen", "green", "red", "dimgrey", save_update=False
        )

        # Snake shall move in right direction after initialization
        self.assertEqual(snake.direction, pygame.K_RIGHT)

        # Try up and down
        snake.direction = pygame.K_UP
        self.assertEqual(snake.direction, pygame.K_UP)
        snake.direction = pygame.K_DOWN
        self.assertEqual(snake.direction, pygame.K_DOWN)

        # Try left and right
        snake.direction = pygame.K_LEFT
        self.assertEqual(snake.direction, pygame.K_LEFT)
        snake.direction = pygame.K_RIGHT
        self.assertEqual(snake.direction, pygame.K_RIGHT)

        # TODO: Test other key events ...

    def test_direction_with_save_update(self):
        """Test 'direction' property with save update"""
        snake = Snake(
            self._sprite_size, "darkgreen", "green", "red", "dimgrey", save_update=True
        )

        # Snake shall move in right direction after initialization
        self.assertEqual(snake.direction, pygame.K_RIGHT)

        # Try up and down
        snake.direction = pygame.K_UP
        self.assertEqual(snake.direction, pygame.K_UP)
        snake.direction = pygame.K_DOWN
        self.assertEqual(snake.direction, pygame.K_UP)

        # Try left and right
        snake.direction = pygame.K_LEFT
        self.assertEqual(snake.direction, pygame.K_LEFT)
        snake.direction = pygame.K_RIGHT
        self.assertEqual(snake.direction, pygame.K_LEFT)

        # Try down and up
        snake.direction = pygame.K_DOWN
        self.assertEqual(snake.direction, pygame.K_DOWN)
        snake.direction = pygame.K_UP
        self.assertEqual(snake.direction, pygame.K_DOWN)

        # Try right and left
        snake.direction = pygame.K_RIGHT
        self.assertEqual(snake.direction, pygame.K_RIGHT)
        snake.direction = pygame.K_LEFT
        self.assertEqual(snake.direction, pygame.K_RIGHT)

        # TODO: Test other key events ...

    def test_reset(self):
        """Test 'reset' of snake"""
        snake = Snake(
            self._sprite_size,
            "darkgreen",
            "green",
            "red",
            "dimgrey",
            10,
            0.5,
            save_update=True,
        )
        # Change direction
        snake.direction = pygame.K_UP
        snake.direction = pygame.K_LEFT
        # Reset
        snake.reset()
        # Test
        for ii in range(0, 5):
            self.assertEqual(
                snake.snake[ii],
                (
                    int(self._screen_size[0] / 4 + ii * self._sprite_size[0]),
                    int(self._screen_size[1] / 2),
                ),
            )
        self.assertEqual(snake.direction, pygame.K_RIGHT)

    def test_do(self):
        """Test 'do' method"""
        snake = Snake(self._sprite_size, "darkgreen", "green", "red", "dimgrey")
        for key_event in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
            snake.do(key_event)
            self.assertEqual(snake.direction, key_event)
        for key_event in {pygame.K_SPACE, pygame.K_ESCAPE}:
            snake.do(key_event)
            self.assertNotEqual(snake.direction, key_event)

    def test_update(self):
        """Test 'update'method"""
        for color in Color:
            snake = Snake(
                self._sprite_size,
                Color.HEAD.value,
                Color.BODY.value,
                Color.APPLE.value,
                Color.WALL.value,
            )
            snake_len = len(snake.snake[:])

            # Reset background color
            self._screen.fill(color.value)
            result = snake.update()

            # Collision
            if self._screen.get_at(snake.snake[-1]) in [
                Color.BODY.value,
                Color.WALL.value,
            ]:
                self.assertFalse(result)
            else:
                self.assertTrue(result)

            # Grow snake
            if self._screen.get_at(snake.snake[-1]) == Color.APPLE.value:
                self.assertEqual(len(snake.snake[:]), snake_len + 1)
            else:
                self.assertEqual(len(snake.snake[:]), snake_len)

    def test_draw(self):
        """Test 'draw' method"""
        bkgrd_color = pygame.color.Color("black")
        head_color = pygame.color.Color("darkgreen")
        body_color = pygame.color.Color("green")
        apple_color = pygame.color.Color("red")
        wall_color = pygame.color.Color("dimgrey")

        for color in [bkgrd_color, head_color, body_color, apple_color, wall_color]:
            snake = Snake(
                self._sprite_size, head_color, body_color, apple_color, wall_color
            )

            # Reset background color
            self._screen.fill(bkgrd_color)
            snake.draw()

            # Test color of body elements at position
            for pos in snake.snake[0:-1]:
                self.assertEqual(self._screen.get_at(pos), body_color)

            # Test color at head position
            match color:
                case bkgrd_color, head_color:
                    self.assertEqual(self._screen.get_at(snake.snake[-1]), head_color)
                case body_color, apple_color, wall_color:
                    self.assertEqual(self._screen.get_at(snake.snake[-1]), color)

    def test_move(self):
        """Test 'move' method"""
        snake = Snake(self._sprite_size, "darkgreen", "green", "red", "dimgrey")

        for direction in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
            new_snake = Snake(self._sprite_size, "darkgreen", "green", "red", "dimgrey")
            new_snake.direction = direction

            new_snake.move()

            # Compare body elements
            for ii in range(0, 4):
                self.assertEqual(new_snake.snake[ii], snake.snake[ii + 1])

            # Compare head position
            if direction == pygame.K_RIGHT:
                self.assertEqual(
                    new_snake.snake[-1][0], snake.snake[-1][0] + self._sprite_size[0]
                )
                self.assertEqual(new_snake.snake[-1][1], snake.snake[-1][1])
            elif direction == pygame.K_UP:
                self.assertEqual(new_snake.snake[-1][0], snake.snake[-1][0])
                self.assertEqual(
                    new_snake.snake[-1][1], snake.snake[-1][1] - self._sprite_size[1]
                )
            elif direction == pygame.K_DOWN:
                self.assertEqual(new_snake.snake[-1][0], snake.snake[-1][0])
                self.assertEqual(
                    new_snake.snake[-1][1], snake.snake[-1][1] + self._sprite_size[1]
                )
            elif direction == pygame.K_LEFT:
                self.assertEqual(
                    new_snake.snake[-1][0], snake.snake[-1][0] - self._sprite_size[0]
                )
                self.assertEqual(new_snake.snake[-1][1], snake.snake[-1][1])


if __name__ == "__main__":
    unittest.main()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
