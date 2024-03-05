import sys
import pygame

class EventHandler:
    def __init__(self, ui_handler_reference) -> None:
        self.ui_handler_reference = ui_handler_reference

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.ui_handler_reference.handle_ui_events(events)