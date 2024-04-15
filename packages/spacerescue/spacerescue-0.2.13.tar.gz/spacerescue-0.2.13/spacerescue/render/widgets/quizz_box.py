import pyray as pr

from spacerescue.render.camera import Camera
from spacerescue.render.widget import Widget
from spacerescue.render.widgets.checkbox import CheckBox
from spacerescue.resources import SCENE_RESOURCES


class QuizzBox(Widget):

    FONT_SPACING = 2
    FONT_SIZE = 28
    FONT_CHAR_WIDTH = (FONT_SIZE + FONT_SPACING) / 2
    FONT_COLOR = pr.Color(255, 255, 255, 255)

    def __init__(
        self,
        id: str,
        position: pr.Vector2,
        size: pr.Vector2,
        question: str,
        choices: dict[str, bool],
    ):
        super().__init__(id, self._get_inner_bound(position, size))
        self.question = question.splitlines()
        self.choices = choices


        self.checkboxes: list[CheckBox] = []
        for i, self.choice in enumerate(self.choices.keys()):
            pos = pr.Vector2(
                self.bound.x,
                self.bound.y + (i + len(self.question)) * QuizzBox.FONT_SIZE,
            )
            self.checkboxes.append(
                CheckBox(
                    f"checkbox{i}",
                    pos,
                    pr.Vector2(QuizzBox.FONT_SIZE - 10, QuizzBox.FONT_SIZE - 10),
                    self.choice,
                    pr.WHITE,  # type: ignore
                    self._checkbox_clicked,
                )
            )

        self.font = SCENE_RESOURCES.load_font("mono_font28")

    def update(self):
        for checkbox in self.checkboxes:
            checkbox.update()

    def draw(self, camera: Camera | None = None):
        for i, line in enumerate(self.question):
            pos = pr.Vector2(
                self.bound.x,
                self.bound.y + i * QuizzBox.FONT_SIZE,
            )
            pr.draw_text_ex(
                self.font,
                line,
                pos,
                QuizzBox.FONT_SIZE,
                QuizzBox.FONT_SPACING,
                QuizzBox.FONT_COLOR,
            )

        for checkbox in self.checkboxes:
            checkbox.draw()

    def _get_inner_bound(self, position: pr.Vector2, size: pr.Vector2) -> pr.Rectangle:
        self.size = pr.Vector2(
            size.x // QuizzBox.FONT_CHAR_WIDTH,
            size.y // QuizzBox.FONT_SIZE,
        )
        return pr.Rectangle(position.x, position.y, size.x, size.y)


    def _checkbox_clicked(self, checkbox):
        for other in self.checkboxes:
            if checkbox.id != other.id:
                other.clicked = False
