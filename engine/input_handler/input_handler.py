import pygame

class InputHandler:
    def __init__(self) -> None:
        pass

    def handle_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                raise SystemExit 