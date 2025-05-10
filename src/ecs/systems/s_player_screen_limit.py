from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_player_screen_limit(world:World, screen:Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagPlayer)

    transform:CTransform
    surface:CSurface
    for _, (transform, surface, _) in components:
        cuad_rect = CSurface.get_area_relative(surface.area, transform.pos)
        if (cuad_rect.left < 0 or cuad_rect.right > screen_rect.width) or (cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height):
            cuad_rect.clamp_ip(screen_rect)
            transform.pos.x = cuad_rect.x
            transform.pos.y = cuad_rect.y