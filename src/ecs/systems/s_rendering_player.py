from esper import World
from pygame import Surface

from src.ecs.components.tags.c_tag_hidden_player import CTagHiddenPlayer
from src.ecs.components.tags.c_tag_winner import CTagWinner
from src.ecs.components.c_timeout import CTimeout

def system_rendering_player(world:World, delta_time:float, switch_scene, start_game_text_update):
    components = world.get_components(CTimeout, CTagHiddenPlayer)

    timeout:CTimeout
    for ent, (timeout, _) in components:
        timeout.remaining -= delta_time

        if timeout.remaining <= 0:
            start_game_text_update(["PLAYER 1", "READY"])
            world.remove_component(ent, CTimeout)
            world.remove_component(ent, CTagHiddenPlayer)
            if world.has_component(ent, CTagWinner):
                switch_scene("WIN_SCENE")
            else:
                switch_scene("LEVEL_01_SCENE")
            world.remove_component(ent, CTagWinner)