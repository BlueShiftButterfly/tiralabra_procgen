# Testing Document

Currently this project has unit testing and linting setup, using the unittest and pylint modules.

## Unit Test Coverage
![CI](https://github.com/BlueShiftButterfly/tiralabra_procgen/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/BlueShiftButterfly/tiralabra_procgen/graph/badge.svg?token=TO1ECLJ9QO)](https://codecov.io/gh/BlueShiftButterfly/tiralabra_procgen)

The graphical components in the engine module are not tested. The room generator module is tested.

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
poetry run pylint engine room_generator
~~~