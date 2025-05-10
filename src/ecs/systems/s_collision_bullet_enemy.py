import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion

def system_collision_bullet_enemy(world:esper.World, bullet_entity_list:list[int], explosion_data:dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    for bullet_entity in bullet_entity_list:
        bullet_transform = world.component_for_entity(bullet_entity, CTransform)
        bullet_surface = world.component_for_entity(bullet_entity, CSurface)
        bullet_rect = CSurface.get_area_relative(bullet_surface.area, bullet_transform.pos)

        for enemy_entity, (enemy_surface, enemy_transform, _) in components:
            enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)
            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, explosion_data, enemy_transform.pos)
                bullet_entity_list.remove(bullet_entity)