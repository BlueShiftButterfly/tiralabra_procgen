import hashlib
import random
import pygame
import pygame_gui

class UIHandler:
    def __init__(self, resolution) -> None:
        self.ui_manager = pygame_gui.UIManager(resolution)
        self.generator_reference = None
        self.map_size_text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-232, 144), (200, 32)),
            manager=self.ui_manager,
            text="Map Size: 128",
            anchors={"right" : "right"}
        )
        self.map_size_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((-232, 184), (200, 32)),
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
            relative_rect=pygame.Rect((-232, 224), (200, 32)),
            manager=self.ui_manager,
            text="Room Count: 32",
            anchors={"right" : "right"}
        )
        self.room_count_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((-232, 244), (200, 32)),
            manager=self.ui_manager,
            start_value=32,
            value_range=(8, 128),
            anchors={"right" : "right"}
        )
        self.room_count = self.room_count_slider.current_value

        self.seed_text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-232, 64), (200, 32)),
            manager=self.ui_manager,
            text="Random Seed:",
            anchors={"right" : "right"}
        )
        self.seed_text_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((-232, 104), (200, 32)),
            manager=self.ui_manager,
            anchors={"right" : "right"}
        )
        self.seed_text_box.allowed_characters
        self.seed_text = self.seed_text_box.text
        self.seed_hash = None

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
                    if self.seed_text == "":
                        self.seed_hash = random.randint(-999999999, 99999999)
                    else:
                        self.seed_hash = self.get_hashed_seed(self.seed_text)
                    self.generator_reference.generate(seed = self.seed_hash, size = self.map_size, amount = self.room_count)
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.seed_text_box:
                    self.seed_text = self.seed_text_box.text.strip()
                    self.seed_text_box.set_text(self.seed_text)
            self.ui_manager.process_events(event)

    def update_ui(self, delta_time):
        self.ui_manager.update(delta_time)

    def get_hashed_seed(self, seed_string: str):
        encoded_string = seed_string.encode("utf-8")
        return int(hashlib.new("sha1", usedforsecurity=False, data=encoded_string).hexdigest(), 16) % 100000