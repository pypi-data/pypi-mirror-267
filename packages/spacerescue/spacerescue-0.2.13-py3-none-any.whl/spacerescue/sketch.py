import logging
import numpy as np
import pyray as pr

from spacerescue.mechanics.game_board import GameBoard
from spacerescue.gameplay.physic.galaxy.galaxy import (
    ALL_PORTALS,
    ALL_STAR_SYSTEM_HABITABLE_PLANETS,
    Galaxy,
)
from spacerescue.resources import GLOBAL_RESOURCES


class Sketch(GameBoard):

    def __init__(self):
        super().__init__()
        self.music = GLOBAL_RESOURCES.load_music("music")
        self._build_galaxy()
        self._build_scenario()

    def update(self):
        if pr.is_music_stream_playing(self.music):
            pr.update_music_stream(self.music)
        super().update()

    def _build_galaxy(self):
        logging.info("INFO: CONTEXT: Generate galaxy ...")
        self.context["galaxy"] = Galaxy()

    def _build_scenario(self):
        logging.info("INFO: CONTEXT: Generate scenario ...")
        galaxy = self.context["galaxy"]
        portals = list(galaxy.filter_stellar_objects(ALL_PORTALS))

        scenario_is_ok = False
        while not scenario_is_ok:
            self.context["start_portal"] = np.random.choice(portals)
            self.context["rescue_portal"] = np.random.choice(portals)
            scenario_is_ok = (
                self.context["start_portal"].name != self.context["rescue_portal"].name
            )

        planets = list(
            galaxy.filter_stellar_objects(
                ALL_STAR_SYSTEM_HABITABLE_PLANETS(self.context["rescue_portal"].parent)
            )
        )
        self.context["rescue_planet"] = np.random.choice(planets)
