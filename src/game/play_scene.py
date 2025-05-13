import json
import pygame
import esper
import math

from src.ecs.components.c_rotation import CRotation
from src.ecs.systems.s_update_rotation import system_update_rotation
import src.engine.game_engine
from src.engine.scenes.layout_scene import LayoutScene
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_player_screen_limit import system_player_screen_limit
from src.ecs.systems.s_animation_player import system_animation_player
from src.ecs.systems.s_bullet_screen_limit import system_bullet_screen_limit
from src.ecs.systems.s_movement import system_movement

from src.create.prefab_creator import create_player, create_input_player, create_bullet

class PlayScene(LayoutScene):

    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open(level_path) as levels_file:
            self.levels_config = json.load(levels_file)
        with open('assets/cfg/bullet.json') as bullets_file:
            self.bullets_config = json.load(bullets_file)
            
        self.bg_color = (self.levels_config['level_01']['bg_color']['r'], self.levels_config['level_01']['bg_color']['g'], self.levels_config['level_01']['bg_color']['b'])
        
        self.player_position = "IDLE"
        self._bullet_burst_queue = []
        self.active_inputs = set()

    def do_draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self._game_engine.game_rect) 
        super().do_draw(screen)
        
    def do_create(self):
        super().do_create()
        self._bullet_entity_list = []
        self._player_entity = create_player(self.ecs_world, self.player_config, self._game_engine.game_rect)
        create_input_player(self.ecs_world)
    
    def do_update(self, delta_time: float):
        system_movement(self.ecs_world, delta_time)
        system_bullet_screen_limit(self.ecs_world, self._game_engine.game_rect, self._bullet_entity_list)
        system_animation_player(self.ecs_world, self.player_position, delta_time)
        system_update_rotation(self.ecs_world)

    def do_action(self, action: CInputCommand):
        
        if action.name == "PLAYER_FIRE" and len(self._bullet_entity_list) < self.levels_config["player_spawn"]["max_bullets"]:
            if action.phase == CommandPhase.START:
                player_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
                player_surf = self.ecs_world.component_for_entity(self._player_entity, CSurface)
                player_rotation = self.ecs_world.component_for_entity(self._player_entity, CRotation)
            
                player_rect = player_surf.area.copy()
                player_rect.topleft = player_transform.pos
                bullet_pos = pygame.Vector2(player_rect.center)

                self._bullet_entity_list.append(create_bullet(self.ecs_world, bullet_pos, self.bullets_config, player_rotation.direction))

        else:
            key = action.name.replace("PLAYER_", "")

            if action.phase == CommandPhase.START:
                self.active_inputs.add(key)
            elif action.phase == CommandPhase.END:
                self.active_inputs.discard(key)

            self._update_player_position()

    def _update_player_position(self):
        directions = sorted(self.active_inputs)

        if not directions:
            self.player_position = "IDLE"
        elif len(directions) == 1:
            self.player_position = directions[0]
        elif len(directions) == 2:
            combo = "_".join(directions)
            self.player_position = combo
        else:
            combo = "_".join(directions[:2])
            self.player_position = combo

    def _update_rotation(self):
        player_anim = self.ecs_world.component_for_entity(self._player_entity, CAnimationPlayer)
        sprite_angle = (player_anim.current_frame * 11.25) - 90
        rad_angle = math.radians(sprite_angle)
        self._player_c_dir.angle = rad_angle
        self._player_c_dir.direction = pygame.Vector2(-math.cos(rad_angle), math.sin(rad_angle))

