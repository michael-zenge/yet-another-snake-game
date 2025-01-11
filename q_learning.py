# Implementation of Q-Learning for a Snake game by Michael Zenge
# Reference: https://en.wikipedia.org/wiki/Q-learning

import pygame
import random
import numpy as np

from apple import Apple
from snake import Snake


class SnakeQLearning:
    def __init__(
        self,
        apple_sprite: Apple,
        snake_sprite: Snake,
        learning_episodes=500,
        exploration_rate=0.2,
        learning_rate=0.2,
        discount_factor=0.5,
        random_seed: int = None,
    ):
        self._apple = apple_sprite
        self._snake = snake_sprite

        self._learning_episodes = learning_episodes
        self._exploration_rate = exploration_rate

        # Q-learning
        self._learning_rate = learning_rate  # alpa
        self._discount_factor = discount_factor  # gamma

        self._random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
            self._quality_table = np.random.rand(4096, 4)
        else:
            self._quality_table = np.zeros(
                (4096, 4)
            )  # Upper limit of 4096 states (actual number of states much lower); 4 possible actions

        self._screen = pygame.display.get_surface()
        self._display_active = pygame.display.get_active()

        self._actions = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]

        self._state_idx = 0
        self._action_idx = 0

        self._episode = 1
        self._step = 0
        self._total_reward = 0

    def is_learning(self) -> bool:
        return self._episode < self._learning_episodes

    def update(self):
        self._step += 1
        self._state_idx = self._get_state_idx()
        self._snake.do(self._action())

    def reward(self):
        new_state_idx = self._get_state_idx()
        reward = self._get_reward(new_state_idx, self._action_idx)

        if self.is_learning():
            # Update quality table
            alpha = self._learning_rate
            gamma = self._discount_factor

            self._quality_table[self._state_idx][self._action_idx] = (
                1 - alpha
            ) * self._quality_table[self._state_idx][self._action_idx]
            self._quality_table[self._state_idx][self._action_idx] += (
                alpha * reward + alpha * gamma * self._get_max_reward(new_state_idx)
            )
        else:
            # No exploration after learning completed
            self._exploration_rate = 0.0
        return reward

    def _get_max_reward(self, state_idx):
        return max(self._quality_table[state_idx][:])

    def _get_reward(self, new_state_idx, action_idx):
        if new_state_idx >= 3072:
            return self._get_reward_with_location_offset(
                new_state_idx, action_idx, pygame.K_DOWN, pygame.K_LEFT, 3072
            )  # higher-right
        elif new_state_idx >= 2048:
            return self._get_reward_with_location_offset(
                new_state_idx, action_idx, pygame.K_DOWN, pygame.K_RIGHT, 2048
            )  # higher-left
        elif new_state_idx >= 1024:
            return self._get_reward_with_location_offset(
                new_state_idx, action_idx, pygame.K_UP, pygame.K_RIGHT, 1024
            )  # lower-left
        else:
            return self._get_reward_with_location_offset(
                new_state_idx, action_idx, pygame.K_UP, pygame.K_LEFT, 0
            )  # lower-right

    def _get_reward_with_location_offset(
        self, new_state_idx, action_idx, ref_action1, ref_action2, offset_idx
    ):
        if (new_state_idx - offset_idx) >= 512:
            # Reset and (re)-draw sprites
            for sprite in [self._apple, self._snake]:
                sprite.reset(self._screen.get_size())
                sprite.draw(self._screen)
            reward = -10  # Collision with wall or body
        elif (new_state_idx - offset_idx) >= 256:
            reward = 10  # Found apple
        else:
            if self._actions[action_idx] in [
                ref_action1,
                ref_action2,
            ]:
                reward = 1  # Move towards apple
            else:
                reward = -1  # Move away from apple

        # Log message
        self._total_reward += reward
        print(
            "Learning:",
            (self._exploration_rate > 0.0),
            "| Episode, Step, Reward:",
            self._episode,
            self._step,
            self._total_reward,
        )
        # New episode, reset logging
        if reward == -10:
            self._episode += 1
            self._step = 0
            self._total_reward = 0

        return reward

    def _action(self):
        random.seed(self._random_seed)
        if random.random() < self._exploration_rate:
            self._action_idx = random.randint(0, len(self._actions) - 1)
        else:
            self._action_idx = self._call_agent_for_action(self._state_idx)
        return self._actions[self._action_idx]

    def _call_agent_for_action(self, state_idx):
        action_idx = 0
        best_action = float("-inf")
        for idx, action in enumerate(self._quality_table[state_idx]):
            if action > best_action:
                best_action = action
                action_idx = idx
        return action_idx

    def _get_state_idx(self):
        snake_head_x = self._snake.snake[-1][0]
        snake_head_y = self._snake.snake[-1][1]

        apple_x = self._apple.position[0]
        apple_y = self._apple.position[1]

        # Check location of head relative to apple
        if snake_head_x >= apple_x and snake_head_y >= apple_y:  # lower-right
            index = 0
        elif snake_head_x < apple_x and snake_head_y >= apple_y:  # lower-left
            index = 1024
        elif snake_head_x < apple_x and snake_head_y < apple_y:  # higher-left
            index = 2048
        elif snake_head_x >= apple_x and snake_head_y < apple_y:  # higher-right
            index = 3072

        # Check locations of head and four neigbouring tiles
        index += self._get_state_idx_with_offset(
            0, 0, 8
        )  # head location (all colors but background)
        index += self._get_state_idx_with_offset(
            0, -self._snake.sprite_size[1], 6
        )  # above
        index += self._get_state_idx_with_offset(
            0, self._snake.sprite_size[1], 4
        )  # below
        index += self._get_state_idx_with_offset(
            -self._snake.sprite_size[0], 0, 2
        )  # left
        index += self._get_state_idx_with_offset(
            self._snake.sprite_size[0], 0, 0
        )  # right

        return index

    def _get_state_idx_with_offset(self, offset_x: int, offset_y: int, bit_shift: int):
        target_coord = (
            self._snake.snake[-1][0] + offset_x,
            self._snake.snake[-1][1] + offset_y,
        )

        color = self._screen.get_at(target_coord)

        if color == self._snake.wall_color:
            return int("11", 2) << bit_shift
        elif color == self._snake.body_color:
            return int("10", 2) << bit_shift
        elif color == self._apple.color:
            return int("01", 2) << bit_shift
        else:
            return int("00", 2) << bit_shift  # background or head color
