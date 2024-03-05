import pygame
import pygame_gui

class UIHandler:
    def __init__(self) -> None:
        self.ui_manager = pygame_gui.UIManager((1280, 720))
        self.generator_reference = None
        self.map_size_text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-232, 64), (200, 32)),
            manager=self.ui_manager,
            text="Map Size: 128",
            anchors={"right" : "right"}
        )
        self.map_size_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((-232, 102), (200, 32)),
            manager=self.ui_manager,
            start_value=128,
            value_range=(32, 512),
            anchors={"right" : "right"}
        )
        self.map_size = self.map_size_slider.current_value
        self.generate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((-232, -64), (200, 32)),
            manager=self.ui_manager,
            text="Generate Map",
            anchors={
                "right" : "right",
                "bottom" : "bottom"
            }
        )
        self.amount_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-232, 142), (200, 32)),
            manager=self.ui_manager,
            text="Room Count: 32",
            anchors={"right" : "right"}
        )
        self.room_count_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((-232, 182), (200, 32)),
            manager=self.ui_manager,
            start_value=32,
            value_range=(8, 128),
            anchors={"right" : "right"}
        )
        self.room_count = self.room_count_slider.current_value

    def set_generator_reference(self, generator):
        self.generator_reference = generator

    def handle_ui_events(self, events):
        for event in events:
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.map_size_slider:
                    self.map_size = self.map_size_slider.current_value
                    self.map_size_text_label.set_text(f"Map size: {self.map_size}")
                if event.ui_element == self.room_count_slider:
                    self.room_count = self.room_count_slider.current_value
                    self.amount_label.set_text(f"Room Count: {self.room_count}")
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.generate_button and self.generator_reference is not None:
                    self.generator_reference.generate(seed = None, size = self.map_size, amount = self.room_count)

            self.ui_manager.process_events(event)

    def update_ui(self, delta_time):
        self.ui_manager.update(delta_time)
        