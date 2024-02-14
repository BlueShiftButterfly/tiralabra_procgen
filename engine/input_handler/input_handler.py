import pygame
import sys

class InputHandler:
    """Input handler is responsible for user input, such as keypresses"""
    inputs = {
        "up" : False,
        "down" : False,
        "left" : False,
        "right" : False,
        "zoom_in" : False,
        "zoom_out" : False,
        "quit" : False
    }
    def __init__(self) -> None:
        self.keybinds = {
            "up" : pygame.K_w,
            "down" : pygame.K_s,
            "left" : pygame.K_a,
            "right" : pygame.K_d,
            "zoom_in" : pygame.K_q,
            "zoom_out" : pygame.K_e,
            "quit" : pygame.K_ESCAPE
        }

    def handle_events(self):
        """Main input loop to handle all pygame user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        for kb in self.keybinds.keys():
            if pressed[self.keybinds[kb]]:
                InputHandler.inputs[kb] = True
                if kb == "quit":
                    pygame.quit()
                    sys.exit()
            else:
                InputHandler.inputs[kb] = False
            
                    
