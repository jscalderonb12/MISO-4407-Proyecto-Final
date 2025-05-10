import json
import pygame
import esper

import src.engine.game_engine
from src.engine.scenes.layout_scene import LayoutScene
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_player_screen_limit import system_player_screen_limit
from src.ecs.systems.s_animation_player import system_animation_player
from src.create.prefab_creator import create_player, create_input_player

class PlayScene(LayoutScene):

    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open(level_path) as levels_file:
            self.levels_config = json.load(levels_file)
            
        self.bg_color = (self.levels_config['level_01']['bg_color']['r'], self.levels_config['level_01']['bg_color']['g'], self.levels_config['level_01']['bg_color']['b'])
        
        self.player_position = "IDLE"
        self.active_inputs = set()

    def do_draw(self, screen):
        screen.fill(self.bg_color)
        super().do_draw(screen)
        
    def do_create(self):
        super().do_create()
        self._bullet_entity_list = []
        self._player_entity = create_player(self.ecs_world, self.player_config, self.levels_config["player_spawn"]["position"])
        create_input_player(self.ecs_world)
    
    def do_update(self, delta_time: float):
        system_animation_player(self.ecs_world, self.player_position, delta_time)
        system_player_screen_limit(self.ecs_world, self.screen)

    def do_action(self, action: CInputCommand):
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
