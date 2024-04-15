import pyray as pr

from spacerescue.render.camera import Camera


class Widget:
    
    def __init__(self, id: str, bound: pr.Rectangle):
        self.id = id
        self.bound = bound
        
    def update(self):
        pass
    
    def draw(self, camera: Camera | None = None):
        pass
    