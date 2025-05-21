import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_winner import CTagWinner
from src.create.prefab_creator import create_explosion
from src.ecs.components.tags.c_tag_hidden_player import CTagHiddenPlayer
from src.ecs.components.c_timeout import CTimeout
from src.ecs.components.c_enemy_state import CEnemyState


def system_collision_player_enemy(world:esper.World, player_entity:int, explosion_data:dict, lose_lives, switch_scene, update_score, max_lives, start_game_text, score, damage_plane_counter, plane_counter):
    components = world.get_components(CSurface, CTransform, CEnemyState, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_rect = CSurface.get_area_relative(player_surface.area, player_transform.pos)

    for enemy_entity, (enemy_surface, enemy_transform, enemy_state, _) in components:
        enemy_rect = CSurface.get_area_relative(enemy_surface.area, enemy_transform.pos)
        if enemy_rect.colliderect(player_rect) and not world.has_component(player_entity, CTagHiddenPlayer):
            world.delete_entity(enemy_entity)
            update_score()
            create_explosion(world, enemy_transform.pos, explosion_data["ENEMY"])
            create_explosion(world, player_transform.pos, explosion_data["PLAYER"])
            current_lives = lose_lives()

            if current_lives[0] <= 0 or enemy_state.type == "boss":
                max_lives[0] = 4
                score[0] = 0
                plane_counter[0] = 40
                start_game_text(["PLAYER 1", "A.D. 1910", "STAGE 1"])

                if enemy_state.type == "boss":
                    world.add_component(player_entity, CTagWinner())
                    world.add_component(player_entity, CTagHiddenPlayer())
                    world.add_component(player_entity, CTimeout(3.0))
                else:
                    switch_scene("GAME_OVER_SCENE")
            else:
                damage_plane_counter()
                world.add_component(player_entity, CTagHiddenPlayer())
                world.add_component(player_entity, CTimeout(3.0))