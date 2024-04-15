import pyray as pr
import numpy as np

from spacerescue.physic.entity import Entity


class Mapper:
    """interface"""
    
    def transform_radius(self, radius: float) -> pr.Vector3:
        raise NotImplementedError

    def transform_position(self, position: np.ndarray) -> pr.Vector3:
        raise NotImplementedError

    def transform_entity(self, entity: Entity) -> tuple[pr.Vector3, pr.Vector3]:
        raise NotImplementedError
    
    def transform_bound(self, bound: np.ndarray) -> tuple[pr.Vector3, pr.Vector3]:
        raise NotImplementedError