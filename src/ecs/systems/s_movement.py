from esper import World
from pygame import Surface

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform

def system_movement(world:World, delta_time:float):
    components = world.get_components(CTransform, CVelocity)

    transform:CTransform
    velocity:CVelocity
    for _, (transform, velocity) in components:
        transform.pos.x += velocity.vel.x * delta_time
        transform.pos.y += velocity.vel.y * delta_time