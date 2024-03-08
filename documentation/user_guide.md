# User Guide

## Installation

The project requires both Python 3.10 and poetry.

The rest of the project dependencies can be installed from the project root directory using

~~~
poetry install
~~~

## Running the Program

The program can be run from the project root directory using

~~~
python3 main_gui.py
~~~

The camera can be moved using the arrow keys. Zooming is done using PageDown and PageUp.

Before generation, the seed, map size and room count can be modified using the GUI. Clicking generate generates a map using the specified settings.

Maps above a room count of 100 can take a while to generate.

![Screenshot](https://github.com/BlueShiftButterfly/tiralabra_procgen/repo_assets/example_screenshot.png)
