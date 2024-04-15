import pyray as pr

from spacerescue.physic.entity import Entity
from spacerescue.core.math import EPSILON, ndarray_to_vector3
from spacerescue.physic.universe import Universe
from spacerescue.gameplay.cameras.camera_galaxy import CameraGalaxy

class CameraFollower(CameraGalaxy):
    
    K = 1e3  # N

    def __init__(self, galaxy: Universe, entity: Entity, length: float):
        super().__init__(entity.position)
        self.galaxy = galaxy
        self.entity = entity
        self.length = length
        self.velocity = pr.vector3_zero()
        self.camera.target,_ = self.galaxy.mapper.transform_entity(self.entity)
        self.camera.position = pr.vector3_add(self.camera.target, ndarray_to_vector3(-self.entity.heading * self.length))

    def update(self, dt: float):
        camera_target, _ = self.galaxy.mapper.transform_entity(self.entity)
        # camera_position = pr.vector3_add(camera_target, ndarray_to_vector3(-self.entity.heading * self.length))
        
        force = self._get_tension_force(dt)
        force = pr.vector3_add(
            force, pr.vector3_scale(self.velocity, -1.0 / (dt + EPSILON))
        )
        self.velocity = pr.vector3_add(self.velocity, pr.vector3_scale(force, dt / 1.0))
        camera_position = pr.vector3_add(
            self.camera.position, pr.vector3_scale(self.velocity, dt)
        )
        
        self.camera.target = camera_target
        self.camera.position = camera_position
        self.position = self.entity.position
        super().update(dt)
        
    def _get_tension_force(self, dt: float):
        v = pr.vector3_subtract(self.camera.position, self.camera.target)
        l = pr.vector3_length(v) - self.length
        return pr.vector3_scale(pr.vector3_normalize(v), -CameraFollower.K * l)
