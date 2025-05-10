import esper
import pygame
import math
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyState

def system_enemy_state(world:esper.World, player_entity:int):
    components = world.get_components(CVelocity, CAnimation, CEnemyState, CTransform)
    player_transform = world.component_for_entity(player_entity, CTransform)
    
    for _, (velocity, animation, enemy_state, transform) in components:
        distance_to_player = _calculate_distance(transform.pos, player_transform.pos)
        
        if enemy_state.state == EnemyState.IDLE:
            if distance_to_player < enemy_state.distance_start_chase:
                _do_idle_state(velocity, animation, enemy_state, transform, player_transform.pos)
        elif enemy_state.state == EnemyState.MOVE:
            _do_move_state(velocity, animation, enemy_state, transform, player_transform.pos)
        else:
            _do_back_state(velocity, animation, enemy_state, transform)

def _do_idle_state(velocity:CVelocity, animation:CAnimation, enemy_state:CEnemyState, transform:CTransform, player_pos:pygame.Vector2):
    _set_animation(animation, 1)
    if enemy_state.position_return is None:
        enemy_state.state = EnemyState.MOVE
        original_position = transform.pos.copy()
        enemy_state.position_return = original_position


def _do_move_state(velocity:CVelocity, animation:CAnimation, enemy_state:CEnemyState, transform:CTransform, player_pos:pygame.Vector2):
    _set_animation(animation, 0)
    distance_from_initial = _calculate_distance(transform.pos, enemy_state.position_return)
    if distance_from_initial >= enemy_state.distance_start_return:
        enemy_state.state = EnemyState.BACK
    else:
        direction = _calculate_direction(transform.pos, player_pos)
        speed = enemy_state.velocity_chase
        velocity.vel.x = direction.x * speed
        velocity.vel.y = direction.y * speed
    
def _do_back_state(velocity:CVelocity, animation:CAnimation, enemy_state:CEnemyState, transform:CTransform):
    _set_animation(animation, 0)
    direction = _calculate_direction(transform.pos, enemy_state.position_return)
    speed = enemy_state.velocity_return
    velocity.vel.x = direction.x * speed
    velocity.vel.y = direction.y * speed

    if enemy_state.position_return == transform.pos:
        enemy_state.state = EnemyState.IDLE
        enemy_state.position_return = None
        velocity.vel.x = 0
        velocity.vel.y = 0

def _set_animation(animation:CAnimation, num_anim:int):
    if animation.current_animation == num_anim:
        return
    animation.current_animation = num_anim
    animation.current_animation_time = 0
    animation.current_frame = animation.animation_list[animation.current_animation].start

def _calculate_distance(pos1, pos2):
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    return math.sqrt(dx * dx + dy * dy)

def _calculate_direction(pos1, pos2):
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    magnitude = math.sqrt(dx * dx + dy * dy)
    
    if magnitude == 0:
        return (0, 0)
    
    return pygame.Vector2(dx / magnitude, dy / magnitude)