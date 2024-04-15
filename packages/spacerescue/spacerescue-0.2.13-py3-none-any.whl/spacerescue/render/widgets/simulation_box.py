import pyray as pr

from spacerescue.physic.universe import Universe
from spacerescue.render.camera import Camera
from spacerescue.render.widget import Widget


class SimulationBox(Widget):

    FONT_SPACING = 2
    FONT_SIZE = 28
    FONT_CHAR_WIDTH = (FONT_SIZE + FONT_SPACING) / 2
    FONT_COLOR = pr.Color(255, 255, 255, 255)
    SIMULATION_RATE = 1 / 60

    def __init__(
        self,
        id: str,
        position: pr.Vector2,
        size: pr.Vector2,
        simulation: Universe,
    ):
        super().__init__(id, self._get_inner_bound(position, size))
        self.simulation = simulation
        self.simulation_speed = 10

    def update(self):
        pos = pr.get_mouse_position()
        if pr.check_collision_point_rec(pos, self.bound):
            if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_ADD) or pr.is_key_pressed(pr.KeyboardKey.KEY_EQUAL):
                self.simulation_speed = min(((self.simulation_speed + 10) // 10) * 10, 100)
            if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_SUBTRACT) or pr.is_key_pressed(pr.KeyboardKey.KEY_MINUS):
                self.simulation_speed = max(((self.simulation_speed - 10) // 10) * 10, 1)
        for _ in range(self.simulation_speed):
            self.simulation.update(SimulationBox.SIMULATION_RATE)

    def draw(self, camera: Camera):
        self.simulation.draw(camera)

    def _get_inner_bound(self, position: pr.Vector2, size: pr.Vector2) -> pr.Rectangle:
        self.size_in_chars = pr.Vector2(
            size.x // SimulationBox.FONT_CHAR_WIDTH,
            size.y // SimulationBox.FONT_SIZE,
        )
        return pr.Rectangle(position.x, position.y, size.x, size.y)
