import json
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene

class GameEngine:
    def __init__(self) -> None:
        self._load_assets()

        pygame.init()
        pygame.display.set_caption(self.window_config['title'])

        self.screen = pygame.display.set_mode((self.window_config['size']['w'], self.window_config['size']['h']), pygame.SCALED)
        self.interface_rect = pygame.Rect(0, 0, self.window_config['size']['w'], 40)
        self.game_rect = pygame.Rect(0, 40, self.window_config['size']['w'], self.window_config['size']['h'] - 40)
        self.bg_color = (self.window_config['bg_color']['r'], self.window_config['bg_color']['g'], self.window_config['bg_color']['b'])
        
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config['framerate']
        self.delta_time = 0
        self.ecs_world = esper.World()
        

        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["LEVEL_01_SCENE"] = PlayScene("assets/cfg/level_01.json", self)
        #self._scenes["GAME_OVER_SCENE"] = GameOverScene(self)
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None

    def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
        self._do_clean()

    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        self.screen.fill(self.bg_color)
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

    def _load_assets(self):
        with open('assets/cfg/window.json', encoding='utf-8') as window_file:
            self.window_config = json.load(window_file)

    def _do_action(self, c_input: CInputCommand):
        self._current_scene.do_action(c_input)