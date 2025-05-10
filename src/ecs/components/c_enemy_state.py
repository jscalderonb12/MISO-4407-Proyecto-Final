from enum import Enum

class CEnemyState:
    def __init__(self, velocity_chase:int, velocity_return:int, distance_start_chase:int, distance_start_return:int):
        self.state = EnemyState.IDLE
        self.velocity_chase = velocity_chase
        self.velocity_return = velocity_return
        self.distance_start_chase = distance_start_chase
        self.distance_start_return = distance_start_return
        self.position_return = None

class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
    BACK = 2