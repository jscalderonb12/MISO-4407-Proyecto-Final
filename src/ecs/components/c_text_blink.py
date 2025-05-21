class CTextBlink:
    def __init__(self, visible:bool = True, last_toggle:int = 0, interval:int = 500):
        self.visible = visible
        self.last_toggle = last_toggle
        self.interval = interval