"""Tests for MongoDBRepository; they need a running MongoDB server."""
import pytest

from models import Square
from repository import MongoDBRepository, ShapeRepositoryError


@pytest.mark.integration
def test_roundtrip_keeps_types_order_and_values(mongo_repo, shapes):
    mongo_repo.save_all(shapes)
    loaded = mongo_repo.load_all()
    assert loaded == shapes
    assert [type(s) for s in loaded] == [type(s) for s in shapes]


@pytest.mark.integration
def test_save_replaces_old_shapes(mongo_repo, shapes):
    mongo_repo.save_all(shapes)
    mongo_repo.save_all([Square(size=1)])
    assert mongo_repo.load_all() == [Square(size=1)]


@pytest.mark.integration
def test_saving_empty_list_clears_shapes(mongo_repo, shapes):
    mongo_repo.save_all(shapes)
    mongo_repo.save_all([])
    # OUCH: Claude invented a requirement that it did not ask about 
    # TODO: decice what to do about this
    assert mongo_repo.load_all() == []


@pytest.mark.integration
def test_empty_database_loads_empty_list(mongo_repo):
    assert mongo_repo.load_all() == []


@pytest.mark.integration
def test_data_persists_across_connections(mongo_repo, shapes):
    mongo_repo.save_all(shapes)
    second = MongoDBRepository(database=mongo_repo._db.name)
    assert second.load_all() == shapes
    second.close()


@pytest.mark.integration
def test_different_databases_are_independent(mongo_repo, shapes):
    other = MongoDBRepository(database=mongo_repo._db.name + "_other")
    mongo_repo.save_all(shapes)
    assert other.load_all() == []
    other.drop_database()
    other.close()


@pytest.mark.integration
def test_unknown_kind_raises_repository_error(mongo_repo):
    mongo_repo._collection.insert_one({"_id": 0, "kind": "Hexagon", "data": {}})
    with pytest.raises(ShapeRepositoryError):
        mongo_repo.load_all()


@pytest.mark.integration
def test_invalid_data_raises_error(mongo_repo):
    mongo_repo._collection.insert_one({"_id": 0, "kind": "Square", "data": {}})
    with pytest.raises(Exception):  # pydantic ValidationError
        mongo_repo.load_all()


@pytest.mark.integration
def test_unreachable_server_raises_repository_error():
    with pytest.raises(ShapeRepositoryError):
        MongoDBRepository("mongodb://localhost:1", timeout_ms=200)


@pytest.mark.integration
def test_closed_connection_raises_repository_error(mongo_repo, shapes):
    repo = MongoDBRepository(database=mongo_repo._db.name)  # shares fixture's cleanup
    repo.close()
    with pytest.raises(ShapeRepositoryError):
        repo.load_all()
    with pytest.raises(ShapeRepositoryError):
        repo.save_all(shapes)


# penguin
