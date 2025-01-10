# Yet Another Snake Game
import pygame


class Snake:
    def __init__(
        self,
        sprite_size,
        head_color,
        body_color,
        apple_color,
        wall_color,
        speed=10,
        speed_inc=0.5,
        save_update=False,
    ):
        self._sprite_size = sprite_size
        self._apple_color = pygame.color.Color(apple_color)
        self._wall_color = pygame.color.Color(wall_color)
        self._speed = speed  # framerate in fps
        self._speed_inc = speed_inc  # speed increment
        self._save_update = save_update  # avoid direction conflicts
        self._direction = 0

        self._head_color = pygame.color.Color(head_color)
        self._head = pygame.Surface(self._sprite_size)
        self._head.fill(self._head_color)

        self._body_color = pygame.color.Color(body_color)
        self._body = pygame.Surface(self._sprite_size)
        self._body.fill(self._body_color)

        # Create sprite object
        self.snake = []

    @property
    def sprite_size(self):
        return self._sprite_size

    @property
    def body_color(self):
        return self._body_color

    @property
    def wall_color(self):
        return self._wall_color

    @property
    def direction(self):
        """Get the current direction."""
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        """Set a new direction."""
        if self._save_update:
            if new_direction == pygame.K_UP and self.direction != pygame.K_DOWN:
                self._direction = new_direction
            elif new_direction == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                self._direction = new_direction
            elif new_direction == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                self._direction = new_direction
            elif new_direction == pygame.K_DOWN and self.direction != pygame.K_UP:
                self._direction = new_direction
        else:
            self._direction = new_direction

    def reset(self, screen_size: tuple[int, int]) -> None:
        self.snake.clear()
        for ii in range(0, 5):
            self.snake.append(
                (
                    int(screen_size[0] / 4 + ii * self._sprite_size[0]),
                    int(screen_size[1] / 2),
                )
            )
        self._direction = pygame.K_RIGHT  # force update

    def do(self, event_key):
        if event_key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
            self.direction = event_key

    def update(self, screen: pygame.surface.Surface) -> None:
        # Move snake
        self.move()

        if screen.get_at(self.snake[-1]) in [self._body_color, self._wall_color]:
            return False

        # Eat apple
        if screen.get_at(self.snake[-1]) == self._apple_color:
            self.snake.insert(0, (self.snake[0]))  # grow snake
            self._speed += self._speed_inc

        # Update speed
        pygame.time.Clock().tick(self._speed)  # framerate in fps

        return True

    def draw(self, screen: pygame.surface.Surface) -> None:
        for pos in self.snake[0:-1]:
            screen.blit(self._body, pos)
        # Do not draw head over apple or wall
        if screen.get_at(self.snake[-1]) not in [
            self._body_color,
            self._wall_color,
            self._apple_color,
        ]:
            screen.blit(self._head, self.snake[-1])

    def move(self):
        if self.direction == pygame.K_RIGHT:
            self.snake.append(
                (self.snake[-1][0] + self._sprite_size[0], self.snake[-1][1])
            )
        elif self.direction == pygame.K_UP:
            self.snake.append(
                (self.snake[-1][0], self.snake[-1][1] - self._sprite_size[1])
            )
        elif self.direction == pygame.K_DOWN:
            self.snake.append(
                (self.snake[-1][0], self.snake[-1][1] + self._sprite_size[1])
            )
        elif self.direction == pygame.K_LEFT:
            self.snake.append(
                (self.snake[-1][0] - self._sprite_size[0], self.snake[-1][1])
            )
        self.snake.pop(0)


# Copyright (c) 2024 michael-zenge, permission granted under MIT license
