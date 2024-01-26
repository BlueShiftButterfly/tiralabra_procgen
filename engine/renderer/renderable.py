from engine.renderer.renderable_types import RenderableType

class Renderable:
    def __init__(self) -> None:
        self.type : RenderableType = None
        self.sorting_layer : int = 0
    
    def __cmp___(self, other):
        if self.sorting_layer > other.sorting_layer:
            return 1
        elif self.sorting_layer < other.sorting_layer:
            return -1
        else:
            return 0