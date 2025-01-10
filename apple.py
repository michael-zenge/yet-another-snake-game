# Yet Another Snake Game feat. Q-Learning by Michael Zenge
import pygame
import random


class Apple:
    def __init__(self, sprite_size, apple_color="red"):
        self._sprite_size = sprite_size
        self._apple_color = pygame.color.Color(apple_color)

        self._screen = pygame.display.get_surface()
        self._screen_size = self._screen.get_size()

        # Create sprite object
        self._image = pygame.Surface(self._sprite_size)
        self._image.fill(self._apple_color)

        # Offset considering wall thickness
        self._offset_x = 2 * self._sprite_size[0]
        self._offset_y = 2 * self._sprite_size[1]

        self._position = (self._offset_x, self._offset_y)

    @property
    def color(self):
        return self._apple_color

    @property
    def position(self):
        return self._position

    def do(self, event_key):
        pass

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.blit(self._image, self.position)

    def update(self, screen: pygame.surface.Surface) -> None:
        # Reset position if eaten by snake
        if screen.get_at(self.position) != self.color:
            self.reset(screen.get_size())
        return True

    def reset(self, screen_size: tuple[int, int], random_seed: int = None) -> None:
        random.seed(random_seed)
        pos_x = random.randrange(
            self._offset_x,
            screen_size[0] - 2 * self._sprite_size[0],
            self._sprite_size[0],
        )
        pos_y = random.randrange(
            self._offset_y,
            screen_size[1] - 2 * self._sprite_size[1],
            self._sprite_size[1],
        )
        self._position = (pos_x, pos_y)


# Copyright (c) 2024 michael-zenge, permission granted under MIT license
