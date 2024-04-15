from __future__ import annotations

import numpy as np
import pyray as pr

from spacerescue.core.math import ndarray_to_vector3
from spacerescue.gameplay.effects.parallax import Parallax
from spacerescue.physic.laws import NewtonianLaws
from spacerescue.physic.entity import Entity
from spacerescue.physic.mapper import Mapper
from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera


class Column:

    TILE_NUMBER = 5

    def __init__(self, world: World, stage: int):
        self.world = world
        self.scored = False
        self.position = np.array([world.bound[2] * 0.5, 0, 0])
        self.velocity = np.array([-World.VELOCITY, 0, 0])
        self.size = int(world.bound[3] / Column.TILE_NUMBER)

        space = self._get_space_pattern(stage)
        self.tiles = np.array(
            [
                [
                    self.position[0],
                    world.bound[3] - (y + 1) * self.size,
                    self.size * 0.5,
                    self.size,
                ]
                for y in range(Column.TILE_NUMBER)
                if y != space
            ]
        )

    def update(self, dt: float):
        self.position += self.velocity * dt
        for tile in self.tiles:
            tile[0] = self.position[0]

    def draw(self, camera: Camera):
        for tile in self.tiles:
            bound = camera.apply_projection_rec(
                *self.world.mapper.transform_bound(tile)
            )
            pr.draw_rectangle_lines_ex(bound, 1, pr.WHITE)  # type: ignore

    def check_collision(self, entity: Entity) -> bool:
        for tile in self.tiles:
            if (
                entity.position[0] + entity.radius > tile[0]
                and entity.position[0] - entity.radius < tile[0] + tile[2] - 1
                and entity.position[1] + entity.radius > tile[1]
                and entity.position[1] - entity.radius < tile[1] + tile[3] - 1
            ):
                return True
        return False

    def _get_space_pattern(self, stage: int):
        min, max = 0, Column.TILE_NUMBER - 1
        patterns = range(Column.TILE_NUMBER)
        match stage:
            case 1:
                choices = [i for i in patterns if i in (min, max)]
            case 2:
                choices = [i for i in patterns if not i in (min, max)]
            case _:
                choices = [i for i in patterns]
        return np.random.choice(choices)


class Particle(Entity):

    RADIUS = 30
    MAX_LIFE = 600

    def __init__(self, world: World, position: np.ndarray):
        super().__init__(
            mass=1,
            radius=Particle.RADIUS,
            position=position.copy(),
            velocity=np.array([-World.VELOCITY, 0, 0]),
        )
        self.world = world
        self.life = Particle.MAX_LIFE

    def update(self, dt: float):
        self.position += self.velocity * dt
        self.life = max(self.life - 1, 0)

    def draw(self, camera: Camera):
        t = self.life / Particle.MAX_LIFE
        rec = camera.apply_projection_rec(*self.world.mapper.transform_entity(self))
        pr.draw_ellipse(int(rec.x), int(rec.y), rec.width * t, rec.height * t, pr.fade(pr.WHITE, t * 0.9))  # type: ignore


class WorldMapper(Mapper):

    def transform_position(self, position: np.ndarray) -> pr.Vector3:
        return ndarray_to_vector3(position)

    def transform_radius(self, radius: float) -> pr.Vector3:
        return pr.Vector3(radius, radius, 0)

    def transform_entity(self, entity: Entity) -> tuple[pr.Vector3, pr.Vector3]:
        position = self.transform_position(entity.position)
        radius = self.transform_radius(entity.radius)
        return position, radius

    def transform_bound(self, bound: np.ndarray) -> tuple[pr.Vector3, pr.Vector3]:
        pos = pr.Vector3(bound[0], bound[1] + bound[3], 1)
        size = pr.Vector3(bound[2], bound[3], 0)
        return pos, size


class World(Universe):

    VELOCITY = 10
    WIDTH_BETWEEN_COLUMNS = 500
    SPAWN_ORIGIN = np.array([-200.0, 0.0, 0.0])
    STAGE_LEN = 50

    def __init__(self, bound: np.ndarray):
        super().__init__(NewtonianLaws(), WorldMapper())
        self.bound = bound
        self.stage = 1
        self.epoch = 0
        self.score = 0
        self.columns = []
        self.particles = []
        self.entities = []

    def reset(self):
        self.background = Parallax(
            "clouds", "buildings", self.mapper.transform_bound(self.bound)
        )
        self.epoch += 1
        self.score = 0
        self.columns = [Column(self, self.stage)]
        self.particles = []
        self.entities = []
        self.simulation_started = False

    def get_front_column(self):
        for column in self.columns:
            if column.position[0] + column.size * 0.5 > World.SPAWN_ORIGIN[0]:
                return column
        return None

    def update(self, dt: float):
        self.simulation_started = (
            self.simulation_started
            or abs(self.columns[0].position[0] - World.SPAWN_ORIGIN[0]) < World.WIDTH_BETWEEN_COLUMNS
        )

        if len(self.columns) > 0:
            self._check_score()
            self._purge_oldest_column()

        if len(self.columns) > 0:
            self._spawn_new_column()

        self.background.update(dt)

        for column in self.columns:
            column.update(dt)

        self.particles = [x for x in self.particles if x.life > 0]
        for particle in self.particles:
            particle.update(dt)

        if self.simulation_started:
            self.entities = [x for x in self.entities if not self._check_collision(x)]
            for entity in self.entities:
                entity.update(dt)

    def draw(self, camera: Camera):
        self.background.draw(camera)

        for column in self.columns:
            column.draw(camera)

        for particle in self.particles:
            particle.draw(camera)

        for entity in self.entities:
            entity.draw(camera)

        rec = camera.apply_projection_rec(*self.mapper.transform_bound(self.bound))
        pr.draw_rectangle_lines_ex(rec, 1, pr.WHITE)  # type: ignore
        pr.draw_text(
            f"EPOCH: {self.epoch}\tSTAGE: {self.stage}\n\nSCORE: {self.score}",
            int(rec.x + 5),
            int(rec.y + 5),
            20,
            pr.WHITE,  # type: ignore
        )

    def _check_score(self):
        column = self.columns[0]
        if column.scored:
            return
        if column.position[0] + column.size * 0.5 < World.SPAWN_ORIGIN[0]:
            self.score += 1
            if self.score % World.STAGE_LEN == 0:
                self.stage = min(self.stage + 1, 3)
            column.scored = True

    def _purge_oldest_column(self):
        column = self.columns[0]
        if column.position[0] + column.size * 0.5 < -self.bound[2] * 0.5:
            self.columns.pop(0)

    def _spawn_new_column(self):
        column = self.columns[-1]
        dist = abs(self.bound[2] * 0.5 - column.position[0])
        if dist > World.WIDTH_BETWEEN_COLUMNS:
            self.columns.append(Column(self, self.stage))

    def _check_collision(self, entity: Entity) -> bool:
        hit = self._hit_boundaries(entity) or self._hit_front_column(entity)
        if hit:
            self.particles.append(Particle(self, entity.position))
        return hit

    def _hit_boundaries(self, entity: Entity):
        return (
            entity.position[0] - entity.radius < self.bound[0]
            or entity.position[0] + entity.radius > self.bound[0] + self.bound[2] - 1
            or entity.position[1] - entity.radius < self.bound[1]
            or entity.position[1] + entity.radius > self.bound[1] + self.bound[3] - 1
        )

    def _hit_front_column(self, entity: Entity) -> bool:
        column = self.get_front_column()
        return column is not None and column.check_collision(entity)
