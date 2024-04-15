import pyray as pr

from spacerescue.physic.entity import Entity
from spacerescue.core.math import ndarray_to_vector3
from spacerescue.physic.universe import Universe
from spacerescue.gameplay.cameras.camera_galaxy import CameraGalaxy

class CameraEntity(CameraGalaxy):

    def __init__(self, galaxy: Universe, entity: Entity):
        super().__init__(entity.position)
        self.galaxy = galaxy
        self.entity = entity
        self.camera.position, _ = self.galaxy.mapper.transform_entity(self.entity)
        self.camera.target = pr.vector3_add(
            self.camera.position, ndarray_to_vector3(entity.heading)
        )
 
    def update(self, dt: float):
        camera_position, _ = self.galaxy.mapper.transform_entity(self.entity)
        camera_target = pr.vector3_add(
            camera_position, ndarray_to_vector3(self.entity.heading)
        )
        self.camera.position = camera_position
        self.camera.target = camera_target
        self.camera.up = ndarray_to_vector3(self.entity.spin_axis)
        
        self.position = self.entity.position
        super().update(dt)
