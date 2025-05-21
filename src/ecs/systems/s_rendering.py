from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_hidden import CTagHidden

def system_rendering(world:World, screen:Surface):
    components = world.get_components(CTransform, CSurface)

    transform:CTransform
    surface:CSurface
    for ent, (transform, surface) in components:
        if world.has_component(ent, CTagHidden):
            continue
        if hasattr(surface, "visible") and not surface.visible:
            continue
        screen.blit(surface.surf, transform.pos, area=surface.area)