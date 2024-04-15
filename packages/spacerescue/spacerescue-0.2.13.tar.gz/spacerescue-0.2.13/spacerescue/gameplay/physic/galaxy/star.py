import pyray as pr
import numpy as np

from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.physic.entity import Entity
from spacerescue.tools.name_generator import NameGenerator


class Star(Entity):

    ANGULAR_VELOCITY = 2e-7 # r⋅s−1   # sun like
    MASS = 1.99e30 # kg               # sun like
    RADIUS = 6.96e8 # m               # sun like
    BLOOM_RATIO = 500
    
    def __init__(
        self,
        galaxy: Universe,
        spin_axis: np.ndarray,
        position: np.ndarray,
        color: pr.Color,
    ):
        super().__init__(
            mass=Star.MASS,
            radius=Star.RADIUS,
            position=position,
            spin_axis=spin_axis
        )
        self.galaxy=galaxy
        self.name = NameGenerator.get_instance().generate_object_name()
        self.color = color
        self.angle = np.random.random() * np.pi
        self.angular_velocity = Star.ANGULAR_VELOCITY
        self.model = GLOBAL_RESOURCES.load_model("sun")

    def update(self, dt):
        self.angle += self.angular_velocity * dt
        super().update(dt)

    def draw(self, camera: Camera):
        if camera.get_lod(self) > 0:
            self.model.transform = pr.matrix_rotate(pr.Vector3(*self.spin_axis), self.angle)
            position, size = self.galaxy.mapper.transform_entity(self)
            pr.draw_model(self.model, position, size.x, pr.WHITE)  # type: ignore
        else:
            self.model.transform = pr.matrix_identity()
            position, size = self.galaxy.mapper.transform_entity(self)
            pr.draw_sphere(position, size.x * Star.BLOOM_RATIO, pr.WHITE)  # type: ignore