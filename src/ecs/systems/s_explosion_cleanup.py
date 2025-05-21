import esper

from src.ecs.components.c_explosion_timer import CExplosionTimer


def system_explosion_cleanup(world: esper.World, delta_time: float):
    for entity, timer in world.get_component(CExplosionTimer):
        timer.timer += delta_time
        if timer.timer >= timer.duration:
            world.delete_entity(entity)