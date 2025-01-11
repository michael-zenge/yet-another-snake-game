# Yet Another Snake Game feat. Q-Learning by Michael Zenge
import pygame

from snake import Snake
from apple import Apple

from q_learning import SnakeQLearning


class SnakeApp:
    """Create a single-window Snake app"""

    def __init__(self):
        """Initialize pygame and the application"""
        pygame.init()

        # Active Q-Learning mode
        self._learning = True

        # Set private attributes
        self._sprite_size = (32, 32)
        self._screen_size = (20 * self._sprite_size[0], 16 * self._sprite_size[1])

        self._bkgrd_color = pygame.color.Color("lemonchiffon")
        self._wall_color = pygame.color.Color("dimgrey")
        self._apple_color = pygame.color.Color("red")
        self._head_color = pygame.color.Color("darkgreen")
        self._body_color = pygame.color.Color("green")

        apple = Apple(self._sprite_size, self._apple_color)
        apple.reset(self._screen_size)

        self._snake = Snake(
            self._sprite_size,
            self._head_color,
            self._body_color,
            self._apple_color,
            self._wall_color,
        )
        self._snake.reset(self._screen_size)

        self._sprites = []
        self._sprites.append(apple)  # add apple first to avoid drawing over snake
        self._sprites.append(self._snake)

        if not self._learning:
            self._screen = pygame.display.set_mode(self._screen_size, pygame.SHOWN)
            pygame.display.set_caption("Yet Another Snake Game")
        else:
            # Allow fast learning in the background
            self._screen = pygame.display.set_mode(self._screen_size, pygame.HIDDEN)
            pygame.display.set_caption("Yet Another Snake Game (Q-Learning)")
            self._snake.speed = 0.0
            self._snake.speed_inc = 0.0

        self._env = SnakeQLearning(self._sprites[0], self._sprites[1], 1000)

        self._running = True
        self._updating = True

    def run(self):
        """Run the main event loop."""
        self.draw()
        while self._running:
            for event in pygame.event.get():
                self.do(event)
            self.update()
        pygame.quit()  # does not exit the program, safe to call more than once

    def do(self, event):
        match event.type:
            case pygame.QUIT:
                self._running = False
                pygame.quit()  # does not exit the program, safe to call more than once
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        self._updating = not self._updating
                    case pygame.K_ESCAPE:
                        self._running = False
                        pygame.quit()  # does not exit the program, safe to call more than once
                    case _:
                        if not self._learning:  # do not accept keyboard input
                            for sprite in self._sprites:
                                sprite.do(event.key)

    def update(self):
        if self._running and self._updating:
            if self._learning:
                self._env.update()

            for sprite in self._sprites:
                success = sprite.update(self._screen)
                if not success and not self._learning:
                    self._running = False
                    pygame.quit()  # does not exit the program, safe to call more than once
                    break

            self.draw()

            if self._learning:
                self._env.reward()

    def draw(self):
        if self._running and self._updating:
            # Un-hide display when learning completed
            if not self._env.is_learning() and not pygame.display.get_active():
                self._snake.speed = 10
                self._screen = pygame.display.set_mode(self._screen_size, pygame.SHOWN)

            # Q-learning requires wall thickness = 2 * size of sprite
            bkgrd_coord = (2 * self._sprite_size[0], 2 * self._sprite_size[1])
            bkgrd_size = (
                self._screen_size[0] - 4 * self._sprite_size[0],
                self._screen_size[1] - 4 * self._sprite_size[1],
            )

            surface = pygame.surface.Surface(self._screen_size)
            surface.fill(self._wall_color)
            screen_bkgrd = pygame.Rect(bkgrd_coord, bkgrd_size)
            pygame.draw.rect(surface, self._bkgrd_color, screen_bkgrd)

            self._screen.blit(surface, (0, 0))

            for sprite in self._sprites:
                sprite.draw(self._screen)

            pygame.display.update()


if __name__ == "__main__":
    SnakeApp().run()

# Copyright (c) 2024 michael-zenge, permission granted under MIT license
