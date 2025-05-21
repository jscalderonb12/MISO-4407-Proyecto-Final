# src/ecs/systems/system_chaser_shoot.py

import pygame
from pygame.math import Vector2
from esper import World
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_shooter import CShooter
from src.create.prefab_creator import create_bullet  # tu función existente

def system_enemy_shoot(world: World, delta_time: float, bullets_cfg: dict):
    """
    Hace que cada chaser con CShooter dispare hacia su dirección
    cada CShooter.fire_rate segundos.
    """
    for ent, (shooter, trans, rot) in world.get_components(CShooter, CTransform, CRotation):
        # acumula tiempo
        shooter.time_since_last += delta_time
        if shooter.time_since_last < shooter.fire_rate:
            continue

        # reinicia y dispara
        shooter.reset_timer()

        # posición de spawn de la bala (puedes ajustar offset)
        bullet_pos = trans.pos.copy()
        # dirección exacta del rot
        direction = rot.direction  

        # crea tu bala usando tu prefab actual
        create_bullet(world, bullet_pos, bullets_cfg, direction)
