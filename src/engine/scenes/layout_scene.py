import pygame
import json

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.create.prefab_creator import create_input_player
from src.ecs.components.c_surface import CSurface

class LayoutScene(Scene):

    def __init__(self, game_engine):
        super().__init__(game_engine)
        with open('assets/cfg/player.json') as player_file:
            self.player_config = json.load(player_file)
        with open('assets/cfg/interface.json') as interface_file:
            self.interface_config = json.load(interface_file)

    def do_create(self):
        self.title_color = pygame.Color(self.interface_config['title_text_color']['r'], self.interface_config['title_text_color']['g'], self.interface_config['title_text_color']['b'])
        #pygame.draw.rect(self.screen, (0, 0, 0), self._game_engine.interface_rect)
        interface_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(interface_entity, CSurface((self._game_engine.interface_rect.width, self._game_engine.interface_rect.height), (0,0,0)))
        pygame.draw.rect(self.screen, (0, 0, 0), self._game_engine.footer_rect)
        create_text(self.ecs_world, "1-UP", 8, self.title_color, pygame.Vector2(0, 0), TextAlignment.LEFT)
        create_text(self.ecs_world, "HI-SCORE", 8, pygame.Color(255, 0, 0), pygame.Vector2(112, 0), TextAlignment.CENTER)
        create_text(self.ecs_world, "0", 8, pygame.Color(255, 255, 255), pygame.Vector2(0, 10), TextAlignment.LEFT)
        create_text(self.ecs_world, "0", 8, pygame.Color(255, 255, 255), pygame.Vector2(112, 10), TextAlignment.CENTER)
        self.draw_lives(self.screen, 4)
        

    def do_draw(self, screen):
        super().do_draw(screen)

    def draw_lives(self, screen, num_lives):
        player_sprite = pygame.image.load(self.player_config["image"]).convert_alpha()
        frame_rect = pygame.Rect(0, 0, 16, 32)
        frame_image = pygame.Surface((32, 32), pygame.SRCALPHA)
        frame_image.blit(player_sprite, (0, 0), frame_rect)

        for i in range(num_lives):
            x = 0 + (i * 15)
            screen.blit(frame_image, (x, 20))
