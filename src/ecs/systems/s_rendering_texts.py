from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_text import CTagText

def system_rendering_texts(world:World, screen:Surface):
    components = world.get_components(CTransform, CSurface, CTagText)

    transform:CTransform
    surface:CSurface
    for _, (transform, surface, _) in components:
        if hasattr(surface, "visible") and not surface.visible:
            continue
        screen.blit(surface.surf, transform.pos, area=surface.area)