from esper import World
from pygame import Surface

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_text_blink import CTextBlink

def system_text_blink(world:World, screen:Surface, total_time:float):
    components = world.get_components(CTextBlink, CSurface)

    textblink:CTextBlink
    surface:CSurface
    for _, (textblink, surface) in components:
        if total_time - textblink.last_toggle >= textblink.interval:
            textblink.visible = not textblink.visible
            textblink.last_toggle = total_time

        surface.visible = textblink.visible