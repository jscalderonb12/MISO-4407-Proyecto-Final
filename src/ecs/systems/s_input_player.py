from typing import Callable
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase

def system_input_player(world:esper.World, event:pygame.event.Event, do_action:Callable[[CInputCommand], None]):
    components = world.get_components(CInputCommand)

    input_command:CInputCommand
    for _, (input_command,) in components:
        if event.type == pygame.KEYDOWN and event.key == input_command.key:
            input_command.phase = CommandPhase.START
            do_action(input_command)
        if event.type == pygame.KEYUP and event.key == input_command.key:
            input_command.phase = CommandPhase.END
            do_action(input_command)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == input_command.key:
            input_command.phase = CommandPhase.START
            input_command.pos = pygame.Vector2(event.pos)
            do_action(input_command)