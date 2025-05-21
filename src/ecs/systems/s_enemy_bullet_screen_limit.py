from esper import World
from pygame import Surface, Rect, Vector2

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

def system_enemy_bullet_screen_limit(world:World, screen:Rect):
    components = world.get_components(CTransform, CSurface, CTagEnemyBullet)
    transform:CTransform
    surface:CSurface
    for entity, (transform, surface, _) in components:
        bullet_center = transform.pos + Vector2(surface.area.width / 2, surface.area.height / 2)

        if (bullet_center.x < 0 or bullet_center.x > screen.width or bullet_center.y < screen.top or bullet_center.y > (screen.top + screen.height)):
            world.delete_entity(entity)