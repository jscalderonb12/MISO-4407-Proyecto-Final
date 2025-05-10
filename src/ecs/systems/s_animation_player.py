import esper

from enum import Enum
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_animation_player import CAnimationPlayer

class PlayerPosition(Enum):
    UP = 0
    DOWN = 16
    LEFT = 8
    RIGHT = 24
    LEFT_UP = 4
    RIGHT_UP = 28
    DOWN_LEFT = 12
    DOWN_RIGHT = 20

    @staticmethod
    def has_key(key):
        return key in PlayerPosition.__members__

def system_animation_player(world:esper.World, player_movement:str, delta_time:float):
    components = world.get_components(CSurface, CAnimationPlayer)
    for _, (surface, animation) in components:
        animation.current_animation_time -= delta_time

        if animation.current_animation_time <= 0:
            animation.current_animation_time = animation.framerate

            if player_movement != "IDLE" and PlayerPosition.has_key(player_movement):
                target_frame = PlayerPosition[player_movement].value
                total_frames = animation.number_frames
                current = animation.current_frame

                diff = (target_frame - current) % total_frames
                if diff != 0:
                    if diff > total_frames / 2:
                        animation.current_frame = (current - 1) % total_frames
                    else:
                        animation.current_frame = (current + 1) % total_frames

        rect_surf = surface.surf.get_rect()
        surface.area.w = rect_surf.w / animation.number_frames
        surface.area.x = animation.current_frame * surface.area.w