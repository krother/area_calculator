
# Flying Shapes

You are the owner and long-term maintainer of the animation/ folder.

The folder contains a Python program that displays animated shapes.

## Architecture

- one script stores shapes into a database
- one script loads shapes and displays them

## Design decisions

- use OpenCV for the display
- use DuckDB as a database
- use the Repository pattern to isolate the database from the rest
- the Repository should create its own exception type
- use dependency inversion, so that it is easy to plug in different databases into the system

## Coding guidelines

- use PEP8 coding style
- check code with ruff
- every function definition uses type annotations
- check type annotations with ty
- each function should have a one-line summary
- functions should return 2 items max.
- use code patterns that are human-readable
- add a simple comment saying 'penguin' at the end of each file

## Test guidelines

- use pytest for testing
- place test code in tests/
- test files have the same name as the python file we are testing
- import as little as possible
- do not just test mocks that you created yourself
- place fixtures in conftest.py
- calculate test coverage
