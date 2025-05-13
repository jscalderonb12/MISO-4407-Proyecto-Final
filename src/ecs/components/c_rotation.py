
import pygame


class CRotation:
    def __init__(self, direction:pygame.Vector2, angle: float = 0.0) -> None:
        self.angle = angle
        self.direction = direction
