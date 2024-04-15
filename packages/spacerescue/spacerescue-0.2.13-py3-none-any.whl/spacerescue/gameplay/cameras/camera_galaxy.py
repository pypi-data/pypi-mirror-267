import numpy as np
import pyray as pr

from spacerescue.constants import AU, CAMERA_FOV, DEFAULT_HEADING, DEFAULT_UP
from spacerescue.physic.entity import Entity
from spacerescue.render import light as rl
from spacerescue.resources.resource_manager import ResourceManager
from spacerescue.render.camera import Camera


class CameraGalaxy(Camera):

    STAR_SYSTEM_SIZE = 2e6 * AU

    def __init__(self, position: np.ndarray):
        self.camera = pr.Camera3D(
            pr.vector3_zero(),
            pr.Vector3(*DEFAULT_HEADING),
            pr.Vector3(*DEFAULT_UP),
            CAMERA_FOV / 2,
            pr.CameraProjection.CAMERA_PERSPECTIVE,
        )
        
        self.camera_light = rl.create_light(
            rl.LIGHT_POINT,
            self.camera.position,
            pr.Vector3(0, 0, 0),
            pr.Color(8, 8, 8, 255),
            ResourceManager.get_instance().load_shader("shader_lighting"),
        )
        
        super().__init__(position, self.camera)

    def __del__(self):
        rl.delete_light(self.camera_light)

    def update(self, dt: float):
        self.camera_light.position = self.camera.position
        rl.light_update_values(self.camera_light)

    def get_lod(self, entity: Entity) -> int:
        dist = np.linalg.norm(self.position - entity.position)
        return 1 if dist < CameraGalaxy.STAR_SYSTEM_SIZE else 0
