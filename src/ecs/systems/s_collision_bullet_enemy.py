import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_winner import CTagWinner
from src.ecs.components.tags.c_tag_hidden_player import CTagHiddenPlayer
from src.ecs.components.c_timeout import CTimeout

from src.ecs.components.c_enemy_state import CEnemyState
from src.create.prefab_creator import create_explosion

def system_collision_bullet_enemy(world:esper.World, bullet_entity_list:list[int], explosion_data:dict, damage_plane_counter, update_score, player_entity:int):
    components = world.get_components(CSurface, CTransform, CEnemyState, CTagEnemy)
    for bullet_entity in bullet_entity_list:
        bullet_transform = world.component_for_entity(bullet_entity, CTransform)
        bullet_surface = world.component_for_entity(bullet_entity, CSurface)
        bullet_rect = CSurface.get_area_relative(bullet_surface.area, bullet_transform.pos)

        for enemy_entity, (enemy_surface, enemy_transform, enemy_state, _) in components:
            enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)
            if enemy_rect.colliderect(bullet_rect):
                world.delete_entity(bullet_entity)
                enemy_state.shot_live -= 1

                if enemy_state.shot_live <= 0:
                    world.delete_entity(enemy_entity)
                    create_explosion(world, enemy_transform.pos, explosion_data["ENEMY"])
                    if enemy_state.type == "boss":
                        world.add_component(player_entity, CTagWinner())
                        world.add_component(player_entity, CTagHiddenPlayer())
                        world.add_component(player_entity, CTimeout(3.0))
                    else:
                        damage_plane_counter()
                    update_score()
                try:
                    bullet_entity_list.remove(bullet_entity)
                except ValueError:
                    continue