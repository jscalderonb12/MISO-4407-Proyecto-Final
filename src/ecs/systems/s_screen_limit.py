import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud

def system_screen_limit(world:esper.World, screen:pygame.Rect):
    components = world.get_components(CTransform, CSurface, CTagCloud)

    transform:CTransform
    surface:CSurface
    for _, (transform, surface, _) in components:
        cuad_rect = CSurface.get_area_relative(surface.area, transform.pos)
        if (cuad_rect.left < 0 or cuad_rect.right > screen.width) or (cuad_rect.top < screen.top or cuad_rect.bottom > (screen.top + screen.height)):
            cuad_rect.clamp_ip(screen)
            transform.pos.x = cuad_rect.x
            transform.pos.y = cuad_rect.y