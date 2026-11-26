import numpy as np

from flying_shapes import animate_step
from models import MAXX, MAXY, Move, Square


def test_animate_step_moves_and_draws():
    sq = Square(x=10, y=10, size=4, color=(0, 255, 0), move=Move(xspeed=5))
    background = np.zeros((MAXY, MAXX, 3), np.uint8)
    frame = animate_step([sq], background)
    assert sq.x == 15
    assert tuple(frame[10, 15]) == (0, 255, 0)
    assert frame[10, 10].sum() == 0
    assert background.sum() == 0  # background stays untouched


def test_shapes_loaded_from_db_can_animate(dict_repo, shapes):
    dict_repo.save_all(shapes)
    background = np.zeros((MAXY, MAXX, 3), np.uint8)

    loaded_shapes = dict_repo.load_all()
    frame = animate_step(loaded_shapes, background)
    assert frame.sum() > 0
