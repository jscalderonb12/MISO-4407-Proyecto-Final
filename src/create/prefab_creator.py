import math
import random
import esper
import pygame

from src.ecs.components.c_animation_enemy import CAnimationEnemy
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_shooter import CShooter
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.tags.c_tag_chase_enemy import CTagChaseEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_state import CEnemyState
from src.engine.service_locator import ServiceLocator

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

def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data))

def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict, enemy_type: str):
    if enemy_type == "Hunter":
        create_ia_enemy(world, pos, enemy_info)
    else:
        enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
        vel_max = enemy_info["velocity_max"]
        vel_min = enemy_info["velocity_min"]
        vel_range_x = vel_min + (random.random() * (vel_max - vel_min))
        vel_range_y = vel_min + (random.random() * (vel_max - vel_min))
        velocity = pygame.Vector2(
            random.choice([-vel_range_x, vel_range_x]),
            random.choice([-vel_range_y, vel_range_y]),
        )
        enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
        world.add_component(enemy_entity, CTagEnemy())
        ServiceLocator.sounds_service.play(enemy_info["sound"])

def create_ia_enemy(world, pos, enemy_info):
    enemy_sprite = ServiceLocator.images_service.get(enemy_info["image"])

    # Obtener tamaño de frame individual del sprite animado
    total_frames = enemy_info["animations"]["number_frames"]
    size = enemy_sprite.get_size()
    size = (size[0] / total_frames, size[1])

    # Posición ajustada al centro del sprite
    pos = pygame.Vector2(pos.x - (size[0] / 2), pos.y - (size[1] / 2))

    velocity = pygame.Vector2(0, 0)  # empieza quieto

    enemy_entity = create_sprite(world, pos, velocity, enemy_sprite)
    world.add_component(enemy_entity, CTagEnemy())
    world.add_component(enemy_entity, CTagChaseEnemy())
    world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CEnemyState(
        velocity_chase= enemy_info["velocity_chase"],
        velocity_return= enemy_info["velocity_return"],
        distance_start_chase= enemy_info["distance_start_chase"],
        distance_start_return= enemy_info["distance_start_return"]
    ))
    # world.add_component(enemy_entity, COriginEnemy(pos.copy()))

def create_player(world:esper.World, player_config:dict, game_rect:pygame.Rect) -> int:
    player_sprite = pygame.image.load(player_config["image"]).convert_alpha()
    size = player_sprite.get_size()
    size = (size[0] / player_config["animations"]["number_frames"], size[1])
    pos = pygame.Vector2((game_rect.width / 2) - (size[0] / 2), (game_rect.height / 2) + game_rect.top - (size[1] / 2))
    vel = pygame.Vector2(player_config["input_velocity"], player_config["input_velocity"])
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

def create_enemy_single(world: esper.World, pos: pygame.Vector2, cfg: dict):
    """
    Crea un enemigo que aparece solo (tipo 'single').
    """
    surf = ServiceLocator.images_service.get(cfg["sprite_sheet"])
    vel = random.uniform(cfg.get("velocity_min", 0), cfg.get("velocity_max", 0))
    angle_deg = cfg.get("spawn_angle_deg", random.choice([0, 90, 180, 270]))
    rad = math.radians(angle_deg)
    direction = pygame.Vector2(math.cos(rad), math.sin(rad))
    entity = create_sprite(world, pos, direction * vel, surf)
    world.add_component(entity, CTagEnemy())
    # animation: static frame or directional
    if cfg.get("frame_count", 1) > 1:
        anim_cfg = {"number_frames": cfg["frame_count"], "framerate": cfg.get("framerate", 12), "initial_frame": int(angle_deg / 360 * cfg["frame_count"]) }
        world.add_component(entity, CAnimationEnemy(anim_cfg))
    return entity


def create_enemy_squadron(world: esper.World, pos: pygame.Vector2, cfg: dict):
    """
    Crea un escuadrón de enemigos (tipo 'squadron').
    """
    squad = []
    size = cfg.get("squad_size", 1)
    for _ in range(size):
        offset = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
        squad.append(create_enemy_single(world, pos + offset, cfg))
    return squad


def create_enemy_chaser(world: esper.World, pos: pygame.Vector2, cfg: dict, player_pos: pygame.Vector2):
    """
    Crea un enemigo que persigue al jugador.
    """
    surf = ServiceLocator.images_service.get(cfg["sprite_sheet"])
    vec = (player_pos - pos).normalize()
    entity = create_sprite(world, pos, pygame.Vector2(0,0), surf)
    world.add_component(entity, CTagEnemy())
    world.add_component(entity, CTagChaseEnemy())
    world.add_component(entity, CAnimationEnemy(cfg.get("animations", {})))
    world.add_component(entity, CEnemyState(
        velocity_chase=cfg["velocity_chase"],
        velocity_return=cfg["velocity_return"],
        distance_start_chase=cfg["distance_start_chase"],
        distance_start_return=cfg["distance_start_return"]
    ))
    world.add_component(entity, CRotation(math.atan2(vec.y, vec.x)))
    world.add_component(entity, CVelocity(pygame.Vector2(cfg["velocity_chase"],cfg["velocity_chase"])))
    return entity


def create_enemy_shooter(world: esper.World, pos: pygame.Vector2, cfg: dict):
    """
    Crea un enemigo que dispara desde posición fija.
    """
    surf = ServiceLocator.images_service.get(cfg["sprite_sheet"])
    speed = cfg.get("velocity", 0)
    angle_deg = cfg.get("spawn_angle_deg", random.choice([0, 90, 180, 270]))
    rad = math.radians(angle_deg)
    direction = pygame.Vector2(math.cos(rad), math.sin(rad))
    entity = create_sprite(world, pos, direction * speed, surf)
    world.add_component(entity, CTagEnemy())
    world.add_component(entity, CShooter(
        fire_rate=cfg["fire_rate"],
        bullet_speed=cfg["bullet_speed"],
        time_since_last=0.0
    ))
    world.add_component(entity, CRotation(rad))
    return entity


