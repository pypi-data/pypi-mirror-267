import numpy as np
import pyray as pr

class Camera:
    
    def __init__(self, position: np.ndarray, camera: pr.Camera3D):
        self.position = position
        self.camera = camera
        
    def get_lod(self, entity) -> int:
        raise NotImplementedError
    
    def apply_projection(self, pos: pr.Vector3) -> pr.Vector2:
        raise NotImplementedError

    def apply_projection_rec(self, pos: pr.Vector3, size: pr.Vector3) -> pr.Rectangle:
        raise NotImplementedError
