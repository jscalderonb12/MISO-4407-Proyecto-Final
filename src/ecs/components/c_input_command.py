from enum import Enum

class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2
    HOLD = 3

class CInputCommand:
    def __init__(self, name:str, key:int):
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        self.pos = None