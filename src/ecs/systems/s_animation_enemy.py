import math
from esper import World
from src.ecs.components.c_animation_enemy import CAnimationEnemy
from src.ecs.components.c_animation_player import CAnimationPlayer
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity


def system_enemy_animation(world: World, delta_time: float):
    """
    Ajusta current_frame de CAnimationEnemy según la dirección de CVelocity,
    mapea el ángulo de movimiento al índice de frame.
    Se incluyen prints para depurar ángulos y cálculos.
    """
    for ent, (anim, vel, surf) in world.get_components(
            CAnimationEnemy, CVelocity, CSurface):
        vec = vel.vel
        # Saltar si no hay movimiento
        if vec.length_squared() == 0:
            continue

        # Calcular ángulo de movimiento en grados [0,360)
        angle_rad = math.atan2(-vec.y, vec.x)
        angle_deg = math.degrees(angle_rad)
        if angle_deg < 0:
            angle_deg += 360

        # Parámetros de la animación
        N = anim.number_frames
        step = 360.0 / N

        # Computar índice crudo relativo a 90°
        raw = (angle_deg - 90.0) / step
        idx0 = math.floor(raw + 0.5)
        frame_idx = idx0 % N

        # Aplicar frame
        anim.current_frame = frame_idx

        # Ajustar área de sprite para el frame actual
        frame_w = surf.surf.get_width() // N
        surf.area.x = frame_idx * frame_w
        surf.area.w = frame_w
        surf.area.h = surf.surf.get_height()