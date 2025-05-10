from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform

def system_rendering(world:World, screen:Surface):
    components = world.get_components(CTransform, CSurface)

    transform:CTransform
    surface:CSurface
    for _, (transform, surface) in components:
        screen.blit(surface.surf, transform.pos, area=surface.area)