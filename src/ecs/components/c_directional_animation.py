from pygame import Surface
from typing import List

class CDirectionalAnimation:
    """Guarda los frames direccionales de un sprite-sheet."""
    def __init__(self, frames: List):      
        frames: List[Surface]
