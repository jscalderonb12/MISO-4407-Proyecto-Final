import esper

from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

def system_collision_player_enemy_bullet(world:esper.World, player_entity:int, pos_data:dict, explosion_data:dict):
    components = world.get_components(CSurface, CTransform, CTagEnemyBullet)

    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    player_animation = world.component_for_entity(player_entity, CAnimationPlayer)

    player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)

    for enemy_entity, (enemy_surface, enemy_transform, _) in components:
        enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)
        if enemy_rect.colliderect(player_rect):
            world.delete_entity(enemy_entity)
            create_explosion(world, enemy_transform.pos, explosion_data["PLAYER"])
            size = player_surface.surf.get_size()
            size = (size[0] / player_animation.number_frames, size[1])
            player_transform.pos.x = pos_data["x"] - size[0] / 2
            player_transform.pos.y = pos_data["y"] - size[1] / 2