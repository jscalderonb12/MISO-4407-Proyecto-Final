import esper
import pygame
import random

from src.create.prefab_creator import create_cloud
from src.ecs.components.c_cloud_spawner import CCloudSpawner

def system_cloud_spawner(world:esper.World, total_time:float, cloud_config:dict):
    components = world.get_components(CCloudSpawner)

    cloud_spawner:CCloudSpawner
    for _, (cloud_spawner,) in components:
        for spawn_event in cloud_spawner.spawn_events:
            if total_time >= spawn_event["time"] and spawn_event["trigger"]:
                cloud_data = cloud_config[spawn_event["type"]]
                create_cloud(
                    world = world, 
                    cloud_config = cloud_data,
                    cloud_pos = pygame.Vector2(spawn_event["position"]["x"], spawn_event["position"]["y"])
                )
                spawn_event["trigger"] = False