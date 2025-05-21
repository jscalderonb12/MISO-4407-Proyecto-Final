import json
import pygame
import esper
import math

from src.ecs.components.c_rotation import CRotation
from src.ecs.systems.s_animation_enemy import system_enemy_animation
from src.ecs.systems.s_enemy_chase import system_enemy_chase
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_update_rotation import system_update_rotation
import src.engine.game_engine
from src.engine.scenes.layout_scene import LayoutScene
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_animation_player import system_animation_player
from src.ecs.systems.s_bullet_screen_limit import system_bullet_screen_limit
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_animation import system_animation
from src.create.prefab_creator import create_player, create_input_player, create_bullet, create_cloud_spawner, create_cloud
from src.create.prefab_creator_interface import create_text, TextAlignment, create_blinking_text, update_text
from src.ecs.systems.s_cloud_spawner import system_cloud_spawner
from src.ecs.systems.s_movement import system_apply_velocity, system_world_movement
from src.ecs.systems.s_cloud_screen_limit import system_cloud_screen_limit
from src.create.prefab_creator import create_enemy_spawner, create_player, create_input_player, create_bullet
from src.ecs.systems.s_pause_game import system_pause_game
from src.ecs.systems.s_text_blink import system_text_blink
from src.ecs.systems.s_deleting_init_texts import system_deleting_init_texts

class PlayScene(LayoutScene):

    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self._load_config_files(level_path)
            
        self.bg_color = (self.levels_config['level_01']['bg_color']['r'], self.levels_config['level_01']['bg_color']['g'], self.levels_config['level_01']['bg_color']['b'])
        
        self.player_position = "IDLE"
        self._bullet_burst_queue = []
        self.active_inputs = set()
        self.pause_game = False
        self.pause_text = None
        self.start_game_text = []
        self.score = 0

    def _load_config_files(self, level_path:str):
        with open(level_path) as levels_file:
            self.levels_config = json.load(levels_file)
        with open('assets/cfg/bullet.json') as bullets_file:
            self.bullets_config = json.load(bullets_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open('assets/cfg/clouds.json') as clouds_file:
            self.clouds_config = json.load(clouds_file)


    def do_draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self._game_engine.game_rect) 
        super().do_draw(screen)
        
    def do_create(self):
        self._bullet_entity_list = []
        create_cloud(self.ecs_world, self.levels_config, self.clouds_config, is_cloud_large=False)
        self._player_entity = create_player(self.ecs_world, self.player_config, self._game_engine.game_rect)
        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_cloud(self.ecs_world, self.levels_config, self.clouds_config, is_cloud_large=True)
        create_input_player(self.ecs_world)
        self.texts_entities = self.crete_init_text(["PLAYER 1", "A.D. 1910", "STAGE 1"])
        super().do_create()
    
    def do_update(self, delta_time: float):
        system_animation_player(self.ecs_world, self.player_position, delta_time)
        system_animation(self.ecs_world, delta_time)
        system_update_rotation(self.ecs_world)
        system_apply_velocity(self.ecs_world, delta_time)
        system_world_movement(self.ecs_world, delta_time)
        system_bullet_screen_limit(self.ecs_world, self._game_engine.game_rect, self._bullet_entity_list)
        system_enemy_spawner(self.ecs_world, delta_time, self.enemies_cfg)
        system_enemy_animation(self.ecs_world, delta_time)
        system_enemy_chase(self.ecs_world, delta_time)
        system_cloud_screen_limit(self.ecs_world, self.screen)
        system_pause_game(self.ecs_world, self.pause_game)
        system_text_blink(self.ecs_world, self.screen, self._game_engine.total_time)
        self.texts_entities = system_deleting_init_texts(self.ecs_world, self._game_engine.total_time, self.texts_entities)
        """ update_text(self.ecs_world, self.current_score_surface, str(self.score))
        update_text(self.ecs_world, self.high_score_surface, str(self.high_score))
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score """

        super().do_update(delta_time)
    
    def do_action(self, action: CInputCommand):

        if action.name == "PAUSE":
            if action.phase == CommandPhase.START:
                """ self.damage_plane_counter() """
                self.pause_game = not self.pause_game

                if self.pause_game:
                    self.pause_text = create_blinking_text(
                        self.ecs_world, 
                        "PAUSED", 
                        8, 
                        pygame.Color(255, 0, 0), 
                        pygame.Vector2(self._game_engine.game_rect.width/2, (self._game_engine.game_rect.height + self._game_engine.UI_HEIGHT)/2), 
                        TextAlignment.CENTER
                    )
                else:
                    self.ecs_world.delete_entity(self.pause_text)
                    self.pause_text = None

        
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

    def crete_init_text(self, texts:list = []):
        texts_entities = []
        initial_pos_x = self._game_engine.game_rect.width/2
        initial_pos_y = 112
        for text in texts:
            texts_entities.append(create_text(
                self.ecs_world, 
                text, 
                8, 
                pygame.Color(255, 255, 255), 
                pygame.Vector2(initial_pos_x, initial_pos_y), 
                TextAlignment.CENTER
            ))
            initial_pos_y += 40

        return texts_entities

