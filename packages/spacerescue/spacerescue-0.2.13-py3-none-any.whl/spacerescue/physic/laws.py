import numpy as np

from spacerescue.core.math import EPSILON, limit, normalize
from spacerescue.physic.entity import Entity

G_BIG = 6.67e-11  # m3⋅kg−1⋅s−2
G_SMALL = 9.81  # m⋅s−2


class Laws:
    """interface"""

    def gravity(self, e: Entity) -> np.ndarray:
        raise NotImplementedError

    def attraction(self, e1: Entity, e2: Entity) -> np.ndarray:
        raise NotImplementedError

    def seek(
        self, e: Entity, t: Entity, v_max: float, f_max: float, dist: float = 0.0
    ) -> np.ndarray:
        raise NotImplementedError

    def arrive(
        self,
        e: Entity,
        t: Entity,
        v_max: float,
        f_max: float,
        radius: float,
        dist: float = 0.0,
    ) -> np.ndarray:
        raise NotImplementedError


class NewtonianLaws(Laws):

    def gravity(self, e: Entity) -> np.ndarray:
        return e.mass * np.array([0, -G_SMALL, 0])

    def attraction(self, e1: Entity, e2: Entity) -> np.ndarray:
        norm = np.linalg.norm(e1.position - e2.position)
        if norm < EPSILON:
            return np.zeros(3)
        attraction_value = (G_BIG * e1.mass * e2.mass) / norm**2
        attraction_vector = (e1.position - e2.position) / norm
        return attraction_value * attraction_vector

    def seek(
        self, e: Entity, t: Entity, v_max: float, f_max: float, dist: float = 0.0
    ) -> np.ndarray:
        if dist > 0.0:
            target = t.position + t.heading * dist
        else:
            target = t.position
        desired_velocity = normalize(target - e.position) * v_max
        steering = limit(desired_velocity - e.velocity, f_max)
        return steering

    def arrive(
        self,
        e: Entity,
        t: Entity,
        v_max: float,
        f_max: float,
        radius: float,
        dist: float = 0.0,
    ) -> np.ndarray:
        if dist > 0.0:
            target = t.position + t.heading * dist
        else:
            target = t.position
        desired_velocity = target - e.position
        distance = np.linalg.norm(desired_velocity)
        if distance < radius:
            desired_velocity = (
                normalize(target - e.position) * v_max * (distance / radius)
            )
        else:
            desired_velocity = normalize(target - e.position) * v_max
        steering = limit(desired_velocity - e.velocity, f_max)
        return steering
