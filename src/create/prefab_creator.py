import math
import random
import esper
import pygame

from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_cloud_spawner import CCloudSpawner

def create_sprite(world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, surf:pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(
        sprite_entity, 
        CSurface.from_surface(surf=surf)
    )
    world.add_component(
        sprite_entity, 
        CTransform(pos=pos)
    )
    world.add_component(
        sprite_entity, 
        CVelocity(vel=vel)
    )

    return sprite_entity

def create_player(world:esper.World, player_config:dict, game_rect:pygame.Rect) -> int:
    player_sprite = pygame.image.load(player_config["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_config["animations"]["number_frames"], size[1])
    pos = pygame.Vector2((game_rect.width / 2) - (size[0] / 2), (game_rect.height / 2) + game_rect.top - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    dir = pygame.Vector2(1, 1)

    player_entity = create_sprite(world = world, pos = pos, vel = vel, surf = player_sprite)
    world.add_component(
        player_entity,
        CTagPlayer()
    )

    world.add_component(
        player_entity,
        CAnimationPlayer(player_config["animations"])
    )

    world.add_component(
        player_entity,
        CPlayerState()
    )

    world.add_component(
        player_entity,
        CRotation(direction=dir)
    )

    return player_entity

def create_cloud(world:esper.World, cloud_config:dict, game_rect:pygame.Rect):
    cloud_sprite = pygame.image.load(cloud_config["image"]).convert_alpha()
    size = cloud_sprite.get_size()
    size = (size[0] / cloud_config["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(random.randint(game_rect.left, game_rect.right - size[0]), random.randint(game_rect.top, game_rect.bottom - size[1]))
    vel = pygame.Vector2(0, 0)

    cloud_entity = create_sprite(world = world, pos = pos, vel = vel, surf = cloud_sprite)
    world.add_component(
        cloud_entity,
        CAnimation(cloud_config["animations"])
    )

def create_cloud_spawner(world:esper.World, level_data:dict):
    cloud_spawner_entity = world.create_entity()
    world.add_component(
        cloud_spawner_entity, 
        CCloudSpawner(levels=level_data)
    )

def create_bullet(world:esper.World, pos:pygame.Vector2, bullet_data:dict, direction:pygame.Vector2):
    bullet_surface = pygame.image.load(bullet_data["image"]).convert_alpha()
    bullet_surface = pygame.transform.scale(bullet_surface, (8, 8))
    bullet_size = bullet_surface.get_rect().size
    pos.x -= bullet_size[0] / 2
    pos.y -= bullet_size[1] / 2

    vel = direction.normalize() * bullet_data["velocity"]

    bullet_entity = create_sprite(world = world, surf = bullet_surface, pos = pos, vel = vel)
    world.add_component(
        bullet_entity,
        CTagBullet()
    )

    return bullet_entity


def create_input_player(world:esper.World):
    input_left_arrow = world.create_entity()
    input_right_arrow = world.create_entity()
    input_up_arrow = world.create_entity()
    input_down_arrow = world.create_entity()
    input_left_wasd = world.create_entity()
    input_right_wasd = world.create_entity()
    input_up_wasd = world.create_entity()
    input_down_wasd = world.create_entity()
    input_start_game = world.create_entity()
    input_fire = world.create_entity()

    world.add_component(input_left_arrow, CInputCommand(name="PLAYER_LEFT", key=pygame.K_LEFT))
    world.add_component(input_right_arrow, CInputCommand(name="PLAYER_RIGHT", key=pygame.K_RIGHT))
    world.add_component(input_up_arrow, CInputCommand(name="PLAYER_UP", key=pygame.K_UP))
    world.add_component(input_down_arrow, CInputCommand(name="PLAYER_DOWN", key=pygame.K_DOWN))
    world.add_component(input_left_wasd, CInputCommand(name="PLAYER_LEFT", key=pygame.K_a))
    world.add_component(input_right_wasd, CInputCommand(name="PLAYER_RIGHT", key=pygame.K_d))
    world.add_component(input_up_wasd, CInputCommand(name="PLAYER_UP", key=pygame.K_w))
    world.add_component(input_down_wasd, CInputCommand(name="PLAYER_DOWN", key=pygame.K_s))
    world.add_component(input_start_game, CInputCommand(name="START_GAME", key=pygame.K_RETURN))
    world.add_component(input_fire, CInputCommand(name="PLAYER_FIRE", key=pygame.BUTTON_LEFT))
    world.add_component(input_fire, CInputCommand(name="PLAYER_FIRE", key=pygame.K_f))

