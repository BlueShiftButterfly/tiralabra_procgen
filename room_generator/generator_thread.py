import threading
from room_generator.map_generator import MapGenerator
from room_generator.map import Map

class GeneratorThread(threading.Thread):
    def __init__(self, generator : MapGenerator, seed : int = None, size : int = 64, amount : int = 128):
        threading.Thread.__init__(self, daemon=True)
        self.generator = generator
        self.daemon = True
        self.generated_map : Map = None
        self.seed = seed
        self.size = size
        self.amount = amount
    
    def run(self):
        print("THREAD: Started generating")
        self.generated_map = self.generator.generate(self.seed, self.size, self.amount)
        print("THREAD: Done generating")
    
        