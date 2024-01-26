import pygame

class InputHandler:
    """Input handler is responsible for user input, such as keypresses"""
    def __init__(self) -> None:
        pass

    def handle_events(self):
        """Main input loop to handle all pygame user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
