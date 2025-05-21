from esper import World
from pygame import Surface

from src.ecs.components.tags.c_tag_hidden import CTagHidden
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_pause import CTagPause

def system_pause_game(world:World, is_pausing:bool):

    if is_pausing:
        for ent, _ in world.get_component(CTagPlayer):
            world.add_component(ent, CTagHidden())
            world.add_component(ent, CTagPause())

        for ent, _ in world.get_component(CTagEnemy):
            world.add_component(ent, CTagHidden())
            world.add_component(ent, CTagPause())

        for ent, _ in world.get_component(CTagBullet):
            world.add_component(ent, CTagHidden())
            world.add_component(ent, CTagPause())

        for ent, _ in world.get_component(CTagCloud):
            world.add_component(ent, CTagPause())
    else:
        for ent, _ in world.get_component(CTagHidden):
            world.remove_component(ent, CTagHidden)
        for ent, _ in world.get_component(CTagPause):
            world.remove_component(ent, CTagPause)