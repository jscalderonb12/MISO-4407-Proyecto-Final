from enum import Enum

class CEnemyState:
    def __init__(self, velocity_chase:int, velocity_return:int, distance_start_chase:int, distance_start_return:int, shot_live:int = 1, type:str = "default"):
        self.state = EnemyState.IDLE
        self.velocity_chase = velocity_chase
        self.velocity_return = velocity_return
        self.distance_start_chase = distance_start_chase
        self.distance_start_return = distance_start_return
        self.position_return = None
        self.shot_live = shot_live
        self.type = type

class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    BACK = 2