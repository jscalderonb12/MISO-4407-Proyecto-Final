import pygame
import json

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand
from src.create.prefab_creator import create_input_player
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_rendering_texts import system_rendering_texts

class LayoutScene(Scene):

    def __init__(self, game_engine):
        super().__init__(game_engine)
        with open('assets/cfg/player.json') as player_file:
            self.player_config = json.load(player_file)
        with open('assets/cfg/interface.json') as interface_file:
            self.interface_config = json.load(interface_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)

        self.high_score = 0
        self.plane_counter_stage = 40

    def do_create(self):
        self.title_color = pygame.Color(self.interface_config['title_text_color']['r'], self.interface_config['title_text_color']['g'], self.interface_config['title_text_color']['b'])
        create_text(self.ecs_world, "1-UP", 8, self.title_color, pygame.Vector2(20, 0), TextAlignment.LEFT)
        create_text(self.ecs_world, "HI-SCORE", 8, pygame.Color(255, 0, 0), pygame.Vector2(112, 0), TextAlignment.CENTER)
        self.current_score_surface = create_text(self.ecs_world, "0", 8, pygame.Color(255, 255, 255), pygame.Vector2(52, 10), TextAlignment.LEFT)
        self.high_score_surface = create_text(self.ecs_world, str(self.high_score), 8, pygame.Color(255, 255, 255), pygame.Vector2(112, 10), TextAlignment.CENTER)
        super().do_create()
        
    def do_draw(self, screen):
        super().do_draw(screen)
        pygame.draw.rect(self.screen, (0, 0, 0), self._game_engine.interface_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self._game_engine.footer_rect)
        self.draw_lives(self.screen, 2)
        self.draw_plane_counter(self.screen)
        system_rendering_texts(self.ecs_world, screen)

    def do_update(self, delta_time):
        super().do_update(delta_time)

    def draw_lives(self, screen, num_lives):
        player_sprite = pygame.image.load(self.player_config["image"]).convert_alpha()
        frame_rect = pygame.Rect(0, 0, 16, 32)
        frame_image = pygame.Surface((32, 32), pygame.SRCALPHA)
        frame_image.blit(player_sprite, (0, 0), frame_rect)

        for i in range(num_lives):
            x = 0 + (i * 15)
            screen.blit(frame_image, (x, 20))

    def draw_plane_counter(self, screen):
        player_sprite = pygame.image.load(self.level_01_cfg["level_01"]["plane_counter"]).convert_alpha()

        icon_count = 8
        max_frame = 40
        icon_width = 16
        icon_height = 16
        frames_per_icon = max_frame // icon_count
        current_frame = self.plane_counter_stage

        for i in range(icon_count):
            remaining = current_frame - (i * frames_per_icon)

            if remaining <= 0:
                continue
            elif remaining >= frames_per_icon:
                visible_width = icon_width
            else:
                visible_width = int(icon_width * (remaining / frames_per_icon))

            if visible_width <= 0:
                continue

            start_x = icon_width - visible_width
            frame_rect = pygame.Rect(start_x, 0, visible_width, icon_height)
            frame_image = pygame.Surface((visible_width, icon_height), pygame.SRCALPHA)
            frame_image.blit(player_sprite, (0, 0), frame_rect)
            x = screen.get_width() - icon_width - (i * (icon_width + 1)) + start_x
            y = 242
            screen.blit(frame_image, (x, y))

    def damage_plane_counter(self, amount=1):
        self.plane_counter_stage = max(0, self.plane_counter_stage - amount)
