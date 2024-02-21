from engine.engine import Engine
from pygame import Vector2
from room_generator.map_generator_visualizer import MapGeneratorVisualizer

def main():
    engine = Engine()
    engine.object_handler.create_camera(Vector2(0,0), engine.renderer.rendering_camera)
    engine.renderer.rendering_camera.zoom = 20
    engine.object_handler.create_debug_grid()
    eg = MapGeneratorVisualizer(engine.object_handler, engine.sprite_loader)
    engine.object_handler.create_generator_object(eg)
    engine.run()

if __name__ == "__main__":
    main()