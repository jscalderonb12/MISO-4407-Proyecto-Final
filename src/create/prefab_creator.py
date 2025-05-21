import math
import random
import esper
import pygame

from src.ecs.components.c_animation_enemy import CAnimationEnemy
from src.ecs.components.c_explosion_timer import CExplosionTimer
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
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_cloud_spawner import CCloudSpawner
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

def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_sprite = ServiceLocator.images_service.get(explosion_info["image"])
    
    
    explosion_entity = create_sprite(world, pos, pygame.Vector2(0,0), explosion_sprite)
    world.add_component(explosion_entity, CAnimation(explosion_info["animations"]))
    world.add_component(explosion_entity, CExplosionTimer(duration=0.5))
    world.add_component(explosion_entity, CTagExplosion())
    ServiceLocator.sounds_service.play(explosion_info["sound"])

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

def create_cloud(world:esper.World, level_config:dict, clouds_config:dict, is_cloud_large:bool):
    for clouds_spawn_event in level_config["cloud_spawn_events"]:
        if (is_cloud_large and clouds_spawn_event["type"] == "CloudLarge") or (not is_cloud_large and clouds_spawn_event["type"] != "CloudLarge"):
            cloud_pos = pygame.Vector2(clouds_spawn_event["position"]["x"], clouds_spawn_event["position"]["y"])
            cloud_config = clouds_config[clouds_spawn_event["type"]]
            cloud_sprite = pygame.image.load(cloud_config["image"]).convert_alpha()
            size = cloud_sprite.get_size()
            size = (size[0] / cloud_config["animations"]["number_frames"], size[1])
            vel = pygame.Vector2(cloud_config["velocity"], cloud_config["velocity"])

            cloud_entity = create_sprite(world = world, pos = cloud_pos, vel = vel, surf = cloud_sprite)
            world.add_component(
                cloud_entity,
                CAnimation(cloud_config["animations"])
            )
            world.add_component(
                cloud_entity,
                CTagCloud()
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
    input_pause = world.create_entity()

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
    world.add_component(input_pause, CInputCommand(name="PAUSE", key=pygame.K_p))

def create_enemy_single(world: esper.World, pos: pygame.Vector2, cfg: dict, player_pos: pygame.Vector2 = None):
    """
    Crea un enemigo individual que aparece apuntando al jugador.
    """
    surf = ServiceLocator.images_service.get(cfg["sprite_sheet"])
    vel_mag = random.uniform(cfg.get("velocity_min", 0), cfg.get("velocity_max", 0))
    # Dirección hacia el jugador
    if player_pos:
        direction = (player_pos - pos).normalize()
    else:
        direction = pygame.Vector2(1, 0)
    entity = create_sprite(world, pos, direction * vel_mag, surf)
    world.add_component(entity, CTagEnemy())
    world.add_component(entity, CRotation(math.atan2(direction.y, direction.x)))
    # Animación direccional si tiene múltiples frames
    if cfg.get("frame_count", 1) > 1:
        anim_cfg = {
            "number_frames": cfg["frame_count"],
            "framerate": cfg.get("framerate", 12),
            "initial_frame": 0
        }
        world.add_component(entity, CAnimationEnemy(anim_cfg))
    return entity


def create_enemy_squadron(world: esper.World, pos: pygame.Vector2, cfg: dict, enemy_types: dict, player_pos: pygame.Vector2):
    """
    Crea un escuadrón en formación de flecha de 4 a 6 enemigos,
    apuntando hacia player_pos al momento del spawn.
    """
    ServiceLocator.sounds_service.play("assets/snd/enemy_launch.ogg")
    squad = []
    prob = cfg.get("chaser_probability", 0.0)
    # Base de dirección hacia el jugador
    if player_pos:
        base_dir = (player_pos - pos).normalize()
    else:
        base_dir = pygame.Vector2(1, 0)
    # Vector perpendicular para alas de la flecha
    perp = pygame.Vector2(-base_dir.y, base_dir.x)
    # Espaciado configurable (más amplio por defecto)
    spacing = cfg.get("spacing", random.randint(5, 30))

    # Offset base para 6 posiciones en flecha
    base_offsets = [
        base_dir * spacing,
        -(base_dir * spacing) + (perp * spacing),
        -(base_dir * spacing) - (perp * spacing),
        -(base_dir * 2 * spacing),
        -(base_dir * 3 * spacing) + (perp * 2 * spacing),
        -(base_dir * 3 * spacing) - (perp * 2 * spacing)
    ]
    # Número aleatorio de enemigos entre 4 y 6
    count = random.randint(3, 6)
    offsets = base_offsets[:count]

    # Velocidad constante para la formación
    vel_mag = random.uniform(cfg.get("velocity_min", 0), cfg.get("velocity_max", 0))
    for offset in offsets:
        spawn_pos = pos + offset
        # Crear cada enemigo en esa posición
        eid:int
        if random.random() < prob:
            chaser_cfg = enemy_types.get("YellowChaser")
            eid = create_enemy_single(world, spawn_pos, cfg, player_pos)
            world.add_component(eid, CTagChaseEnemy())
            world.add_component(eid, CEnemyState(
                velocity_chase=chaser_cfg["velocity_chase"],
                velocity_return=chaser_cfg["velocity_return"],
                distance_start_chase=chaser_cfg["distance_start_chase"],
                distance_start_return=chaser_cfg["distance_start_return"]
            ))
            if random.random() < cfg.get("shoot_probability", 0.0):
                world.add_component(
                    eid,
                    CShooter(
                        fire_rate=cfg["shoot_rate"],
                        bullet_speed=cfg["bullet_speed"]
                    )
                )
        else:
            eid = create_enemy_single(world, spawn_pos, cfg, player_pos)
        # Ajustar su velocidad hacia el jugador
        vel_comp = world.component_for_entity(eid, CVelocity)
        vel_comp.vel = base_dir * vel_mag
        squad.append(eid)
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
    if random.random() < cfg.get("shoot_probability", 0.0):
        world.add_component(
            entity,
            CShooter(
                fire_rate=cfg["shoot_rate"],
                bullet_speed=cfg["bullet_speed"]
            )
        )
    world.add_component(entity, CRotation(math.atan2(vec.y, vec.x)))
    world.add_component(entity, CVelocity(pygame.Vector2(cfg["velocity_chase"],cfg["velocity_chase"])))
    return entity


def create_enemy_shooter(world: esper.World, pos: pygame.Vector2, cfg: dict, player_pos: pygame.Vector2):
    """
    Crea un enemigo que dispara desde posición fija apuntando al jugador.
    """
    surf = ServiceLocator.images_service.get(cfg["sprite_sheet"])
    speed = cfg.get("velocity", 0)
    # Dirección hacia el jugador
    if player_pos:
        direction = (player_pos - pos).normalize()
    else:
        direction = pygame.Vector2(1, 0)
    entity = create_sprite(world, pos, direction * speed, surf)
    world.add_component(entity, CTagEnemy())
    world.add_component(entity, CShooter(
        fire_rate=cfg["fire_rate"],
        bullet_speed=cfg["bullet_speed"],
        time_since_last=0.0
    ))
    world.add_component(entity, CRotation(math.atan2(direction.y, direction.x)))
    return entity


