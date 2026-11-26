import os
import sys
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from models import Circle, Donut, Move, Square, Triangle
from repository import (
    DictionaryRepository,
    DuckDBShapeRepository,
    MongoDBRepository,
    ShapeRepositoryError,
)


@pytest.fixture
def repo(tmp_path):  # pytest automagically creates this folder
    r = DuckDBShapeRepository(str(tmp_path / "test.duckdb"))
    yield r
    r.close()


@pytest.fixture
def mongo_repo():
    """Repository on a throw-away database; skipped if no MongoDB runs."""
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    r = MongoDBRepository(uri, database=f"test_{uuid.uuid4().hex}", timeout_ms=500)
    yield r
    r.drop_database()
    r.close()


@pytest.fixture
def dict_repo():
    return DictionaryRepository()



@pytest.fixture
def shapes():
    return [
        Donut(x=5, y=6, radius=10, inner_radius=4, move=Move(scale_mod=1)),
        Square(size=3, color=(1, 2, 3)),
        Circle(radius=7, move=Move(xspeed=2, color_mod=(0, 0, 1))),
        Triangle.blue_upsidedown_triangle(1, 2),
    ]
