import logging
import traceback
import numpy as np
import pyray as pr


from spacerescue.resources import (
    GLOBAL_RESOURCES,
    STRING_BACK,
    STRING_CODE_IS_INCORRECT,
    STRING_REPLAY,
    STRING_SIMULATION_CAPTION,
    STRING_TRAIN,
    STRING_TRAINING_SUCCESS,
)
from spacerescue.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from spacerescue.mechanics.game_scene import (
    GameScene,
    GameSceneEnd,
    GameSceneNext,
    GameSceneResult,
    GameSubScene,
)
from spacerescue.mechanics.challenge import CodeChallenge
from spacerescue.gameplay.cameras.camera_simulator import CameraSimulator
from spacerescue.gameplay.physic.simulator.drone_factory import DroneFactory
from spacerescue.gameplay.widgets.monitor import Monitor
from spacerescue.render.widgets.simulation_box import SimulationBox
from spacerescue.gameplay.scenes.computer_console import ComputerConsole
from spacerescue.gameplay.physic.simulator.world import World
from spacerescue.render.animators.open_horizontal import OpenHorizontal
from spacerescue.render.effects.fade_scr import FadeScr
from spacerescue.render.widgets.button import Button
from spacerescue.render.widgets.message_box import MessageBox
from spacerescue.render.widgets.screen import Screen


class SimulatorConsole(ComputerConsole):
    def update(self) -> GameSceneResult:
        if self.state == 4:
            self.state = 0
            return GameSceneNext(SimulatorBench(self, self.challenge).enter())
        else:
            return super().update()


class SimulatorBench(GameSubScene):

    BORDER_SIZE = 80
    DISTANCE_WIN = 214
    BOUND_SCREEN = pr.Rectangle(200, 112, SCREEN_WIDTH - 390, SCREEN_HEIGHT - 240)
    DRONE_ORIGIN = np.array([World.SPAWN_ORIGIN[0], BOUND_SCREEN.height / 2, 1])
    BOUND_REAL = np.array(
        [-BOUND_SCREEN.width / 2, 0, BOUND_SCREEN.width, BOUND_SCREEN.height]
    )

    def __init__(self, scene: GameScene, challenge: CodeChallenge):
        super().__init__(scene)
        self.challenge = challenge
        self.factory: DroneFactory | None = self.challenge.get_answer()
        self.world = World(SimulatorBench.BOUND_REAL)
        self.camera = CameraSimulator(self.world, SimulatorBench.BOUND_SCREEN)

    def enter(self):
        super().enter()
        pr.stop_music_stream(GLOBAL_RESOURCES.load_music("music"))
        self._build_ui()
        self.simulation_training = True
        self.simulation_running = False
        self.state = 0
        self.scroll = 0
        
    def update(self):
        match self.state:
            case 0:
                if self.fade_in.is_playing():
                    self.fade_in.update()
                else:
                    self._boot_simulation()

            case 1:
                try:
                    if self.simulation_running:
                        self.simulation_box.update()
                except Exception as x:
                    self._on_training_exception(str(x))

                if len(self.world.entities) == 0 and len(self.world.particles) == 0:
                    self._boot_simulation()
                elif self.world.score >= SimulatorBench.DISTANCE_WIN:
                    self._on_training_success()
                    
                if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_MULTIPLY) or pr.is_key_pressed(pr.KeyboardKey.KEY_EIGHT):
                    self.simulation_training = not self.simulation_training
                    self._boot_simulation()

                for button in self.buttons:
                    button.update()

            case 2:
                if self.message_box is not None:
                    self.message_box.update()
                elif self.simulation_running:
                    self._boot_simulation()

            case 3:
                return GameSceneEnd(self.scene)

            case 4:
                self.leave()
                return GameSceneEnd(self.scene)

        return super().update()

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(Monitor.BG_COLOR)
        if self.state >= 1 and self.simulation_running:
            assert isinstance(self.simulation_box.widget, SimulationBox)
            self.simulation_box.caption = STRING_SIMULATION_CAPTION.format(
                self.simulation_box.widget.simulation_speed,
                STRING_TRAIN if self.simulation_training else STRING_REPLAY
            )
            self.simulation_box.draw(self.camera)
        self.screen.draw()
        if self.state >= 1:
            for button in self.buttons:
                button.draw()
        if self.state == 2 and self.message_box is not None:
            self.message_box.draw()
        if self.state == 0:
            self.fade_in.draw()
        pr.end_drawing()

    def _build_ui(self):
        self.fade_in = FadeScr(0.5)
        self.screen = Screen("widget", "console")
        self.simulation_box = Monitor(
            "widget",
            SimulationBox(
                "widget",
                pr.Vector2(
                    SimulatorBench.BOUND_SCREEN.x,
                    SimulatorBench.BOUND_SCREEN.y,
                ),
                pr.Vector2(
                    SimulatorBench.BOUND_SCREEN.width,
                    SimulatorBench.BOUND_SCREEN.height,
                ),
                self.world,
            ),
            caption="Loading ...",
            border_size=ComputerConsole.BORDER_SIZE,
        )
        self.message_box = None
        self.buttons = [
            Button(
                "button_back",
                pr.Vector2(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 45),
                pr.Vector2(200, 38),
                STRING_BACK,
                Button.RED,
                self._button_is_clicked,
            ),
        ]

    def _on_training_exception(self, reason: str):
        logging.error(traceback.format_exc())
        mb = MessageBox(
            "mb_training_exception",
            pr.Vector2(max(pr.measure_text(str(reason), 20) + 40, 500), 300),
            STRING_CODE_IS_INCORRECT.format(reason=reason),
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
        self.simulation_running = False
        self.state = 2

    def _on_training_success(self):
        mb = MessageBox(
            "mb_training_success",
            pr.Vector2(500, 300),
            STRING_TRAINING_SUCCESS,
            self._message_box_is_closed,
        )
        self.message_box = OpenHorizontal(mb, 0.3, MessageBox.BG_COLOR)
        self.state = 2

    def _button_is_clicked(self, button: Button):
        if button.id == "button_back":
            self.state = 3

    def _message_box_is_closed(self, message_box: MessageBox):
        self.message_box = None
        match message_box.id:
            case "mb_training_exception":
                self.state = 3
            case "mb_training_success":
                self._shutdown_simulation()

    def _boot_simulation(self):
        assert self.factory is not None
        try:
            self.world.reset()
            self.factory.reset(self.simulation_training)
            self.world.entities = self.factory.get_drones(
                self.world, SimulatorBench.DRONE_ORIGIN
            )
            self.simulation_training = self.factory.training
            self.simulation_running = True
            self.state = 1
        except Exception as x:
            self._on_training_exception(str(x))

    def _shutdown_simulation(self):
        assert self.factory is not None
        try:
            self.factory.close()
            self.simulation_running = False
            self.challenge.on_good_answer()
            self.state = 4
        except Exception as x:
            self._on_training_exception(str(x))
