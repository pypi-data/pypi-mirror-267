import pyray as pr

from spacerescue.gameplay.physic.simulator.world import World
from spacerescue.render.camera import Camera


class CameraSimulator(Camera):
    
    def __init__(self, world: World, bound_screen: pr.Rectangle):
        sx = bound_screen.width / world.bound[2]
        sy = bound_screen.height / world.bound[3]
        x0 = bound_screen.x + bound_screen.width * 0.5
        y0 = bound_screen.y + bound_screen.height
        self._projection = pr.Matrix(sx, 0, x0, 0, 0, -sy, y0, 0, 0, 0, 1, 0, 0, 0, 0, 1)

    def apply_projection(self, pos: pr.Vector3) -> pr.Vector2:
        pos = pr.vector3_transform(pos, self._projection)
        return pr.Vector2(pos.x, pos.y)

    def apply_projection_rec(self, pos: pr.Vector3, size: pr.Vector3) -> pr.Rectangle:
        pos = pr.vector3_transform(pos, self._projection)
        size = pr.vector3_transform(size, self._projection)
        return pr.Rectangle(pos.x, pos.y, abs(size.x), abs(size.y))
