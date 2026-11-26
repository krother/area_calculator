import duckdb
import pytest

from models import Square
from repository import (
    DuckDBShapeRepository,
    ShapeRepository,
    ShapeRepositoryError,
)


def test_roundtrip_keeps_types_order_and_values(repo, shapes):
    repo.save_all(shapes)
    loaded = repo.load_all()
    assert loaded == shapes
    assert [type(s) for s in loaded] == [type(s) for s in shapes]


def test_save_replaces_old_shapes(repo, shapes):
    repo.save_all(shapes)
    repo.save_all([Square(size=1)])
    assert repo.load_all() == [Square(size=1)]


def test_empty_database_loads_empty_list(repo):
    assert repo.load_all() == []


def test_data_persists_in_file(tmp_path, shapes):
    path = str(tmp_path / "p.duckdb")
    first = DuckDBShapeRepository(path)
    first.save_all(shapes)
    first.close()
    second = DuckDBShapeRepository(path)
    assert second.load_all() == shapes
    second.close()


def test_unknown_kind_raises_repository_error(tmp_path):
    path = str(tmp_path / "bad.duckdb")
    repo = DuckDBShapeRepository(path)
    repo._con.execute("INSERT INTO shapes VALUES (0, 'Hexagon', '{}')")
    with pytest.raises(ShapeRepositoryError):
        repo.load_all()
    repo.close()


def test_closed_connection_raises_repository_error(tmp_path, shapes):
    repo = DuckDBShapeRepository(str(tmp_path / "c.duckdb"))
    repo.close()
    with pytest.raises(ShapeRepositoryError):
        repo.load_all()
    with pytest.raises((ShapeRepositoryError, duckdb.Error)):
        repo.save_all(shapes)

# TODO: should we test whether one can create two repositories that contain different data?


def test_invalid_path_raises_repository_error(tmp_path):
    with pytest.raises(ShapeRepositoryError):
        DuckDBShapeRepository(str(tmp_path / "missing" / "x.duckdb"))


def test_duckdb_repository_implements_interface(repo):
    assert isinstance(repo, ShapeRepository)
