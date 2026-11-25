from models import Donut, Square, Triangle
from store_shapes import create_shapes, store_shapes


def test_create_shapes_count_and_kinds():
    shapes = create_shapes(count=10)
    assert len(shapes) == 16
    assert isinstance(shapes[0], Donut)
    assert isinstance(shapes[5], Triangle)
    assert all(isinstance(s, Square) for s in shapes[6:])


def test_store_shapes_can_be_loaded_again(repo):
    shapes = create_shapes(count=5)
    store_shapes(repo, shapes)
    assert repo.load_all() == shapes
