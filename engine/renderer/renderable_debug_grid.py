from engine.renderer.renderable_types import RenderableType
from engine.renderer.renderable import Renderable

class RenderableDebugGrid(Renderable):
    """Used to render the debug grid by the render queue. For debugging purposes only"""
    def __init__(self) -> None:
        super().__init__()
        self.type = RenderableType.DEBUG_GRID
