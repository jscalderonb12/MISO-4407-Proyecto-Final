import esper
import pygame

from src.ecs.components.tags.c_tag_text import CTagText

def system_deleting_init_texts(world:esper.World, total_time:float, texts:list):
    components = world.get_components(CTagText)

    for _, (_,) in components:
        if total_time > 4.0:
            for text in texts:
                world.delete_entity(text)
            texts = []
        
    return texts