import math
from pygame.math import Vector2
from esper import World
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.tags.c_tag_chase_enemy import CTagChaseEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_enemy_chase(world: World, delta_time: float):
    """
    Sistema que mueve a los enemigos de tipo 'chaser' persiguiendo al jugador.
    Usa CEnemyState.distance_start_chase/return para alternar velocidad.
    Actualiza CVelocity y CRotation de cada chaser.
    """
    # Obtener la posición del jugador (asumimos un solo jugador)
    player_ent_list = [ent for ent, _ in world.get_components(CTagPlayer)]
    if not player_ent_list:
        return
    player_ent = player_ent_list[0]
    player_pos = world.component_for_entity(player_ent, CTransform).pos

    # Procesar cada enemigo IA
    for ent, (transform, vel, rot, state) in world.get_components(
            CTransform, CVelocity, CRotation, CEnemyState):
        if not world.has_component(ent, CTagChaseEnemy):
            continue
        # Vector hacia el jugador
        to_player = player_pos - transform.pos
        dist = to_player.length()
        if dist == 0:
            continue
        # Elegir velocidad según distancia
        if dist <= state.distance_start_chase:
            speed = state.velocity_chase
        else:
            speed = state.velocity_return
        # Normalizar dirección y asignar velocidad
        direction = to_player.normalize()
        vel.vel = direction * speed
        # Actualizar rotación para apuntar al jugador
        angle = math.atan2(direction.y, direction.x)
        rot.angle = angle
        rot.direction = Vector2(math.cos(angle), math.sin(angle))