from esper import World
from pygame import Surface

from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_movement(world:World, delta_time:float):
    components = world.get_components(CTransform, CVelocity)

    transform:CTransform
    velocity:CVelocity
    for _, (transform, velocity) in components:
        transform.pos.x += velocity.vel.x * delta_time
        transform.pos.y += velocity.vel.y * delta_time

def system_world_movement(world:World, delta_time: float):
    """
    Sistema de movimiento del entorno para llamar como función:
    Mueve todas las entidades con CTransform excepto la nave,
    en sentido inverso a CRotation.direction de la nave.

    :param world: instancia de World de Esper
    :param delta_time: tiempo transcurrido desde el último frame
    """
    # Obtener rotación de la nave
    rotations = world.get_components(CRotation, CTagPlayer, CVelocity)
    if not rotations:
        return
    # Solo tomamos la primera entidad etiquetada como nave
    _, (rot, _, ship_velocity) = rotations[0]

    # Calcula vector de desplazamiento del mundo
    dx = rot.direction.x * ship_velocity.vel.x * delta_time
    dy = rot.direction.y * ship_velocity.vel.y * delta_time

    # Desplaza todas las entidades menos la nave
    for ent, transform in world.get_component(CTransform):
        if world.has_component(ent, CTagPlayer)\
           or world.has_component(ent, CTagBullet):
            continue
        transform.pos.x -= dx
        transform.pos.y -= dy

def system_apply_velocity(world, delta_time: float):
    for ent, (transform, velocity) in world.get_components(CTransform, CVelocity):
        if world.has_component(ent, CTagPlayer):
            continue
        transform.pos.x += velocity.vel.x * delta_time
        transform.pos.y += velocity.vel.y * delta_time
    