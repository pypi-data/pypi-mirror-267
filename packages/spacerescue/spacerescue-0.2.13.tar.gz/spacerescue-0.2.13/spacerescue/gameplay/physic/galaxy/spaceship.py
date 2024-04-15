import pyray as pr
import numpy as np

from spacerescue.constants import AU, SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.render.camera import Camera
from spacerescue.resources import GLOBAL_RESOURCES
from spacerescue.physic.entity import Entity
from spacerescue.core.math import lerp, ndarray_to_vector3, normalize
from spacerescue.gameplay.cameras.camera_entity import CameraEntity
from spacerescue.gameplay.physic.galaxy.galaxy import ALL_STARS, Galaxy

class Spaceship(Entity):

    def __init__(self, galaxy: Galaxy, position: np.ndarray, heading: np.ndarray):
        super().__init__(
            mass=1.0, # 3.2e9 kg
            radius=144,
            position=position,
            velocity=np.zeros(3),
        )
        self.galaxy=galaxy
        self.model = GLOBAL_RESOURCES.load_model("ncc-1701")
        self.model.materials[0].shader = GLOBAL_RESOURCES.load_shader(
            "shader_lighting"
        )
        self.heading = heading
        self.heading_speed = 1e-6
        self.target = None

    def is_arrived(self, radius: float = 0.005 * AU) -> bool:
        if self.target is None:
            return False
        dist = float(np.linalg.norm(self.position - self.target.position))
        return abs(dist - self.target_dist) < radius

    def arrive(
        self,
        target: Entity | None,
        dist: float = 0.0,
        pulse_speed: float = 1e5,
        pulse_force: float = 1.0,
        slow_radius: float = 0.5 * AU,
    ):
        self.target = target
        self.target_dist = dist
        self.pulse_speed = pulse_speed
        self.pulse_force = pulse_force
        self.slow_radius = slow_radius
        self.velocity = 0

    def update(self, dt: float):
        self.parent = self.galaxy.find_closest_stellar_object(
            self.position, ALL_STARS
        )
        
        # Apply gravitational force

        # closest_mass = self.universe.find_closest_stellar_object(
        #     self.position, ALL_STAR_SYSTEM_OBJECTS(self.parent)
        # )
        # if closest_mass is not None:
        #     force = self.universe.laws.attraction(self.parent, self)
        #     self.add_force(force)
        #     closest_mass.add_force(-force)

        # Apply steering behavior force

        if self.target is not None:
            self.add_force(
                self.galaxy.laws.arrive(
                    self,
                    self.target,
                    self.pulse_speed,
                    self.pulse_force,
                    self.slow_radius,
                    self.target_dist,
                )
            )

        super().update(dt)

        if self.target is not None:
            desired_heading = normalize(self.target.position - self.position)
            self.heading = lerp(
                self.heading, desired_heading, self.heading_speed * dt
            )
            
    def draw(self, camera: Camera):
        self.model.transform = pr.matrix_invert(
            pr.matrix_look_at(
                pr.vector3_zero(),
                ndarray_to_vector3(self.heading),
                ndarray_to_vector3(self.spin_axis),
            )
        )
        position, size = self.galaxy.mapper.transform_entity(self)
        pr.draw_model(self.model, position, size.x, pr.WHITE)  # type: ignore

    def collect_photons(self, direction: np.ndarray | None = None) -> pr.RenderTexture:
        direction = direction if direction is not None else self.heading
        camera = CameraEntity(self.galaxy, self)
        surface = pr.load_render_texture(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
        pr.begin_texture_mode(surface)
        pr.clear_background(pr.BLACK)  # type: ignore
        pr.begin_mode_3d(camera.camera)
        self.galaxy.draw(camera)
        pr.end_mode_3d()
        pr.end_texture_mode()
        return surface
