from engine.engine import Engine
from pygame import Vector2
from room_generator.engine_generator import EngineGenerator

def main():
    engine = Engine()
    engine.object_handler.create_camera(Vector2(0,0), engine.renderer.rendering_camera)
    engine.renderer.rendering_camera.zoom = 15
    eg = EngineGenerator(engine.object_handler)
    engine.object_handler.create_generator_object(eg)
    engine.run()

if __name__ == "__main__":
    main()