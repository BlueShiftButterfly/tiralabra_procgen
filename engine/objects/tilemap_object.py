from pygame import Vector2
from engine.objects.object import Object
from engine.renderer.renderable_tilemap import RenderableTilemap, VisualTile
from room_generator.grid import Grid

class TilemapObject(Object):
    def __init__(
            self,
            object_id: str,
            position: Vector2=Vector2(0,0),
            renderable_component : RenderableTilemap=None,
            grid: Grid=None,
            tilemap_palette: dict=None
        ) -> None:
        self.grid = grid
        self.tilemap_palette = tilemap_palette
        super().__init__(object_id, position, renderable_component)
        self.renderable_component.set_tiles(self.get_visual_tiles())
        

    def get_visual_tiles(self) -> list[VisualTile]:
        visual_tiles = []
        for y in range(self.grid.bounds[0][1], self.grid.bounds[1][1]+1):
            for x in range(self.grid.bounds[0][0], self.grid.bounds[1][0]+1):
                surface_name = self.grid.get_cell(x, y)
                if surface_name is None:
                    continue
                surface = self.tilemap_palette[surface_name]
                visual_tiles.append(VisualTile(x, y, surface))
        return visual_tiles

    def update(self, delta_time: float):
        return super().update(delta_time)