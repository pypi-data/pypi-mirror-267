from __future__ import annotations

import numpy as np


from spacerescue.constants import (
    DEFAULT_HEADING,
    DEFAULT_UP,
)
from spacerescue.core.math import normalize
from spacerescue.render.camera import Camera


class Entity:

    def __init__(
        self,
        mass: float,
        radius: float,
        position: np.ndarray,
        velocity: np.ndarray | None = None,
        spin_axis: np.ndarray | None = None,
        parent: Entity | None = None,
    ):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity if velocity is not None else np.zeros(3)
        self.spin_axis = spin_axis if spin_axis is not None else np.array(DEFAULT_UP)
        self.parent = parent
        self.heading = (
            normalize(self.velocity) if self.has_some_speed() else np.array(DEFAULT_HEADING)
        )
        self._forces = np.zeros(3)

    def update(self, dt: float):
        self.apply_forces(dt)
        self.clear_force()

    def draw(self, camera: Camera):
        raise NotImplementedError

    def clear_force(self):
        self._forces = np.zeros(3)

    def add_force(self, force: np.ndarray):
        self._forces += force

    def apply_forces(self, dt: float):
        self.velocity += self._forces * dt / self.mass
        self.position += self.velocity * dt

    def get_speed(self) -> float:
        return float(np.linalg.norm(self.velocity))

    def has_some_speed(self) -> bool:
        return self.get_speed() != 0.0
