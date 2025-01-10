# Yet Another Snake Game feat. Q-Learning by Michael Zenge
#
# Run unit tests in project directory with "python -m tests.test_snake"
#

import unittest
import pygame

from apple import Apple
from snake import Snake

from tests.color import Color

from q_learning import SnakeQLearning


class test_q_learning(unittest.TestCase):
    def setUp(self):
        self._sprite_size = (16, 16)
        self._screen_size = (20 * self._sprite_size[0], 16 * self._sprite_size[1])
        self._screen = pygame.display.set_mode(self._screen_size)

        self._apple = Apple(self._sprite_size, Color.APPLE.value)
        self._apple.reset(self._screen_size, 1000)

        self._snake = Snake(
            self._sprite_size,
            Color.HEAD.value,
            Color.BODY.value,
            Color.APPLE.value,
            Color.WALL.value,
        )
        self._snake.reset(self._screen_size)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_update(self):
        """Test change of direction after update"""
        env = SnakeQLearning(self._apple, self._snake, 200, 0.0, 0.2, 0.5, 1000)
        orig_direction = env._snake.direction
        self.assertEqual(orig_direction, pygame.K_RIGHT)
        env.update()
        new_direction = env._snake.direction
        self.assertEqual(new_direction, pygame.K_LEFT)

    def test_reward(self):
        """Test reward method"""
        env = SnakeQLearning(self._apple, self._snake, 200, 0.0, 0.2, 0.5, 1000)
        self.assertEqual(env.reward(), 1)

        env = SnakeQLearning(self._apple, self._snake, 1, 1.0, 0.2, 0.5, 1000)
        self.assertEqual(env._exploration_rate, 1.0)
        self.assertEqual(env.reward(), 1)
        self.assertEqual(env._exploration_rate, 0.0)

    def test_get_max_reward(self):
        """Test calcuation of maximum reward"""
        env = SnakeQLearning(self._apple, self._snake, 200, 0.0, 0.2, 0.5, 1000)
        self.assertAlmostEqual(env._get_max_reward(0), 0.95, 2)
        self.assertAlmostEqual(env._get_max_reward(4095), 0.98, 2)

    def test_get_reward(self):
        """Test reward for selected states"""
        env = SnakeQLearning(self._apple, self._snake)
        self.assertEqual(env._get_reward(4095, 0), -10)
        self.assertEqual(env._get_reward(3071, 0), -10)
        self.assertEqual(env._get_reward(2047, 0), -10)
        self.assertEqual(env._get_reward(1023, 0), -10)

        self.assertEqual(env._get_reward(3328, 0), 10)
        self.assertEqual(env._get_reward(2304, 0), 10)
        self.assertEqual(env._get_reward(1280, 0), 10)
        self.assertEqual(env._get_reward(256, 0), 10)

        self.assertEqual(env._get_reward(3072, 0), -1)
        self.assertEqual(env._get_reward(2048, 0), 1)
        self.assertEqual(env._get_reward(1024, 0), 1)
        self.assertEqual(env._get_reward(0, 0), -1)

    def test_get_reward_with_location_offset(self):
        """Test reward for selected state-action pairs"""
        env = SnakeQLearning(self._apple, self._snake)
        for action_idx in range(0, 4):
            self.assertEqual(
                env._get_reward_with_location_offset(
                    512, action_idx, pygame.K_DOWN, pygame.K_RIGHT, 0
                ),
                -10,
            )
            self.assertEqual(
                env._get_reward_with_location_offset(
                    256, action_idx, pygame.K_DOWN, pygame.K_RIGHT, 0
                ),
                10,
            )
        self.assertEqual(
            env._get_reward_with_location_offset(
                128, 0, pygame.K_DOWN, pygame.K_RIGHT, 0
            ),
            1,
        )
        self.assertEqual(
            env._get_reward_with_location_offset(
                0, 3, pygame.K_DOWN, pygame.K_RIGHT, 0
            ),
            -1,
        )

    def test_action(self):
        """Test return of '_action' method"""
        # exploration_rate = 0.0
        env = SnakeQLearning(self._apple, self._snake, 200, 0.0, 0.2, 0.5, 1000)
        self.assertEqual(env._action(), pygame.K_DOWN)
        # exploration_rate = 100.0
        env = SnakeQLearning(self._apple, self._snake, 200, 100.0, 0.2, 0.5, 1000)
        self.assertEqual(env._action(), pygame.K_RIGHT)

    def test_call_agent_for_action(self):
        """Test actions for selected states"""
        env = SnakeQLearning(self._apple, self._snake, 200, 0.2, 0.2, 0.5, 1000)
        self.assertEqual(env._call_agent_for_action(0), 2)
        self.assertEqual(env._call_agent_for_action(512), 3)
        self.assertEqual(env._call_agent_for_action(3072), 0)
        self.assertEqual(env._call_agent_for_action(4095), 1)

    def test_get_state_idx(self):
        """Test state depending on relative positions of snake and apple only"""
        env = SnakeQLearning(self._apple, self._snake)
        self._apple.reset(self._screen_size, 3000)
        self.assertEqual(env._get_state_idx(), 0)
        self._apple.reset(self._screen_size, 2000)
        self.assertEqual(env._get_state_idx(), 1024)
        self._apple.reset(self._screen_size, 1000)
        self.assertEqual(env._get_state_idx(), 2048)
        self._apple.reset(self._screen_size, 100)
        self.assertEqual(env._get_state_idx(), 3072)

    def test_get_state_idx_with_offset(self):
        """Test state depending on the color at current location"""
        env = SnakeQLearning(self._apple, self._snake)
        for color in Color:
            self._screen.fill(color.value)
            self._snake.draw(self._screen)
            match color:
                case Color.WALL:
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 0), 3)
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 2), 12)
                    # Snake body to the left
                    self.assertEqual(
                        env._get_state_idx_with_offset(-self._sprite_size[0], 0, 4), 32
                    )
                case Color.BODY:
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 0), 2)
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 2), 8)
                    # Snake body to the left
                    self.assertEqual(
                        env._get_state_idx_with_offset(-self._sprite_size[0], 0, 4), 32
                    )
                case Color.APPLE:
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 0), 1)
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 2), 4)
                    # Snake body to the left
                    self.assertEqual(
                        env._get_state_idx_with_offset(-self._sprite_size[0], 0, 4), 32
                    )
                case _:
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 0), 0)
                    self.assertEqual(env._get_state_idx_with_offset(0, 0, 2), 0)
                    # Snake body to the left
                    self.assertEqual(
                        env._get_state_idx_with_offset(-self._sprite_size[0], 0, 6), 128
                    )


if __name__ == "__main__":
    unittest.main()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
