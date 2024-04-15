import pyray as pr
import numpy as np

from spacerescue.render.animator import Animator
from spacerescue.render.camera import Camera
from spacerescue.resources import SCENE_RESOURCES

class Parallax(Animator):

    def __init__(self, background: str, foreground: str, bound: tuple[pr.Vector3, pr.Vector3]):
        self.layers = [
            {"surface": SCENE_RESOURCES.load_texture(background), "speed": 1.0},
            {"surface": SCENE_RESOURCES.load_texture(foreground), "speed": 2.0},
        ]
        self.bound = bound
        self.scroll = 0
        
        for layer in self.layers:
            pr.set_texture_wrap(layer["surface"], pr.TextureWrap.TEXTURE_WRAP_REPEAT)

    def update(self, dt: float):
        self.scroll += dt

    def draw(self, camera: Camera):
        bound = camera.apply_projection_rec(*self.bound)
        for layer in self.layers:
            surface, speed = layer["surface"], layer["speed"]
            pr.draw_texture_pro(
                surface,
                pr.Rectangle(self.scroll * speed, 0, surface.width, surface.height),
                bound,
                pr.vector2_zero(),
                0.0,
                pr.WHITE,  # type: ignore
            )