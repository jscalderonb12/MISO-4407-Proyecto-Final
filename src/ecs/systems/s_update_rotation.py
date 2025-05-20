
import math

from esper import World
import pygame

from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_update_rotation(world:World):
    query = world.get_components(CAnimationPlayer, CRotation, CTagPlayer)
    
    for _, components in query:
        c_a: CAnimationPlayer = components[0]
        c_r: CRotation = components[1]

        sprite_angle = (c_a.current_frame * 11.25) - 90
        rad_angle = math.radians(sprite_angle)
        c_r.angle = rad_angle
        c_r.direction = pygame.Vector2(-math.cos(rad_angle), math.sin(rad_angle))
