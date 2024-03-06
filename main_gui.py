import pygame
from engine.engine import Engine
from pygame import Vector2
from room_generator.map_generator_visualizer import MapGeneratorVisualizer

def main():
    engine = Engine(render_resolution=(1920, 1080), pygame_render_flags=pygame.FULLSCREEN)
    engine.object_handler.create_camera(Vector2(0,0), engine.renderer.rendering_camera)
    engine.renderer.rendering_camera.zoom = 5
    eg = MapGeneratorVisualizer(engine.object_handler, engine.sprite_loader)
    obj_id = engine.object_handler.create_generator_object(eg)
    engine.object_handler.create_objects_from_creation_queue()
    engine.ui_handler.set_generator_reference(engine.object_handler.get_object_from_id(obj_id))
    engine.run()

if __name__ == "__main__":
    main()