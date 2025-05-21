import json
import pygame
import esper
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_player_screen_limit import system_player_screen_limit
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_bullet_screen_limit import system_bullet_screen_limit
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_animation_player import system_animation_player
from src.create.prefab_creator import create_enemy_spawner , create_player_square, create_input_player, create_bullet_square

class GameEngine:
    def __init__(self) -> None:
        self._load_assets()

        pygame.init()
        pygame.display.set_caption(self.window_config['title'])

        self.screen = pygame.display.set_mode((self.window_config['size']['w'], self.window_config['size']['h']))
        self.bg_color = (self.window_config['bg_color']['r'], self.window_config['bg_color']['g'], self.window_config['bg_color']['b'])
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config['framerate']
        self.delta_time = 0
        self.total_time = 0
        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._bullet_entity_list = []
        self._player_entity = create_player_square(self.ecs_world, self.player_config, self.levels_config["player_spawn"]["position"])

        self._player_vel = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_enemy_spawner(self.ecs_world, self.levels_config)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        self.total_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.total_time, self.enemy_types_config)
        system_movement(self.ecs_world, self.delta_time)
        system_enemy_state(self.ecs_world, self._player_entity)
        system_screen_bounce(self.ecs_world, self.screen)
        system_player_screen_limit(self.ecs_world, self.screen)
        system_bullet_screen_limit(self.ecs_world, self.screen, self._bullet_entity_list)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.levels_config["player_spawn"]["position"], self.explosion_config)
        system_collision_bullet_enemy(self.ecs_world, self._bullet_entity_list, self.explosion_config)
        system_animation(self.ecs_world, self.delta_time)
        system_animation_player(self.ecs_world, "IDLE")
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _load_assets(self):
        with open('assets/cfg/window.json', encoding='utf-8') as window_file:
            self.window_config = json.load(window_file)
        if "window" in self.window_config:
            self.window_config = self.window_config["window"]
        with open('assets/cfg/enemies.json') as enemies_file:
            self.enemy_types_config = json.load(enemies_file)
        with open('assets/cfg/level_01.json') as levels_file:
            self.levels_config = json.load(levels_file)
        with open('assets/cfg/player.json') as player_file:
            self.player_config = json.load(player_file)
        with open('assets/cfg/bullet.json') as bullet_file:
            self.bullet_config = json.load(bullet_file)
        with open('assets/cfg/explosion.json') as explosion_file:
            self.explosion_config = json.load(explosion_file)

    def _do_action(self, c_input:CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase in (CommandPhase.START, CommandPhase.HOLD):
                system_animation_player(self.ecs_world, "LEFT")
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase in (CommandPhase.START, CommandPhase.HOLD):
                system_animation_player(self.ecs_world, "RIGHT")
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_vel.vel.y -= self.player_config["input_velocity"]
            if c_input.phase == CommandPhase.END:
                self._player_vel.vel.y += self.player_config["input_velocity"]
        if c_input.name == "PLAYER_DOWN":    
            if c_input.phase == CommandPhase.START:
                self._player_vel.vel.y += self.player_config["input_velocity"]
            if c_input.phase == CommandPhase.END:
                self._player_vel.vel.y -= self.player_config["input_velocity"]
        if c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                player_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
                player_surf = self.ecs_world.component_for_entity(self._player_entity, CSurface)
                player_rect = player_surf.area.copy()
                player_rect.topleft = player_transform.pos
                bullet_pos = pygame.Vector2(player_rect.center)
                self.add_bullet_entity(bullet_pos, c_input.pos)

    def add_bullet_entity(self, bullet_pos:pygame.Vector2, mouse_pos:pygame.Vector2) -> None:
        if len(self._bullet_entity_list) < self.levels_config["player_spawn"]["max_bullets"]:
            self._bullet_entity_list.append(
                create_bullet_square(self.ecs_world, bullet_pos, self.bullet_config, mouse_pos)
            )