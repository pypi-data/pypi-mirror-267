from spacerescue.constants import (
    AU,
)

from spacerescue.core.pyray import is_skip_key
from spacerescue.mechanics.game_scene import GameSceneEnd
from spacerescue.gameplay.physic.galaxy.hyperspace_portal import HyperspacePortal
from spacerescue.gameplay.scenes.travel_in_space import TravelInSpace


class TravelToPortal(TravelInSpace):
    
    def enter(self):
        super().enter()
        self.start_portal: HyperspacePortal = self.game_state.game_board.context["start_portal"]
        self.spaceship.arrive(self.start_portal, dist = 0.1 * AU)
 
    def update(self):
        if self.spaceship.is_arrived() or is_skip_key():
            self.spaceship.position = self.start_portal.position + self.start_portal.heading * 0.1 * AU
            self.spaceship.velocity = 0
            self.spaceship.heading = -self.start_portal.heading
            return GameSceneEnd(self)
        else:
            return super().update()
           