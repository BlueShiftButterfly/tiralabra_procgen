from engine.engine import Engine
from pygame import Vector2

if __name__ == "__main__":
    e = Engine()

    e.object_handler.create_camera(Vector2(0,0), e.renderer.rendering_camera)
    
    e.object_handler.create_line(Vector2(0,0), Vector2(2,1))
    s = e.object_handler.create_point(Vector2(0,0))
    e.object_handler.create_point(Vector2(2,1))

    e.run()
    