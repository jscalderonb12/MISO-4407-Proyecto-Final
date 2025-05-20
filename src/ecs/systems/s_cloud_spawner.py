import esper
import pygame
import random

from src.create.prefab_creator import create_cloud
from src.ecs.components.c_cloud_spawner import CCloudSpawner

def system_cloud_spawner(world:esper.World, total_time:float, cloud_config:dict, game_rect:pygame.Rect):
    components = world.get_components(CCloudSpawner)

    cloud_spawner:CCloudSpawner
    for _, (cloud_spawner,) in components:
        for spawn_event in cloud_spawner.spawn_events:
            if total_time >= spawn_event["time"] and spawn_event["trigger"]:
                #cloud_data = cloud_types[spawn_event["cloud_type"]]
                create_cloud(
                    world = world, 
                    cloud_config = cloud_config,
                    game_rect= game_rect
                )
                spawn_event["trigger"] = False