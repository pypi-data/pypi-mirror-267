import pyray as pr
import numpy as np

from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.tools.name_generator import NameGenerator
from spacerescue.core.math import ndarray_to_vector3, normalize
from spacerescue.physic.entity import Entity


class HyperspacePortal(Entity):
    
    VELOCITY = 1e-6 # r⋅s−1
    PORTALS_MASS = 0.0001 # kg
    RADIUS = 2e7 # m
    
    def __init__(
        self,
        galaxy: Universe,
        position: np.ndarray,
        star: Entity,
    ):
        super().__init__(
            mass=HyperspacePortal.PORTALS_MASS,
            radius=HyperspacePortal.RADIUS,
            position=position,
            spin_axis=star.spin_axis,
            parent=star,
        )
        self.galaxy = galaxy
        self.name = NameGenerator.get_instance().generate_object_name()
        self.angle = np.random.random() * np.pi
        self.angular_velocity = HyperspacePortal.VELOCITY
        self.heading = normalize(self.parent.position - self.position) if self.parent is not None else np.zeros(3)
        self.model = GLOBAL_RESOURCES.load_model("wormhole")

    def update(self, dt):
        self.angle += self.angular_velocity * dt
        super().update(dt)

    def draw(self, camera: Camera):
        if camera.get_lod(self) > 0:
            self.model.transform = pr.matrix_multiply(
                pr.matrix_rotate_z(self.angle),
                pr.matrix_invert(
                    pr.matrix_look_at(
                        pr.vector3_zero(),
                        ndarray_to_vector3(self.heading),
                        ndarray_to_vector3(self.spin_axis),
                    )
                ),
            )
            position, size = self.galaxy.mapper.transform_entity(self)
            pr.draw_model(self.model, position, size.x, pr.WHITE)  # type: ignore
