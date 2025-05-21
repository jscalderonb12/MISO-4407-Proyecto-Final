import random
from pygame import Rect
import pygame
from pygame.math import Vector2
from esper import World
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.create.prefab_creator import (
    create_enemy_single,
    create_enemy_squadron,
    create_enemy_chaser,
    create_enemy_shooter
)

def system_enemy_spawner(world: World, delta_time: float, enemy_types: dict, screen_rect:Rect):
    """
    Procesa CEnemySpawner para generar enemigos según eventos.
    - Chasers IA: nacen en bordes con comportamiento de IA
    - Squadron: aparecen frente al jugador y entran de frente
    - Shooter y single: emergen de bordes apuntando al jugador
    """
    # Posición y rotación del jugador
    player_entities = [e for e, _ in world.get_components(CTagPlayer)]
    player_pos = None
    player_rot = None
    if player_entities:
        player_ent = player_entities[0]
        player_pos = world.component_for_entity(player_ent, CTransform).pos
        player_rot = world.component_for_entity(player_ent, CRotation)

    for ent, (spawner,) in world.get_components(CEnemySpawner):
        for evt in spawner.spawn_events:
            evt['elapsed'] = evt.get('elapsed', 0.0) + delta_time
            
            if evt['elapsed'] >= evt['time']:
                evt['elapsed'] %= evt['time']
                etype = evt['enemy_type']
                cfg = enemy_types.get(etype)
                if not cfg:
                    continue

                # Squadron: aparece frente al jugador
                if cfg.get('type') == 'squadron' and player_pos and player_rot:
                    spawn_dir = player_rot.direction
                    spawn_dist = max(screen_rect.width, screen_rect.height) / 2 + 50
                    pos = player_pos + spawn_dir * spawn_dist
                    print(f"[Spawner] Squadron spawn_dir={spawn_dir}, spawn_pos={pos}")
                    create_enemy_squadron(world, pos, cfg, enemy_types, player_pos)
                    continue

                # Resto de tipos: borde aleatorio
                pos = random_edge_position(screen_rect)
                if cfg.get('type') == 'chaser':
                    create_enemy_chaser(world, pos, cfg, player_pos)
                elif cfg.get('type') == 'shooter':
                    create_enemy_shooter(world, pos, cfg, player_pos)
                else:
                    create_enemy_single(world, pos, cfg, player_pos)


def random_edge_position(screen_rect: pygame.Rect) -> Vector2:
    """Genera una posición aleatoria justo fuera de un borde de la pantalla."""
    w, h = screen_rect.width, screen_rect.height
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        return Vector2(random.uniform(0, w), -10)
    if side == "bottom":
        return Vector2(random.uniform(0, w), h + 10)
    if side == "left":
        return Vector2(-10, random.uniform(0, h))
    # right
    return Vector2(w + 10, random.uniform(0, h))


# def system_enemy_spawner(world:esper.World, total_time:float, enemy_types:dict):
#     components = world.get_components(CEnemySpawner)

#     enemy_spawner:CEnemySpawner
#     for _, (enemy_spawner,) in components:
#         for spawn_event in enemy_spawner.spawn_events:
#             if total_time >= spawn_event["time"] and spawn_event["trigger"]:
#                 enemy_data = enemy_types[spawn_event["enemy_type"]]
#                 create_enemy_square(
#                     world = world, 
#                     pos = pygame.Vector2(spawn_event["position"]["x"], spawn_event["position"]["y"]),
#                     enemy_info = enemy_data,
#                     enemy_type = spawn_event["enemy_type"]
#                 )
#                 spawn_event["trigger"] = False
