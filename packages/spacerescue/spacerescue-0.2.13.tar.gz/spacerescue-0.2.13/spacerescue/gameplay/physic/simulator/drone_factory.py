class DroneFactory:
    
    def __init__(self):
        self.training = True

    def reset(self, training: bool):
        self.training = training
        
    def get_drones(self, *args) -> list:
        raise NotImplementedError
    
    def close(self):
        pass