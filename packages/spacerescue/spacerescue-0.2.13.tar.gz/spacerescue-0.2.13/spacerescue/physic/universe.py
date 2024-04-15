from spacerescue.physic.laws import Laws
from spacerescue.physic.mapper import Mapper
from spacerescue.render.camera import Camera


class Universe:
    """interface"""

    def __init__(self, laws: Laws, mapper: Mapper):
        self.laws = laws
        self.mapper = mapper
        
    def update(self, dt: float):
        raise NotImplementedError
    
    def draw(self, camera: Camera):
        raise NotImplementedError
