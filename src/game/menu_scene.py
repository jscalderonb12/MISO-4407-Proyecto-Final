import pygame
import json

from src.engine.scenes.layout_scene import LayoutScene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.create.prefab_creator import create_input_player

class MenuScene(LayoutScene):

    def __init__(self, game_engine):
        super().__init__(game_engine)

    def do_create(self):
        super().do_create()
        create_text(self.ecs_world, "PLAY", 8, pygame. Color(0, 190, 255), pygame.Vector2(110, 50), TextAlignment.CENTER)

        self.game_logo = pygame.image.load(self.interface_config["game_logo"]).convert_alpha()
        
        create_text(self.ecs_world, "PUSH START BUTTON", 8, pygame. Color(0, 190, 255), pygame.Vector2(110, 123), TextAlignment.CENTER)
        create_text(self.ecs_world, "ONE PLAYER ONLY", 8, pygame. Color(0, 190, 255), pygame.Vector2(101, 140), TextAlignment.CENTER)

        create_text(self.ecs_world, f"1ST BONUS {self.interface_config['extra_life_increase_1']} PTS.", 8, pygame. Color(0, 190, 255), pygame.Vector2(120, 165), TextAlignment.CENTER)
        create_text(self.ecs_world, f"AND EVERY {self.interface_config['extra_life_increase_2']} PTS.", 8, pygame. Color(0, 190, 255), pygame.Vector2(120, 182), TextAlignment.CENTER)

        create_text(self.ecs_world, f"© UNIANDES 2025", 8, pygame. Color(255, 255, 255), pygame.Vector2(110, 215), TextAlignment.CENTER)

        create_input_player(self.ecs_world)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01_SCENE")

    def do_draw(self, screen):
        screen.blit(self.game_logo, (40, 65))
        super().do_draw(screen)
        pygame.display.flip()