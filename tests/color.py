# Yet Another Snake Game feat. Q-Learning by Michael Zenge

import pygame
from enum import Enum

class Color(Enum):
    WALL = pygame.color.Color('dimgrey')
    BKGRD = pygame.color.Color('lemonchiffon')
    APPLE = pygame.color.Color('red')
    HEAD = pygame.color.Color('darkgreen')
    BODY = pygame.color.Color('green')

# Copyright (c) 2024 michael-zenge, permission granted under MIT license