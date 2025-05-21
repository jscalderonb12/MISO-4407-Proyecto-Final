import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud

def system_cloud_screen_limit(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagCloud)

    transform:CTransform
    surface:CSurface
    for _, (transform, surface, _) in components:
        cuad_rect = CSurface.get_area_relative(surface.area, transform.pos)
        if cuad_rect.right < 0:
            transform.pos.x = screen_rect.width
        elif cuad_rect.left > screen_rect.width:
            transform.pos.x = -cuad_rect.width

        if cuad_rect.bottom < 0:
            transform.pos.y = screen_rect.height
        elif cuad_rect.top > screen_rect.height:
            transform.pos.y = -cuad_rect.height