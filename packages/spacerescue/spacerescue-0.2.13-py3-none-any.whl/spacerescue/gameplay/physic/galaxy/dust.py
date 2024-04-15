import pyray as pr
import numpy as np

from spacerescue.constants import AU, PARSEC
from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.physic.entity import Entity
from spacerescue.resources import GLOBAL_RESOURCES


class Dust(Entity):

    MASS = 1e-5 # kg
    RADIUS = 1.5e-3 * PARSEC
    COLOR = (96, 0, 64, 32)

    def __init__(
        self, galaxy: Universe, position: np.ndarray, star: Entity
    ):
        super().__init__(
            mass=Dust.MASS,
            radius=Dust.RADIUS * 2,
            position=position + np.random.rand(3) * AU,
            parent=star,
        )
        self.galaxy = galaxy
        self.color = Dust.COLOR
        self.rotation = 180 * np.random.rand()
        self.texture = GLOBAL_RESOURCES.load_texture("particule")

    def draw(self, camera: Camera):
        if camera.get_lod(self) == 0:
            mat_view = pr.get_camera_matrix(camera.camera)
            source = pr.Rectangle(0.0, 0.0, self.texture.width, self.texture.height)
            position, size = self.galaxy.mapper.transform_entity(self)
            up = pr.Vector3(mat_view.m1, mat_view.m5, mat_view.m9)
            pr.draw_billboard_pro(
                camera.camera,
                self.texture,
                source,
                position,
                up,
                pr.Vector2(size.x, size.y),
                pr.vector2_zero(),
                self.rotation,
                self.color, # type: ignore
            )