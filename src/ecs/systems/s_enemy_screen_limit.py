import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_screen_limit(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagEnemy)
    transform:CTransform
    surface:CSurface
    for entity, (transform, surface, _) in components:
        enemy_rect = CSurface.get_area_relative(surface.area, transform.pos)
        margin = 64
        if (enemy_rect.right < (0 - margin) or enemy_rect.left > (screen_rect.width + margin) or enemy_rect.bottom < (0 - margin) or enemy_rect.top > (screen_rect.height + margin)):
            world.delete_entity(entity)