from enum import Enum
import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator
from src.ecs.components.tags.c_tag_text import CTagText
from src.ecs.components.c_text_blink import CTextBlink

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int, color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    world.add_component(text_entity,
                        CTagText())
    return text_entity

def create_blinking_text(world: esper.World, txt: str, size: int, color: pygame.Color,pos: pygame.Vector2, alignment: TextAlignment, interval: float = 0.5) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    surface = CSurface.from_text(txt, font, color)
    surface.visible = True 
    world.add_component(text_entity, surface)

    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= surface.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= surface.area.centerx

    world.add_component(text_entity, CTransform(pos + origin))
    world.add_component(text_entity, CTagText())
    world.add_component(text_entity, CTextBlink(interval=interval))

    return text_entity


def update_text(world: esper.World, entity_id: int, new_text: str):
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)

    surf = world.component_for_entity(entity_id, CSurface)
    transform = world.component_for_entity(entity_id, CTransform)
    color = surf.color
    
    new_surf = CSurface.from_text(new_text, font, color)
    surf.surf = new_surf.surf
    surf.area = new_surf.area