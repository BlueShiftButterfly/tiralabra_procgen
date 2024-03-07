import sys
import pygame

class InputHandler:
    """Input handler is responsible for user input, such as keypresses"""
    inputs = {
        "up" : False,
        "down" : False,
        "left" : False,
        "right" : False,
        "zoom_in" : False,
        "zoom_out" : False,
        "quit" : False,
        "space" : False
    }

    def __init__(self) -> None:
        self.keybinds = {
            "up" : pygame.K_UP,
            "down" : pygame.K_DOWN,
            "left" : pygame.K_LEFT,
            "right" : pygame.K_RIGHT,
            "zoom_in" : pygame.K_PAGEDOWN,
            "zoom_out" : pygame.K_PAGEUP,
            "quit" : pygame.K_ESCAPE,
            "space" : pygame.K_SPACE
        }

    def handle_input(self):
        """Main input loop to handle all pygame user input events"""
        pressed = pygame.key.get_pressed()
        for kb in self.keybinds.keys():
            if pressed[self.keybinds[kb]]:
                InputHandler.inputs[kb] = True
                if kb == "quit":
                    pygame.quit()
                    sys.exit()
            else:
                InputHandler.inputs[kb] = False
