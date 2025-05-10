from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_screen_limit(world:World, screen:Surface, bullet_entity_list:list[int]):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)

    transform:CTransform
    surface:CSurface
    for entity, (transform, surface, _) in components:
        cuad_rect = CSurface.get_area_relative(surface.area, transform.pos)
        if (cuad_rect.left < 0 or cuad_rect.right > screen_rect.width) or (cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height):
            world.delete_entity(entity)
            bullet_entity_list.remove(entity)