import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_animation import CAnimation

def system_animation(world:esper.World, delta_time:float):
    components = world.get_components(CSurface, CAnimation)
    for _, (surface, animation) in components:
        animation.current_animation_time -= delta_time
        
        if animation.current_animation_time <= 0:
            animation.current_animation_time = animation.animation_list[animation.current_animation].framerate
            animation.current_frame += 1

            if animation.current_frame > animation.animation_list[animation.current_animation].end:
                if animation.animation_list[0].name != "EXPLODE":
                    animation.current_frame = animation.animation_list[animation.current_animation].start

            rect_surf = surface.surf.get_rect()
            surface.area.w = rect_surf.w / animation.number_frames
            surface.area.x = animation.current_frame * surface.area.w