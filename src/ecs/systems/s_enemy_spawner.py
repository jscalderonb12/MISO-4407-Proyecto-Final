import esper
import pygame
import random

from src.create.prefab_creator import create_enemy_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner

def system_enemy_spawner(world:esper.World, total_time:float, enemy_types:dict):
    components = world.get_components(CEnemySpawner)

    enemy_spawner:CEnemySpawner
    for _, (enemy_spawner,) in components:
        for spawn_event in enemy_spawner.spawn_events:
            if total_time >= spawn_event["time"] and spawn_event["trigger"]:
                enemy_data = enemy_types[spawn_event["enemy_type"]]
                create_enemy_square(
                    world = world, 
                    pos = pygame.Vector2(spawn_event["position"]["x"], spawn_event["position"]["y"]),
                    enemy_data = enemy_data,
                    enemy_type = spawn_event["enemy_type"]
                )
                spawn_event["trigger"] = False