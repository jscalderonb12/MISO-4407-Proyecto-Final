from pygame.math import Vector2
from esper import World
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.create.prefab_creator import (
    create_enemy_single,
    create_enemy_squadron,
    create_enemy_chaser,
    create_enemy_shooter
)

def system_enemy_spawner(world: World, delta_time: float, enemy_types: dict):
    """
    Procesador que genera enemigos basados en eventos de CEnemySpawner.
    Usa los campos 'time', 'enemy_type' y 'position' de cada evento.
    """
    for ent, (spawner,) in world.get_components(CEnemySpawner):
        for evt in spawner.spawn_events:
            # Acumula tiempo
            evt["elapsed"] = evt.get("elapsed", 0.0) + delta_time
            # Si ya disparó, saltar
            if not evt.get("trigger", True):
                continue
            # Disparar cuando elapsed >= time
            if evt["elapsed"] >= evt.get("time", 0.0):
                evt["trigger"] = False

                # Configuración de este tipo de enemigo
                cfg = enemy_types[evt["enemy_type"]]
                pos = Vector2(evt["position"]["x"], evt["position"]["y"])
                etype = cfg.get("type", "single")

                # Para chasers, obtenemos la posición del jugador
                player_pos = None
                if etype == "chaser":
                    player_ent = next(pid for pid, _ in world.get_components(CTagPlayer))
                    player_pos = world.component_for_entity(player_ent, CTransform).pos

                # Delegar creación al prefab_creator según el tipo
                if etype == "single":
                    create_enemy_single(world, pos, cfg)
                elif etype == "squadron":
                    create_enemy_squadron(world, pos, cfg)
                elif etype == "chaser":
                    create_enemy_chaser(world, pos, cfg, player_pos)
                elif etype == "shooter":
                    create_enemy_shooter(world, pos, cfg)
                else:
                    # Default: spawn single
                    create_enemy_single(world, pos, cfg)


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
