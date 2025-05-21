import pygame
import json

from src.engine.scenes.layout_scene import LayoutScene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand

class GameOverScene(LayoutScene):

    def __init__(self, game_engine):
        super().__init__(game_engine)
        
        self.bg_color = (self.level_01_cfg['level_01']['bg_color']['r'], self.level_01_cfg['level_01']['bg_color']['g'], self.level_01_cfg['level_01']['bg_color']['b'])
        self.wait_duration = 3.0

    def do_create(self):
        super().do_create()
        pygame.draw.rect(self.screen, self.bg_color, self._game_engine.game_rect) 
        create_text(self.ecs_world, "PLAYER 1", 8, pygame. Color(255, 255, 255), pygame.Vector2(80, 115), TextAlignment.LEFT)
        create_text(self.ecs_world, "GAME OVER", 8, pygame. Color(255, 0, 0), pygame.Vector2(80, 140), TextAlignment.LEFT)

    def do_update(self, delta_time: float):
        self.wait_duration -= delta_time
        if self.wait_duration <= 0.0:
            self.wait_duration = 3.0
            self.switch_scene("MENU_SCENE")

    def do_draw(self, screen):
        super().do_draw(screen)