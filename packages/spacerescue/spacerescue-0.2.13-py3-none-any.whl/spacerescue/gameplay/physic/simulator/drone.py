import numpy as np
import pyray as pr

from spacerescue.physic.entity import Entity
from spacerescue.gameplay.physic.simulator.world import World
from spacerescue.render.camera import Camera


class Drone(Entity):

    THRUST = 6000
    MASS = 10
    RADIUS = 10

    def __init__(self, world: World, position: np.ndarray):
        super().__init__(
            mass=Drone.MASS,
            radius=Drone.RADIUS,
            position=position.copy(),
            velocity=np.zeros(3),
        )
        self.world = world
        self.last_score = 0
        self.life = 0

    def get_life(self) -> int:
        return self.life

    def get_last_score(self) -> int:
        return self.last_score

    def get_sensor_data(self) -> list[int]:
        result = []
        front_column = self.world.get_front_column()
        if front_column:
            result = [0] * 8
            result[0] = self.position[1] # baro
            result[1] = self.velocity[1] # gyro
            result[2] = int(abs(front_column.position[0] - self.position[0])) # ultrasound
            for tile in front_column.tiles: # camera
                pixel = int((self.world.bound[3] - tile[1]) / tile[3] - 1)
                result[pixel + 3] = 1
        return result

    def get_action(self) -> str:
        raise NotImplementedError

    def update(self, dt: float):
        action = self.get_action()
        if action == "thrust":
            self.add_force(np.array([0, Drone.THRUST, 0]))
        self.add_force(self.world.laws.gravity(self))
        super().update(dt)
 
        self.last_score = self.world.score
        self.life += 1

    def draw(self, camera: Camera):
        rec = camera.apply_projection_rec(*self.world.mapper.transform_entity(self))
        pr.draw_ellipse(int(rec.x), int(rec.y), rec.width, rec.height, pr.WHITE)  # type: ignore
