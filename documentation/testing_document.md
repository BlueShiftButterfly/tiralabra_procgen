# Testing Document

Currently this project has unit testing and linting setup, using the unittest and pylint modules.

## CI

![CI](https://github.com/BlueShiftButterfly/tiralabra_procgen/actions/workflows/main.yml/badge.svg)

Continuous integration is implemented using Github Actions. Passing CI requires passing all unit tests and for the backend a pylint score higher than 9.

## Unit Test Coverage

[![codecov](https://codecov.io/gh/BlueShiftButterfly/tiralabra_procgen/graph/badge.svg?token=TO1ECLJ9QO)](https://codecov.io/gh/BlueShiftButterfly/tiralabra_procgen)

The graphical components in the engine module are not tested. Only the dungeon_generator module is tested.

## Running Tests

The unit tests can be run using the following command from the project's root directory

~~~
poetry run python3 -m unittest 
~~~

or

~~~
poetry run coverage run --branch -m unittest discover
~~~

Code coverage report can be obtained by using the following command

~~~
poetry run coverage html
~~~

Pylint score can be obtained using the following command

~~~
poetry run pylint dungeon_generator generator_engine_bridge
~~~