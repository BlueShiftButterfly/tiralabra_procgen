from engine.renderer.renderable_types import RenderableType

class Renderable:
    """Base class for all renderable objects. Processed by the renderer in the render queue"""
    def __init__(self) -> None:
        self.type : RenderableType = None
        self.sorting_layer : int = 0

    def __cmp___(self, other):
        if self.sorting_layer > other.sorting_layer:
            return 1
        if self.sorting_layer < other.sorting_layer:
            return -1
        return 0
