import pyray as pr
import numpy as np

from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.tools.name_generator import NameGenerator
from spacerescue.physic.entity import Entity


class Planet(Entity):
    
    ANGULAR_VELOCITY = 7.29e-7 # r⋅s−1   # earth like
    
    def __init__(
        self,
        galaxy: Universe,
        mass: float,
        radius: float,
        position: np.ndarray,
        velocity: np.ndarray,
        model: str,
        star: Entity,
        is_habitable: bool
    ):
        super().__init__(
            mass=mass,
            radius=radius,
            position=position,
            velocity=velocity,
            spin_axis=star.spin_axis,
            parent=star,
        )
        self.galaxy = galaxy
        self.name = NameGenerator.get_instance().generate_planet_name()
        self.is_habitable = is_habitable
        self.angle = np.random.random() * np.pi
        self.angular_velocity = Planet.ANGULAR_VELOCITY
        self.model = GLOBAL_RESOURCES.load_model(model)
        self.model.materials[0].shader = GLOBAL_RESOURCES.load_shader("shader_lighting")

    def update(self, dt: float):
        self.angle += self.angular_velocity * dt
        if self.parent is not None:
            force = self.galaxy.laws.attraction(self.parent, self)
            self.add_force(force)
            self.parent.add_force(-force)
        super().update(dt)

    def draw(self, camera: Camera):
        if camera.get_lod(self) > 0:
            self.model.transform = pr.matrix_rotate(pr.Vector3(*self.spin_axis), self.angle)
            position, size = self.galaxy.mapper.transform_entity(self)
            pr.draw_model(self.model, position, size.x, pr.WHITE)  # type: ignore
