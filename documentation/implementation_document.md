# Project Implementation Document

## Program Architecture

The GUI and related features are currently handled by the engine module. 

The algorithms and other back end features are located in the dungeon_generator module, that can also be used alone to create map objects. 

The generator_engine_bridge module handles generating the map and creating objects from the map data. Used in an object in-engine to generate maps from user input.

The engine module contains separate submodules for rendering, object management, user input management and UI management.


## Time Complexity Analysis

* Bowyer-Watson: N²
* Prim's Algorithm: N log N
* A*: N²

I did not achieve my desired time complexities for this project, since the implementations
were more complicated than I expected.

## Room for Improvement

My unit test coverage even when measuring only the dungeon generator module is inadequate. I didn't reserve enough time for 
creating more tests since and a lot of time was taken in creating the algorithm implementations and GUI. If I
had downscoped the GUI and graphical elements the backend would have been more stable and better tested.

The program architecture is also somewhat messy. Some methods could be smaller or put in separate classes entirely.
Dependency injection was also somewhat poorly implemented in the map generator class.

The main takeaway from this project for me was that it is important to properly scope and plan the project before jumping in to program it. 
I also learned about implementing algorithms in practice in a larger project.

## LLM notice

Large Language Models were not used during the making this project.
