class CAnimationPlayer:
    def __init__(self, animations:dict):
        self.number_frames = animations["number_frames"]
        self.framerate = 1.0 / animations["framerate"]
        self.current_animation_time = 0
        self.current_frame = animations["initial_frame"]