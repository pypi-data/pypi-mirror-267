import pyray as pr
import numpy as np

from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.physic.entity import Entity
from spacerescue.resources import GLOBAL_RESOURCES


class Asteroid(Entity):

    MASS = 1e14  # kg
    ANGULAR_VELOCITY = 1  # r⋅s−1
    RADIUS = 1e6  # m

    def __init__(self, galaxy: Universe, position: np.ndarray):
        super().__init__(
            mass=Asteroid.MASS,
            radius=Asteroid.RADIUS,
            position=position,
        )
        self.galaxy = galaxy
        self.angle = np.random.random() * np.pi
        self.angular_velocity = Asteroid.ANGULAR_VELOCITY
        self.model = GLOBAL_RESOURCES.load_model("asteroid")
        self.model.materials[0].shader = GLOBAL_RESOURCES.load_shader("shader_lighting")

    def update(self, dt):
        self.angle += self.angular_velocity * dt
        super().update(dt)

    def draw(self, camera: Camera):
        if camera.get_lod(self) > 0:
            self.model.transform = pr.matrix_rotate_xyz(
                pr.Vector3(*(self.angle, self.angle, self.angle))
            )
            position, size = self.galaxy.mapper.transform_entity(self)
            pr.draw_model(self.model, position, size.x, pr.WHITE)  # type: ignore
