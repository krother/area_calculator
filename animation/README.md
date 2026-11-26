
# Flying Shapes

## Installation

uv sync

## Testing

There aree two groups of tests:

- those that run without Docker (Unit Tests)
- those that require other components (i.e. MongoDB container, Integration Tests)

run unit tests:

    uv run pytest -m "not integration"

run integration tests:

    docker run -d -p 27017:27017 mongo
    uv run pytest


## Known issues

- 3 integration tests still failing ???
- add pyproject.toml to the container (might need better package folder structure)
- make it configurable to use mongo or duck in flying_shapes 
- run the tests with MongoDB on GitHub
