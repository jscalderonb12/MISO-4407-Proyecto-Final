class CEnemySpawner:
    def __init__(self, levels:dict):
        self.spawn_events:list = levels["enemy_spawn_events"]
        for spawn_event in self.spawn_events:
            spawn_event["trigger"] = True
