import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, PlayerState

def system_player_state(world:esper.World):
    components = world.get_components(CInputCommand, CAnimation, CPlayerState)
    
    for _, (inputCommand, animation, player_state) in components:
        if player_state.state == PlayerState.IDLE:
            _do_idle_state(inputCommand, animation, player_state)
        else:
            _do_move_state(inputCommand, animation, player_state)

def _do_idle_state(inputCommand:CInputCommand, animation:CAnimation, player_state:CPlayerState):
    _set_animation(animation, 1)
    if inputCommand.phase == CommandPhase.START:
        player_state.state = PlayerState.MOVE


def _do_move_state(inputCommand:CInputCommand, animation:CAnimation, player_state:CPlayerState):
    _set_animation(animation, 0)
    if inputCommand.phase == CommandPhase.END:
        player_state.state = PlayerState.IDLE

def _set_animation(animation:CAnimation, num_anim:int):
    if animation.current_animation == num_anim:
        return
    animation.current_animation = num_anim
    animation.current_animation_time = 0
    animation.current_frame = animation.animation_list[animation.current_animation].start